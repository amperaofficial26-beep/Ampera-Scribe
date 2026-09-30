"""Pustaka template Ampera Scribe: jenis dokumen -> daftar cabang."""
from . import (tpl_undangan, tpl_tugas, tpl_keterangan, tpl_permohonan,
               tpl_pemberitahuan, tpl_izin, tpl_pernyataan, tpl_sk, tpl_lainnya)

TEMPLATES = {
    "Surat Undangan": tpl_undangan.ITEMS,
    "Surat Tugas": tpl_tugas.ITEMS,
    "Surat Keterangan": tpl_keterangan.ITEMS,
    "Surat Permohonan": tpl_permohonan.ITEMS,
    "Surat Pemberitahuan": tpl_pemberitahuan.ITEMS,
    "Surat Izin": tpl_izin.ITEMS,
    "Surat Pernyataan": tpl_pernyataan.ITEMS,
    "Surat Keputusan": tpl_sk.ITEMS,
    "Surat Edaran": tpl_lainnya.EDARAN,
    "Pengumuman": tpl_lainnya.PENGUMUMAN,
    "Memo / Nota Dinas": tpl_lainnya.MEMO,
    "Surat Pengantar": tpl_lainnya.PENGANTAR,
    "Berita Acara": tpl_lainnya.BERITA_ACARA,
}

JENIS = list(TEMPLATES)
JUMLAH = sum(len(v) for v in TEMPLATES.values())


def get(jenis, tpl_id):
    for t in TEMPLATES.get(jenis, []):
        if t["id"] == tpl_id:
            return t
    return TEMPLATES[jenis][0]


def opsi(tpl, key, default=None):
    return tpl.get("opsi", {}).get(key, default)


def brief_from_fields(tpl, values):
    """Ubah isian field template jadi teks bahan untuk AI."""
    baris = []
    for f in tpl["fields"]:
        v = (values.get(f["key"]) or "").strip()
        if v:
            baris.append(f"{f['label']}: {v}" if "\n" not in v else f"{f['label']}:\n{v}")
    return "\n".join(baris)
