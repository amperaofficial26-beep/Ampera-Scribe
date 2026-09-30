# Analisis Repositori — Ampera Scribe

Tanggal analisis: 29 September 2026
Isi repo: `app.py` (≈400 baris), `requirements.txt`. Tidak ada README, lisensi, .gitignore, test, atau CI.

## 1. Ringkasan produk

Aplikasi Streamlit satu-file untuk membuat dokumen berbahasa Indonesia (Surat Resmi, Undangan, Laporan, Rangkuman, Notulen) dengan bantuan LLM, lalu mengekspornya ke **.docx** (python-docx) dan **.pdf** (ReportLab).

Alur: input sidebar (kop surat, layout) → brief → `generate()` memanggil provider OpenAI-compatible (Groq, lalu Plugsky) → hasil JSON (judul/pembuka/isi/penutup) bisa diedit → `build_docx()` / `build_pdf()` → tombol unduh.

**Kekuatan:** kode padat dan rapi, dua renderer berbagi struktur data `d` yang sama, mini-markup (`# `, `- `, baris kosong) sederhana tapi efektif, fallback multi-provider, dukungan kop surat + tanda tangan + nomor halaman (PAGE/NUMPAGES field asli di Word).

## 2. Temuan teknis (prioritas)

### Bug / risiko nyata
| # | Isu | Lokasi | Dampak |
|---|-----|--------|--------|
| B1 | Font PDF dipetakan ke core font (Times-Roman/Helvetica). "Calibri" jadi Helvetica, dan **glyph non-Latin1 (—, “ ”, →, emoji) jadi kotak hitam** | `FONTS`, `build_pdf` | Output PDF beda dari Word; karakter rusak |
| B2 | `re.search(r"\{.*\}", ...)` bisa `None` → `AttributeError` yang tertelan jadi pesan provider gagal | `generate()` | Error membingungkan; tidak ada retry |
| B3 | Tidak ada `response_format={"type":"json_object"}` maupun validasi skema | `generate()` | Parsing rapuh |
| B4 | `nomor/lampiran/perihal/tujuan` hanya terdefinisi saat `is_surat`; jika user ganti jenis dokumen setelah generate, Streamlit rerun bisa `NameError` | baris ~346 & ~385 | Crash UI |
| B5 | `build_docx`/`build_pdf` dipanggil setiap rerun (setiap ketikan di editor) — dua dokumen dibangun ulang tanpa cache | blok akhir | Lambat pada dokumen panjang |
| B6 | Upload logo/tanda tangan tidak divalidasi ukuran/dimensi; gambar besar bisa membengkakkan memori | uploader | DoS ringan |
| B7 | Elemen kop pakai tabel tanpa `t.style`/border off eksplisit di Word; margin/lebar kolom dihitung manual | `build_docx` | Layout bisa meleset di kertas Legal |
| B8 | `esc()` hanya untuk ReportLab; teks Word aman, tapi mini-markup tidak mendukung bold/italic inline | `blocks()` | Fitur terbatas |
| B9 | `requirements.txt` tanpa pin versi | repo | Build tidak reproducible |

### Kebersihan repo
- Tidak ada **README**, petunjuk menjalankan, atau contoh `.streamlit/secrets.toml`.
- Tidak ada **.gitignore** (risiko `secrets.toml`/`__pycache__` ikut ter-commit).
- Tidak ada **lisensi**, tidak ada test, tidak ada CI.
- Histori commit tipis ("Update app.py") — tidak ada konvensi commit.

## 3. Rekomendasi pengembangan

### Tahap 0 — Fondasi (½ hari)
1. `README.md`: deskripsi, screenshot, cara jalan (`streamlit run app.py`), cara isi `GROQ_API_KEY`.
2. `.gitignore` (Python + `.streamlit/secrets.toml`), `secrets.toml.example`, `LICENSE`.
3. Pin versi di `requirements.txt`; tambahkan `ruff` + GitHub Actions (lint + smoke test).

### Tahap 1 — Stabilitas (1–2 hari)
4. Refactor jadi paket: `ampera/ai.py`, `ampera/docx_builder.py`, `ampera/pdf_builder.py`, `ampera/models.py` (dataclass `DocConfig`, `Kop`, `Sign`, `DocData`), `app.py` tinggal UI. Ini juga membuat builder bisa dites tanpa Streamlit.
5. Perbaiki B2–B4: JSON mode + validasi skema (pydantic), pesan error per-provider yang jelas, state dokumen disimpan utuh di `st.session_state` (termasuk field surat).
6. `@st.cache_data` untuk `build_docx`/`build_pdf` berdasarkan hash dict `d`, atau bangun file hanya saat tombol "Siapkan unduhan" ditekan.
7. Embed font TTF (DejaVu/Liberation atau Carlito untuk Calibri-metric) via `pdfmetrics.registerFont` agar B1 hilang dan PDF ≈ Word.

### Tahap 2 — Fitur bernilai tinggi
8. **Pratinjau PDF in-app** (render halaman pertama ke gambar via pypdfium2) — hilangkan siklus unduh-cek-ulang.
9. **Template dokumen** siap pakai: Surat Tugas, Surat Keterangan, SK, Berita Acara, Undangan Rapat, Notulen — dengan field terstruktur, bukan hanya brief bebas.
10. **Simpan & muat konfigurasi** (kop, font, tanda tangan) sebagai profil JSON per organisasi.
11. **Editor kaya**: dukung `**tebal**`, `*miring*`, tabel sederhana `|a|b|`, penomoran otomatis (1., a., i.).
12. **Riwayat dokumen** + tombol "Perbaiki bagian ini" (regenerate per-seksi dengan instruksi).
13. Nomor surat otomatis dengan pola (`001/SK/AMP/IX/2026`) memakai angka Romawi bulan.
14. Ekspor tambahan: Markdown/HTML, dan `.docx` dari template pengguna (docxtpl).

### Tahap 3 — Skala
15. Pisahkan backend FastAPI (`/generate`, `/render`) agar bisa dipakai non-Streamlit; Streamlit jadi klien.
16. Autentikasi ringan + kuota bila di-deploy publik (API key provider Anda yang terbakar).
17. Dockerfile + deploy (Streamlit Cloud / Fly.io), logging terstruktur, metrik penggunaan.
18. Test: unit untuk `blocks()`, snapshot byte-level/struktur untuk docx, dan smoke test PDF (jumlah halaman > 0).

## 4. Saran urutan kerja

1. Tahap 0 (README, .gitignore, pin versi) — cepat, langsung menaikkan kualitas repo.
2. B2/B3/B4 — bug yang paling sering terlihat user.
3. Refactor modul + test `blocks()`.
4. Font TTF + pratinjau PDF — dua fitur dengan dampak persepsi kualitas terbesar.
5. Template dokumen & profil kop — nilai jual utama untuk instansi.
