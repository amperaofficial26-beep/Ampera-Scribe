from .common import F, T, PEG, IDENT_RINGKAS, PENANDATANGAN_SURAT, DASAR, TABEL, TEMBUSAN, ACARA

TUGAS = F("tugas", "Uraian tugas", "area", "Menghadiri Bimbingan Teknis ...")
PERIODE = F("periode", "Waktu pelaksanaan", "text", "10 - 17 Februari 2026")
TEMPAT_TUGAS = F("tempat_tugas", "Tempat pelaksanaan", "text", "Hotel Grand Candi, Semarang")
BAKU_TUTUP = ("Demikian surat tugas ini dibuat untuk dilaksanakan dengan penuh tanggung jawab.")

ITEMS = [
    T("st_lapangan", "Surat Tugas Kerja Lapangan",
      "Perusahaan; isi berupa paragraf naratif (tugas, biaya, K3, laporan).",
      "Surat Tugas Kerja Lapangan",
      ["Identitas pemberi tugas", "Identitas penerima tugas",
       "Paragraf uraian tugas dan periode", "Paragraf biaya operasional dan peralatan",
       "Paragraf kewajiban K3 dan pelaporan", "Paragraf penutup"],
      PENANDATANGAN_SURAT + [F("nama_peg", "Nama penerima tugas", "text", ""),
                             F("nik_peg", "NIK", "text", ""),
                             F("jabatan_peg", "Jabatan penerima", "text", ""),
                             TUGAS, PERIODE, TEMPAT_TUGAS,
                             F("biaya", "Ketentuan biaya", "area",
                               "ditanggung sepenuhnya oleh perusahaan sesuai standar "
                               "operasional prosedur yang berlaku")],
      {"pembuka": "Saya yang bertanda tangan di bawah ini:",
       "penutup": "Demikian surat tugas ini dibuat sebagai dokumen resmi agar dapat "
                  "dipergunakan sebagaimana mestinya. Seluruh pihak terkait dimohon "
                  "memberikan bantuan dan kerja sama demi kelancaran tugas tersebut."},
      meta="judul", ttd=1),

    T("st_perusahaan", "Surat Tugas Perusahaan (blok terstruktur)",
      "Blok pemberi & penerima tugas lengkap, lalu rincian tugas berblok.",
      "Surat Tugas",
      ["Identitas yang memberi tugas", "Identitas yang ditugaskan",
       "Rincian tugas (Keperluan, Tempat, Waktu, Keterangan)", "Penutup"],
      PENANDATANGAN_SURAT + [F("perusahaan", "Perusahaan", "text", ""),
                             F("alamat_perusahaan", "Alamat perusahaan", "area", "")] +
      IDENT_RINGKAS + [F("nik_peg", "NIK penerima", "text", ""),
                       F("keperluan_tugas", "Keperluan", "text",
                         "Menghadiri Pameran Teknologi Digital Indonesia"),
                       TEMPAT_TUGAS, PERIODE,
                       F("keterangan", "Keterangan biaya/hak", "area",
                         "berhak atas biaya perjalanan dinas sesuai ketentuan perusahaan")],
      {"pembuka": "Yang bertanda tangan di bawah ini:",
       "penutup": BAKU_TUTUP},
      meta="judul", ttd=1),

    T("st_kampus", "Surat Tugas Perguruan Tinggi",
      "Judul dispasi, daftar petugas dalam tabel, blok Dasar/Tujuan/Waktu/Tempat.",
      "SURAT TUGAS",
      ["Kalimat penugasan", "Tabel daftar yang ditugaskan",
       "Dasar", "Tujuan", "Waktu", "Tempat", "Penutup"],
      [F("pemberi", "Pejabat pemberi tugas", "text", "Rektor Universitas ..."),
       TABEL, DASAR, F("tujuan_tugas", "Tujuan", "area",
                       "Melaksanakan Visitasi Akreditasi ke Sekolah/Madrasah Tahap 3"),
       PERIODE, TEMPAT_TUGAS],
      {"pembuka": "{pemberi} dengan ini menugaskan:",
       "penutup": "Demikian untuk dilaksanakan sebagaimana mestinya, dan diminta untuk "
                  "membuat laporan kegiatan."},
      meta="judul", ttd=1, tabel=True, judul_spasi=True),

    T("spt_sekolah", "Surat Perintah Tugas (blangko)",
      "Gaya blangko instansi; isian bisa dibiarkan titik-titik untuk diisi tangan.",
      "Surat Perintah Tugas",
      ["Kalimat perintah", "Identitas yang diperintah",
       "Kegiatan yang diikuti", "Rincian bernomor (Hari, Tanggal, Tempat)", "Penutup"],
      PEG + [F("kegiatan", "Kegiatan yang diikuti", "text",
               "Bimbingan Teknis Penulisan Laporan Penelitian Tindakan Kelas"),
             F("hari", "Hari", "text", "Senin"),
             F("tanggal_acara", "Tanggal", "text", "2 Februari - 30 Mei 2026"),
             TEMPAT_TUGAS],
      {"pembuka": "Dengan ini diperintahkan kepada:",
       "penutup": "Demikian untuk dilaksanakan dengan penuh tanggung jawab dan sekembalinya "
                  "dari tugas untuk segera melaporkan hasilnya."},
      meta="judul", ttd=1, blangko=True),

    T("st_asn", "Surat Penugasan Pegawai (ASN)",
      "Pemberi & penerima sama-sama lengkap: NIP, Pangkat/Gol, e-mail, unit kerja.",
      "Surat Penugasan",
      ["Identitas pemberi tugas", "Identitas yang ditugaskan", "Uraian tugas", "Penutup"],
      [F("nama_ttd", "Nama pemberi tugas", "text", ""),
       F("nip_ttd", "NIP pemberi", "text", ""),
       F("pangkat_ttd", "Pangkat/Gol. Ruang pemberi", "text", ""),
       F("jabatan_ttd", "Jabatan pemberi", "text", "Kepala Sekolah")] + PEG +
      [F("email_peg", "E-mail penerima", "text", ""),
       F("telp_peg", "Telp/HP penerima", "text", ""), TUGAS],
      {"pembuka": "Yang bertanda tangan di bawah ini:",
       "penutup": "Demikian Surat Penugasan ini dikeluarkan untuk dapat dilaksanakan dengan "
                  "baik dan penuh rasa tanggung jawab."},
      meta="judul", ttd=1, stempel=True),

    T("st_sekolah_lengkap", "Surat Tugas Sekolah/Yayasan (lengkap)",
      "Blok Dasar, tabel petugas multi-orang, rincian kegiatan, dan tembusan.",
      "Surat Tugas",
      ["Dasar", "Kalimat penugasan", "Tabel daftar yang ditugaskan",
       "Rincian kegiatan (Nama Kegiatan, Penyelenggara, Tempat, Hari/Tanggal, Waktu)",
       "Penutup"],
      [DASAR, F("pemberi", "Pejabat pemberi tugas", "text", "Kepala TK ..."), TABEL,
       F("nama_kegiatan", "Nama kegiatan", "text",
         "Bimbingan Teknis Implementasi Kurikulum Merdeka")] +
      [F("penyelenggara", "Penyelenggara", "text", "Dinas Pendidikan Provinsi")] +
      ACARA + [TEMBUSAN],
      {"pembuka": "Yang bertanda tangan di bawah ini, {pemberi}, dengan ini menugaskan kepada:",
       "penutup": "Demikian surat tugas ini dibuat untuk dilaksanakan dengan penuh tanggung "
                  "jawab. Setelah melaksanakan tugas, yang bersangkutan diharapkan "
                  "menyampaikan laporan kepada kepala satuan. Atas perhatian dan kerja "
                  "samanya, diucapkan terima kasih."},
      meta="judul", ttd=1, tabel=True, tembusan=True, stempel=True),

    T("st_pemerintah", "Surat Tugas Instansi Pemerintah",
      "Daftar petugas cukup ditulis 'terlampir'; ada tembusan bernomor.",
      "Surat Tugas",
      ["Kalimat penugasan", "Keterangan daftar nama terlampir",
       "Paragraf peran dan kegiatan", "Penutup"],
      [F("pemberi", "Pejabat pemberi tugas", "text",
         "Ketua Lembaga Penelitian dan Pengabdian kepada Masyarakat"),
       F("peran", "Peran penerima tugas", "text", "Sebagai Peserta"),
       F("nama_kegiatan", "Nama kegiatan", "area",
         "Workshop Peningkatan Tata Kelola OJS dan Input ARJUNA"),
       F("waktu_kegiatan", "Tanggal kegiatan", "text", "11 - 12 September 2026"),
       F("tempat_kegiatan", "Tempat kegiatan", "area", ""), TEMBUSAN],
      {"pembuka": "{pemberi}, memberi tugas kepada: (Daftar nama-nama terlampir)",
       "penutup": "Demikian surat tugas ini dibuat untuk dilaksanakan dengan penuh tanggung "
                  "jawab. Dan setelah melaksanakan tugas, harap menyampaikan laporan tertulis."},
      meta="judul", ttd=1, tembusan=True),
]
