"""Tema "Ampera Scribe" - desain ulang sesuai gambar referensi (navy gelap, kaca biru-ungu)."""
import re
import streamlit as st

_MS = "font-family:'Material Symbols Rounded';font-weight:400;font-style:normal;line-height:1;" \
      "letter-spacing:normal;text-transform:none;white-space:nowrap;direction:ltr;" \
      "-webkit-font-feature-settings:'liga';font-feature-settings:'liga';"

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
.st-key-left_settings_panel,.st-key-right_template_panel{position:fixed;top:5.6rem;bottom:2.6rem;width:21.8rem;box-sizing:border-box;
  z-index:1001;overflow-y:auto;overflow-x:hidden;padding:4.1rem 1rem 1.4rem;border-radius:28px;
  border:1px solid var(--line);background:linear-gradient(180deg,rgba(16,26,70,.78),rgba(8,14,40,.84)) !important;
  box-shadow:0 24px 70px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.07);
  backdrop-filter:blur(26px) saturate(1.3);-webkit-backdrop-filter:blur(26px) saturate(1.3);
  scrollbar-width:thin;scrollbar-color:rgba(79,140,255,.55) transparent}
.st-key-left_settings_panel{left:1.1rem}
.st-key-right_template_panel{right:1.1rem}
@media (min-width:1200px){.block-container{max-width:calc(100vw - 48rem) !important}}
@media (max-width:1199px){
  .st-key-left_settings_panel,.st-key-right_template_panel{position:relative;inset:auto;width:auto;margin-bottom:1rem}
  .block-container{padding-top:6rem !important}}

/* tombol tutup panel */
.st-key-left_sidebar_top_toggle,.st-key-right_panel_top_toggle{position:fixed;top:6.25rem;z-index:1004}
.st-key-left_sidebar_top_toggle{left:2.2rem;width:10.9rem}
.st-key-right_panel_top_toggle{right:2.2rem;width:20.2rem}
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
.amp-orb-wrap{display:flex;justify-content:center;align-items:center;height:21rem;margin-top:clamp(1rem,13vh,9rem)}
.amp-orb{width:12.2rem;height:12.2rem;border-radius:50%;position:relative;animation:ampFloat 7s ease-in-out infinite;
  background:
    radial-gradient(circle at 30% 26%,#fff 0%,#cfe8ff 12%,rgba(120,180,255,.85) 32%,transparent 58%),
    radial-gradient(circle at 74% 58%,#ff6fae 0%,rgba(222,92,200,.85) 22%,transparent 52%),
    radial-gradient(circle at 60% 85%,rgba(96,70,255,.9),transparent 55%),
    radial-gradient(circle at 50% 50%,#3a66ff 0%,#2a35b8 70%,#1a1f6e 100%);
  box-shadow:0 0 50px rgba(100,140,255,.50),0 0 130px rgba(236,72,153,.28),inset -14px -18px 44px rgba(20,24,110,.65),inset 10px 10px 32px rgba(255,255,255,.30)}
.amp-orb::after{content:"";position:absolute;inset:-14%;border-radius:50%;z-index:-1;background:radial-gradient(circle,rgba(110,140,255,.30),transparent 68%);filter:blur(18px)}
@keyframes ampFloat{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-8px) scale(1.025)}}
@media (prefers-reduced-motion:reduce){.amp-orb,.stApp::before,.stApp::after{animation:none}}

/* kotak info */
.amp-info{display:flex;align-items:center;gap:1.2rem;max-width:49rem;margin:1.1rem auto 0;padding:1.25rem 1.5rem;border-radius:18px;border:1.5px solid transparent;
  background:linear-gradient(rgba(14,22,66,.92),rgba(14,22,66,.92)) padding-box,linear-gradient(90deg,rgba(79,140,255,.75),rgba(168,85,247,.75)) border-box;
  box-shadow:0 18px 50px rgba(30,40,140,.25)}
.amp-info-ic{width:3.1rem;height:3.1rem;flex:none;border-radius:14px;display:flex;align-items:center;justify-content:center;background:rgba(79,110,255,.22)}
.amp-info-ic .ms{font-size:1.5rem;color:#a9c0ff}
.amp-info p{margin:0;font-size:.95rem;line-height:1.65}
.amp-info b{color:#fff;font-weight:700}
.amp-info b.hl{color:var(--cyan)}

/* lain-lain */
[data-testid="stAlert"]{border:1px solid var(--line2) !important;border-radius:18px !important;background:rgba(24,38,96,.55) !important}
[data-testid="stTabs"] button{border-radius:999px !important}
[data-testid="stTabs"] button[aria-selected="true"]{background:rgba(79,140,255,.20) !important}
iframe,[data-testid="stHtml"]{border:0 !important;background:transparent !important}
</style>
"""

ICONS = [  # (kata kunci, ikon label, ikon dalam kolom)
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
    """Ikon di samping label dan di dalam kolom isian, untuk semua field template aktif."""
    rules = []
    for f in tpl.get("fields", []):
        cls = re.sub(r"[^\w-]", "-", f"fld_{tpl['id']}_{f['key']}")
        il, ifld = icon_for(f.get("label", f["key"]))
        sel = f".st-key-{cls}"
        area = f.get("type") == "area"
        top = "top:.9rem" if area else "top:50%;transform:translateY(-50%)"
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
