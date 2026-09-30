from .common import F, T, IDENT, IDENT_RINGKAS, SISWA, MHS, POIN, TEMBUSAN, SAKSI

SANKSI = F("konsekuensi", "Konsekuensi bila dilanggar", "area",
           "bersedia menerima sanksi sesuai dengan peraturan yang berlaku")
TUTUP = ("Demikian surat pernyataan ini saya buat dengan sebenarnya dan penuh kesadaran, "
         "tanpa paksaan dari pihak manapun.")

ITEMS = [
    T("pny_taat_sekolah", "Pernyataan Kesanggupan Mentaati Peraturan (sekolah)",
      "Blangko; kotak materai; dua TTD (orang tua & siswa).",
      "Surat Pernyataan Kesanggupan Mentaati Peraturan",
      ["Identitas pembuat pernyataan", "Isi pernyataan kesanggupan", "Penutup"],
      SISWA + [F("alamat_org", "Alamat", "area", ""),
               F("instansi", "Nama sekolah", "text", "")],
      {"pembuka": "Saya yang bertandatangan di bawah ini:",
       "penutup": "Dengan sungguh-sungguh menyatakan bahwa saya siap menjadi Peserta Didik "
                  "di {instansi} dan saya bersedia mentaati segala peraturan yang ada di "
                  "{instansi}. Demikian Surat Pernyataan ini saya tandatangani di atas "
                  "materai secara sukarela tanpa paksaan dari pihak manapun dan disaksikan "
                  "oleh Orang Tua/Wali."},
      meta="judul", ttd=2, ttd_label=["Mengetahui Orang Tua/Wali", "Pembuat Pernyataan"],
      materai=True, tutup_tgl="ditetapkan", blangko=True),

    T("pny_taat_kampus", "Pernyataan Kesanggupan Mentaati Tata Tertib (kampus)",
      "Poin komitmen bernomor (bebas narkoba, tidak pindah prodi, sanksi).",
      "Surat Pernyataan Kesanggupan Mentaati Peraturan & Tata Tertib",
      ["Dasar peraturan kampus", "Identitas mahasiswa",
       "Poin-poin pernyataan bernomor", "Penutup"],
      MHS + [F("nik", "NIK", "text", ""), F("ttl", "Tempat, tanggal lahir", "text", ""),
             F("sekolah", "Asal sekolah", "text", ""),
             F("alamat_org", "Alamat", "area", ""),
             F("instansi", "Nama kampus", "text", ""), POIN],
      {"pembuka": "Berdasarkan Peraturan dan Tata Tertib yang berlaku di {instansi}, maka "
                  "saya yang bertanda tangan di bawah ini menyatakan:",
       "penutup": "Demikian pernyataan ini saya buat dengan sesungguhnya dan dengan penuh "
                  "kesadaran."},
      meta="judul", ttd=2, ttd_label=["Mengetahui Orang Tua/Wali", "Yang membuat pernyataan"],
      materai=True),

    T("pny_tidak_beasiswa", "Pernyataan Tidak Sedang Menerima Beasiswa Lain",
      "Identitas akademik lengkap (IP/IPK); konsekuensi mengembalikan uang beasiswa.",
      "Surat Pernyataan Tidak Sedang Menerima Beasiswa Lain",
      ["Identitas mahasiswa", "Isi pernyataan", "Konsekuensi", "Penutup"],
      MHS + [F("ttl", "Tempat/tanggal lahir", "text", ""),
             F("jk", "Jenis kelamin", "text", ""),
             F("ipk", "IP dan IPK terakhir", "text", "2.83 dan 3.27"),
             F("telp", "Kontak Person / HP", "text", ""),
             F("beasiswa", "Nama beasiswa yang dilamar", "text", "")],
      {"pembuka": "Saya yang bertanda tangan di bawah ini:",
       "penutup": "Dengan ini menerangkan bahwa saya sebagai calon penerima {beasiswa} "
                  "tidak sedang menerima beasiswa lainnya. Apabila di kemudian hari "
                  "terbukti saya sedang menerima beasiswa lain, maka saya bersedia "
                  "mengembalikan uang beasiswa yang saya terima atau sanksi akademis atau "
                  "sanksi sesuai ketentuan yang berlaku."},
      meta="judul", ttd=2, ttd_label=["Mengetahui Wakil Dekan", "Yang membuat pernyataan"]),

    T("pny_tidak_bekerja", "Pernyataan Tidak Sedang Bekerja / Ikatan Dinas",
      "Paling ringkas, blangko; satu paragraf + kesediaan menerima sanksi.",
      "Surat Pernyataan Tidak Sedang Bekerja / Status Ikatan Dinas",
      ["Identitas mahasiswa", "Isi pernyataan", "Penutup"],
      MHS + [F("ttl", "Tempat / tanggal lahir", "text", ""),
             F("fakultas", "Fakultas", "text", ""),
             F("alamat_org", "Alamat", "area", ""), SANKSI],
      {"pembuka": "Saya yang bertanda tangan di bawah ini:",
       "penutup": "Saya adalah benar mahasiswa yang terdaftar pada semester berjalan, dan "
                  "pada saat ini tidak sedang bekerja maupun dalam Status Ikatan Dinas pada "
                  "pihak manapun, dan saya bersedia menerima sanksi bila mana pernyataan "
                  "saya tidak benar. Demikian surat pernyataan saya perbuat untuk "
                  "dipergunakan seperlunya."},
      kop=False, meta="judul", ttd=1, blangko=True),

    T("pny_kebenaran_dokumen", "Pernyataan Kebenaran Data / Dokumen (PPDB)",
      "Dua blok identitas berlabel (orang tua & calon murid); dua TTD + materai.",
      "Surat Pernyataan Kebenaran Dokumen",
      ["Identitas orang tua/wali", "Identitas calon murid",
       "Poin-poin pernyataan", "Penutup"],
      [F("nama_ortu", "Nama orang tua/wali", "text", ""),
       F("alamat_ortu", "Alamat orang tua", "area", ""),
       F("pekerjaan", "Pekerjaan", "text", ""),
       F("nama_siswa", "Nama calon murid", "text", ""),
       F("nisn", "NISN", "text", ""), F("alamat_siswa", "Alamat calon murid", "area", ""),
       F("sekolah", "Asal sekolah", "text", ""),
       F("seleksi", "Nama proses seleksi", "text", "SPMB SMA/SMK Negeri Tahun 2026/2027"),
       POIN],
      {"pembuka": "Yang bertanda tangan di bawah ini merupakan orang tua/wali dari calon "
                  "murid yang mengikuti proses seleksi {seleksi}, menyatakan bahwa:",
       "penutup": "Demikian Surat Pernyataan ini kami buat dengan sebenar-benarnya, untuk "
                  "dapat dipergunakan sebagaimana mestinya, dan kepada yang berkepentingan "
                  "untuk menjadikan maklum."},
      kop=False, meta="judul", ttd=2, ttd_label=["Calon Murid", "Yang membuat (Ortu/Wali)"],
      materai=True),

    T("pny_beasiswa_ortu", "Pernyataan Kesediaan Penerima Beasiswa (orang tua)",
      "Data orang tua + data siswa; poin termasuk sifat program confidential.",
      "Surat Pernyataan Beasiswa Pendidikan",
      ["Identitas orang tua", "Identitas siswa", "Poin-poin pernyataan", "Penutup"],
      [F("nama_ortu", "Nama orang tua", "text", ""),
       F("ttl", "Tempat, tanggal lahir", "text", ""),
       F("nik", "No KTP/NIK", "text", ""), F("alamat_org", "Alamat", "area", ""),
       F("nama_siswa", "Nama siswa", "text", ""), F("usia", "Usia", "text", ""),
       F("kelas", "Kelas", "text", ""),
       F("program_beasiswa", "Program beasiswa & masa berlaku", "text", ""), POIN],
      {"pembuka": "Yang bertanda tangan di bawah ini, saya orang tua siswa pelamar "
                  "beasiswa pendidikan, menyatakan dengan sesungguhnya bahwa saya:",
       "penutup": "Apabila di kemudian hari diketahui ada pernyataan yang tidak benar atau "
                  "yang tidak dipenuhi, saya siap menerima konsekuensi yang berlaku. "
                  "Demikian surat pernyataan ini dibuat dengan sebenar-benarnya untuk "
                  "dipergunakan sebagaimana mestinya."},
      meta="judul", ttd=1, materai=True),

    T("pny_belum_menikah", "Pernyataan Belum Pernah Menikah",
      "Identitas kependudukan lengkap; materai; blok saksi dengan tanda tangan.",
      "Surat Pernyataan Belum Pernah Menikah",
      ["Identitas pembuat pernyataan", "Isi pernyataan", "Konsekuensi", "Penutup"],
      IDENT + [F("kewarganegaraan", "Warga negara", "text", "Indonesia"), SAKSI],
      {"pembuka": "Yang bertanda tangan di bawah ini:",
       "penutup": "Menyatakan dengan sesungguhnya bahwa saya sampai dengan dibuatnya "
                  "pernyataan ini belum pernah menikah. Demikian surat pernyataan ini saya "
                  "buat dengan sebenarnya, dan apabila di kemudian hari ternyata saya "
                  "berbohong, saya bersedia bertanggung jawab di hadapan pihak yang "
                  "berwenang sesuai peraturan perundang-undangan yang berlaku."},
      kop=False, meta="judul", ttd=1, ttd_label=["Yang Menyatakan"],
      materai=True, saksi=True),

    T("pny_kehilangan", "Pernyataan Kehilangan (barang/dokumen)",
      "Narasi kronologi kehilangan; harapan diterbitkan surat keterangan kepolisian.",
      "Surat Pernyataan Kehilangan",
      ["Identitas pelapor", "Kronologi kehilangan", "Harapan tindak lanjut", "Penutup"],
      IDENT + [F("status_kawin", "Status perkawinan", "text", ""),
               F("telp", "No Telp/HP", "text", ""),
               F("barang", "Barang/dokumen yang hilang", "text", "KTP dengan NIK ..."),
               F("kronologi", "Kronologi (waktu dan rute)", "area",
                 "pada tanggal ... dalam perjalanan dari ... menuju ...")],
      {"pembuka": "Saya yang bertanda tangan di bawah ini:",
       "penutup": "Demikian surat pernyataan ini saya buat dengan sebenar-benarnya dengan "
                  "harapan pihak kepolisian dapat memberikan surat keterangan kehilangan "
                  "agar saya dapat mengurus penggantinya. Terima kasih atas perhatian dari "
                  "Bapak/Ibu."},
      kop=False, meta="judul", ttd=1, ttd_label=["Yang menyatakan"]),

    T("pny_pengunduran_diri", "Pernyataan Pengunduran Diri",
      "Menyebut posisi, tanggal efektif, apresiasi, dan komitmen transisi.",
      "Surat Pengunduran Diri",
      ["Identitas dan pernyataan pengunduran diri", "Alasan dan apresiasi",
       "Komitmen masa transisi", "Penutup"],
      [F("nama_org", "Nama", "text", ""), F("alamat_org", "Alamat", "area", ""),
       F("jabatan_org", "Posisi/jabatan", "text", ""),
       F("perusahaan", "Perusahaan/organisasi", "text", ""),
       F("tgl_efektif", "Efektif per tanggal", "text", "1 September 2026"),
       F("alasan", "Alasan (opsional)", "area", "")],
      {"pembuka": "Saya, {nama_org}, yang bertempat tinggal di {alamat_org}, dengan ini "
                  "mengajukan pengunduran diri dari posisi {jabatan_org} di {perusahaan}, "
                  "efektif per {tgl_efektif}.",
       "penutup": "Saya akan memastikan transisi berjalan lancar hingga tanggal "
                  "pengunduran diri saya. Terima kasih atas perhatian dan kerjasamanya."},
      kop=False, meta="polos", ttd=1, ttd_label=["Hormat Saya"]),
]
