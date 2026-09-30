"""Blok pembangun template Ampera Scribe.

Satu cabang template = dict dengan kunci:
    id      : kunci unik
    nama    : nama tampil
    desc    : penjelasan singkat
    kop     : True kalau surat berkop instansi
    meta    : "kiri"  -> Nomor/Lampiran/Hal di blok kiri atas (surat berkop)
              "judul" -> judul di tengah, nomor tepat di bawah judul
              "polos" -> tanpa nomor surat (surat pribadi / blangko)
    judul   : judul dokumen (dipakai kalau meta != "kiri")
    fields  : daftar isian khusus cabang ini
    outline : kerangka bagian isi (jadi sub-judul "# " atau urutan paragraf)
    baku    : contoh kalimat baku {pembuka, penutup} yang harus ditiru AI
    opsi    : fitur tata letak yang dinyalakan
              ttd       : jumlah penandatangan (1-4)
              ttd_label : label tiap penandatangan
              materai   : tampilkan kotak materai
              tembusan  : sediakan blok tembusan
              saksi     : sediakan blok saksi bertanda tangan
              tabel     : sediakan tabel daftar (petugas/peserta/barang)
              salam     : "umum" | "islami"
              tutup_tgl : "kota" (Kota, tanggal) | "ditetapkan" (Ditetapkan di/Pada tanggal)
              sifat     : tampilkan field Sifat (Biasa/Segera/Penting)
              blangko   : isian kosong jadi titik-titik
              slip      : "izin_ortu" | "kembar" -> slip sobek di bawah dokumen
"""


def F(k, l, t="text", ph=""):
    return {"key": k, "label": l, "type": t, "ph": ph}


def T(id, nama, desc, judul, outline, fields, baku, kop=True, meta="kiri", **opsi):
    return {"id": id, "nama": nama, "desc": desc, "kop": kop, "meta": meta,
            "judul": judul, "fields": fields, "outline": outline, "baku": baku,
            "opsi": opsi}


# ---------- kelompok field yang sering dipakai ulang ----------
IDENT = [
    F("nama_org", "Nama", "text", "Budi Santoso"),
    F("ttl", "Tempat / tanggal lahir", "text", "Bandar Lampung, 12 Mei 1990"),
    F("nik", "NIK", "text", ""),
    F("jk", "Jenis kelamin", "text", "Laki-laki"),
    F("agama", "Agama", "text", "Islam"),
    F("pekerjaan", "Pekerjaan", "text", ""),
    F("alamat_org", "Alamat", "area", ""),
]
IDENT_RINGKAS = [
    F("nama_org", "Nama", "text", "Budi Santoso"),
    F("jabatan_org", "Jabatan", "text", ""),
    F("alamat_org", "Alamat", "area", ""),
]
SISWA = [
    F("nama_siswa", "Nama siswa", "text", "Pebri Ramadhan"),
    F("kelas", "Kelas", "text", "XI IPA 2"),
    F("nis", "NIS / NISN", "text", ""),
    F("sekolah", "Asal sekolah", "text", ""),
]
MHS = [
    F("nama_mhs", "Nama mahasiswa", "text", ""),
    F("nim", "NIM", "text", ""),
    F("prodi", "Program studi / jurusan", "text", ""),
    F("semester", "Semester / tahun akademik", "text", "V (Lima) / 2025-2026"),
]
PEG = [
    F("nama_peg", "Nama pegawai", "text", ""),
    F("nip", "NIP / NUPTK / NIK", "text", ""),
    F("pangkat", "Pangkat / Gol. Ruang", "text", "Penata Muda, III/a"),
    F("jabatan_peg", "Jabatan", "text", ""),
    F("unit", "Unit kerja", "text", ""),
]
PENANDATANGAN_SURAT = [
    F("nama_ttd", "Nama pemberi keterangan/tugas", "text", ""),
    F("jabatan_ttd", "Jabatan pemberi", "text", ""),
]
ACARA = [
    F("hari_tgl", "Hari / tanggal", "text", "Senin, 5 Oktober 2026"),
    F("waktu", "Waktu / jam", "text", "09.00 WIB - selesai"),
    F("tempat", "Tempat", "text", "Aula Kantor Lantai 2"),
]
AGENDA = F("agenda", "Agenda / pembahasan (satu per baris)", "area",
           "Pembukaan\nPemaparan program\nDiskusi\nPenutup")
TUJUAN = [
    F("penerima", "Nama penerima", "text", "Bapak/Ibu Guru"),
    F("jabatan_penerima", "Jabatan penerima", "text", ""),
    F("instansi_penerima", "Instansi penerima", "text", ""),
    F("alamat_penerima", "Alamat penerima", "text", "di Tempat"),
]
DASAR = F("dasar", "Dasar / rujukan (satu per baris)", "area",
          "Surat Kepala Dinas Nomor ... tanggal ... perihal ...")
KEPERLUAN = F("keperluan", "Untuk keperluan", "text", "")
TABEL = F("tabel", "Daftar (pisahkan kolom dengan |, baris pertama = judul kolom)", "area",
          "Nama | NIP | Jabatan | Unit Kerja\nDewi Lestari, S.Pd. | 1234567890 | Guru | SD N 1")
TEMBUSAN = F("tembusan", "Tembusan (satu per baris)", "area",
             "Kepala Dinas Pendidikan\nArsip")
SAKSI = F("saksi", "Saksi (Nama (Hubungan), satu per baris)", "area",
          "Budi Santoso (Orang Tua/Wali)\nRina Anggraini (Ketua RT 04)")
POIN = F("poin", "Poin-poin isi (satu per baris)", "area", "")
