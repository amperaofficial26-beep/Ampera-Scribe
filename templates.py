"""Pustaka template dokumen Ampera Scribe.

Struktur satu template:
    id       : kunci unik
    nama     : nama yang tampil di UI
    desc     : penjelasan singkat
    surat    : True  -> pakai blok kop/nomor/lampiran/perihal/tujuan (format surat)
               False -> pakai judul di tengah (format laporan/makalah)
    judul    : usulan judul default (boleh dipakai/diubah user)
    outline  : kerangka bagian yang harus ditulis AI (jadi "# sub-judul" di isi)
    fields   : field isian khusus template ->
               (key, label, tipe, placeholder)
               tipe: "text" | "area" | "date" | "num"
"""

F = lambda k, l, t="text", ph="": {"key": k, "label": l, "type": t, "ph": ph}

# ---------- field yang sering dipakai ulang ----------
ACARA = [
    F("nama_acara", "Nama acara", "text", "Rapat Koordinasi Triwulan I"),
    F("hari_tgl", "Hari / tanggal", "text", "Senin, 5 Oktober 2026"),
    F("waktu", "Waktu", "text", "09.00 WIB - selesai"),
    F("tempat", "Tempat", "text", "Aula Kantor Lantai 2"),
    F("agenda", "Agenda / susunan acara (satu per baris)", "area",
      "Pembukaan\nPemaparan program\nDiskusi\nPenutup"),
]
PEG = [
    F("nama_org", "Nama orang / pihak", "text", "Budi Santoso"),
    F("jabatan_org", "Jabatan / status", "text", "Staf Administrasi"),
    F("nip_org", "NIP / NIK / NIM", "text", ""),
]

TEMPLATES = {
    # ============================================================ SURAT RESMI
    "Surat Resmi": [
        {
            "id": "surat_tugas", "nama": "Surat Tugas", "surat": True,
            "desc": "Penugasan pegawai untuk melaksanakan kegiatan tertentu.",
            "judul": "Surat Tugas",
            "outline": ["Dasar penugasan", "Data pegawai yang ditugaskan",
                        "Uraian tugas", "Waktu dan tempat pelaksanaan", "Penutup"],
            "fields": PEG + [
                F("dasar", "Dasar / rujukan penugasan", "area", "Surat Undangan No. ... tanggal ..."),
                F("tugas", "Uraian tugas", "area", "Mengikuti Bimbingan Teknis ..."),
                F("waktu_tugas", "Waktu pelaksanaan", "text", "5 - 7 Oktober 2026"),
                F("tempat_tugas", "Tempat pelaksanaan", "text", "Hotel Sheraton, Bandar Lampung"),
            ],
        },
        {
            "id": "surat_keterangan", "nama": "Surat Keterangan", "surat": True,
            "desc": "Menerangkan status, domisili, atau keadaan seseorang.",
            "judul": "Surat Keterangan",
            "outline": ["Identitas pemberi keterangan", "Identitas yang diterangkan",
                        "Isi keterangan", "Peruntukan surat", "Penutup"],
            "fields": PEG + [
                F("alamat_org", "Alamat", "area", ""),
                F("isi_keterangan", "Hal yang diterangkan", "area",
                  "Benar-benar warga RT 05 / RW 02 dan berkelakuan baik"),
                F("keperluan", "Untuk keperluan", "text", "Pengurusan beasiswa"),
            ],
        },
        {
            "id": "surat_permohonan", "nama": "Surat Permohonan", "surat": True,
            "desc": "Memohon bantuan, izin, dana, narasumber, atau kerja sama.",
            "judul": "Surat Permohonan",
            "outline": ["Latar belakang", "Isi permohonan", "Harapan dan ucapan terima kasih"],
            "fields": [
                F("yang_dimohon", "Hal yang dimohon", "text", "Bantuan dana kegiatan"),
                F("latar", "Latar belakang / alasan", "area", ""),
                F("rincian", "Rincian permohonan", "area", ""),
                F("batas_waktu", "Batas waktu yang diharapkan", "text", ""),
            ],
        },
        {
            "id": "surat_pemberitahuan", "nama": "Surat Pemberitahuan", "surat": True,
            "desc": "Menyampaikan informasi resmi kepada pihak terkait.",
            "judul": "Surat Pemberitahuan",
            "outline": ["Pembuka", "Isi pemberitahuan", "Hal yang perlu diperhatikan", "Penutup"],
            "fields": [
                F("pokok", "Pokok pemberitahuan", "text", "Perubahan jam pelayanan"),
                F("detail", "Detail informasi", "area", ""),
                F("berlaku", "Mulai berlaku", "text", "1 November 2026"),
            ],
        },
        {
            "id": "surat_edaran", "nama": "Surat Edaran", "surat": True,
            "desc": "Instruksi/imbauan yang berlaku untuk banyak penerima.",
            "judul": "Surat Edaran",
            "outline": ["Dasar", "Maksud dan tujuan", "Ketentuan / poin edaran", "Penutup"],
            "fields": [
                F("dasar", "Dasar hukum / rujukan", "area", ""),
                F("poin", "Poin-poin edaran (satu per baris)", "area", ""),
                F("sasaran", "Ditujukan untuk", "text", "Seluruh kepala unit kerja"),
            ],
        },
        {
            "id": "sk", "nama": "Surat Keputusan (SK)", "surat": True,
            "desc": "Keputusan resmi dengan format Menimbang - Mengingat - Memutuskan.",
            "judul": "Surat Keputusan",
            "outline": ["Menimbang", "Mengingat", "Memutuskan", "Diktum Kesatu s.d. terakhir"],
            "fields": [
                F("tentang", "Tentang", "text", "Pengangkatan Panitia Hari Ulang Tahun"),
                F("menimbang", "Pertimbangan (satu per baris)", "area", ""),
                F("mengingat", "Dasar hukum (satu per baris)", "area", ""),
                F("memutuskan", "Isi keputusan (satu per baris)", "area", ""),
                F("mulai_berlaku", "Mulai berlaku", "text", "sejak tanggal ditetapkan"),
            ],
        },
        {
            "id": "surat_pernyataan", "nama": "Surat Pernyataan", "surat": False,
            "desc": "Pernyataan pribadi bermaterai tentang suatu komitmen/fakta.",
            "judul": "Surat Pernyataan",
            "outline": ["Identitas pembuat pernyataan", "Isi pernyataan", "Penutup dan kesediaan sanksi"],
            "fields": PEG + [
                F("alamat_org", "Alamat", "area", ""),
                F("isi_pernyataan", "Isi pernyataan (satu per baris)", "area", ""),
                F("konsekuensi", "Konsekuensi bila dilanggar", "text",
                  "bersedia menerima sanksi sesuai ketentuan yang berlaku"),
            ],
        },
        {
            "id": "surat_kuasa", "nama": "Surat Kuasa", "surat": False,
            "desc": "Pelimpahan wewenang dari pemberi ke penerima kuasa.",
            "judul": "Surat Kuasa",
            "outline": ["Identitas pemberi kuasa", "Identitas penerima kuasa",
                        "Hal yang dikuasakan", "Penutup"],
            "fields": [
                F("pemberi", "Pemberi kuasa (nama, NIK, alamat)", "area", ""),
                F("penerima", "Penerima kuasa (nama, NIK, alamat)", "area", ""),
                F("dikuasakan", "Hal yang dikuasakan", "area", "Mengambil dokumen ... di ..."),
                F("masa", "Masa berlaku", "text", ""),
            ],
        },
        {
            "id": "surat_rekomendasi", "nama": "Surat Rekomendasi", "surat": True,
            "desc": "Merekomendasikan seseorang untuk studi, kerja, atau beasiswa.",
            "judul": "Surat Rekomendasi",
            "outline": ["Identitas pemberi rekomendasi", "Identitas yang direkomendasikan",
                        "Penilaian dan alasan", "Rekomendasi dan penutup"],
            "fields": PEG + [
                F("untuk", "Direkomendasikan untuk", "text", "Program Beasiswa Unggulan 2026"),
                F("kelebihan", "Kelebihan / prestasi (satu per baris)", "area", ""),
                F("lama_kenal", "Lama mengenal / hubungan", "text", "3 tahun sebagai dosen pembimbing"),
            ],
        },
        {
            "id": "surat_peringatan", "nama": "Surat Peringatan (SP)", "surat": True,
            "desc": "Teguran resmi atas pelanggaran disiplin kerja.",
            "judul": "Surat Peringatan",
            "outline": ["Dasar", "Uraian pelanggaran", "Peringatan dan sanksi", "Penutup"],
            "fields": PEG + [
                F("tingkat", "Tingkat peringatan", "text", "SP-1"),
                F("pelanggaran", "Uraian pelanggaran", "area", ""),
                F("sanksi", "Sanksi bila diulang", "area", ""),
            ],
        },
        {
            "id": "surat_balasan", "nama": "Surat Balasan", "surat": True,
            "desc": "Menjawab surat masuk (menerima/menolak/menindaklanjuti).",
            "judul": "Surat Balasan",
            "outline": ["Rujukan surat masuk", "Tanggapan", "Tindak lanjut", "Penutup"],
            "fields": [
                F("surat_masuk", "Nomor & tanggal surat yang dibalas", "text", ""),
                F("sikap", "Sikap", "text", "Menerima / Menyetujui"),
                F("tanggapan", "Isi tanggapan", "area", ""),
            ],
        },
        {
            "id": "surat_izin", "nama": "Surat Izin (tidak masuk)", "surat": True,
            "desc": "Izin tidak masuk kerja/sekolah karena alasan tertentu.",
            "judul": "Surat Izin",
            "outline": ["Identitas", "Alasan izin", "Lama izin", "Penutup"],
            "fields": PEG + [
                F("alasan", "Alasan izin", "area", "Sakit demam dan perlu istirahat"),
                F("lama", "Lama izin", "text", "2 hari, 1 - 2 Oktober 2026"),
                F("lampiran_izin", "Lampiran pendukung", "text", "Surat keterangan dokter"),
            ],
        },
        {
            "id": "surat_pengantar", "nama": "Surat Pengantar", "surat": True,
            "desc": "Pengantar pengiriman dokumen/barang atau pengantar warga.",
            "judul": "Surat Pengantar",
            "outline": ["Maksud pengantar", "Daftar dokumen/barang yang dikirim", "Penutup"],
            "fields": [
                F("maksud", "Maksud pengantar", "text", ""),
                F("daftar", "Daftar dokumen / barang (satu per baris)", "area", ""),
            ],
        },
        {
            "id": "surat_lamaran", "nama": "Surat Lamaran Kerja", "surat": False,
            "desc": "Lamaran kerja lengkap dengan data diri dan berkas.",
            "judul": "Surat Lamaran Pekerjaan",
            "outline": ["Sumber informasi lowongan", "Data diri", "Kualifikasi dan pengalaman",
                        "Berkas terlampir", "Harapan dan penutup"],
            "fields": [
                F("posisi", "Posisi yang dilamar", "text", "Staf Administrasi"),
                F("perusahaan", "Perusahaan tujuan", "text", ""),
                F("sumber_info", "Sumber informasi lowongan", "text", "Instagram resmi perusahaan"),
                F("data_diri", "Data diri (nama, TTL, pendidikan, kontak)", "area", ""),
                F("pengalaman", "Pengalaman & keahlian", "area", ""),
                F("berkas", "Berkas terlampir (satu per baris)", "area", "CV\nFotokopi ijazah\nKTP"),
            ],
        },
    ],

    # ============================================================== UNDANGAN
    "Undangan": [
        {
            "id": "und_rapat", "nama": "Undangan Rapat", "surat": True,
            "desc": "Undangan rapat internal lengkap dengan agenda.",
            "judul": "Undangan Rapat",
            "outline": ["Pembuka", "Detail waktu dan tempat", "Agenda rapat", "Penutup"],
            "fields": ACARA + [F("catatan", "Catatan tambahan", "area", "Mohon hadir tepat waktu")],
        },
        {
            "id": "und_acara", "nama": "Undangan Acara Resmi", "surat": True,
            "desc": "Peresmian, pelantikan, HUT instansi, dan acara seremonial.",
            "judul": "Undangan Acara",
            "outline": ["Pembuka", "Detail acara", "Susunan acara", "Harapan kehadiran"],
            "fields": ACARA + [
                F("pakaian", "Pakaian", "text", "Batik / Seragam Dinas"),
                F("konfirmasi", "Konfirmasi kehadiran ke", "text", ""),
            ],
        },
        {
            "id": "und_seminar", "nama": "Undangan Seminar / Workshop", "surat": True,
            "desc": "Undangan kegiatan ilmiah dengan narasumber.",
            "judul": "Undangan Seminar",
            "outline": ["Pembuka dan latar kegiatan", "Detail pelaksanaan",
                        "Narasumber dan materi", "Cara pendaftaran", "Penutup"],
            "fields": ACARA + [
                F("narasumber", "Narasumber (satu per baris)", "area", ""),
                F("biaya", "Biaya / gratis", "text", "Gratis"),
                F("daftar_link", "Link / cara pendaftaran", "text", ""),
            ],
        },
        {
            "id": "und_syukuran", "nama": "Undangan Syukuran / Tasyakuran", "surat": False,
            "desc": "Undangan semi-formal untuk acara keluarga atau syukuran.",
            "judul": "Undangan Syukuran",
            "outline": ["Salam pembuka", "Maksud acara", "Waktu dan tempat", "Harapan kehadiran"],
            "fields": ACARA + [F("tuan_rumah", "Tuan rumah / keluarga", "text", "")],
        },
        {
            "id": "und_warga", "nama": "Undangan Warga (RT/RW)", "surat": True,
            "desc": "Undangan musyawarah, kerja bakti, atau arisan warga.",
            "judul": "Undangan Musyawarah Warga",
            "outline": ["Pembuka", "Waktu dan tempat", "Agenda musyawarah", "Penutup"],
            "fields": ACARA + [F("wilayah", "RT / RW / Dusun", "text", "RT 05 RW 02")],
        },
        {
            "id": "und_pernikahan", "nama": "Undangan Pernikahan", "surat": False,
            "desc": "Undangan pernikahan dengan akad dan resepsi.",
            "judul": "Undangan Pernikahan",
            "outline": ["Salam pembuka", "Nama kedua mempelai dan orang tua",
                        "Waktu akad", "Waktu resepsi", "Harapan doa restu"],
            "fields": [
                F("mempelai_pria", "Mempelai pria (nama & orang tua)", "area", ""),
                F("mempelai_wanita", "Mempelai wanita (nama & orang tua)", "area", ""),
                F("akad", "Akad nikah (hari, tanggal, jam)", "text", ""),
                F("resepsi", "Resepsi (hari, tanggal, jam)", "text", ""),
                F("tempat", "Tempat", "area", ""),
            ],
        },
    ],

    # =============================================================== LAPORAN
    "Laporan": [
        {
            "id": "lap_kegiatan", "nama": "Laporan Kegiatan", "surat": False,
            "desc": "Laporan pelaksanaan kegiatan/acara beserta evaluasi.",
            "judul": "Laporan Kegiatan",
            "outline": ["Pendahuluan", "Dasar Kegiatan", "Maksud dan Tujuan", "Waktu dan Tempat",
                        "Peserta", "Pelaksanaan Kegiatan", "Anggaran", "Hasil yang Dicapai",
                        "Kendala dan Saran", "Penutup"],
            "fields": ACARA + [
                F("penyelenggara", "Penyelenggara", "text", ""),
                F("peserta", "Peserta / jumlah peserta", "text", ""),
                F("anggaran", "Anggaran (rincian singkat)", "area", ""),
                F("hasil", "Hasil yang dicapai", "area", ""),
                F("kendala", "Kendala", "area", ""),
            ],
        },
        {
            "id": "lap_bulanan", "nama": "Laporan Bulanan / Periodik", "surat": False,
            "desc": "Laporan kinerja rutin per bulan atau per triwulan.",
            "judul": "Laporan Bulanan",
            "outline": ["Pendahuluan", "Ringkasan Capaian", "Uraian Kegiatan",
                        "Realisasi Target", "Kendala", "Rencana Periode Berikutnya", "Penutup"],
            "fields": [
                F("periode", "Periode laporan", "text", "September 2026"),
                F("unit", "Unit / bagian", "text", ""),
                F("capaian", "Capaian utama (satu per baris)", "area", ""),
                F("target", "Target vs realisasi", "area", ""),
                F("rencana", "Rencana bulan depan", "area", ""),
            ],
        },
        {
            "id": "lap_keuangan", "nama": "Laporan Keuangan Sederhana", "surat": False,
            "desc": "Laporan pemasukan, pengeluaran, dan saldo kegiatan/organisasi.",
            "judul": "Laporan Keuangan",
            "outline": ["Pendahuluan", "Sumber Dana", "Rincian Pemasukan",
                        "Rincian Pengeluaran", "Saldo Akhir", "Penutup"],
            "fields": [
                F("periode", "Periode", "text", "1 - 30 September 2026"),
                F("pemasukan", "Pemasukan (uraian : jumlah, satu per baris)", "area",
                  "Iuran anggota : 2.000.000\nDonasi : 500.000"),
                F("pengeluaran", "Pengeluaran (uraian : jumlah, satu per baris)", "area", ""),
                F("saldo", "Saldo akhir", "text", ""),
            ],
        },
        {
            "id": "lap_dinas", "nama": "Laporan Perjalanan Dinas", "surat": False,
            "desc": "Laporan hasil perjalanan dinas atau kunjungan kerja.",
            "judul": "Laporan Perjalanan Dinas",
            "outline": ["Dasar Perjalanan", "Maksud dan Tujuan", "Waktu dan Tempat",
                        "Pelaksana", "Hasil Kunjungan", "Kesimpulan dan Saran"],
            "fields": PEG + [
                F("dasar", "Dasar / surat tugas", "text", ""),
                F("tujuan_kota", "Tujuan (kota/instansi)", "text", ""),
                F("waktu_tugas", "Waktu", "text", ""),
                F("hasil", "Hasil / temuan", "area", ""),
            ],
        },
        {
            "id": "lap_pkl", "nama": "Laporan Magang / PKL", "surat": False,
            "desc": "Laporan praktik kerja lapangan mahasiswa/siswa.",
            "judul": "Laporan Praktik Kerja Lapangan",
            "outline": ["Pendahuluan", "Profil Tempat PKL", "Waktu Pelaksanaan",
                        "Uraian Kegiatan", "Kompetensi yang Diperoleh",
                        "Kendala dan Solusi", "Kesimpulan dan Saran"],
            "fields": PEG + [
                F("instansi_pkl", "Tempat PKL", "text", ""),
                F("periode", "Periode PKL", "text", "1 Juli - 30 September 2026"),
                F("bidang", "Bidang / divisi penempatan", "text", ""),
                F("kegiatan", "Kegiatan yang dilakukan (satu per baris)", "area", ""),
                F("pembimbing", "Pembimbing lapangan", "text", ""),
            ],
        },
        {
            "id": "lap_praktikum", "nama": "Laporan Praktikum", "surat": False,
            "desc": "Laporan percobaan/praktikum sains dan teknik.",
            "judul": "Laporan Praktikum",
            "outline": ["Tujuan Praktikum", "Dasar Teori", "Alat dan Bahan",
                        "Langkah Kerja", "Hasil Pengamatan", "Pembahasan", "Kesimpulan"],
            "fields": [
                F("judul_praktikum", "Judul praktikum", "text", ""),
                F("mata_kuliah", "Mata kuliah / pelajaran", "text", ""),
                F("alat_bahan", "Alat dan bahan (satu per baris)", "area", ""),
                F("langkah", "Langkah kerja (satu per baris)", "area", ""),
                F("data", "Data / hasil pengamatan", "area", ""),
            ],
        },
        {
            "id": "proposal", "nama": "Proposal Kegiatan", "surat": False,
            "desc": "Proposal pengajuan kegiatan lengkap dengan anggaran.",
            "judul": "Proposal Kegiatan",
            "outline": ["Latar Belakang", "Dasar Pemikiran", "Nama dan Tema Kegiatan",
                        "Maksud dan Tujuan", "Sasaran Peserta", "Waktu dan Tempat",
                        "Susunan Acara", "Susunan Panitia", "Anggaran Biaya", "Penutup"],
            "fields": ACARA + [
                F("tema", "Tema kegiatan", "text", ""),
                F("latar", "Latar belakang", "area", ""),
                F("sasaran", "Sasaran peserta", "text", ""),
                F("panitia", "Susunan panitia (satu per baris)", "area", ""),
                F("anggaran", "Rencana anggaran (uraian : jumlah)", "area", ""),
            ],
        },
        {
            "id": "proposal_sponsor", "nama": "Proposal Sponsorship", "surat": False,
            "desc": "Penawaran kerja sama sponsor untuk sebuah event.",
            "judul": "Proposal Sponsorship",
            "outline": ["Latar Belakang", "Profil Kegiatan", "Data Peserta dan Jangkauan",
                        "Paket Sponsorship", "Kontraprestasi", "Penutup dan Kontak"],
            "fields": ACARA + [
                F("target_audiens", "Target audiens & jumlah", "text", ""),
                F("paket", "Paket sponsor (nama : nilai : benefit)", "area", ""),
                F("kontak", "Kontak person", "text", ""),
            ],
        },
    ],

    # ============================================================= RANGKUMAN
    "Rangkuman": [
        {
            "id": "rang_materi", "nama": "Rangkuman Materi Pelajaran", "surat": False,
            "desc": "Ringkasan materi belajar per bab dengan poin penting.",
            "judul": "Rangkuman Materi",
            "outline": ["Pokok Bahasan", "Uraian Materi", "Poin-Poin Penting",
                        "Contoh", "Kesimpulan"],
            "fields": [
                F("mapel", "Mata pelajaran / kuliah", "text", ""),
                F("bab", "Bab / topik", "text", ""),
                F("materi", "Materi yang dirangkum", "area", ""),
            ],
        },
        {
            "id": "rang_buku", "nama": "Ringkasan Buku", "surat": False,
            "desc": "Ringkasan isi buku beserta pelajaran yang bisa diambil.",
            "judul": "Ringkasan Buku",
            "outline": ["Identitas Buku", "Sinopsis", "Pokok Pikiran Tiap Bagian",
                        "Kelebihan dan Kekurangan", "Pelajaran yang Dipetik"],
            "fields": [
                F("judul_buku", "Judul buku", "text", ""),
                F("penulis_buku", "Penulis & penerbit", "text", ""),
                F("tahun_hal", "Tahun terbit & jumlah halaman", "text", ""),
                F("isi_buku", "Catatan isi buku", "area", ""),
            ],
        },
        {
            "id": "rang_jurnal", "nama": "Ringkasan Jurnal / Artikel", "surat": False,
            "desc": "Review singkat artikel ilmiah: metode, hasil, kesimpulan.",
            "judul": "Ringkasan Jurnal",
            "outline": ["Identitas Artikel", "Latar Belakang Penelitian", "Metode",
                        "Hasil dan Pembahasan", "Kesimpulan", "Catatan Kritis"],
            "fields": [
                F("judul_artikel", "Judul artikel", "text", ""),
                F("penulis_artikel", "Penulis, jurnal, tahun", "text", ""),
                F("abstrak", "Abstrak / catatan isi", "area", ""),
            ],
        },
        {
            "id": "exec_summary", "nama": "Executive Summary", "surat": False,
            "desc": "Ringkasan eksekutif satu halaman untuk pimpinan.",
            "judul": "Ringkasan Eksekutif",
            "outline": ["Konteks", "Temuan Utama", "Dampak", "Rekomendasi", "Langkah Berikutnya"],
            "fields": [
                F("topik", "Topik", "text", ""),
                F("temuan", "Temuan utama (satu per baris)", "area", ""),
                F("rekomendasi", "Rekomendasi (satu per baris)", "area", ""),
            ],
        },
        {
            "id": "rang_rapat", "nama": "Ringkasan Hasil Rapat", "surat": False,
            "desc": "Versi padat hasil rapat untuk dibagikan ke peserta.",
            "judul": "Ringkasan Hasil Rapat",
            "outline": ["Informasi Rapat", "Pokok Pembahasan", "Keputusan", "Tindak Lanjut"],
            "fields": [
                F("nama_acara", "Nama rapat", "text", ""),
                F("hari_tgl", "Hari / tanggal", "text", ""),
                F("bahasan", "Pokok pembahasan (satu per baris)", "area", ""),
                F("keputusan", "Keputusan (satu per baris)", "area", ""),
            ],
        },
    ],

    # ====================================================== CATATAN / NOTULEN
    "Catatan / Notulen": [
        {
            "id": "notulen", "nama": "Notulen Rapat", "surat": False,
            "desc": "Notulen lengkap: peserta, jalannya rapat, keputusan.",
            "judul": "Notulen Rapat",
            "outline": ["Informasi Rapat", "Peserta", "Agenda", "Jalannya Rapat",
                        "Keputusan", "Tindak Lanjut", "Penutup"],
            "fields": ACARA + [
                F("pimpinan", "Pimpinan rapat", "text", ""),
                F("notulis", "Notulis", "text", ""),
                F("peserta", "Peserta hadir (satu per baris)", "area", ""),
                F("jalannya", "Catatan jalannya rapat", "area", ""),
                F("keputusan", "Keputusan (satu per baris)", "area", ""),
                F("tindak_lanjut", "Tindak lanjut (tugas : penanggung jawab : tenggat)", "area", ""),
            ],
        },
        {
            "id": "berita_acara", "nama": "Berita Acara", "surat": False,
            "desc": "Pencatatan resmi suatu peristiwa/kegiatan yang telah terjadi.",
            "judul": "Berita Acara",
            "outline": ["Waktu dan Tempat", "Pihak yang Hadir", "Uraian Peristiwa",
                        "Kesimpulan", "Penutup"],
            "fields": [
                F("perihal_ba", "Berita acara tentang", "text", "Pembukaan Dokumen Penawaran"),
                F("hari_tgl", "Hari / tanggal", "text", ""),
                F("waktu", "Waktu", "text", ""),
                F("tempat", "Tempat", "text", ""),
                F("pihak", "Pihak yang hadir (satu per baris)", "area", ""),
                F("uraian", "Uraian peristiwa", "area", ""),
            ],
        },
        {
            "id": "bast", "nama": "Berita Acara Serah Terima", "surat": False,
            "desc": "BAST barang, pekerjaan, atau jabatan antara dua pihak.",
            "judul": "Berita Acara Serah Terima",
            "outline": ["Waktu dan Tempat", "Identitas Pihak Pertama", "Identitas Pihak Kedua",
                        "Objek yang Diserahterimakan", "Pernyataan Serah Terima", "Penutup"],
            "fields": [
                F("pihak1", "Pihak pertama (nama, jabatan)", "area", ""),
                F("pihak2", "Pihak kedua (nama, jabatan)", "area", ""),
                F("objek", "Objek serah terima (nama : jumlah : kondisi)", "area", ""),
                F("hari_tgl", "Hari / tanggal", "text", ""),
                F("tempat", "Tempat", "text", ""),
            ],
        },
        {
            "id": "mom", "nama": "Minutes of Meeting (MoM)", "surat": False,
            "desc": "Catatan rapat gaya korporat dengan tabel action item.",
            "judul": "Minutes of Meeting",
            "outline": ["Meeting Info", "Attendees", "Discussion Points",
                        "Decisions", "Action Items", "Next Meeting"],
            "fields": [
                F("nama_acara", "Nama meeting", "text", ""),
                F("hari_tgl", "Tanggal", "text", ""),
                F("peserta", "Attendees (satu per baris)", "area", ""),
                F("bahasan", "Discussion points (satu per baris)", "area", ""),
                F("tindak_lanjut", "Action items (tugas : PIC : due date)", "area", ""),
                F("next", "Jadwal meeting berikutnya", "text", ""),
            ],
        },
        {
            "id": "catatan_harian", "nama": "Catatan Harian Kegiatan", "surat": False,
            "desc": "Logbook harian magang, PKL, atau proyek.",
            "judul": "Catatan Harian Kegiatan",
            "outline": ["Identitas", "Catatan Per Hari", "Ringkasan Capaian", "Catatan Pembimbing"],
            "fields": PEG + [
                F("periode", "Periode", "text", "Minggu ke-3, 15 - 19 September 2026"),
                F("log", "Catatan per hari (tanggal : kegiatan)", "area",
                  "15/09 : Orientasi dan pengenalan unit\n16/09 : Input data pelanggan"),
            ],
        },
        {
            "id": "daftar_hadir", "nama": "Catatan Kehadiran & Hasil", "surat": False,
            "desc": "Rekap kehadiran peserta plus catatan hasil kegiatan.",
            "judul": "Catatan Kehadiran dan Hasil Kegiatan",
            "outline": ["Informasi Kegiatan", "Rekap Kehadiran", "Catatan Hasil", "Penutup"],
            "fields": ACARA + [
                F("peserta", "Daftar peserta (nama : hadir/tidak)", "area", ""),
                F("catatan", "Catatan hasil", "area", ""),
            ],
        },
    ],
}

JENIS = list(TEMPLATES)


def get(jenis, tpl_id):
    for t in TEMPLATES.get(jenis, []):
        if t["id"] == tpl_id:
            return t
    return TEMPLATES[jenis][0]


def brief_from_fields(tpl, values):
    """Ubah isian field template jadi teks bahan untuk AI."""
    baris = []
    for f in tpl["fields"]:
        v = (values.get(f["key"]) or "").strip()
        if v:
            baris.append(f"{f['label']}: {v}" if "\n" not in v
                         else f"{f['label']}:\n{v}")
    return "\n".join(baris)
