import base64
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
APP_VER = f"v6 - {TPL.JUMLAH} template contoh nyata + terjemahan"
BASE_DIR = Path(__file__).resolve().parent
MAIN_LOGO = BASE_DIR / "assets" / "ampera_scribe_logo_animated.webp"

# ---------- Tema UI: Liquid Glass ----------
def inject_glassliquid_theme():
    """Suntikkan gaya visual glass-liquid, latar hitam bertekstur, dan glow animasi."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,300..700,0..1,-50..200&display=swap');

        :root {
            --amp-bg: #030303;
            --amp-bg-2: #08080d;
            --amp-glass: rgba(255, 255, 255, 0.075);
            --amp-glass-strong: rgba(255, 255, 255, 0.14);
            --amp-border: rgba(255, 255, 255, 0.22);
            --amp-border-soft: rgba(255, 255, 255, 0.11);
            --amp-text: #f7f7fb;
            --amp-muted: rgba(247, 247, 251, 0.70);
            --amp-blue: #7dd3fc;
            --amp-cyan: #22d3ee;
            --amp-violet: #a78bfa;
            --amp-pink: #fb7185;
            --amp-shadow: 0 24px 80px rgba(0, 0, 0, 0.55);
        }

        html, body, [data-testid="stAppViewContainer"], .stApp {
            color: var(--amp-text) !important;
            background: transparent !important;
        }

        .stApp {
            min-height: 100vh;
            overflow-x: hidden;
            background-color: var(--amp-bg) !important;
            background-image:
                radial-gradient(circle at 14% 22%, rgba(255,255,255,.055) 0 1px, transparent 1px 5px),
                radial-gradient(circle at 84% 18%, rgba(255,255,255,.040) 0 1px, transparent 1px 4px),
                radial-gradient(circle at 32% 82%, rgba(255,255,255,.030) 0 1px, transparent 1px 6px),
                repeating-linear-gradient(115deg, rgba(255,255,255,.028) 0 1px, transparent 1px 7px),
                linear-gradient(180deg, #020203 0%, #050507 46%, #020203 100%) !important;
            background-attachment: fixed !important;
        }

        .stApp::before {
            content: "";
            position: fixed;
            left: -22vw;
            right: -22vw;
            bottom: -42vh;
            height: 82vh;
            pointer-events: none;
            z-index: 0;
            opacity: .82;
            filter: blur(36px) saturate(1.45) hue-rotate(0deg);
            mix-blend-mode: screen;
            transform-origin: 50% 100%;
            background:
                conic-gradient(from 178deg at 50% 100%,
                    rgba(34, 211, 238, 0.00) 0deg,
                    rgba(34, 211, 238, 0.36) 18deg,
                    rgba(125, 211, 252, 0.05) 42deg,
                    rgba(167, 139, 250, 0.32) 66deg,
                    rgba(251, 113, 133, 0.08) 88deg,
                    rgba(34, 211, 238, 0.00) 118deg,
                    rgba(251, 113, 133, 0.34) 150deg,
                    rgba(167, 139, 250, 0.16) 178deg,
                    rgba(34, 211, 238, 0.00) 220deg,
                    rgba(34, 211, 238, 0.28) 252deg,
                    rgba(34, 211, 238, 0.00) 300deg),
                radial-gradient(ellipse at 50% 100%, rgba(34, 211, 238, 0.40) 0%, rgba(167, 139, 250, 0.18) 35%, transparent 68%);
            animation: amperaGlow 18s ease-in-out infinite alternate;
        }

        .stApp::after {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            opacity: .18;
            mix-blend-mode: overlay;
            background-image:
                radial-gradient(circle at 12% 18%, rgba(255,255,255,.35) 0 .7px, transparent .8px),
                radial-gradient(circle at 78% 34%, rgba(255,255,255,.25) 0 .6px, transparent .7px),
                radial-gradient(circle at 44% 72%, rgba(255,255,255,.22) 0 .8px, transparent .9px),
                linear-gradient(100deg, transparent 0 48%, rgba(255,255,255,.04) 49% 50%, transparent 51% 100%);
            background-size: 11px 11px, 17px 17px, 23px 23px, 41px 41px;
        }

        @keyframes amperaGlow {
            0% {
                transform: translate3d(-2%, 0, 0) scaleX(1) scaleY(.95);
                filter: blur(36px) saturate(1.45) hue-rotate(0deg);
                opacity: .70;
            }
            33% {
                transform: translate3d(2%, -4vh, 0) scaleX(1.08) scaleY(1.05);
                filter: blur(42px) saturate(1.65) hue-rotate(92deg);
                opacity: .86;
            }
            66% {
                transform: translate3d(-1%, -8vh, 0) scaleX(.96) scaleY(1.12);
                filter: blur(40px) saturate(1.8) hue-rotate(196deg);
                opacity: .78;
            }
            100% {
                transform: translate3d(2%, -2vh, 0) scaleX(1.12) scaleY(1.02);
                filter: blur(38px) saturate(1.55) hue-rotate(315deg);
                opacity: .88;
            }
        }

        [data-testid="stAppViewContainer"],
        [data-testid="stSidebar"],
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        .main, .block-container {
            position: relative;
            z-index: 1;
        }

        [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
            background: transparent !important;
        }

        .block-container {
            max-width: 1120px;
            padding-top: 2.1rem !important;
            padding-bottom: 3.2rem !important;
        }

        .block-container > div {
            border: 0 !important;
            border-radius: 0 !important;
            padding: 0 !important;
            background: transparent !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
            box-shadow: none !important;
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(160deg, rgba(255,255,255,.10), rgba(255,255,255,.035)),
                rgba(4,4,8,.72) !important;
            border-right: 1px solid var(--amp-border-soft);
            box-shadow: 24px 0 70px rgba(0, 0, 0, .40), inset -1px 0 0 rgba(255,255,255,.06);
            backdrop-filter: blur(30px) saturate(1.35);
            -webkit-backdrop-filter: blur(30px) saturate(1.35);
        }

        [data-testid="stSidebar"] > div,
        [data-testid="stSidebarContent"] {
            background: transparent !important;
        }

        [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stExpander"] {
            border: 1px solid rgba(255,255,255,.12) !important;
            border-radius: 22px !important;
            background: linear-gradient(145deg, rgba(255,255,255,.085), rgba(255,255,255,.028)) !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.10), 0 16px 45px rgba(0,0,0,.22);
            overflow: hidden;
        }

        [data-testid="stExpander"] summary {
            color: var(--amp-text) !important;
            font-weight: 700 !important;
            letter-spacing: .01em;
        }

        h1, h2, h3, h4, h5, h6,
        p, span, label, div, li,
        [data-testid="stMarkdownContainer"],
        [data-testid="stWidgetLabel"],
        [data-testid="stCaptionContainer"] {
            color: var(--amp-text);
        }

        [data-testid="stCaptionContainer"],
        small, .amp-muted {
            color: var(--amp-muted) !important;
        }

        .material-symbols-rounded {
            font-family: 'Material Symbols Rounded';
            font-weight: normal;
            font-style: normal;
            font-size: 1.25rem;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            white-space: nowrap;
            direction: ltr;
            -webkit-font-feature-settings: 'liga';
            -webkit-font-smoothing: antialiased;
            font-variation-settings: 'FILL' 0, 'wght' 500, 'GRAD' 0, 'opsz' 24;
        }

        .app-hero {
            position: relative;
            overflow: hidden;
            border-radius: 32px;
            border: 1px solid rgba(255,255,255,.18);
            padding: clamp(1.25rem, 3vw, 2.1rem);
            margin-bottom: 1.2rem;
            background:
                radial-gradient(circle at 16% 0%, rgba(125,211,252,.20), transparent 34%),
                radial-gradient(circle at 95% 12%, rgba(251,113,133,.16), transparent 36%),
                linear-gradient(135deg, rgba(255,255,255,.15), rgba(255,255,255,.045) 58%, rgba(255,255,255,.09));
            box-shadow: inset 0 1px 0 rgba(255,255,255,.20), 0 22px 70px rgba(0,0,0,.35);
        }

        .app-hero::after {
            content: "";
            position: absolute;
            width: 42%;
            height: 1px;
            left: 9%;
            top: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,.9), transparent);
            opacity: .75;
        }

        .app-hero-badge,
        .section-heading,
        .result-heading {
            display: flex;
            align-items: center;
            gap: .72rem;
        }

        .app-hero-badge .material-symbols-rounded,
        .section-heading .material-symbols-rounded,
        .result-heading .material-symbols-rounded {
            width: 2.4rem;
            height: 2.4rem;
            border-radius: 999px;
            color: #031014;
            background: linear-gradient(135deg, rgba(125,211,252,.96), rgba(167,139,250,.92), rgba(251,113,133,.90));
            box-shadow: 0 12px 35px rgba(34,211,238,.20), inset 0 1px 0 rgba(255,255,255,.55);
            font-variation-settings: 'FILL' 1, 'wght' 520, 'GRAD' 0, 'opsz' 28;
        }

        .app-hero h1 {
            margin: .65rem 0 .18rem;
            font-size: clamp(2.1rem, 6vw, 4.7rem);
            line-height: .92;
            letter-spacing: -.07em;
            background: linear-gradient(120deg, #fff, #d9f7ff 35%, #c4b5fd 70%, #fecdd3);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent !important;
            text-shadow: 0 0 34px rgba(125,211,252,.14);
        }

        .app-hero p {
            max-width: 780px;
            margin: .35rem 0 0;
            color: rgba(247,247,251,.76) !important;
            font-size: 1.02rem;
        }

        .section-heading {
            margin: .45rem 0 1rem;
        }

        .section-heading strong,
        .result-heading h2 {
            display: block;
            margin: 0;
            font-size: 1.28rem;
            line-height: 1.1;
        }

        .section-heading small {
            display: block;
            margin-top: .22rem;
            font-size: .78rem;
            letter-spacing: .07em;
            text-transform: uppercase;
        }

        .result-heading {
            margin: 1.2rem 0 .9rem;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-baseweb="select"] > div,
        [data-baseweb="base-input"],
        [data-testid="stDateInput"] input,
        [data-testid="stFileUploader"] section {
            color: var(--amp-text) !important;
            background: rgba(255,255,255,.075) !important;
            border: 1px solid rgba(255,255,255,.16) !important;
            border-radius: 16px !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.12), 0 10px 28px rgba(0,0,0,.20) !important;
        }

        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus,
        [data-baseweb="select"] > div:focus-within,
        [data-testid="stDateInput"] input:focus {
            border-color: rgba(125,211,252,.72) !important;
            box-shadow: 0 0 0 1px rgba(125,211,252,.26), 0 0 38px rgba(34,211,238,.12) !important;
        }

        input::placeholder, textarea::placeholder {
            color: rgba(247,247,251,.42) !important;
        }

        [data-testid="stSlider"] [role="slider"] {
            background: linear-gradient(135deg, var(--amp-blue), var(--amp-violet)) !important;
            border-color: rgba(255,255,255,.55) !important;
            box-shadow: 0 0 22px rgba(125,211,252,.42) !important;
        }

        [data-testid="stSlider"] div[data-testid="stTickBar"] {
            background: rgba(255,255,255,.12) !important;
        }

        .stButton > button,
        .stDownloadButton > button,
        [data-testid="baseButton-secondary"],
        [data-testid="baseButton-primary"] {
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,.24) !important;
            border-radius: 18px !important;
            color: #ffffff !important;
            background:
                linear-gradient(135deg, rgba(255,255,255,.18), rgba(255,255,255,.06) 48%, rgba(255,255,255,.12)) !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.28), 0 18px 42px rgba(0,0,0,.35) !important;
            backdrop-filter: blur(18px) saturate(1.55);
            -webkit-backdrop-filter: blur(18px) saturate(1.55);
            transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease, background .22s ease !important;
        }

        .stButton > button::before,
        .stDownloadButton > button::before,
        [data-testid="baseButton-secondary"]::before,
        [data-testid="baseButton-primary"]::before {
            content: "";
            position: absolute;
            inset: -65% auto -65% -50%;
            width: 48%;
            transform: rotate(22deg) translateX(-120%);
            background: linear-gradient(90deg, transparent, rgba(255,255,255,.50), transparent);
            transition: transform .65s ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        [data-testid="baseButton-secondary"]:hover,
        [data-testid="baseButton-primary"]:hover {
            transform: translateY(-1px);
            border-color: rgba(125,211,252,.72) !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.34), 0 22px 55px rgba(34,211,238,.16), 0 18px 42px rgba(0,0,0,.42) !important;
        }

        .stButton > button:hover::before,
        .stDownloadButton > button:hover::before,
        [data-testid="baseButton-secondary"]:hover::before,
        [data-testid="baseButton-primary"]:hover::before {
            transform: rotate(22deg) translateX(360%);
        }

        [data-testid="baseButton-primary"] {
            background:
                linear-gradient(135deg, rgba(34,211,238,.46), rgba(167,139,250,.30) 45%, rgba(251,113,133,.30)) !important;
            border-color: rgba(255,255,255,.32) !important;
        }

        [data-testid="stIconMaterial"] {
            color: #ffffff !important;
            font-variation-settings: 'FILL' 0, 'wght' 560, 'GRAD' 0, 'opsz' 24;
        }

        [data-testid="stChatMessage"] {
            border: 1px solid rgba(255,255,255,.12);
            border-radius: 22px;
            background: linear-gradient(145deg, rgba(255,255,255,.082), rgba(255,255,255,.032));
            box-shadow: inset 0 1px 0 rgba(255,255,255,.12), 0 12px 36px rgba(0,0,0,.22);
        }

        [data-testid="stChatInput"] {
            border-radius: 22px;
            background: rgba(255,255,255,.06) !important;
            border: 1px solid rgba(255,255,255,.14) !important;
            box-shadow: 0 18px 45px rgba(0,0,0,.28) !important;
            backdrop-filter: blur(18px);
        }

        [data-testid="stTabs"] button {
            border-radius: 999px !important;
            color: rgba(247,247,251,.72) !important;
        }

        [data-testid="stTabs"] button[aria-selected="true"] {
            color: #ffffff !important;
            background: rgba(255,255,255,.10) !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.18);
        }

        [data-testid="stAlert"] {
            border: 1px solid rgba(125,211,252,.24) !important;
            border-radius: 22px !important;
            background: linear-gradient(145deg, rgba(125,211,252,.11), rgba(255,255,255,.045)) !important;
            color: var(--amp-text) !important;
        }

        iframe,
        [data-testid="stHtml"],
        [data-testid="stHtml"] > div {
            border: 0 !important;
            box-shadow: none !important;
            background: transparent !important;
            outline: 0 !important;
        }

        .brand-logo-wrap {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: clamp(220px, 30vw, 340px);
            margin: 0 auto .75rem;
            pointer-events: none;
        }

        .brand-logo-wrap img {
            width: clamp(210px, 28vw, 360px);
            max-width: 72%;
            height: auto;
            display: block;
            mix-blend-mode: screen;
            transform-origin: 50% 55%;
            will-change: transform, filter;
            animation: amperaLogoFloat 6.5s ease-in-out infinite,
                       amperaLogoGlow 4.8s ease-in-out infinite alternate;
            filter: drop-shadow(0 0 34px rgba(34, 211, 238, .25))
                    drop-shadow(0 0 70px rgba(167, 139, 250, .18));
        }

        @keyframes amperaLogoFloat {
            0%, 100% { transform: translate3d(0, 0, 0) scale(1); }
            50% { transform: translate3d(0, -6px, 0) scale(1.015); }
        }

        @keyframes amperaLogoGlow {
            0% {
                filter: drop-shadow(0 0 30px rgba(34, 211, 238, .25))
                        drop-shadow(0 0 66px rgba(167, 139, 250, .17));
            }
            50% {
                filter: drop-shadow(0 0 38px rgba(236, 72, 153, .26))
                        drop-shadow(0 0 78px rgba(132, 204, 22, .14));
            }
            100% {
                filter: drop-shadow(0 0 34px rgba(251, 191, 36, .20))
                        drop-shadow(0 0 74px rgba(34, 211, 238, .18));
            }
        }

        hr {
            border-color: rgba(255,255,255,.11) !important;
        }

        a { color: #a5f3fc !important; }

        @media (max-width: 640px) {
            .block-container > div {
                padding: 0 !important;
                border-radius: 0 !important;
            }
            .app-hero {
                border-radius: 24px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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


def image_data_uri(path):
    """Konversi aset gambar lokal ke data URI untuk logo inline tanpa zona iframe."""
    suffix = Path(path).suffix.lower()
    mime = {
        ".png": "image/png",
        ".webp": "image/webp",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }.get(suffix, "application/octet-stream")
    encoded = base64.b64encode(Path(path).read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def secret(k):
    try:
        return st.secrets[k]
    except Exception:
        return os.environ.get(k, "")


def tgl(d):
    return f"{d.day} {BULAN[d.month - 1]} {d.year}"


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


# ---------- Status ----------
ss = st.session_state
ss.setdefault("doc", None)
ss.setdefault("hasil", None)
ss.setdefault("notice", None)
ss.setdefault("form", {})

inject_glassliquid_theme()

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

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("""
    <div class="section-heading">
        <span class="material-symbols-rounded">tune</span>
        <div>
            <strong>Pengaturan dokumen</strong>
            <small>Liquid glass workspace</small>
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
        tone = st.selectbox("Gaya bahasa", ["Formal", "Formal ramah", "Ringkas"])
        length = st.selectbox("Panjang", ["Ringkas", "Sedang", "Panjang"], index=1)

    o = tpl.get("opsi", {})
    pakai_kop = tpl.get("kop", True)
    meta_mode = tpl.get("meta", "kiri")

    with st.expander("02  Isi data", expanded=True):
        nilai = {}
        for f in tpl["fields"]:
            key = f"fld_{tpl['id']}_{f['key']}"
            if f["type"] == "area":
                nilai[f["key"]] = st.text_area(f["label"], value=f.get("ph", ""),
                                               key=key, height=90)
            elif f["type"] == "date":
                nilai[f["key"]] = tgl(st.date_input(f["label"], key=key))
            elif f["type"] == "num":
                nilai[f["key"]] = str(st.number_input(f["label"], key=key, step=1))
            else:
                nilai[f["key"]] = st.text_input(f["label"], value=f.get("ph", ""), key=key)
        catatan = st.text_area("Catatan tambahan untuk AI", key="catatan_tpl", height=70,
                               placeholder="hal lain yang perlu ditulis...")

    with st.expander("03  Kop, nomor & penerima", expanded=False):
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

    with st.expander("04  Tanda tangan & lampiran blok", expanded=False):
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

    with st.expander("05  Tata letak halaman", expanded=False):
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
        ss.doc, ss.hasil, ss.notice = None, None, None
        st.rerun()

# ---------- Halaman utama ----------
st.markdown(
    f"""
    <div class="brand-logo-wrap" aria-label="Logo Ampera Scribe">
        <img src="{image_data_uri(MAIN_LOGO)}" alt="Ampera Scribe">
    </div>
    """,
    unsafe_allow_html=True,
)

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
        st.components.v1.html(build_html(doc), height=1100, scrolling=True)
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
    st.info("Pilih **jenis** dan **template** di sidebar, isi datanya, lalu tekan "
            "**Let's go, buat file nya**. Semua template disalin dari contoh surat "
            "nyata, jadi kalimat bakunya sudah mengikuti aslinya — AI hanya mengisi "
            "bagian variabel.")
