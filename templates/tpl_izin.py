from .common import F, T, SISWA, IDENT_RINGKAS, PEG, TABEL, ACARA, IDENT

SAKIT = F("alasan", "Alasan", "area", "sakit dan perlu istirahat total")
LAMA = F("lama", "Lama izin", "text", "3 (tiga) hari")

ITEMS = [
    # ---------- A. sekolah ----------
    T("izin_siswa_narasi", "Izin Sakit Siswa (naratif)",
      "Semua info menyatu dalam paragraf, tanpa blok identitas.",
      "Surat Izin",
      ["Paragraf pemberitahuan berisi nama anak, kelas, tanggal, dan alasan",
       "Paragraf permohonan izin", "Penutup"],
      SISWA + [SAKIT, LAMA, F("tgl_izin", "Tanggal izin", "text", ""),
               F("guru", "Ditujukan kepada", "text", "Bapak/Ibu Guru")],
      {"pembuka": "Dengan surat ini, kami ingin memberitahukan bahwa putra/putri kami yang "
                  "bernama {nama_siswa}, kelas {kelas}, pada {tgl_izin} tidak bisa "
                  "mengikuti pelajaran seperti biasanya dikarenakan {alasan}.",
       "penutup": "Demikian surat izin yang dapat kami sampaikan. Saya berharap Bapak/Ibu "
                  "Guru dapat memaklumi dan memberikan izin. Atas perhatian Bapak/Ibu "
                  "Guru, kami mengucapkan terima kasih."},
      kop=False, meta="polos", ttd=1, ttd_label=["Orang Tua/Wali Murid"]),

    T("izin_siswa_identitas", "Izin Sakit Siswa (dengan identitas)",
      "Blok Nama / Kelas / Nomor Induk Siswa.",
      "Surat Izin",
      ["Kalimat pembuka sebagai wali murid", "Identitas siswa",
       "Paragraf alasan tidak masuk", "Penutup"],
      SISWA + [SAKIT, F("tgl_izin", "Tanggal izin", "text", "")],
      {"pembuka": "Dengan ini saya selaku wali murid dari:",
       "penutup": "Memberitahukan bahwa anak saya tersebut di atas tidak dapat mengikuti "
                  "pelajaran pada hari ini, {tgl_izin} dikarenakan {alasan}. Oleh sebab itu "
                  "mohon kiranya diberikan izin. Demikian yang dapat saya sampaikan. Atas "
                  "perhatian dan maklumnya diucapkan terima kasih."},
      kop=False, meta="polos", ttd=1, ttd_label=["Orang Tua/Wali Murid"]),

    T("izin_siswa_sembuh", "Izin Sakit Siswa (sampai sembuh)",
      "Tanpa batas tanggal; izin sampai anak sembuh.",
      "Surat Izin",
      ["Kalimat pembuka sebagai orang tua/wali", "Identitas siswa",
       "Paragraf alasan", "Permohonan izin sampai sembuh", "Penutup"],
      SISWA + [SAKIT, F("alamat_org", "Alamat", "area", ""),
               F("wali_kelas", "Wali kelas", "text", "")],
      {"pembuka": "Dengan ini saya selaku orang tua/wali murid dari:",
       "penutup": "Oleh karena itu, kami memohon kepada Bapak/Ibu Guru Wali Kelas agar "
                  "memberikan izin sampai anak saya sembuh. Demikian yang dapat saya "
                  "sampaikan. Atas perhatian Bapak/Ibu Guru kami ucapkan terima kasih."},
      kop=False, meta="polos", ttd=1, ttd_label=["Orang Tua/Wali Murid"]),

    # ---------- B. kerja ----------
    T("izin_kerja_keluarga", "Izin Tidak Masuk Kerja (urusan keluarga)",
      "Blangko; jabatan berupa pilihan; alasan keluarga mendesak.",
      "Permohonan Izin Tidak Masuk Kerja",
      ["Identitas pemohon", "Paragraf alasan dan tanggal tidak masuk", "Penutup"],
      IDENT_RINGKAS + [F("tgl_izin", "Tanggal tidak masuk", "text", ""),
                       F("alasan", "Alasan", "area",
                         "kepentingan keluarga yang sangat mendesak yaitu menjenguk "
                         "keluarga yang sakit di kampung")],
      {"pembuka": "Saya yang bertanda tangan di bawah ini:",
       "penutup": "Demikian surat izin saya sampaikan dengan sebenar-benarnya. Atas "
                  "perhatiannya saya ucapkan terima kasih."},
      kop=False, meta="polos", ttd=1, blangko=True, pilihan=True),

    T("izin_kerja_sakit", "Izin Tidak Masuk Kerja (sakit, surat dokter)",
      "Blok identitas karyawan; periode; lampiran surat dokter.",
      "Surat Izin Tidak Masuk Kerja",
      ["Identitas karyawan", "Paragraf permohonan izin dan periode",
       "Alasan medis dan lampiran surat dokter", "Penutup"],
      [F("nama_org", "Nama", "text", ""), F("alamat_org", "Alamat", "area", ""),
       F("nik", "No. Induk Karyawan", "text", ""),
       F("jabatan_org", "Jabatan", "text", ""),
       F("tgl_izin", "Periode izin", "text", "10 s.d. 16 Oktober 2026"), LAMA,
       F("lampiran_dokter", "Lampiran", "text", "Surat keterangan dari dokter")],
      {"pembuka": "Saya yang bertanda tangan di bawah ini:",
       "penutup": "Demikian surat izin ini saya buat sebenar-benarnya, atas izin yang "
                  "diberikan saya mengucapkan banyak terima kasih."},
      kop=False, meta="polos", ttd=1),

    T("izin_kerja_tugas", "Izin Tidak Masuk Kerja (komitmen tugas)",
      "Tanggal blangko; menyebut tugas tertunda akan diselesaikan.",
      "Permohonan Izin Tidak Masuk Kerja",
      ["Identitas karyawan", "Paragraf pemberitahuan tidak masuk",
       "Komitmen menyelesaikan tugas tertunda", "Penutup"],
      [F("nama_org", "Nama", "text", ""), F("jabatan_org", "Jabatan", "text", ""),
       F("nik", "Nomor ID", "text", ""), F("telp", "No. Telp/Hp", "text", ""),
       F("tgl_izin", "Tanggal", "text", "__/__ sampai __/__"), SAKIT],
      {"pembuka": "Bersama dengan surat ini saya:",
       "penutup": "Adapun tugas-tugas yang tertunda selama tidak hadir kerja akan "
                  "diselesaikan ketika saya sudah masuk bekerja lagi dengan kondusif. "
                  "Mohon doa untuk kesembuhan saya pula. Atas perhatian dan kebijaksanaan "
                  "yang diberikan, saya ucapkan terima kasih."},
      kop=False, meta="polos", ttd=1, blangko=True),

    # ---------- C. keluar kantor ----------
    T("izin_keluar_kantor", "Izin Keluar Kantor pada Jam Kerja",
      "Berkop instansi; jam keluar sampai jam kembali; ditandatangani atasan.",
      "Surat Izin Keluar Kantor pada Jam Kerja",
      ["Kalimat pemberian izin", "Identitas pegawai", "Keperluan dan rentang jam", "Penutup"],
      PEG + [F("keperluan_izin", "Keperluan pribadi", "text", ""),
             F("jam_keluar", "Jam keluar", "text", ""),
             F("jam_kembali", "Jam kembali", "text", "")],
      {"pembuka": "Yang bertanda tangan di bawah ini, memberikan izin kepada:",
       "penutup": "Demikian untuk dipergunakan sebagaimana mestinya."},
      meta="judul", ttd=1, blangko=True),

    T("izin_keluar_slip", "Izin Keluar Kantor (slip kembar)",
      "Dua slip identik berbingkai dalam satu halaman, dipisah garis potong.",
      "Surat Izin Keluar Kantor pada Jam Kerja",
      ["Kalimat pemberian izin", "Identitas pegawai", "Keperluan dan rentang jam", "Penutup"],
      [F("nama_org", "Nama", "text", ""), F("jabatan_org", "Jabatan", "text", ""),
       F("unit", "Unit kerja", "text", ""),
       F("keperluan_izin", "Keperluan (pribadi/pekerjaan)", "text", ""),
       F("jam_keluar", "Jam keluar", "text", ""),
       F("jam_kembali", "Jam kembali", "text", "")],
      {"pembuka": "Yang bertanda tangan di bawah ini, memberikan izin kepada:",
       "penutup": "Demikian untuk digunakan sebagaimana mestinya."},
      kop=False, meta="judul", ttd=1, ttd_label=["H.R.D"],
      blangko=True, coret=True, slip="kembar", bingkai=True),

    # ---------- D. rombongan & keramaian ----------
    T("izin_rombongan", "Izin Meninggalkan Pelajaran (rombongan)",
      "Salam Islami; tabel peserta; rentang tanggal latihan; dua penandatangan.",
      "Surat Izin Meninggalkan Pelajaran",
      ["Salam", "Kalimat maksud mengikuti kegiatan",
       "Rincian kegiatan (Hari/tanggal, Waktu, Tempat)", "Tabel daftar peserta",
       "Penutup dan salam"],
      ACARA + [F("nama_kegiatan", "Nama kegiatan", "text",
                 "Boys Scout Competition (BSC) VII"),
               F("tgl_latihan", "Rentang tanggal izin", "text",
                 "30 Oktober - 7 November 2026"),
               F("jam_pelajaran", "Jam pelajaran yang ditinggalkan", "text",
                 "jam ke 5 - 8"), TABEL],
      {"pembuka": "Sehubungan dengan akan diikutsertakannya siswa kami dalam kegiatan "
                  "{nama_kegiatan} yang akan dilaksanakan pada waktu tersebut, kami mohon "
                  "izin meninggalkan pelajaran pada {jam_pelajaran} untuk peserta berikut:",
       "penutup": "Demikian atas izin yang diberikan disampaikan terima kasih."},
      salam="islami", ttd=2, ttd_label=["Kamabigus", "Pembina"], tabel=True,
      verifikasi="Kepala Sekolah"),

    T("izin_keramaian", "Izin Keramaian (Rame-Rame)",
      "Izin keramaian dari desa; pertimbangan berjenjang Camat, Danramil, Kapolsek.",
      "Surat Pengantar Keterangan Izin Rame-Rame",
      ["Kalimat pemerintah desa menerangkan", "Identitas pemohon",
       "Rincian acara (Waktu, Tempat, Acara, Mengadakan)",
       "Ketentuan yang harus dipatuhi", "Penutup"],
      IDENT + [F("usia", "Umur", "text", ""),
               F("hari_tgl", "Hari / tanggal", "text", "Minggu malam Senin, 26-27 April"),
               F("tempat", "Tempat", "area", ""),
               F("acara", "Acara", "text", "Pernikahan"),
               F("hiburan", "Mengadakan", "text", "Hiburan Organ Tunggal"),
               F("ketentuan", "Ketentuan (satu per baris)", "area",
                 "Pada waktu dilaksanakan rame-rame disertai dengan ketentraman dan "
                 "ketertiban lingkungan\nTidak dibenarkan melakukan hal-hal yang "
                 "bertentangan dengan adat istiadat")],
      {"pembuka": "Pemerintah Desa ... Kecamatan ... Kabupaten ..., dalam rangka memenuhi "
                  "Permohonan Izin Rame-rame:",
       "penutup": "Dengan ini menerangkan dengan seharusnya serta memberikan pertimbangan "
                  "atas permohonan yang bersangkutan dengan ketentuan sebagaimana "
                  "tersebut di atas."},
      meta="judul", ttd=1, an=True,
      pertimbangan=["Camat", "Danramil", "Kapolsek"]),
]
