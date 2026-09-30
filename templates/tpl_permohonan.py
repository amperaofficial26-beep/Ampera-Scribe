from .common import F, T, ACARA, AGENDA, TUJUAN, IDENT_RINGKAS, TEMBUSAN, TABEL

TUTUP = ("Demikian surat permohonan ini kami sampaikan. Atas perhatian dan kerja samanya, "
         "kami ucapkan terima kasih.")
KEGIATAN = F("nama_kegiatan", "Nama kegiatan", "text", "")
LATAR = F("latar", "Latar belakang", "area", "")

ITEMS = [
    T("mohon_dana", "Permohonan Bantuan Dana (organisasi)",
      "Salam Islami, data organisasi, janji laporan, tiga penandatangan.",
      "Surat Permohonan Bantuan Dana",
      ["Salam dan puji syukur", "Data organisasi pemohon", "Latar belakang keprihatinan",
       "Isi permohonan bantuan", "Janji pertanggungjawaban", "Penutup dan salam"],
      [F("organisasi", "Nama organisasi", "text", ""),
       F("alamat_org", "Alamat organisasi", "area", ""),
       F("izin_org", "Izin pendirian organisasi", "text", ""),
       F("tujuan_bantuan", "Bantuan untuk", "text", "korban bencana alam"), LATAR],
      {"pembuka": "Segala puji dan syukur kita panjatkan ke hadirat Allah SWT. "
                  "Kami yang bertandatangan di bawah ini:",
       "penutup": "Demikianlah surat permohonan ini kami buat. Atas keikhlasan dan bantuan "
                  "yang diberikan, kami segenap panitia mengucapkan banyak terima kasih."},
      salam="islami", ttd=3, ttd_label=["Ketua", "Sekretaris", "Bendahara"]),

    T("mohon_sponsor", "Permohonan Sponsorship",
      "Menyebut timbal balik (logo di spanduk/medsos); lampiran proposal.",
      "Surat Permohonan Sponsorship",
      ["Latar belakang kegiatan", "Isi permohonan dukungan",
       "Kontraprestasi bagi sponsor", "Waktu dan lokasi kegiatan", "Penutup"],
      [KEGIATAN, LATAR, F("bentuk_dukungan", "Bentuk dukungan yang diminta", "text",
                          "dana, hadiah perlombaan, maupun kontribusi lainnya"),
       F("timbal_balik", "Kontraprestasi", "area",
         "nama dan logo perusahaan dicantumkan pada spanduk, baliho, dan media sosial"),
       F("tanggal_kegiatan", "Tanggal kegiatan", "text", ""),
       F("lokasi", "Lokasi", "text", "")],
      {"pembuka": "Dalam rangka {latar}, kami bermaksud menyelenggarakan serangkaian "
                  "kegiatan. Sehubungan dengan hal tersebut, kami mengajukan permohonan "
                  "dukungan sponsor kepada Bapak/Ibu berupa {bentuk_dukungan}.",
       "penutup": "Sebagai bahan pertimbangan, bersama surat ini kami lampirkan proposal "
                  "kegiatan secara lengkap. Demikian surat ini kami sampaikan. Atas "
                  "perhatian dan dukungannya, kami ucapkan terima kasih."},
      ttd=1),

    T("mohon_izin_tempat", "Permohonan Izin Tempat",
      "Salam Islami; rincian ruangan yang diminta; empat penandatangan + Mengetahui.",
      "Surat Permohonan Izin Tempat",
      ["Salam dan puji syukur", "Rincian kegiatan (Hari, Tanggal, Waktu, Peserta)",
       "Isi permohonan penggunaan tempat", "Penutup dan salam"],
      ACARA + [F("peserta", "Jumlah peserta", "text", "80 pelajar"), KEGIATAN,
               F("fasilitas", "Ruangan/fasilitas yang diminta", "area",
                 "2 ruang untuk inap, 1 ruang untuk kelas, 1 ruang untuk sekretariat, "
                 "serta fasilitas mushola dan MCK"), TEMBUSAN],
      {"pembuka": "Puji syukur kami panjatkan ke hadirat Allah. Sehubungan dengan akan "
                  "diadakannya {nama_kegiatan} yang insya Allah kami selenggarakan pada:",
       "penutup": "Demikian surat ini kami sampaikan dengan harapan terkabulnya permohonan "
                  "kami. Akhirnya atas perhatian dan perkenannya kami ucapkan terima kasih."},
      salam="islami", ttd=4,
      ttd_label=["Ketua", "Sekretaris", "Ketua Putra", "Ketua Putri"], tembusan=True),

    T("mohon_pembicara", "Permohonan Menjadi Pembicara",
      "Detail seminar, lampiran TOR, kontak konfirmasi, permintaan makalah.",
      "Surat Permohonan Menjadi Pembicara",
      ["Paragraf permohonan kesediaan", "Rincian acara (Seminar, Hari/Tanggal, Waktu, Tempat)",
       "Lampiran TOR dan kontak konfirmasi", "Penutup"],
      ACARA + TUJUAN + [F("seminar", "Nama seminar/acara", "area", ""),
                        F("kontak", "Kontak konfirmasi (nama & nomor)", "area", ""),
                        F("email_kirim", "Email pengiriman makalah", "text", "")],
      {"pembuka": "Dengan hormat, sehubungan dengan {seminar} yang akan kami laksanakan, "
                  "kami bermohon kesediaan Bapak/Ibu untuk menjadi Pembicara pada:",
       "penutup": "Bersama ini turut kami sampaikan Term of Reference (TOR) dan mengingat "
                  "singkatnya waktu, mohon konfirmasi kesediaan Bapak/Ibu. Atas perhatian "
                  "dan kesediaannya, kami sampaikan terima kasih."},
      ttd=1),

    T("mohon_narasumber", "Permohonan Menjadi Narasumber",
      "Paragraf doa/salam sejahtera; latar belakang program; topik terlampir.",
      "Surat Permohonan Menjadi Narasumber",
      ["Salam dan doa", "Latar belakang program", "Isi permohonan",
       "Rincian acara (Hari/Tanggal, Pukul, Tempat, Topik/Tema)", "Penutup"],
      ACARA + TUJUAN + [F("program", "Nama program", "text", ""), LATAR,
                        F("topik", "Topik / tema", "text", "terlampir")],
      {"pembuka": "Teriring salam dan hormat kami sampaikan semoga Bapak/Ibu dalam keadaan "
                  "sehat dan selalu dalam lindungan Tuhan Yang Maha Esa. Sehubungan dengan "
                  "telah dibentuknya {program}, {latar}. Oleh karena itu kami memohon "
                  "kepada Ibu/Bapak untuk dapat menjadi narasumber pada:",
       "penutup": "Demikian surat permohonan ini kami sampaikan, atas perhatian dan "
                  "kesediaannya diucapkan terima kasih."},
      ttd=1),

    T("mohon_cuti_blangko", "Permohonan Cuti Kerja (blangko)",
      "Pakai 'Up.'; lama cuti angka + huruf; isian titik-titik.",
      "Surat Permohonan Cuti Kerja",
      ["Identitas pemohon", "Isi permohonan cuti dan lamanya",
       "Keterangan tanggal cuti", "Peruntukan cuti", "Penutup"],
      IDENT_RINGKAS + [F("telp", "No. Telp", "text", ""),
                       F("lama_cuti", "Lama cuti", "text", "3 (tiga) hari"),
                       F("tgl_cuti", "Tanggal cuti", "text", "1 s/d 3 Oktober 2026"),
                       F("alasan", "Cuti dipergunakan untuk", "area", "")],
      {"pembuka": "Dengan hormat, saya yang bertanda tangan di bawah ini:",
       "penutup": "Demikian surat permohonan cuti ini saya buat. Atas perhatian dan "
                  "toleransinya saya sampaikan banyak terima kasih."},
      kop=False, meta="judul", ttd=1, up=True, blangko=True),

    T("mohon_cuti_tahunan", "Permohonan Cuti Tahunan",
      "Ringkas; sebut tanggal mulai bekerja kembali dan email kontak.",
      "Surat Izin Cuti Tahunan",
      ["Identitas pemohon", "Isi permohonan cuti", "Tanggal masuk kembali", "Penutup"],
      [F("nama_org", "Nama", "text", ""), F("divisi", "Divisi", "text", ""),
       F("jabatan_org", "Jabatan", "text", ""),
       F("lama_cuti", "Lama cuti", "text", "2 hari"),
       F("tgl_cuti", "Tanggal cuti", "text", "Kamis, 5 s.d. Jumat, 6 November 2026"),
       F("masuk_lagi", "Mulai bekerja kembali", "text", "Senin, 9 November 2026"),
       F("email_kontak", "Email kontak", "text", "")],
      {"pembuka": "Dengan hormat, yang bertanda tangan di bawah ini:",
       "penutup": "Demikian permohonan cuti ini saya ajukan. Terima kasih atas perhatian "
                  "Bapak/Ibu."},
      kop=False, meta="polos", ttd=1),

    T("mohon_cuti_keluarga", "Permohonan Cuti Urusan Keluarga",
      "Sangat ringkas; identitas inline; alasan keluarga.",
      "Permohonan Cuti Urusan Keluarga",
      ["Identitas pemohon", "Isi permohonan dan alasan", "Penutup"],
      [F("nama_org", "Nama", "text", ""), F("nik", "NIK", "text", ""),
       F("jabatan_org", "Jabatan", "text", ""), F("divisi", "Divisi", "text", ""),
       F("lama_cuti", "Lama cuti", "text", "1 (satu) hari"),
       F("tgl_cuti", "Tanggal cuti", "text", ""),
       F("alasan", "Alasan", "area", "anak sakit dan perlu pendampingan ke dokter")],
      {"pembuka": "Dengan hormat, yang bertanda tangan di bawah ini:",
       "penutup": "Demikian surat permohonan cuti ini saya ajukan. Atas perhatian "
                  "Bapak/Ibu, saya ucapkan terima kasih."},
      kop=False, meta="polos", ttd=1),

    T("mohon_cuti_besar", "Permohonan Cuti Besar (Istirahat Panjang)",
      "Dasar hukum PP/PKB + UU 13/2003; masa kerja; kesediaan serah terima tugas.",
      "Permohonan Cuti Besar (Istirahat Panjang)",
      ["Identitas pemohon lengkap", "Dasar hak cuti besar dan masa kerja",
       "Durasi dan tanggal cuti", "Rencana penggunaan cuti",
       "Kesediaan serah terima tugas", "Penutup"],
      [F("nama_org", "Nama lengkap", "text", ""), F("nik", "Nomor Induk Karyawan", "text", ""),
       F("jabatan_org", "Jabatan", "text", ""), F("divisi", "Departemen", "text", ""),
       F("mulai_kerja", "Tanggal mulai bekerja", "text", ""),
       F("masa_kerja", "Masa kerja", "text", "7 (tujuh) tahun"),
       F("dasar_hukum", "Dasar aturan", "text",
         "Peraturan Perusahaan (PP) serta UU No. 13 Tahun 2003"),
       F("lama_cuti", "Durasi cuti", "text", "1 (satu) bulan"),
       F("tgl_cuti", "Tanggal cuti", "text", ""),
       F("rencana", "Rencana penggunaan cuti", "area", ""), TEMBUSAN],
      {"pembuka": "Dengan hormat, saya yang bertanda tangan di bawah ini:",
       "penutup": "Demikian surat permohonan ini saya sampaikan. Besar harapan saya agar "
                  "permohonan cuti besar ini dapat dipertimbangkan dan disetujui. Atas "
                  "perhatian, pengertian, dan kebijaksanaan Bapak/Ibu, saya ucapkan "
                  "terima kasih."},
      kop=False, meta="polos", ttd=1, tembusan=True),

    T("mohon_pindah_sekolah", "Permohonan Pindah Sekolah",
      "Ada formulir balasan yang diisi sekolah tujuan dan dikirim kembali.",
      "Surat Permohonan Pindah Sekolah",
      ["Identitas orang tua/wali", "Identitas anak didik",
       "Isi permohonan pindah dan sekolah tujuan", "Alasan", "Penutup"],
      [F("nama_org", "Nama orang tua/wali", "text", ""),
       F("pekerjaan", "Pekerjaan", "text", ""), F("alamat_org", "Alamat", "area", ""),
       F("nama_siswa", "Nama anak didik", "text", ""),
       F("no_induk", "Nomor induk", "text", ""), F("jk", "Jenis kelamin", "text", ""),
       F("kelompok", "Kelompok / kelas", "text", ""),
       F("sekolah_tujuan", "Sekolah tujuan", "text", ""),
       F("alamat_tujuan", "Alamat sekolah tujuan", "area", ""),
       F("alasan", "Alasan pindah", "area", "")],
      {"pembuka": "Yang bertanda tangan di bawah ini:",
       "penutup": "Atas perhatian Bapak/Ibu, kami ucapkan terima kasih."},
      kop=False, meta="judul", ttd=1, slip="balasan_sekolah"),

    T("mohon_magang", "Permohonan Tempat Magang Mahasiswa",
      "Salam Islami; daftar Nama + NIM + Prodi; periode dan bidang penempatan.",
      "Surat Permohonan Tempat Magang Mahasiswa",
      ["Salam dan puji syukur", "Latar belakang program magang",
       "Daftar mahasiswa", "Periode dan bidang penempatan", "Penutup dan salam"],
      [F("program", "Program / prodi", "text", ""),
       F("periode", "Periode magang", "text", "04 September 2026 s/d 03 Maret 2027"),
       F("lama", "Lama magang", "text", "6 (enam) bulan"), TABEL,
       F("bidang", "Bidang penempatan", "text", "Akuntansi dan/atau Perpajakan")],
      {"pembuka": "Puji syukur kita panjatkan kehadirat Allah SWT. Sehubungan dengan "
                  "program magang mahasiswa {program} selama {lama} terhitung mulai "
                  "tanggal {periode}, bersama ini kami mohon agar mahasiswa kami:",
       "penutup": "Demikian surat permohonan ini kami sampaikan, atas perhatian dan "
                  "kerjasamanya kami ucapkan terima kasih."},
      salam="islami", ttd=1, tabel=True),

    T("mohon_penelitian", "Permohonan Izin Magang & Penelitian",
      "Gabungan KKM dan izin penelitian; daftar mahasiswa terlampir; tembusan.",
      "Permohonan Izin Kerja Magang dan Izin Penelitian",
      ["Latar belakang kurikulum dan peningkatan keterampilan",
       "Isi permohonan magang dan penelitian", "Keterangan daftar terlampir", "Penutup"],
      [F("fakultas", "Fakultas", "text", ""),
       F("mata_kuliah", "Mata kuliah terkait", "text", "Kuliah Kerja Magang (KKM)"),
       F("periode", "Periode", "text", ""), TEMBUSAN],
      {"pembuka": "Dengan hormat, dalam rangka memenuhi kurikulum dan peningkatan "
                  "keterampilan mahasiswa, Dekan {fakultas} mengajukan permohonan "
                  "mahasiswa yang tersebut dalam daftar terlampir untuk diterima "
                  "melaksanakan magang dan izin penelitian di instansi yang Bapak/Ibu "
                  "pimpin.",
       "penutup": "Besar harapan kami kegiatan magang dan izin penelitian ini dapat "
                  "terlaksana dengan baik. Demikian disampaikan, atas perhatian dan "
                  "kerjasamanya diucapkan terima kasih."},
      ttd=1, tembusan=True),
]
