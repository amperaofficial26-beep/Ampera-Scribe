from .common import F, T, ACARA, TUJUAN, DASAR, TABEL, TEMBUSAN, POIN, PEG

TUTUP = ("Demikian pemberitahuan ini disampaikan. Atas perhatiannya diucapkan terima kasih.")

ITEMS = [
    T("pbt_jadwal", "Pemberitahuan Perubahan Jadwal",
      "Poin bernomor dengan sub-poin bertanggal; sebut kanal daring.",
      "Pemberitahuan Perubahan Jadwal",
      ["Salam dan kalimat pembuka", "Poin-poin perubahan jadwal beserta sub-rinciannya",
       "Imbauan kepada orang tua/peserta", "Penutup"],
      [POIN, F("mulai_berlaku", "Mulai berlaku", "text", "18 Oktober 2026"),
       F("kanal", "Kanal daring (jika ada)", "text", "YouTube ...")],
      {"pembuka": "Melalui surat ini ada beberapa hal yang perlu kami sampaikan kepada "
                  "Bapak/Ibu, yaitu:",
       "penutup": "Demikian surat pemberitahuan ini kami sampaikan. Atas perhatian "
                  "Bapak/Ibu kami mengucapkan terima kasih."},
      ttd=1),

    T("pbt_libur", "Pemberitahuan Libur & Cuti Bersama",
      "Paragraf salam sejahtera; poin tanggal libur, cuti, dan masuk kembali.",
      "Pemberitahuan Libur dan Cuti Bersama",
      ["Salam sejahtera dan doa", "Kalimat pembuka peringatan hari besar",
       "Poin tanggal libur, cuti bersama, dan masuk kembali", "Imbauan", "Penutup"],
      [F("peringatan", "Peringatan hari besar", "text", "Tahun Baru Imlek 2574"),
       POIN, F("masuk_lagi", "Masuk kembali", "text", ""), TEMBUSAN],
      {"pembuka": "Salam sejahtera kami sampaikan semoga Bapak/Ibu selalu berada dalam "
                  "keadaan sehat wal'afiat. Dalam rangka memperingati {peringatan}, maka "
                  "bersama dengan ini diberitahukan bahwa:",
       "penutup": TUTUP},
      ttd=1, tembusan=True),

    T("pbt_libur_dinas", "Pemberitahuan Libur dari Dinas",
      "Dasar berlapis (Keppres, Surat Sekda, kalender pendidikan); banyak penerima.",
      "Pemberitahuan Pelaksanaan Libur",
      ["Dasar peraturan berlapis", "Poin tanggal libur dan masuk kembali", "Penutup"],
      [DASAR, POIN, TEMBUSAN] + TUJUAN,
      {"pembuka": "Sehubungan dengan telah ditetapkannya {dasar}, dan sesuai dengan "
                  "kalender pendidikan, dengan ini disampaikan kepada Bapak/Ibu bahwa:",
       "penutup": "Demikian surat ini dibuat agar dipedomani, atas perhatiannya diucapkan "
                  "terima kasih."},
      ttd=1, tembusan=True, penerima_nomor=True),

    T("pbt_kegiatan_ortu", "Pemberitahuan Kegiatan ke Orang Tua",
      "Ada biaya per siswa dan slip izin orang tua yang disobek & dikembalikan.",
      "Pemberitahuan Kegiatan",
      ["Kalimat pembuka maksud kegiatan",
       "Rincian kegiatan (Hari/Tanggal, Waktu, Biaya, Tujuan)", "Penutup"],
      ACARA + [F("nama_kegiatan", "Nama kegiatan", "text", "Outing Class"),
               F("kelas", "Kelas peserta", "text", "VII dan VIII"),
               F("biaya", "Biaya per siswa", "text", "Rp 200.000"),
               F("tujuan_lokasi", "Tujuan", "text", ""),
               F("batas_balasan", "Batas pengembalian slip", "text", ""), TEMBUSAN],
      {"pembuka": "Kami beritahukan kepada Bapak/Ibu wali murid kelas {kelas}, bahwa dalam "
                  "rangka menambah wawasan pengetahuan, sekolah bermaksud mengadakan "
                  "kegiatan pembelajaran di luar kelas ({nama_kegiatan}) yang akan "
                  "dilaksanakan pada:",
       "penutup": "Demikian surat pemberitahuan kami, atas perhatian dan kerjasamanya kami "
                  "ucapkan terima kasih."},
      ttd=2, ttd_label=["Ketua", "Sekretaris"], verifikasi="Kepala Sekolah",
      tembusan=True, slip="izin_ortu"),

    T("pbt_kegiatan_organisasi", "Pemberitahuan Kegiatan Organisasi",
      "Salam Islami; rincian kegiatan; penandatangan Pembina & Ketua Pelaksana.",
      "Pemberitahuan Kegiatan",
      ["Salam", "Kalimat pembuka maksud pemberitahuan",
       "Rincian kegiatan (Hari, Tanggal, Waktu, Tempat, Kegiatan)", "Penutup dan salam"],
      ACARA + [F("nama_kegiatan", "Nama kegiatan", "text", ""),
               F("organisasi", "Organisasi / gugus depan", "text", "")],
      {"pembuka": "Sehubungan dengan akan dilaksanakan {nama_kegiatan} {organisasi}, maka "
                  "kami bermaksud untuk memberikan informasi kepada Bapak/Ibu/Wali Murid. "
                  "Kegiatan akan dilaksanakan pada:",
       "penutup": "Demikian surat ini kami buat dan sampaikan, agar pemberitahuan ini dapat "
                  "diterima dengan baik. Atas izin dan kerjasama Bapak/Ibu/Wali Murid kami "
                  "mengucapkan terima kasih."},
      salam="islami", ttd=2, ttd_label=["Pembina", "Ketua Pelaksana"]),

    T("pbt_upacara", "Pemberitahuan Kegiatan Upacara/Akademik",
      "Dasar surat edaran; poin bernomor rangkaian hari & kegiatan; imbauan ke ortu.",
      "Pemberitahuan",
      ["Dasar surat edaran", "Poin-poin informasi kegiatan per hari",
       "Imbauan kepada orang tua", "Penutup"],
      [DASAR, POIN, F("kelas", "Kelas terdampak", "text", "VII dan VIII")],
      {"pembuka": "Sehubungan dengan {dasar}, maka bersama ini kami sampaikan "
                  "informasi-informasi sebagai berikut:",
       "penutup": "Demikian pemberitahuan ini kami sampaikan untuk menjadikan periksa, atas "
                  "perhatian dan kerjasamanya, kami ucapkan terima kasih."},
      ttd=1),

    T("pbt_kerja_bakti", "Pemberitahuan Kerja Bakti (RT/RW)",
      "Rincian agenda kerja; blok NB berisi sanksi solidaritas; slogan.",
      "Pemberitahuan Kerja Bakti",
      ["Salam", "Kalimat maksud kegiatan",
       "Rincian (Hari/Tanggal, Waktu, Tempat, Agenda kerja)", "Penutup", "Catatan (NB)"],
      ACARA + [F("agenda_kerja", "Agenda kerja (satu per baris)", "area",
                 "Membersihkan got saluran utama\nMembuat aliran got di pinggir sawah"),
               F("wilayah", "Wilayah", "text", "RT 008 / RW 05"),
               F("nb", "Catatan NB", "area",
                 "Sesuai dengan aturan AD/ART yang berlaku, warga yang tidak bisa ikut "
                 "melaksanakan kerja bakti akan dikenakan sanksi solidaritas sebesar "
                 "Rp 20.000"),
               F("slogan", "Slogan (opsional)", "text",
                 "TIDAK PERLU HEBAT, YANG PENTING BISA BERMANFAAT")],
      {"pembuka": "Dalam rangka mewujudkan lingkungan yang bersih dan sehat, kami selaku "
                  "pengurus {wilayah} mengundang Bapak/Ibu di lingkungan {wilayah} untuk "
                  "kerja bakti yang akan diselenggarakan pada:",
       "penutup": "Demikian undangan ini kami sampaikan, atas kerjasama yang baik dan "
                  "semangat kekeluargaan dalam menjaga lingkungan yang aman dan sehat, "
                  "kami ucapkan terima kasih."},
      salam="islami", ttd=1, nb=True),

    T("pbt_harga", "Pemberitahuan Kenaikan Harga",
      "Tabel produk vs kenaikan harga; tanggal mulai berlaku.",
      "Pemberitahuan Kenaikan Harga",
      ["Kalimat pembuka informasi kenaikan", "Tabel produk dan kenaikan harga",
       "Keterangan tindak lanjut", "Penutup"],
      [TABEL, F("mulai_berlaku", "Mulai berlaku", "text", "23 November 2026"),
       F("produk", "Kelompok produk", "text", "")],
      {"pembuka": "Bersama ini kami sampaikan bahwa akan terdapat kenaikan harga pada "
                  "produk {produk} yang akan berlaku mulai tanggal {mulai_berlaku}, "
                  "sebagai berikut:",
       "penutup": "Keputusan perubahan harga akan kami informasikan kembali. Demikian surat "
                  "pemberitahuan kami sampaikan, atas perhatian dan kerjasama yang baik, "
                  "kami ucapkan terima kasih."},
      ttd=1, tabel=True),

    T("pbt_seleksi", "Pemberitahuan Seleksi/Rekrutmen (dinas)",
      "Paling kompleks: Sifat, penerima bernomor, syarat a-k, dokumen 1-20, tabel jadwal.",
      "Pemberitahuan",
      ["Latar belakang program", "Dasar peraturan", "Syarat peserta (huruf a, b, c, ...)",
       "Dokumen kelengkapan (bernomor)", "Tabel jadwal tahapan", "Penutup"],
      [F("program", "Nama program", "text",
         "Program Penyiapan Calon Kepala Sekolah"), DASAR,
       F("syarat", "Syarat (satu per baris)", "area", ""),
       F("dokumen", "Dokumen kelengkapan (satu per baris)", "area", ""),
       TABEL, TEMBUSAN],
      {"pembuka": "Dalam rangka pelaksanaan {program}, bersama ini diberitahukan bahwa:",
       "penutup": "Demikian disampaikan untuk dilaksanakan, atas kerjasama yang baik "
                  "diucapkan terima kasih."},
      ttd=1, sifat=True, tembusan=True, tabel=True, penerima_nomor=True),

    T("pbt_gaji_berkala", "Pemberitahuan Kenaikan Gaji Berkala",
      "Daftar data pegawai bernomor + blok gaji baru; dasar Peraturan Pemerintah.",
      "Pemberitahuan Kenaikan Gaji Berkala",
      ["Kalimat pembuka pemenuhan masa kerja", "Data pegawai bernomor",
       "Blok kenaikan gaji berkala yang diperoleh", "Dasar peraturan", "Penutup"],
      PEG + [F("ttl", "Tempat/tanggal lahir", "text", ""),
             F("gaji_lama", "Gaji pokok lama", "text", "Rp 3.214.700"),
             F("gaji_baru", "Gaji pokok baru", "text", "Rp 3.315.900"),
             F("masa_kerja", "Berdasarkan masa kerja", "text", "14 Tahun 00 Bulan"),
             F("tmt", "Terhitung mulai tanggal", "text", "01 Januari 2026"),
             F("sk_terakhir", "SK terakhir (pejabat, tanggal, nomor)", "area", ""),
             F("dasar_pp", "Dasar Peraturan Pemerintah", "text",
               "Peraturan Pemerintah Nomor 15 Tahun 2019"), TEMBUSAN],
      {"pembuka": "Dengan ini diberitahukan bahwa berhubung dengan telah dipenuhinya masa "
                  "kerja dan syarat-syarat lainnya kepada:",
       "penutup": "Diharapkan agar sesuai dengan {dasar_pp} pegawai tersebut dapat "
                  "dibayarkan penghasilannya berdasarkan gaji pokok baru."},
      ttd=1, sifat=True, tembusan=True, an=True, nomor_urut=True),
]
