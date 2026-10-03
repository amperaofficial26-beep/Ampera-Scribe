import os, re, json, datetime
from pathlib import Path

import streamlit as st
from openai import OpenAI

import templates as TPL
from templates import TEMPLATES, JENIS, get as get_tpl, brief_from_fields, opsi
from render import (build_docx, build_pdf, build_html, parse_list, parse_table,
                    PAPER, FONTS, PAGE_FMT, ALIGN, POS)

st.set_page_config(page_title="Ampera Scribe", layout="centered")

# ---------- Konfigurasi ----------
PROVIDERS = [
    ("Groq", "https://api.groq.com/openai/v1", "llama-3.3-70b-versatile", "GROQ_API_KEY"),
    ("Plugsky", "https://plugsky.com/v1", "plugsky-lite", "PLUGSKY_API_KEY"),
]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
         "September", "Oktober", "November", "Desember"]
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
APP_VER = f"v6 - {TPL.JUMLAH} template contoh nyata + terjemahan"
BASE_DIR = Path(__file__).resolve().parent
THINKING_ORB = BASE_DIR / "assets" / "thinking_orb.html"

# ---------- Tema UI: navy gelap, kaca biru-ungu ----------
_MS = ("font-family:'Material Symbols Rounded';font-weight:400;font-style:normal;line-height:1;"
       "letter-spacing:normal;text-transform:none;white-space:nowrap;direction:ltr;"
       "-webkit-font-feature-settings:'liga';font-feature-settings:'liga';")

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,300..700,0..1,-50..200&display=swap');
:root{
  --bg:#050a1f; --panel:rgba(11,19,52,.80); --card:rgba(24,38,92,.50); --field:rgba(32,50,112,.34);
  --line:rgba(112,140,255,.20); --line2:rgba(112,140,255,.34);
  --text:#eef3ff; --muted:rgba(190,205,255,.62); --blue:#4f8cff; --violet:#8b5cf6; --pink:#f472b6; --cyan:#5cc8ff;
}
html,body,.stApp,[data-testid="stAppViewContainer"]{font-family:'Plus Jakarta Sans',sans-serif !important;color:var(--text) !important}
.stApp{
  background-color:var(--bg) !important;
  background-image:
    radial-gradient(ellipse 55% 45% at 50% 48%,rgba(70,90,255,.16),transparent 70%),
    radial-gradient(ellipse 45% 30% at 88% 104%,rgba(236,72,153,.22),transparent 70%),
    radial-gradient(ellipse 60% 38% at 40% 108%,rgba(99,102,241,.30),transparent 70%),
    radial-gradient(ellipse 40% 30% at 8% 6%,rgba(37,99,235,.22),transparent 70%),
    linear-gradient(180deg,#040816 0%,#070d28 55%,#050a1f 100%) !important;
  background-attachment:fixed !important;
}
.stApp::before,.stApp::after{content:"";position:fixed;pointer-events:none;z-index:0;border-radius:50%;
  border:1px solid rgba(120,150,255,.22);box-shadow:0 0 40px rgba(99,102,241,.18),inset 0 0 60px rgba(99,102,241,.08)}
.stApp::before{width:140vw;height:70vh;left:-20vw;bottom:-46vh;animation:ampDrift 22s ease-in-out infinite alternate}
.stApp::after{width:110vw;height:60vh;left:-5vw;top:-38vh;border-color:rgba(120,150,255,.14);animation:ampDrift 28s ease-in-out infinite alternate-reverse}
@keyframes ampDrift{from{transform:translateX(-2%) rotate(-1deg)}to{transform:translateX(2%) rotate(1deg)}}
[data-testid="stHeader"],[data-testid="stDecoration"]{background:transparent !important}
[data-testid="stToolbar"],[data-testid="stStatusWidget"],[data-testid="stMainMenu"],[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],[data-testid="collapsedControl"],#MainMenu,.stDeployButton{display:none !important}
.block-container{position:relative;z-index:1;max-width:1120px;padding-top:5.6rem !important;padding-bottom:3rem !important}
.block-container > div{background:transparent !important;border:0 !important;box-shadow:none !important}
h1,h2,h3,h4,p,label,li,span,div{color:var(--text)}
[data-testid="stCaptionContainer"],small{color:var(--muted) !important}
a{color:var(--cyan) !important}
hr{border-color:var(--line) !important}

/* ===== Top bar ===== */
.amp-top{position:fixed;inset:0 0 auto 0;height:4.75rem;z-index:1002;display:flex;align-items:center;justify-content:space-between;
  padding:0 1.8rem 0 2.6rem;border-bottom:1px solid var(--line);border-radius:0 0 26px 26px;
  background:linear-gradient(180deg,rgba(14,24,64,.92),rgba(8,14,40,.86));backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px)}
.amp-brand{display:flex;align-items:center;gap:.9rem}
.amp-brand svg{width:3.1rem;height:3.1rem;filter:drop-shadow(0 0 14px rgba(79,140,255,.55))}
.amp-brand b{display:block;font-size:1.65rem;font-weight:700;letter-spacing:-.02em;line-height:1.05}
.amp-brand small{display:block;font-size:.82rem;margin-top:.1rem}
.amp-actions{display:flex;align-items:center;gap:.85rem}
.amp-ic{width:2.7rem;height:2.7rem;border-radius:50%;display:flex;align-items:center;justify-content:center;
  background:rgba(40,58,128,.40);border:1px solid var(--line)}
.amp-ic .ms,.amp-lang .ms{font-size:1.3rem;color:#dbe6ff}
.amp-lang{height:2.7rem;padding:0 1.05rem;border-radius:999px;display:flex;align-items:center;gap:.5rem;
  background:rgba(40,58,128,.40);border:1px solid var(--line);font-weight:600;font-size:.95rem}
.amp-sep{width:1px;height:1.9rem;background:var(--line2);margin:0 .1rem}
.amp-av{width:2.8rem;height:2.8rem;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:1.1rem;
  background:linear-gradient(135deg,#4f8cff,#a855f7 60%,#f472b6);box-shadow:0 0 20px rgba(139,92,246,.45)}
.ms{""" + _MS + """font-size:1.25rem;display:inline-flex}
.material-symbols-rounded{""" + _MS + """display:inline-flex;align-items:center;justify-content:center;font-size:1.25rem}

/* ===== Panel kiri & kanan (kartu melayang) ===== */
.st-key-left_settings_panel,.st-key-right_template_panel{position:fixed;top:5.6rem;bottom:2.6rem;width:18.5rem;box-sizing:border-box;
  z-index:1001;overflow-y:auto;overflow-x:hidden;padding:4.1rem 1rem 1.4rem;border-radius:28px;
  border:1px solid var(--line);background:linear-gradient(180deg,rgba(16,26,70,.78),rgba(8,14,40,.84)) !important;
  box-shadow:0 24px 70px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.07);
  backdrop-filter:blur(26px) saturate(1.3);-webkit-backdrop-filter:blur(26px) saturate(1.3);
  scrollbar-width:thin;scrollbar-color:rgba(79,140,255,.55) transparent}
.st-key-left_settings_panel{left:1.1rem}
.st-key-right_template_panel{right:1.1rem}
@media (min-width:1200px){.block-container{max-width:calc(100vw - 42rem) !important}}
@media (max-width:1199px){
  .st-key-left_settings_panel,.st-key-right_template_panel{position:relative;inset:auto;width:auto;margin-bottom:1rem}
  .block-container{padding-top:6rem !important}}

/* tombol tutup panel */
.st-key-left_sidebar_top_toggle,.st-key-right_panel_top_toggle{position:fixed;top:6.25rem;z-index:1004}
.st-key-left_sidebar_top_toggle{left:2.2rem;width:9.8rem}
.st-key-right_panel_top_toggle{right:2.2rem;width:16.9rem}
.st-key-left_sidebar_top_toggle button,.st-key-right_panel_top_toggle button{min-height:2.5rem !important;border-radius:999px !important;
  background:rgba(24,38,96,.70) !important;border:1px solid var(--line) !important;box-shadow:none !important;font-size:.9rem !important;font-weight:600 !important}
.st-key-right_panel_top_toggle button{position:relative}
.st-key-right_panel_top_toggle button::after{content:"chevron_right";""" + _MS + """position:absolute;right:.9rem;top:50%;transform:translateY(-50%);
  font-size:1.2rem;color:#dbe6ff}

/* judul panel */
.section-heading{display:flex;align-items:center;gap:.85rem;margin:.2rem 0 1.1rem}
.section-heading .material-symbols-rounded{width:3.2rem;height:3.2rem;flex:none;border-radius:50%;color:#fff;font-size:1.55rem;
  background:linear-gradient(135deg,#3b82f6,#7c5cff);box-shadow:0 8px 26px rgba(79,140,255,.45),inset 0 1px 0 rgba(255,255,255,.4)}
.section-heading strong{display:block;font-size:1.42rem;font-weight:700;line-height:1.15;letter-spacing:-.01em}
.section-heading small{display:block;margin-top:.2rem;font-size:.74rem;letter-spacing:.05em;text-transform:uppercase}
.result-heading{display:flex;align-items:center;gap:.8rem;margin:1.2rem 0 .9rem}
.result-heading .material-symbols-rounded{width:2.6rem;height:2.6rem;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#7c5cff);color:#fff}
.result-heading h2{margin:0;font-size:1.4rem}

/* kartu expander */
[data-testid="stExpander"]{border:1px solid var(--line) !important;border-radius:20px !important;overflow:hidden;
  background:var(--card) !important;box-shadow:inset 0 1px 0 rgba(255,255,255,.06)}
[data-testid="stExpander"] summary{position:relative;padding:.85rem 1rem .85rem 3.1rem !important;font-weight:700;font-size:1rem}
[data-testid="stExpander"] summary::before{content:"description";""" + _MS + """position:absolute;left:1rem;top:50%;transform:translateY(-50%);
  font-size:1.35rem;color:#bcd0ff}
.st-key-right_template_panel [data-testid="stExpander"] summary::before{content:"folder"}
[data-testid="stExpander"] details{border:0 !important}

/* label & input */
[data-testid="stWidgetLabel"] p{font-size:.88rem;font-weight:600;color:var(--text)}
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,[data-testid="stTextArea"] textarea,[data-testid="stDateInput"] input,
[data-baseweb="select"] > div,[data-baseweb="base-input"],[data-testid="stFileUploader"] section{
  color:var(--text) !important;background:var(--field) !important;border:1px solid var(--line) !important;border-radius:14px !important;box-shadow:none !important}
[data-baseweb="base-input"] input,[data-baseweb="base-input"] textarea{border:0 !important;background:transparent !important}
[data-testid="stTextInput"] input:focus,[data-testid="stTextArea"] textarea:focus,[data-baseweb="select"] > div:focus-within{
  border-color:rgba(92,200,255,.7) !important;box-shadow:0 0 0 1px rgba(92,200,255,.25),0 0 26px rgba(79,140,255,.18) !important}
input::placeholder,textarea::placeholder{color:rgba(190,205,255,.40) !important}
[data-baseweb="popover"] > div,[data-baseweb="menu"]{background:#0c1436 !important;border:1px solid var(--line) !important;border-radius:14px !important}
[data-testid="stSlider"] [role="slider"]{background:linear-gradient(135deg,#4f8cff,#8b5cf6) !important;box-shadow:0 0 18px rgba(79,140,255,.5) !important}

/* tombol umum */
.stButton > button,.stDownloadButton > button{border-radius:14px !important;color:#fff !important;font-weight:600 !important;
  border:1px solid var(--line2) !important;background:rgba(36,54,124,.55) !important;box-shadow:none !important;transition:transform .2s,border-color .2s,box-shadow .2s !important}
.stButton > button:hover,.stDownloadButton > button:hover{transform:translateY(-1px);border-color:rgba(92,200,255,.7) !important;box-shadow:0 10px 30px rgba(79,140,255,.22) !important}
.st-key-view_template_btn button{min-height:3rem !important;border:0 !important;font-size:.98rem !important;
  background:linear-gradient(90deg,#2563eb,#6d4aff) !important;box-shadow:0 12px 30px rgba(79,70,229,.40) !important}
/* tombol utama (CTA) */
.st-key-main_generate button{min-height:3.5rem !important;border-radius:999px !important;font-size:1.02rem !important;border:2px solid transparent !important;
  background:linear-gradient(#0b1747,#0b1747) padding-box,linear-gradient(90deg,#3b82f6,#a855f7) border-box !important;
  box-shadow:0 0 34px rgba(79,140,255,.30) !important}
.st-key-main_generate button:hover{box-shadow:0 0 48px rgba(139,92,246,.50) !important}

/* orb tengah */
.amp-orb-wrap{display:flex;justify-content:center;align-items:center;height:11rem;margin-top:4rem}
.amp-orb{width:8rem;height:8rem;border-radius:50%;position:relative;
  background:
    radial-gradient(circle at 30% 26%,#fff 0%,#cfe8ff 12%,rgba(120,180,255,.85) 32%,transparent 58%),
    radial-gradient(circle at 74% 58%,#ff6fae 0%,rgba(222,92,200,.85) 22%,transparent 52%),
    radial-gradient(circle at 60% 85%,rgba(96,70,255,.9),transparent 55%),
    radial-gradient(circle at 50% 50%,#3a66ff 0%,#2a35b8 70%,#1a1f6e 100%);
  box-shadow:0 0 50px rgba(100,140,255,.50),0 0 130px rgba(236,72,153,.28),inset -14px -18px 44px rgba(20,24,110,.65),inset 10px 10px 32px rgba(255,255,255,.30)}
.amp-orb::after{content:"";position:absolute;inset:-14%;border-radius:50%;z-index:-1;background:radial-gradient(circle,rgba(110,140,255,.30),transparent 68%);filter:blur(18px)}
@keyframes ampFloat{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-8px) scale(1.025)}}
@media (prefers-reduced-motion:reduce){.stApp::before,.stApp::after{animation:none}}

/* kotak info */
.amp-info{display:flex;align-items:center;gap:.9rem;max-width:36rem;margin:1rem auto 0;padding:.9rem 1.1rem;border-radius:18px;border:1.5px solid transparent;
  background:linear-gradient(rgba(14,22,66,.92),rgba(14,22,66,.92)) padding-box,linear-gradient(90deg,rgba(79,140,255,.75),rgba(168,85,247,.75)) border-box;
  box-shadow:0 18px 50px rgba(30,40,140,.25)}
.amp-info-ic{width:2.5rem;height:2.5rem;flex:none;border-radius:14px;display:flex;align-items:center;justify-content:center;background:rgba(79,110,255,.22)}
.amp-info-ic .ms{font-size:1.5rem;color:#a9c0ff}
.amp-info p{margin:0;font-size:.85rem;line-height:1.55}
.amp-info b{color:#fff;font-weight:700}
.amp-info b.hl{color:var(--cyan)}

/* lain-lain */
[data-testid="stAlert"]{border:1px solid var(--line2) !important;border-radius:18px !important;background:rgba(24,38,96,.55) !important}
[data-testid="stTabs"] button{border-radius:999px !important}
[data-testid="stTabs"] button[aria-selected="true"]{background:rgba(79,140,255,.20) !important}
iframe,[data-testid="stHtml"]{border:0 !important;background:transparent !important}
</style>
"""

# (kata kunci, ikon label, ikon dalam kolom)
ICONS = [
    (("latar", "belakang"), "subject", "notes"),
    (("hari", "tanggal", "tgl"), "today", "calendar_today"),
    (("waktu", "jam", "pukul"), "timer", "schedule"),
    (("tempat", "lokasi", "ruang"), "pin_drop", "location_on"),
    (("diundang", "kepada", "penerima", "peserta", "nama", "siapa"), "account_circle", "person"),
    (("pokok", "tentang", "perihal", "hal", "agenda", "acara", "bahasan"), "format_list_bulleted", "format_list_bulleted"),
    (("alamat",), "home", "home"),
    (("telp", "kontak", "hp", "wa"), "call", "call"),
    (("email", "surel"), "mail", "mail"),
    (("nomor", "no."), "tag", "tag"),
    (("jabatan",), "badge", "badge"),
]


def icon_for(label):
    low = (label or "").lower()
    for kata, il, ifld in ICONS:
        if any(k in low for k in kata):
            return il, ifld
    return "edit_note", "edit_note"


def inject_glassliquid_theme():
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def field_icons_css(tpl):
    """Ikon di samping label dan di dalam kolom isian untuk semua field template aktif."""
    rules = []
    for f in tpl.get("fields", []):
        cls = re.sub(r"[^\w-]", "-", f"fld_{tpl['id']}_{f['key']}")
        il, ifld = icon_for(f.get("label", f["key"]))
        sel = f".st-key-{cls}"
        top = "top:.9rem" if f.get("type") == "area" else "top:50%;transform:translateY(-50%)"
        rules.append(
            f"{sel} [data-testid='stWidgetLabel'] p::before{{content:'{il}';{_MS}font-size:1.05rem;"
            f"color:#9db4ff;vertical-align:-4px;margin-right:.45rem;display:inline-block}}"
            f"{sel} [data-baseweb='base-input']{{position:relative}}"
            f"{sel} [data-baseweb='base-input']::before{{content:'{ifld}';{_MS}position:absolute;left:.8rem;{top};"
            f"font-size:1.15rem;color:#8fa8ff;z-index:2;pointer-events:none}}"
            f"{sel} input,{sel} textarea{{padding-left:2.7rem !important}}"
        )
    return "<style>" + "".join(rules) + "</style>"


_LOGO = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="ag" x1="0" y1="1" x2="1" y2="0">'
         '<stop offset="0" stop-color="#2f6bff"/><stop offset="1" stop-color="#8fd3ff"/></linearGradient></defs>'
         '<path d="M8 30 56 6 44 56 30 38 20 48 22 34Z" fill="url(#ag)"/>'
         '<path d="M22 34 56 6 30 38Z" fill="#fff" opacity=".35"/></svg>')


def render_topbar():
    st.markdown(
        f"""<div class="amp-top">
        <div class="amp-brand">{_LOGO}<div><b>Ampera Scribe</b><small>AI Writing Assistant</small></div></div>
        <div class="amp-actions">
          <div class="amp-ic"><span class="ms">light_mode</span></div>
          <div class="amp-lang"><span class="ms">language</span>ID</div>
          <div class="amp-sep"></div>
          <div class="amp-ic"><span class="ms">history</span></div>
          <div class="amp-av">A</div>
        </div></div>""",
        unsafe_allow_html=True)


def render_orb():
    st.markdown('<div class="amp-orb-wrap"><div class="amp-orb"></div></div>', unsafe_allow_html=True)


def render_info_box():
    st.markdown(
        """<div class="amp-info"><div class="amp-info-ic"><span class="ms">auto_awesome</span></div>
        <p>Pilih jenis dan template di panel kanan, isi data di sidebar kiri, lalu tekan
        <b class="hl">Let's go, buat file nya</b>. Gunakan tombol <b>Lihat template lengkap</b>
        untuk melihat gambaran surat sebelum dibuat.</p></div>""",
        unsafe_allow_html=True)


def mat_button(label, icon, **kwargs):
    """Button dengan ikon Material Symbols; fallback aman bila Streamlit lama belum mendukung `icon`."""
    try:
        return st.button(label, icon=icon, **kwargs)
    except TypeError as e:
        if "icon" not in str(e):
            raise
        return st.button(label, **kwargs)


def mat_download_button(label, data, file_name, mime, icon, **kwargs):
    """Download button dengan ikon Material Symbols; fallback aman bila Streamlit lama belum mendukung `icon`."""
    try:
        return st.download_button(label, data, file_name, mime, icon=icon, **kwargs)
    except TypeError as e:
        if "icon" not in str(e):
            raise
        return st.download_button(label, data, file_name, mime, **kwargs)


def secret(k):
    try:
        return st.secrets[k]
    except Exception:
        return os.environ.get(k, "")


def tgl(d):
    return f"{d.day} {BULAN[d.month - 1]} {d.year}"


def tgl_hari(d):
    return f"{HARI[d.weekday()]}, {tgl(d)}"


# ---------- AI ----------
KEYS = ("judul", "pembuka", "isi", "penutup")


def _json_blob(txt):
    """Ambil objek JSON pertama yang kurung kurawalnya seimbang (abaikan ```fence```)."""
    txt = re.sub(r"```[a-zA-Z]*", "", txt or "").replace("```", "")
    start = txt.find("{")
    while start != -1:
        depth, in_str, esc_ch = 0, False, False
        for i in range(start, len(txt)):
            c = txt[i]
            if in_str:
                if esc_ch:
                    esc_ch = False
                elif c == "\\":
                    esc_ch = True
                elif c == '"':
                    in_str = False
            elif c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return txt[start:i + 1]
        start = txt.find("{", start + 1)
    return None


REASON_PAT = re.compile(
    r"\b(we need to|we should|the user|let's craft|let us|i should|the spec|"
    r"as an ai|output json|valid json|must follow template|acceptable\.|probably okay)\b", re.I)


def _strip_reasoning(txt):
    """Buang blok berpikir model (<think>...</think>, 'Analysis:' dsb) dan pagar kode."""
    t = txt or ""
    t = re.sub(r"<(think|thinking|reasoning|scratchpad)>.*?</\1>", "", t, flags=re.S | re.I)
    t = re.sub(r"<(think|thinking|reasoning|scratchpad)>.*", "", t, flags=re.S | re.I)
    t = re.sub(r"```[a-zA-Z]*", "", t).replace("```", "")
    return t.strip()


def _salvage_json(txt):
    """JSON terpotong (kehabisan token): tutup string/kurung yang menggantung."""
    start = txt.find('{"')
    if start == -1:
        start = txt.find("{")
    if start == -1:
        return None
    t = txt[start:]
    depth, in_str, esc_ch = 0, False, False
    for c in t:
        if in_str:
            if esc_ch:
                esc_ch = False
            elif c == "\\":
                esc_ch = True
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
    if depth <= 0 and not in_str:
        return None
    t = t.rstrip().rstrip(",")
    if in_str:
        t += '"'
    return t + "}" * max(depth, 0)


def _from_text(txt):
    """Fallback: model balas teks biasa -> pecah jadi judul/pembuka/isi/penutup.
    Menolak teks yang jelas-jelas catatan berpikir model, bukan isi dokumen."""
    t = (txt or "").strip()
    if not t:
        return None
    if REASON_PAT.search(t[:1500]) or t.lower().count("json") >= 2:
        raise ValueError("model membalas catatan berpikir, bukan dokumen")
    par = [p.strip() for p in re.split(r"\n\s*\n", t) if p.strip()]
    judul = ""
    if par and len(par[0]) < 120 and "\n" not in par[0]:
        judul = par.pop(0).lstrip("# ").strip()
    pembuka = par.pop(0) if par else ""
    penutup = par.pop() if len(par) > 1 else ""
    return {"judul": judul, "pembuka": pembuka, "isi": "\n\n".join(par), "penutup": penutup}


def _normalize(data):
    out = {}
    for k in KEYS:
        v = data.get(k, "")
        if isinstance(v, list):
            v = "\n\n".join(map(str, v))
        elif isinstance(v, dict):
            v = "\n\n".join(f"# {a}\n{b}" for a, b in v.items())
        out[k] = str(v or "")
    return out


PLACEHOLDER = re.compile(r"^[\[\(<]{1,2}[^\]\)>]{0,60}[\]\)>]{1,2}[.,]?$")


def _esc_ctrl(t):
    """Escape newline/tab mentah yang ada DI DALAM string JSON (bikin json.loads gagal)."""
    out, in_str, esc_ch = [], False, False
    for c in t:
        if in_str:
            if esc_ch:
                esc_ch = False
            elif c == "\\":
                esc_ch = True
            elif c == '"':
                in_str = False
            elif c == "\n":
                out.append("\\n"); continue
            elif c == "\r":
                continue
            elif c == "\t":
                out.append("\\t"); continue
        elif c == '"':
            in_str = True
        out.append(c)
    return "".join(out)


def _loads(t):
    for cand in (t, _esc_ctrl(t)):
        try:
            return json.loads(cand)
        except Exception:
            pass
    return None


def _deep_find(obj, depth=0):
    """Cari dict {judul,pembuka,isi,penutup} walau terbungkus/di-encode berlapis."""
    if depth > 4:
        return None
    if isinstance(obj, str):
        t = obj.strip()
        if not (t.startswith("{") or t.startswith('"') or '\\"judul' in t or '"judul' in t):
            return None
        for cand in (t, _json_blob(t), t.replace('\\"', '"').replace("\\\\n", "\\n")):
            if not cand:
                continue
            v = _loads(cand)
            if v is not None and not isinstance(v, str):
                r = _deep_find(v, depth + 1)
                if r:
                    return r
            elif isinstance(v, str) and v != t:
                r = _deep_find(v, depth + 1)
                if r:
                    return r
            blob = _json_blob(cand)
            if blob and blob != cand:
                v2 = _loads(blob)
                if v2 is not None:
                    r = _deep_find(v2, depth + 1)
                    if r:
                        return r
        return None
    if isinstance(obj, list):
        for x in obj:
            r = _deep_find(x, depth + 1)
            if r:
                return r
        return None
    if isinstance(obj, dict):
        if any(k in obj for k in KEYS):
            return obj
        # kasus {"{\"judul\":...}": ""} -> JSON tersembunyi di key
        for k, v in obj.items():
            for cand in (k, v):
                r = _deep_find(cand, depth + 1)
                if r:
                    return r
    return None


def _tidy(v):
    """Rapikan satu nilai teks dari AI."""
    t = str(v or "")
    if "\\n" in t and "\n" not in t:          # newline masih berupa literal \n
        t = t.replace("\\n", "\n")
    t = t.replace("\\t", " ").replace('\\"', '"').replace("\\'", "'")
    t = t.strip()
    if t.startswith("{") and t.endswith("}"):
        t = t[1:-1].strip()
    if len(t) > 1 and t[0] == t[-1] and t[0] in "\"'":
        t = t[1:-1].strip()
    t = re.sub(r"^(judul|pembuka|isi|penutup)\s*:\s*", "", t, flags=re.I)
    out = []
    for ln in t.splitlines():
        s_ = ln.strip()
        if not s_:
            out.append("")
            continue
        if PLACEHOLDER.match(s_):            # buang [Penanggung Jawab], [Tanggal], dst.
            continue
        s_ = re.sub(r"^#{2,}\s*", "# ", s_)   # ## Judul -> # Judul
        if not s_.startswith("# "):
            s_ = re.sub(r"^[*+•]\s+", "- ", s_)
            s_ = re.sub(r"^\d+[.)]\s+", "- ", s_)
        out.append(s_)
    t = "\n".join(out)
    t = re.sub(r"\n{3,}", "\n\n", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t.strip()


def _split_sections(data):
    """Pindahkan sub-judul '# Pembuka' / '# Penutup' di dalam isi ke field-nya sendiri."""
    isi, buang = [], None
    blok = re.split(r"\n(?=# )", data["isi"])
    sisa = []
    for b in blok:
        head = b.split("\n", 1)[0].lstrip("# ").strip().lower()
        body = b.split("\n", 1)[1].strip() if "\n" in b else ""
        if head in ("pembuka", "salam pembuka", "pendahuluan surat") and not data["pembuka"]:
            data["pembuka"] = body
        elif head in ("penutup", "salam penutup", "kata penutup"):
            if not data["penutup"]:
                data["penutup"] = body
        else:
            sisa.append(b)
    data["isi"] = "\n\n".join(x.strip() for x in sisa if x.strip())
    return data


def _parse(raw):
    txt = _strip_reasoning(raw)
    for cand in (txt, _json_blob(txt), _salvage_json(txt)):
        if not cand:
            continue
        data = _deep_find(cand) or _deep_find(_loads(cand) if _loads(cand) is not None else None)
        if data:
            data = {k: _tidy(v) for k, v in _normalize(data).items()}
            if (data["isi"] + data["pembuka"]).strip():
                return _split_sections(data)
    data = _from_text(txt)
    if data:
        data = {k: _tidy(v) for k, v in _normalize(data).items()}
        return _split_sections(data)
    raise ValueError("balasan AI kosong / tidak bisa dibaca")


class _Safe(dict):
    def __missing__(self, k):
        return "..."


def fill(text, values):
    """Isi placeholder {key} pada kalimat baku dengan nilai dari form."""
    try:
        return (text or "").format_map(_Safe({k: (v or "").strip()
                                              for k, v in (values or {}).items()}))
    except Exception:
        return text or ""


def generate(jenis, brief, tone, length, tpl=None, values=None):
    """Susun dokumen. Kalimat baku template dipakai apa adanya; AI mengisi bagian isi."""
    tpl = tpl or {}
    outline = tpl.get("outline") or []
    baku = tpl.get("baku") or {}
    pembuka_baku = fill(baku.get("pembuka", ""), values)
    penutup_baku = fill(baku.get("penutup", ""), values)

    sys_msg = (
        "Kamu penulis dokumen resmi berbahasa Indonesia yang meniru contoh surat nyata. "
        "JANGAN menulis proses berpikir, analisis, komentar, atau bahasa Inggris. "
        "Balas LANGSUNG satu objek JSON valid, tanpa teks lain dan tanpa blok kode, "
        'dengan tepat 4 kunci: {"judul":"","pembuka":"","isi":"","penutup":""}. '
        "Keempat nilai wajib string berbahasa Indonesia siap cetak.\n"
        'Aturan "isi": sub-judul diawali "# ", butir daftar diawali "- ", '
        'daftar bernomor diawali "1. ", baris tabel ditulis "| sel | sel |" '
        "(baris pertama adalah judul kolom), data identitas ditulis "
        '"Label: nilai" satu per baris, paragraf dipisah satu baris kosong. '
        'Jangan mengulang isi "pembuka" atau "penutup" di dalam "isi". '
        "Jangan mengarang nama, nomor, atau tanggal yang tidak diberikan; "
        "lewati bagian yang datanya tidak ada. "
        "Jangan menulis nama penanda tangan atau blok tanda tangan."
    )
    ker = ""
    if outline:
        ker = ("\nKerangka bagian untuk \"isi\" (urut, lewati yang datanya tidak ada):\n"
               + "\n".join(f"{i}. {s}" for i, s in enumerate(outline, 1)) + "\n")
    baku_txt = ""
    if pembuka_baku or penutup_baku:
        baku_txt = ("\nKalimat baku yang WAJIB dipakai persis (jangan diubah):\n"
                    f"pembuka: {pembuka_baku}\npenutup: {penutup_baku}\n")
    usr = (f"Jenis dokumen: {jenis}\nTemplate: {tpl.get('nama', jenis)}\n"
           f"Judul: {tpl.get('judul', '')}\nGaya bahasa: {tone}\nPanjang: {length}\n"
           f"{ker}{baku_txt}\nBahan:\n{brief}\n\nKeluarkan HANYA JSON-nya sekarang.")
    msgs = [{"role": "system", "content": sys_msg}, {"role": "user", "content": usr}]
    fixmsg = {"role": "user", "content": ("Balasan sebelumnya tidak terpakai. Keluarkan HANYA "
                                          "objek JSON dengan kunci judul, pembuka, isi, "
                                          "penutup dalam bahasa Indonesia.")}
    data, prov = _call(msgs, fixmsg)
    if pembuka_baku:
        data["pembuka"] = pembuka_baku
    if penutup_baku:
        data["penutup"] = penutup_baku
    if tpl.get("judul"):
        data["judul"] = tpl["judul"]
    return data, prov


def _call(msgs, fixmsg=None, parse=True, temperature=0.3):
    errors, skipped = [], []
    for name, url, model, key in PROVIDERS:
        k = secret(key)
        url = secret(key.replace("API_KEY", "BASE_URL")) or url
        model = secret(key.replace("API_KEY", "MODEL")) or model
        if not (k and url and model):
            skipped.append(name)
            continue
        client = OpenAI(base_url=url, api_key=k, timeout=180, max_retries=1)
        attempts = [({"response_format": {"type": "json_object"}}, msgs), ({}, msgs)]
        if fixmsg:
            attempts.append(({}, msgs + [fixmsg]))
        for kw, mm in attempts:
            try:
                r = client.chat.completions.create(model=model, temperature=temperature,
                                                   max_tokens=4096, messages=mm, **kw)
                raw = (r.choices[0].message.content or "").strip()
            except Exception as e:
                errors.append(f"{name} ({model}) - {type(e).__name__}: {e}")
                continue
            try:
                return (_parse(raw) if parse else raw), name
            except Exception as e:
                errors.append(f"{name} ({model}) - {e}. Cuplikan: {raw[:100]!r}")
    if not errors:
        raise RuntimeError("Belum ada API key aktif. Isi GROQ_API_KEY di Streamlit Secrets "
                           f"(provider yang dilewati: {', '.join(skipped) or '-'}).")
    raise RuntimeError("Semua provider gagal:\n- " + "\n- ".join(dict.fromkeys(errors)))


# ---------- Terjemahan ----------
LANG = {"Indonesia → Inggris": ("Indonesian", "English"),
        "Inggris → Indonesia": ("English", "Indonesian")}


def translate(doc, arah):
    """Terjemahkan judul/pembuka/isi/penutup dokumen, mini-markup dipertahankan."""
    src, dst = LANG[arah]
    sys_msg = (
        f"You are a professional translator of official documents from {src} to {dst}. "
        "Reply with ONE valid JSON object only, no other text, no code fence, with exactly "
        'these 4 keys: {"judul":"","pembuka":"","isi":"","penutup":""}. '
        f"Translate every value into {dst}, keeping the formatting markup intact: lines "
        'starting with "# " stay sub-headings, "- " stay bullets, "1. " stay numbered, '
        'lines with "|" stay table rows, "Label: value" lines keep that shape. '
        "Do not translate proper names, numbers, dates, or document numbers. "
        "Do not add explanations."
    )
    payload = json.dumps({k: doc.get(k, "") for k in KEYS}, ensure_ascii=False)
    msgs = [{"role": "system", "content": sys_msg},
            {"role": "user", "content": payload + "\n\nOutput the translated JSON now."}]
    data, prov = _call(msgs, temperature=0.1)
    return data, prov


def template_preview_content(tpl, values):
    """Buat isi contoh lengkap untuk preview template tanpa memanggil AI."""
    sample = {}
    for f in tpl.get("fields", []):
        val = (values or {}).get(f["key"], "")
        val = str(val or f.get("ph") or f"Contoh {f['label']}").strip()
        sample[f["key"]] = val

    baku = tpl.get("baku") or {}
    pembuka = fill(baku.get("pembuka", ""), sample)
    penutup = fill(baku.get("penutup", ""), sample)
    if not pembuka:
        pembuka = ("Dengan hormat, berdasarkan data dan kebutuhan yang tercantum "
                   "pada template ini, berikut pratinjau susunan dokumen yang akan dibuat.")
    if not penutup:
        penutup = ("Demikian pratinjau template ini dibuat agar pengguna dapat melihat "
                   "gambaran hasil akhir sebelum dokumen disusun.")

    data_lines = []
    for f in tpl.get("fields", []):
        label = f.get("label", f["key"])
        data_lines.append(f"{label}: {sample.get(f['key'], '...')}")

    parts = []
    if data_lines:
        parts.append("# Data utama template\n" + "\n".join(data_lines))

    outline = tpl.get("outline") or []
    if outline:
        parts.append("# Susunan bagian dokumen\n" +
                     "\n".join(f"{i}. {section}" for i, section in enumerate(outline, 1)))

    parts.append("# Contoh isi yang akan dikembangkan\n"
                 "- Bagian ini akan disusun otomatis berdasarkan data yang diisi.\n"
                 "- Kalimat baku template dipertahankan sesuai contoh surat.\n"
                 "- Nama, nomor, tanggal, dan rincian lain mengikuti input pengguna.")

    return {
        "judul": tpl.get("judul", tpl.get("nama", "Template dokumen")),
        "pembuka": pembuka,
        "isi": "\n\n".join(parts),
        "penutup": penutup,
    }


# ---------- Status ----------
ss = st.session_state
ss.setdefault("doc", None)
ss.setdefault("hasil", None)
ss.setdefault("notice", None)
ss.setdefault("page", "home")
ss.setdefault("right_panel_open", True)
ss.setdefault("left_sidebar_open", True)
ss.setdefault("form", {})

inject_glassliquid_theme()
render_topbar()

if not ss.left_sidebar_open:
    st.markdown(
        """
        <style>
        .st-key-left_settings_panel {
            display: none !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

SLIP_DEFAULT = {
    "izin_ortu": ("# Surat Balasan Orang Tua/Wali\n\n"
                  "Nama Orang Tua/Wali: ...................................\n"
                  "Nama Peserta Didik: ...................................\n"
                  "Kelas: ...................................\n\n"
                  "Memberi izin / tidak memberi izin *) putra/putri kami untuk mengikuti "
                  "kegiatan tersebut.\n\n*) coret yang tidak perlu"),
    "kembar": ("# Salinan untuk Arsip\n\n"
               "Nama: ...................................\n"
               "Jabatan: ...................................\n"
               "Unit Kerja: ...................................\n"
               "Keperluan: pribadi / pekerjaan *)\n"
               "Jam keluar: ................  Jam kembali: ................\n\n"
               "*) Coret yang tidak perlu"),
    "balasan_sekolah": ("# Formulir Balasan Sekolah Tujuan\n\n"
                        "Nama Sekolah: ...................................\n"
                        "Menerima / tidak menerima *) peserta didik tersebut di atas.\n"
                        "Diterima di kelompok/kelas: ...................................\n"
                        "Tanggal: ...................................\n\n"
                        "*) coret yang tidak perlu"),
}

# ---------- Tombol sidebar & panel kanan di area toolbar custom ----------
left_sidebar_label = "Tutup sidebar" if ss.left_sidebar_open else "Buka sidebar"
left_sidebar_icon = ":material/arrow_back:" if ss.left_sidebar_open else ":material/view_sidebar:"
with st.container(key="left_sidebar_top_toggle"):
    if mat_button(left_sidebar_label, left_sidebar_icon,
                  use_container_width=True, key="toggle_left_sidebar_top"):
        ss.left_sidebar_open = not ss.left_sidebar_open
        st.rerun()

top_panel_label = "Tutup panel kanan" if ss.right_panel_open else "Buka panel kanan"
top_panel_icon = ":material/close:" if ss.right_panel_open else ":material/view_sidebar:"
with st.container(key="right_panel_top_toggle"):
    if mat_button(top_panel_label, top_panel_icon,
                  use_container_width=True, key="toggle_right_panel_top"):
        ss.right_panel_open = not ss.right_panel_open
        st.rerun()

# ---------- Panel kanan: template ----------
jenis = ss.get("jenis", JENIS[0])
if jenis not in JENIS:
    jenis = JENIS[0]
    ss["jenis"] = jenis

daftar = TEMPLATES[jenis]
nama_opsi = [t["nama"] for t in daftar]
tpl_state_key = "tpl_" + jenis
nama_tpl = ss.get(tpl_state_key, nama_opsi[0])
if nama_tpl not in nama_opsi:
    nama_tpl = nama_opsi[0]
    ss[tpl_state_key] = nama_tpl
tpl = next(t for t in daftar if t["nama"] == nama_tpl)
tone = ss.get("tone", "Formal")
if tone not in ["Formal", "Formal ramah", "Ringkas"]:
    tone = "Formal"
length = ss.get("length", "Sedang")
if length not in ["Ringkas", "Sedang", "Panjang"]:
    length = "Sedang"

if ss.right_panel_open:
    with st.container(key="right_template_panel"):
        st.markdown("""
        <div class="section-heading">
            <span class="material-symbols-rounded">view_sidebar</span>
            <div>
                <strong>Template dokumen</strong>
                <small>Pilih dan lihat contoh lengkap</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("01  Jenis & template", expanded=True):
            jenis = st.selectbox("Jenis dokumen", JENIS, key="jenis")
            daftar = TEMPLATES[jenis]
            nama_tpl = st.selectbox(f"Template ({len(daftar)} contoh nyata)",
                                    [t["nama"] for t in daftar], key="tpl_" + jenis)
            tpl = next(t for t in daftar if t["nama"] == nama_tpl)
            st.caption(tpl["desc"])
            tone = st.selectbox("Gaya bahasa", ["Formal", "Formal ramah", "Ringkas"], key="tone")
            length = st.selectbox("Panjang", ["Ringkas", "Sedang", "Panjang"], index=1, key="length")

        if mat_button("Lihat template lengkap", ":material/visibility:",
                      use_container_width=True, key="view_template_btn"):
            ss.page = "template_preview"
            st.rerun()

        if ss.page == "template_preview":
            if mat_button("Kembali ke generator", ":material/arrow_back:",
                          use_container_width=True, key="back_from_template_panel"):
                ss.page = "home"
                st.rerun()

        st.caption("Preview memakai struktur template dan data yang sedang diisi, tanpa memanggil AI.")
# Sesuaikan lebar konten utama dengan panel yang sedang terbuka.
_open_panels = int(ss.left_sidebar_open) + int(ss.right_panel_open)
if _open_panels == 2:
    _main_width_css = "calc(100vw - 42rem)"
elif _open_panels == 1:
    _main_width_css = "min(1120px, calc(100vw - 21.5rem))"
else:
    _main_width_css = "1120px"
st.markdown(
    f"""
    <style>
    @media (min-width: 1200px) {{
        .block-container {{
            max-width: {_main_width_css} !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# nilai template dipakai panel kiri dan halaman utama
o = tpl.get("opsi", {})
pakai_kop = tpl.get("kop", True)
meta_mode = tpl.get("meta", "kiri")

# ---------- Panel kiri: data & pengaturan ----------
with st.container(key="left_settings_panel"):
    st.markdown("""
    <div class="section-heading">
        <span class="material-symbols-rounded">tune</span>
        <div>
            <strong>Pengaturan dokumen</strong>
            <small>Data, kop, dan tata letak</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(field_icons_css(tpl), unsafe_allow_html=True)

    with st.expander("01  Isi data", expanded=True):
        nilai = {}
        for f in tpl["fields"]:
            key = f"fld_{tpl['id']}_{f['key']}"
            if f["type"] == "area":
                nilai[f["key"]] = st.text_area(f["label"], value=f.get("ph", ""),
                                               key=key, height=90)
            elif f["type"] == "date":
                _d = st.date_input(f["label"], key=key, format="DD/MM/YYYY")
                nilai[f["key"]] = tgl_hari(_d) if "hari" in f["label"].lower() else tgl(_d)
            elif f["type"] == "num":
                nilai[f["key"]] = str(st.number_input(f["label"], key=key, step=1))
            else:
                nilai[f["key"]] = st.text_input(f["label"], value=f.get("ph", ""), key=key)
        catatan = st.text_area("Catatan tambahan untuk AI", key="catatan_tpl", height=70,
                               placeholder="hal lain yang perlu ditulis...")

    with st.expander("02  Kop, nomor & penerima", expanded=False):
        kop = None
        if pakai_kop:
            kop = {
                "name": st.text_input("Nama instansi", "PEMERINTAH KABUPATEN ..."),
                "addr": st.text_input("Alamat", "Jalan Merdeka No. 1, Bandar Lampung"),
                "contact": st.text_input("Kontak", "Telp. (0721) 000000 | email@instansi.go.id"),
                "logo": None,
            }
            up = st.file_uploader("Logo (PNG/JPG)", ["png", "jpg", "jpeg"])
            if up:
                kop["logo"] = up.read()
        kota = st.text_input("Kota", "Bandar Lampung")
        tanggal = tgl(st.date_input("Tanggal surat", datetime.date.today()))
        kota_tgl = f"{kota}, {tanggal}"
        meta = None
        nomor_judul = ""
        if meta_mode == "kiri":
            meta = {"kota_tgl": kota_tgl, "nomor": st.text_input("Nomor surat", "800/   /2026"),
                    "lampiran": st.text_input("Lampiran", "-"),
                    "hal": st.text_input("Hal / perihal", tpl["judul"]),
                    "sifat": st.text_input("Sifat", "Biasa") if o.get("sifat") else "",
                    "tujuan": st.text_area("Kepada Yth. (satu per baris)",
                                           "Bapak/Ibu ...\ndi Tempat", height=80),
                    "up": st.text_input("Up. (opsional)", "") if o.get("up") else ""}
        elif meta_mode == "judul":
            nomor_judul = st.text_input("Nomor surat (di bawah judul)", "800/   /2026")
        tentang = ""
        if o.get("sk") or o.get("tentang"):
            tentang = st.text_input("Tentang", nilai.get("tentang", ""))

    with st.expander("03  Tanda tangan & lampiran blok", expanded=False):
        n_ttd = st.number_input("Jumlah penandatangan", 1, 4, int(o.get("ttd", 1)))
        labels = o.get("ttd_label") or []
        ttds = []
        for i in range(int(n_ttd)):
            st.markdown(f"**Penandatangan {i + 1}**")
            lab = st.text_input("Label", labels[i] if i < len(labels) else "",
                                key=f"lab{i}")
            jab = st.text_input("Jabatan", "" if lab else "Kepala Sekolah", key=f"jab{i}")
            nm = st.text_input("Nama", "", key=f"nm{i}")
            nip = st.text_input("NIP / NIK", "", key=f"nip{i}")
            ttd_img = st.file_uploader("Gambar tanda tangan", ["png", "jpg", "jpeg"],
                                       key=f"img{i}")
            ttds.append({"label": lab, "jabatan": jab, "nama": nm, "nip": nip,
                         "img": ttd_img.read() if ttd_img else None})
        verifikasi = st.text_input("Blok 'Mengetahui' (kosongkan bila tidak perlu)",
                                   o.get("verifikasi", ""))
        materai = st.checkbox("Kotak materai", bool(o.get("materai")))
        registrasi = st.checkbox("Blok registrasi (Dicatat Nomor/Tanggal)",
                                 bool(o.get("registrasi")))
        tutup_tgl = "ditetapkan" if st.checkbox(
            "Pakai 'Ditetapkan di / Pada tanggal'",
            o.get("tutup_tgl") == "ditetapkan") else "kota"
        tembusan_txt = st.text_area("Tembusan (satu per baris)",
                                    nilai.get("tembusan", "") if o.get("tembusan") else "",
                                    height=70)
        saksi_txt = st.text_area("Saksi (satu per baris)",
                                 nilai.get("saksi", "") if o.get("saksi") else "", height=70)
        nb_txt = st.text_area("Catatan NB", nilai.get("nb", "") if o.get("nb") else "",
                              height=60)
        slip_key = o.get("slip")
        slip_txt = st.text_area("Slip sobek di bawah dokumen",
                                SLIP_DEFAULT.get(slip_key, "") if slip_key else "",
                                height=120)

    with st.expander("04  Tata letak halaman", expanded=False):
        cfg = {
            "paper": st.selectbox("Ukuran kertas", list(PAPER)),
            "font": st.selectbox("Huruf", list(FONTS)),
            "size": st.slider("Ukuran huruf (pt)", 9, 14, 12),
            "spacing": st.select_slider("Spasi", [1.0, 1.15, 1.5, 2.0], 1.15),
            "mx": st.slider("Margin kiri-kanan (cm)", 1.5, 4.0, 2.5, 0.1),
            "my": st.slider("Margin atas-bawah (cm)", 1.5, 4.0, 2.5, 0.1),
            "align": st.selectbox("Perataan teks", list(ALIGN)),
            "pagefmt": st.selectbox("Nomor halaman", list(PAGE_FMT)),
            "pagepos": st.selectbox("Posisi nomor halaman", POS, index=1),
        }

    if mat_button("Reset dokumen", ":material/restart_alt:", use_container_width=True):
        ss.doc, ss.hasil, ss.notice, ss.page = None, None, None, "home"
        st.rerun()

# ---------- Rakit dokumen ----------
def rakit(data):
    """Gabungkan hasil AI + pengaturan sidebar jadi satu dokumen siap render."""
    return {
        "cfg": cfg, "kop": kop, "meta": meta,
        "memo": ({"tanggal": tanggal, "dari": nilai.get("dari", ""),
                  "kepada": nilai.get("kepada", ""),
                  "tembusan": nilai.get("tembusan_memo", ""),
                  "subyek": nilai.get("subyek", "")} if meta_mode == "memo" else None),
        "judul": data.get("judul") or tpl["judul"],
        "nomor_judul": nomor_judul, "tentang": tentang,
        "pembuka": data.get("pembuka", ""), "isi": data.get("isi", ""),
        "penutup": data.get("penutup", ""),
        "ttds": ttds, "kota_tgl": kota_tgl, "tutup_tgl": tutup_tgl,
        "verifikasi": verifikasi.strip(), "tembusan": parse_list(tembusan_txt),
        "saksi": parse_list(saksi_txt), "nb": nb_txt.strip(),
        "registrasi": registrasi, "materai": materai, "slip": slip_txt.strip(),
    }


# ---------- Halaman utama / preview template ----------
if ss.page == "template_preview":
    st.markdown("""
    <div class="result-heading">
        <span class="material-symbols-rounded">article</span>
        <h2>Preview template lengkap</h2>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"{jenis} · {tpl['nama']} · Preview ini memakai struktur template dan data yang sedang diisi.")

    back_cols = st.columns([1, 1.15, 1])
    with back_cols[1]:
        if mat_button("Kembali ke generator", ":material/arrow_back:",
                      use_container_width=True, key="back_from_template_page"):
            ss.page = "home"
            st.rerun()

    preview_doc = rakit(template_preview_content(tpl, nilai))
    st.iframe(build_html(preview_doc), height=1120)
else:
    render_orb()

    cta_cols = st.columns([1, 1.2, 1])
    with cta_cols[1]:
        buat = mat_button("Let's go, buat file nya", ":material/rocket_launch:",
                          type="primary", use_container_width=True, key="main_generate")

    if ss.notice:
        kind, text = ss.notice
        if kind == "success":
            st.success(text)
        elif kind == "error":
            st.error(text)
        else:
            st.info(text)

    if buat:
        bahan = brief_from_fields(tpl, nilai)
        tambahan = catatan.strip()
        if tambahan:
            bahan += "\nCatatan tambahan: " + tambahan
        with st.spinner("Menyusun dokumen…"):
            try:
                data, prov = generate(jenis, bahan, tone, length, tpl, nilai)
                ss.hasil = data
                ss.doc = rakit(data)
                ss.notice = ("success",
                             f"{data.get('judul', tpl['judul'])} selesai disusun "
                             f"(model: {prov}). Silakan lihat pratinjau dan unduh di bawah.")
            except Exception as e:
                ss.notice = ("error", f"Gagal: {e}")
        st.rerun()

    # ---------- Hasil ----------
    if ss.doc:
        doc = ss.doc
        st.divider()
        st.markdown("""
        <div class="result-heading">
            <span class="material-symbols-rounded">description</span>
            <h2>Hasil dokumen</h2>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([2, 1])
        with c1:
            arah = st.selectbox("Terjemahkan isi dokumen",
                                ["(tidak diterjemahkan)"] + list(LANG))
        with c2:
            st.write("")
            if mat_button("Terjemahkan", ":material/translate:", use_container_width=True,
                          disabled=arah == "(tidak diterjemahkan)"):
                with st.spinner("Menerjemahkan…"):
                    try:
                        data, prov = translate(ss.hasil, arah)
                        ss.hasil = data
                        doc.update({k: data.get(k, doc.get(k, "")) for k in KEYS})
                        ss.doc = doc
                        st.success(f"Dokumen diterjemahkan ({arah}, model: {prov}).")
                    except Exception as e:
                        st.error(f"Gagal menerjemahkan: {e}")

        t1, t2 = st.tabs(["Pratinjau", "Edit teks"])
        with t1:
            st.iframe(build_html(doc), height=1100)
        with t2:
            doc["judul"] = st.text_input("Judul", doc["judul"])
            doc["pembuka"] = st.text_area("Pembuka", doc["pembuka"], height=110)
            doc["isi"] = st.text_area("Isi", doc["isi"], height=380)
            doc["penutup"] = st.text_area("Penutup", doc["penutup"], height=110)
            if mat_button("Simpan perubahan", ":material/save:"):
                ss.doc = doc
                st.rerun()

        nama_file = re.sub(r"[^\w\- ]+", "", doc["judul"] or "dokumen").strip().replace(" ", "_")
        d1, d2 = st.columns(2)
        with d1:
            mat_download_button("Unduh Word (.docx)", build_docx(doc), f"{nama_file}.docx",
                                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                ":material/download:", use_container_width=True)
        with d2:
            mat_download_button("Unduh PDF", build_pdf(doc), f"{nama_file}.pdf",
                                "application/pdf", ":material/download:", use_container_width=True)
    else:
        render_info_box()
