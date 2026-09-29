import io, os, re, json, datetime
import streamlit as st
from openai import OpenAI
from PIL import Image as PILImage
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH as WA
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable

st.set_page_config(page_title="AI Dokumen", page_icon="📄", layout="wide")

# ---------- Konfigurasi ----------
# Provider gratis (format OpenAI-compatible). Dicoba berurutan; key disimpan di Streamlit Secrets.
PROVIDERS = [
    ("Groq", "https://api.groq.com/openai/v1", "llama-3.3-70b-versatile", "GROQ_API_KEY"),
    ("Plugsky", "https://plugsky.com/v1", "plugsky-lite", "PLUGSKY_API_KEY"),  # bisa ditimpa lewat Secrets
]
PAPER = {"A4": (21, 29.7), "Letter": (21.59, 27.94), "Legal": (21.59, 35.56)}
FONTS = {"Times New Roman": ("Times-Roman", "Times-Bold"), "Arial": ("Helvetica", "Helvetica-Bold"),
         "Calibri": ("Helvetica", "Helvetica-Bold")}
PAGE_FMT = {"Tidak ada": "", "1": "{p}", "Halaman 1": "Halaman {p}",
            "Halaman 1 dari N": "Halaman {p} dari {n}", "1 / N": "{p} / {n}"}
ALIGN = {"Rata kiri-kanan": (TA_JUSTIFY, WA.JUSTIFY), "Rata kiri": (TA_LEFT, WA.LEFT)}
POS = ["Kiri", "Tengah", "Kanan"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
         "September", "Oktober", "November", "Desember"]
SURAT = ("Surat Resmi", "Undangan")
DOC_TYPES = ["Surat Resmi", "Undangan", "Laporan", "Rangkuman", "Catatan / Notulen"]
SIGN_W = 7  # lebar blok tanda tangan (cm)


def secret(k):
    try:
        return st.secrets[k]
    except Exception:
        return os.environ.get(k, "")


def tgl(d):
    return f"{d.day} {BULAN[d.month - 1]} {d.year}"


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def blocks(text):
    out = []
    for b in re.split(r"\n\s*\n", (text or "").strip()):
        b = b.strip()
        if not b:
            continue
        lines = b.splitlines()
        if b.startswith("# "):
            out.append(("h", b[2:].strip()))
        elif all(l.strip().startswith("- ") for l in lines):
            out += [("li", l.strip()[2:]) for l in lines]
        else:
            out.append(("p", " ".join(l.strip() for l in lines)))
    return out


# ---------- AI ----------
def generate(doc_type, brief, tone, length):
    sys_msg = ("Kamu penulis dokumen profesional berbahasa Indonesia. Balas HANYA JSON valid: "
               '{"judul":"","pembuka":"","isi":"","penutup":""}. '
               'Di "isi", pisahkan paragraf dengan baris kosong; awali sub-judul dengan "# " '
               'dan butir daftar dengan "- ". Jangan mengarang nama, angka, atau tanggal yang tidak diberikan. '
               "Jangan sertakan salam tanda tangan/nama penulis di penutup.")
    usr = f"Jenis dokumen: {doc_type}\nGaya bahasa: {tone}\nPanjang: {length}\n\nBahan:\n{brief}"
    last = None
    for name, url, model, key in PROVIDERS:
        k = secret(key)
        url = secret(key.replace("API_KEY", "BASE_URL")) or url
        model = secret(key.replace("API_KEY", "MODEL")) or model
        if not (k and url and model):
            continue
        try:
            r = OpenAI(base_url=url, api_key=k).chat.completions.create(
                model=model, temperature=0.4,
                messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": usr}])
            data = json.loads(re.search(r"\{.*\}", r.choices[0].message.content, re.S).group(0))
            if isinstance(data.get("isi"), list):
                data["isi"] = "\n\n".join(map(str, data["isi"]))
            return data, name
        except Exception as e:
            last = f"{name}: {e}"
    raise RuntimeError(last or "Belum ada API key. Isi GROQ_API_KEY di Streamlit Secrets.")


# ---------- Word ----------
def _field(run, code):
    a = OxmlElement("w:fldChar"); a.set(qn("w:fldCharType"), "begin")
    i = OxmlElement("w:instrText"); i.set(qn("xml:space"), "preserve"); i.text = code
    b = OxmlElement("w:fldChar"); b.set(qn("w:fldCharType"), "end")
    for x in (a, i, b):
        run._r.append(x)


def _hr(par):
    pPr = par._p.get_or_add_pPr()
    bd = OxmlElement("w:pBdr"); ln = OxmlElement("w:bottom")
    for k, v in (("val", "single"), ("sz", "12"), ("space", "1"), ("color", "000000")):
        ln.set(qn("w:" + k), v)
    bd.append(ln); pPr.append(bd)


def build_docx(d):
    c, k, sg = d["cfg"], d["kop"], d["sign"]
    doc = Document(); s = doc.sections[0]
    pw, ph = PAPER[c["paper"]]
    s.page_width, s.page_height = Cm(pw), Cm(ph)
    s.left_margin = s.right_margin = Cm(c["mx"])
    s.top_margin = s.bottom_margin = Cm(c["my"])
    W = pw - 2 * c["mx"]
    n = doc.styles["Normal"]
    n.font.name = c["font"]; n.font.size = Pt(c["size"])
    n.element.rPr.rFonts.set(qn("w:eastAsia"), c["font"])
    n.paragraph_format.line_spacing = c["spacing"]
    n.paragraph_format.space_after = Pt(6)

    def P(text="", align=None, bold=False, size=None, after=None, container=None, underline=False):
        p = (container or doc).add_paragraph()
        if align is not None:
            p.alignment = align
        if after is not None:
            p.paragraph_format.space_after = Pt(after)
        if text:
            r = p.add_run(text); r.bold = bold; r.underline = underline
            if size:
                r.font.size = Pt(size)
        return p

    if k["name"] or k["logo"]:
        t = doc.add_table(rows=1, cols=2); t.autofit = False
        c0, c1 = t.rows[0].cells
        c0.width, c1.width = Cm(3), Cm(W - 3)
        if k["logo"]:
            c0.paragraphs[0].add_run().add_picture(io.BytesIO(k["logo"]), width=Cm(2.3))
        first = c1.paragraphs[0]; first.alignment = WA.CENTER
        r = first.add_run(k["name"]); r.bold = True; r.font.size = Pt(c["size"] + 4)
        for line in (k["addr"], k["contact"]):
            if line:
                P(line, WA.CENTER, size=c["size"] - 1, after=0, container=c1)
        _hr(P(after=6))

    body_al = ALIGN[c["align"]][1]
    if d["meta"]:
        m = d["meta"]
        P(m["kota_tgl"], WA.RIGHT)
        for lab, val in (("Nomor", m["nomor"]), ("Lampiran", m["lampiran"]), ("Perihal", m["perihal"])):
            if val:
                p = P(f"{lab}\t: {val}", after=0)
                p.paragraph_format.tab_stops.add_tab_stop(Cm(2.5))
        P()
        if m["tujuan"]:
            P("Yth. " + m["tujuan"], after=0); P("di tempat")
    else:
        P(d["judul"], WA.CENTER, bold=True, size=c["size"] + 2)

    for part in (d["pembuka"], d["isi"], d["penutup"]):
        for kind, txt in blocks(part):
            if kind == "h":
                P(txt, bold=True)
            elif kind == "li":
                doc.add_paragraph(txt, style="List Bullet")
            else:
                P(txt, body_al)

    if sg["nama"]:
        left = {"Kiri": 0, "Tengah": (W - SIGN_W) / 2, "Kanan": W - SIGN_W}[sg["pos"]]
        right = {"Kiri": W - SIGN_W, "Tengah": (W - SIGN_W) / 2, "Kanan": 0}[sg["pos"]]

        def SP(*a, **kw):
            p = P(*a, **kw)
            p.paragraph_format.left_indent, p.paragraph_format.right_indent = Cm(left), Cm(right)
            return p

        P()
        SP(sg["kota_tgl"], WA.CENTER, after=0)
        SP(sg["jabatan"], WA.CENTER, after=0)
        if sg["img"]:
            p = SP(align=WA.CENTER, after=0)
            p.add_run().add_picture(io.BytesIO(sg["img"]), width=Cm(3.5))
        else:
            for _ in range(3):
                SP(after=0)
        SP(sg["nama"], WA.CENTER, bold=True, underline=True, after=0)
        if sg["nip"]:
            SP(sg["nip"], WA.CENTER, after=0)

    tpl = PAGE_FMT[c["pagefmt"]]
    if tpl:
        p = s.footer.paragraphs[0]
        p.alignment = {"Kiri": WA.LEFT, "Tengah": WA.CENTER, "Kanan": WA.RIGHT}[c["pagepos"]]
        for part in re.split(r"(\{p\}|\{n\})", tpl):
            if part == "{p}":
                _field(p.add_run(), "PAGE")
            elif part == "{n}":
                _field(p.add_run(), "NUMPAGES")
            elif part:
                p.add_run(part)
    buf = io.BytesIO(); doc.save(buf)
    return buf.getvalue()


# ---------- PDF ----------
def _img(data, w_cm):
    iw, ih = PILImage.open(io.BytesIO(data)).size
    return Image(io.BytesIO(data), width=w_cm * cm, height=w_cm * cm * ih / iw)


def _canvas(tpl, pos, font, size, pw, mx, my):
    class NC(rl_canvas.Canvas):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw); self._st = []

        def showPage(self):
            self._st.append(dict(self.__dict__)); self._startPage()

        def save(self):
            total = len(self._st)
            for x in self._st:
                self.__dict__.update(x)
                if tpl:
                    self.setFont(font, size - 1)
                    t, y = tpl.format(p=self._pageNumber, n=total), my / 2
                    if pos == "Kiri":
                        self.drawString(mx, y, t)
                    elif pos == "Kanan":
                        self.drawRightString(pw - mx, y, t)
                    else:
                        self.drawCentredString(pw / 2, y, t)
                super().showPage()
            super().save()
    return NC


def build_pdf(d):
    c, k, sg = d["cfg"], d["kop"], d["sign"]
    reg, bold = FONTS[c["font"]]
    pw, ph = [x * cm for x in PAPER[c["paper"]]]
    mx, my = c["mx"] * cm, c["my"] * cm
    W = pw - 2 * mx
    lead = c["size"] * c["spacing"] * 1.2
    S = lambda name, **kw: ParagraphStyle(name, fontName=kw.pop("fontName", reg), fontSize=kw.pop("fontSize", c["size"]),
                                          leading=kw.pop("leading", lead), spaceAfter=kw.pop("spaceAfter", 6), **kw)
    body = S("body", alignment=ALIGN[c["align"]][0])
    ctr = S("ctr", alignment=TA_CENTER, spaceAfter=0)
    story = []

    if k["name"] or k["logo"]:
        txt = [Paragraph(esc(k["name"]), S("kn", fontName=bold, fontSize=c["size"] + 4, alignment=TA_CENTER,
                                            leading=(c["size"] + 4) * 1.2, spaceAfter=0))]
        for line in (k["addr"], k["contact"]):
            if line:
                txt.append(Paragraph(esc(line), S("kl", fontSize=c["size"] - 1, alignment=TA_CENTER, spaceAfter=0)))
        if k["logo"]:
            t = Table([[_img(k["logo"], 2.3), txt]], colWidths=[3 * cm, W - 3 * cm])
            t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
            story.append(t)
        else:
            story += txt
        story += [Spacer(1, 4), HRFlowable(width="100%", thickness=1.5, color=colors.black), Spacer(1, 10)]

    if d["meta"]:
        m = d["meta"]
        story.append(Paragraph(esc(m["kota_tgl"]), S("r", alignment=2)))
        rows = [[lab, ": " + val] for lab, val in (("Nomor", m["nomor"]), ("Lampiran", m["lampiran"]),
                                                    ("Perihal", m["perihal"])) if val]
        if rows:
            t = Table([[Paragraph(esc(a), body), Paragraph(esc(b), body)] for a, b in rows],
                      colWidths=[2.5 * cm, W - 2.5 * cm])
            t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                                   ("TOPPADDING", (0, 0), (-1, -1), 0)]))
            story += [t, Spacer(1, 10)]
        if m["tujuan"]:
            story += [Paragraph("Yth. " + esc(m["tujuan"]), S("y", spaceAfter=0)), Paragraph("di tempat", body)]
    else:
        story.append(Paragraph(esc(d["judul"]), S("t", fontName=bold, fontSize=c["size"] + 2, alignment=TA_CENTER,
                                                  spaceAfter=10)))

    for part in (d["pembuka"], d["isi"], d["penutup"]):
        for kind, txt in blocks(part):
            if kind == "h":
                story.append(Paragraph(f"<b>{esc(txt)}</b>", body))
            elif kind == "li":
                story.append(Paragraph(esc(txt), S("li", alignment=TA_LEFT, spaceAfter=2), bulletText="•"))
            else:
                story.append(Paragraph(esc(txt), body))

    if sg["nama"]:
        cell = [Spacer(1, 12), Paragraph(esc(sg["kota_tgl"]), ctr), Paragraph(esc(sg["jabatan"]), ctr)]
        cell.append(_img(sg["img"], 3.5) if sg["img"] else Spacer(1, 2 * cm))
        cell.append(Paragraph(f"<u><b>{esc(sg['nama'])}</b></u>", ctr))
        if sg["nip"]:
            cell.append(Paragraph(esc(sg["nip"]), ctr))
        t = Table([[cell]], colWidths=[SIGN_W * cm], hAlign={"Kiri": "LEFT", "Tengah": "CENTER", "Kanan": "RIGHT"}[sg["pos"]])
        t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
        story.append(t)

    buf = io.BytesIO()
    SimpleDocTemplate(buf, pagesize=(pw, ph), leftMargin=mx, rightMargin=mx, topMargin=my, bottomMargin=my).build(
        story, canvasmaker=_canvas(PAGE_FMT[c["pagefmt"]], c["pagepos"], reg, c["size"], pw, mx, my))
    return buf.getvalue()


# ---------- UI ----------
st.title("📄 AI Pembuat Dokumen")

with st.sidebar:
    st.header("Kop surat")
    kop_name = st.text_input("Nama instansi / organisasi")
    kop_addr = st.text_area("Alamat", height=70)
    kop_contact = st.text_input("Telp / email / website")
    logo = st.file_uploader("Logo (PNG/JPG)", type=["png", "jpg", "jpeg"])

    st.header("Layout")
    paper = st.selectbox("Ukuran kertas", list(PAPER))
    mx = st.slider("Margin kiri-kanan (cm)", 1.0, 4.0, 2.5, 0.1)
    my = st.slider("Margin atas-bawah (cm)", 1.5, 4.0, 2.5, 0.1)
    font = st.selectbox("Font", list(FONTS))
    size = st.slider("Ukuran font", 9, 16, 12)
    spacing = st.slider("Spasi baris", 1.0, 2.0, 1.15, 0.05)
    align = st.selectbox("Perataan teks", list(ALIGN))
    pagefmt = st.selectbox("Nomor halaman", list(PAGE_FMT), index=3)
    pagepos = st.selectbox("Posisi nomor halaman", POS, index=1)

c1, c2 = st.columns(2)
with c1:
    doc_type = st.selectbox("Jenis dokumen", DOC_TYPES)
    tone = st.selectbox("Gaya bahasa", ["Formal", "Semi-formal", "Ringkas dan padat"])
    length = st.selectbox("Target panjang", ["1 halaman", "2 halaman", "3 halaman atau lebih"])
with c2:
    kota = st.text_input("Kota", "Jakarta")
    tanggal = st.date_input("Tanggal", datetime.date.today())

is_surat = doc_type in SURAT
if is_surat:
    a, b = st.columns(2)
    nomor = a.text_input("Nomor surat"); lampiran = b.text_input("Lampiran")
    perihal = a.text_input("Perihal (kosongkan = otomatis dari AI)")
    tujuan = b.text_input("Ditujukan kepada")

brief = st.text_area("Isi / bahan dokumen (poin, catatan, detail acara, dll.)", height=160)

with st.expander("Tanda tangan"):
    s1, s2 = st.columns(2)
    jabatan = s1.text_input("Jabatan penandatangan")
    nama = s2.text_input("Nama penandatangan")
    nip = s1.text_input("NIP / info tambahan (opsional)")
    sign_pos = s2.selectbox("Posisi tanda tangan", POS, index=2)
    sign_img = st.file_uploader("Gambar tanda tangan / stempel (opsional)", type=["png", "jpg", "jpeg"])

if st.button("✨ Buat dokumen", type="primary", disabled=not brief.strip()):
    with st.spinner("AI sedang menulis..."):
        try:
            res, used = generate(doc_type, brief, tone, length)
            for key in ("judul", "pembuka", "isi", "penutup"):
                st.session_state[key] = str(res.get(key, ""))
            st.session_state["ready"] = True
            st.caption(f"Dibuat dengan {used}")
        except Exception as e:
            st.error(f"Gagal: {e}")

if st.session_state.get("ready"):
    st.subheader("Edit hasil")
    st.text_input("Judul", key="judul")
    st.text_area("Pembuka", key="pembuka", height=100)
    st.text_area("Isi (paragraf dipisah baris kosong, '# ' sub-judul, '- ' butir)", key="isi", height=260)
    st.text_area("Penutup", key="penutup", height=80)

    kt = f"{kota}, {tgl(tanggal)}"
    d = {
        "cfg": dict(paper=paper, mx=mx, my=my, font=font, size=size, spacing=spacing, align=align,
                    pagefmt=pagefmt, pagepos=pagepos),
        "kop": dict(name=kop_name, addr=kop_addr, contact=kop_contact, logo=logo.getvalue() if logo else None),
        "meta": dict(kota_tgl=kt, nomor=nomor, lampiran=lampiran, perihal=perihal or st.session_state["judul"],
                     tujuan=tujuan) if is_surat else None,
        "sign": dict(jabatan=jabatan, nama=nama, nip=nip, pos=sign_pos, kota_tgl=kt,
                     img=sign_img.getvalue() if sign_img else None),
        "judul": st.session_state["judul"], "pembuka": st.session_state["pembuka"],
        "isi": st.session_state["isi"], "penutup": st.session_state["penutup"],
    }
    try:
        d1, d2 = st.columns(2)
        d1.download_button("⬇️ Unduh Word (.docx)", build_docx(d), "dokumen.docx",
                           "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        d2.download_button("⬇️ Unduh PDF", build_pdf(d), "dokumen.pdf", "application/pdf")
    except Exception as e:
        st.error(f"Gagal membuat file: {e}")
