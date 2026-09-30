from .common import F, T, ACARA, AGENDA, TUJUAN, TEMBUSAN

LATAR = F("latar", "Latar belakang undangan", "area",
          "omset perusahaan mengalami penurunan yang cukup signifikan")
DIUNDANG = F("diundang", "Siapa yang diundang", "text", "seluruh Kepala Divisi")

BAKU_TUTUP = ("Demikian undangan ini kami sampaikan, mengingat pentingnya rapat ini maka "
              "Bapak/Ibu dimohon hadir tepat pada waktunya. Atas perhatiannya, kami ucapkan "
              "terima kasih.")

ITEMS = [
    T("und_rapat_perusahaan", "Undangan Rapat Perusahaan",
      "Undangan rapat internal perusahaan; tanggal sejajar kanan baris Nomor.",
      "Undangan Rapat",
      ["Paragraf pembuka berisi latar belakang dan maksud mengundang",
       "Rincian rapat (Hari/Tanggal, Waktu, Tempat, Tentang)",
       "Paragraf penutup"],
      ACARA + [LATAR, DIUNDANG, F("tentang", "Tentang / pokok bahasan", "text", ""),
               F("inisial", "Kode inisial pengetik", "text", "JM/KS")],
      {"pembuka": "Sehubungan dengan {latar}, maka dengan ini kami mengundang {diundang} "
                  "untuk hadir dalam rapat yang akan dilaksanakan pada:",
       "penutup": BAKU_TUTUP},
      ttd=1, tgl_sejajar=True),

    T("und_rapat_kerja", "Undangan Rapat Kerja / Rakernas",
      "Undangan rapat kerja skala besar; penerima lengkap dengan alamat.",
      "Undangan Rapat Kerja",
      ["Paragraf pembuka berisi agenda besar organisasi",
       "Rincian rapat (Hari/tanggal, Jam, Tempat)", "Paragraf penutup", "Hormat kami"],
      ACARA + TUJUAN + [LATAR, DIUNDANG],
      {"pembuka": "Sehubungan dengan {latar} yang akan dilaksanakan, maka dengan ini kami "
                  "mengundang {diundang} agar dapat menghadiri rapat kerja tersebut. "
                  "Rapat ini akan dilaksanakan pada:",
       "penutup": "Demikian surat undangan ini kami sampaikan, mengingat betapa pentingnya "
                  "acara ini kami sangat mengharapkan kehadiran dari Bapak/Ibu tepat waktu. "
                  "Atas perhatiannya kami ucapkan banyak terima kasih."},
      ttd=1),

    T("und_rapat_sekolah_ringkas", "Undangan Rapat Sekolah (ringkas)",
      "Gaya poster: judul besar di tengah, tanpa nomor surat, detail dalam kotak.",
      "Undangan Rapat Sekolah",
      ["Paragraf undangan singkat", "Rincian rapat dalam kotak", "Ucapan terima kasih"],
      ACARA + [F("nama_rapat", "Nama rapat", "text",
                 "Rapat Persiapan Pelaksanaan Ujian Akhir Semester"),
               DIUNDANG],
      {"pembuka": "Kami mengundang {diundang} untuk menghadiri \u201c{nama_rapat}\u201d "
                  "yang akan dilaksanakan pada:",
       "penutup": "Atas perhatian dan kehadirannya kami ucapkan terima kasih."},
      meta="polos", ttd=1, kotak_detail=True),

    T("und_rapat_keagamaan", "Undangan Rapat Organisasi Keagamaan",
      "Salam Islami, paragraf puji syukur, dua penandatangan (Ketua & Sekretaris).",
      "Undangan Rapat",
      ["Salam dan paragraf puji syukur", "Paragraf maksud mengundang",
       "Rincian rapat (Hari/Tanggal, Waktu, Pembahasan, Tempat)",
       "Paragraf penutup dan salam"],
      ACARA + [F("pembahasan", "Pembahasan", "text", ""), LATAR, DIUNDANG],
      {"pembuka": "Puji syukur kita ucapkan ke hadirat Allah Ta'ala yang telah melimpahkan "
                  "nikmat dan karunia-Nya. Semoga kita selalu dapat mensyukurinya. "
                  "Sehubungan dengan akan dilaksanakannya {latar}, maka panitia perlu "
                  "mengundang Bapak/Ibu untuk bersama-sama hadir pada:",
       "penutup": "Demikian undangan ini kami sampaikan, atas kehadiran Bapak/Ibu kami "
                  "ucapkan terima kasih."},
      salam="islami", ttd=2, ttd_label=["Ketua", "Sekretaris"]),

    T("und_rapat_ortu", "Undangan Rapat Sekolah ke Orang Tua",
      "Kop panjang, paragraf salam sejahtera, Hari & Tanggal terpisah, ada tembusan.",
      "Undangan Rapat",
      ["Salam sejahtera dan doa", "Paragraf maksud undangan",
       "Rincian (Hari, Tanggal, Waktu, Tempat)", "Paragraf penutup"],
      [F("hari", "Hari", "text", "Sabtu"), F("tanggal_acara", "Tanggal", "text",
                                             "3 Desember 2026")] +
      ACARA[1:] + [F("kegiatan", "Kegiatan yang dipersiapkan", "text",
                     "Ujian Kompetensi Keahlian dan Ujian Sekolah"),
                   F("kelas", "Tingkat / kelas", "text", "XII (Dua Belas)"),
                   F("tapel", "Tahun pelajaran", "text", "2026/2027"), TEMBUSAN],
      {"pembuka": "Salam sejahtera kami sampaikan semoga Bapak/Ibu selalu berada dalam "
                  "keadaan sehat wal'afiat serta selalu diberikan kelancaran dalam "
                  "menjalankan segala aktivitasnya. Dalam rangka persiapan menghadapi "
                  "{kegiatan} Tahun Pelajaran {tapel}, bersama ini kami mengundang "
                  "kehadiran Bapak/Ibu Orang Tua/Wali Peserta Didik Kelas {kelas} pada:",
       "penutup": "Mengingat pertemuan ini kami anggap penting, kehadiran Bapak/Ibu sangat "
                  "diharapkan tepat pada waktunya. Demikian undangan ini kami sampaikan. "
                  "Atas perhatiannya diucapkan terima kasih."},
      ttd=1, tembusan=True),

    T("und_meeting_en", "Meeting Invitation (English)",
      "Undangan rapat berbahasa Inggris untuk mitra/klien asing.",
      "Meeting Invitation",
      ["Opening paragraph with purpose", "Meeting details (Day/Date, Time, Location)",
       "Agenda list", "Closing paragraph"],
      ACARA + [AGENDA, F("purpose", "Purpose of the meeting", "area",
                         "to enhance cooperation between companies in the industry"),
               F("invitee", "Who is invited", "text", "all general managers")],
      {"pembuka": "To {purpose}, we would like to invite you to a meeting for {invitee}. "
                  "We are holding the meeting on:",
       "penutup": "We are looking forward to your participation in this meeting. "
                  "Thank you for your cooperation."},
      bahasa="en", ttd=1),
]
