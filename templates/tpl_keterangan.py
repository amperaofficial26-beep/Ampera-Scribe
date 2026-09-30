from .common import (F, T, IDENT, IDENT_RINGKAS, SISWA, MHS, PEG,
                     PENANDATANGAN_SURAT, KEPERLUAN, TEMBUSAN, SAKSI, TABEL)

TUTUP_UMUM = ("Demikian surat keterangan ini dibuat dengan sebenarnya untuk dapat "
              "dipergunakan sebagaimana mestinya.")
ORTU = [F("ayah", "Nama ayah (pekerjaan, pangkat)", "area", ""),
        F("ibu", "Nama ibu (pekerjaan, pangkat)", "area", "")]

ITEMS = [
    # ---------- A. aktif kuliah / sekolah ----------
    T("sk_aktif_kuliah", "Keterangan Aktif Kuliah (sederhana)",
      "Blangko kampus; penutup 'Dikeluarkan di / Pada tanggal'; ditandatangani An. Dekan.",
      "Surat Keterangan Aktif Kuliah",
      ["Kalimat pembuka pejabat menerangkan", "Identitas mahasiswa",
       "Pernyataan status aktif dan peruntukan", "Penutup"],
      MHS + [F("ttl", "Tempat/tgl lahir", "text", ""),
             F("fakultas", "Fakultas", "text", ""), KEPERLUAN],
      {"pembuka": "{jabatan_ttd} dengan ini menerangkan bahwa:",
       "penutup": "Demikianlah Surat Keterangan ini diberikan untuk dapat dipergunakan "
                  "sebagaimana mestinya."},
      meta="judul", ttd=1, tutup_tgl="ditetapkan", an=True, blangko=True),

    T("sk_aktif_kuliah_ortu", "Keterangan Aktif Kuliah (dengan data orang tua)",
      "Tambah data ayah & ibu (pekerjaan, pangkat); ada catatan verifikasi.",
      "Surat Keterangan Aktif Kuliah",
      ["Identitas pejabat yang menerangkan", "Identitas mahasiswa",
       "Data orang tua", "Pernyataan status aktif", "Penutup"],
      PENANDATANGAN_SURAT + MHS + [F("ttl", "Tempat/tgl lahir", "text", ""),
                                   F("alamat_org", "Alamat", "area", "")] + ORTU +
      [F("tahun_akademik", "Tahun akademik & semester", "text", "2025/2026 - Semester VI")],
      {"pembuka": "Yang Bertanda Tangan di bawah ini {nama_ttd}, {jabatan_ttd}, "
                  "menerangkan bahwa:",
       "penutup": "Adalah Benar dan Aktif mengikuti perkuliahan pada Tahun Akademik "
                  "{tahun_akademik}. Demikian Surat Keterangan ini dibuat untuk digunakan "
                  "sebagaimana mestinya."},
      meta="judul", ttd=2, ttd_label=["Diperiksa oleh", "Ka. BAA"]),

    T("sk_masih_kuliah_tunjangan", "Keterangan Masih Kuliah (untuk tunjangan)",
      "Untuk pengurusan tunjangan/pensiun; memuat data orang tua penerima pensiun.",
      "Surat Pernyataan Masih Kuliah",
      ["Identitas pejabat", "Identitas mahasiswa", "Data orang tua/wali penerima pensiun",
       "Keperluan", "Penutup"],
      PENANDATANGAN_SURAT + MHS + [F("kelas_kuliah", "Kelas", "text", "Reguler Sore"),
                                   F("status_akademik", "Status akademik", "text",
                                     "2025/2026 tercatat sebagai Mahasiswa Aktif"),
                                   F("nama_ortu", "Nama orang tua/wali", "text", ""),
                                   F("nip_ortu", "NIP/NRP orang tua", "text", ""),
                                   F("pangkat_ortu", "Pangkat/Golongan orang tua", "text", ""),
                                   F("sk_pensiun", "Nomor SK Pensiun", "text", ""),
                                   F("instansi_ortu", "Instansi/Perusahaan", "text", ""),
                                   KEPERLUAN, TEMBUSAN],
      {"pembuka": "Yang bertanda tangan di bawah ini: ... dengan ini menyatakan bahwa:",
       "penutup": "Demikian Surat Pernyataan ini dibuat dengan sesungguhnya, agar dapat "
                  "dipergunakan sebagaimana mestinya."},
      meta="judul", ttd=1, tembusan=True, no_formulir=True),

    # ---------- B. domisili ----------
    T("sk_domisili_desa", "Keterangan Domisili (Desa/Kelurahan)",
      "Berkop desa; merujuk surat pengantar RT/Kelian Banjar.",
      "Surat Keterangan Domisili",
      ["Kalimat pejabat menerangkan", "Identitas warga",
       "Rujukan surat pengantar RT/lingkungan", "Pernyataan domisili dan keperluan",
       "Penutup"],
      [F("pejabat", "Pejabat yang menerangkan", "text",
         "Kepala Desa ... Kecamatan ... Kabupaten ...")] + IDENT +
      [F("kewarganegaraan", "Kewarganegaraan", "text", "Indonesia"),
       F("pengantar", "Surat pengantar RT/lingkungan (nomor & tanggal)", "text", ""),
       KEPERLUAN],
      {"pembuka": "{pejabat}, dengan ini menerangkan bahwa warga kami:",
       "penutup": "Demikian surat keterangan ini kami buat dengan sebenarnya untuk dapat "
                  "dipergunakan sebagaimana mestinya."},
      meta="judul", ttd=1),

    T("sk_domisili_rt", "Keterangan Domisili RT/RW (blangko)",
      "Tanpa kop resmi; field sampai status perkawinan & agama; TTD Ketua RT.",
      "Surat Keterangan",
      ["Kalimat Ketua RT menerangkan", "Identitas warga",
       "Pernyataan domisili dan keperluan", "Penutup"],
      IDENT + [F("status_kawin", "Status perkawinan", "text", "Kawin"),
               F("rt_rw", "RT / RW", "text", "RT 005 / RW 002"), KEPERLUAN],
      {"pembuka": "Yang bertanda tangan di bawah ini Ketua RT ... RW ... Desa ... "
                  "Kecamatan ... Kabupaten ... dengan ini menerangkan bahwa:",
       "penutup": "Orang tersebut di atas adalah benar-benar warga kami dan berdomisili di "
                  "wilayah kami. Surat keterangan ini dibuat sebagai kelengkapan pengurusan. "
                  + TUTUP_UMUM},
      kop=False, meta="judul", ttd=1, blangko=True),

    T("sk_domisili_nomor", "Keterangan Domisili (identitas bernomor)",
      "Identitas bernomor 1-10, blok 'Keterangan Lain', dua tanda tangan.",
      "Surat Keterangan Domisili",
      ["Kalimat pejabat menerangkan", "Identitas warga bernomor",
       "Keterangan lain", "Penutup"],
      IDENT + [F("status_kawin", "Status perkawinan", "text", ""),
               F("ket_lain", "Keterangan lain (satu per baris)", "area",
                 "Benar-benar penduduk Desa ...\nBenar mendaftar sebagai anggota ...")],
      {"pembuka": "Yang bertanda tangan di bawah ini Kepala Desa ... Kecamatan ... "
                  "menerangkan dengan sebenarnya:",
       "penutup": TUTUP_UMUM},
      meta="judul", ttd=2, ttd_label=["Tanda tangan Ybs.", "Kepala Desa"], nomor_urut=True),

    # ---------- C. kerja ----------
    T("sk_pengalaman_modern", "Keterangan Pengalaman Kerja (perusahaan modern)",
      "Ada bullet pencapaian terukur dan alasan berakhirnya hubungan kerja.",
      "Surat Pengalaman Kerja",
      ["Identitas pemberi keterangan", "Identitas karyawan",
       "Bullet pencapaian selama bekerja", "Alasan berakhirnya hubungan kerja", "Penutup"],
      PENANDATANGAN_SURAT + [F("nama_peg", "Nama karyawan", "text", ""),
                             F("nik_peg", "NIK karyawan", "text", ""),
                             F("jabatan_peg", "Posisi terakhir", "text", ""),
                             F("pencapaian", "Pencapaian (satu per baris)", "area",
                               "Kepemimpinan efektif dalam proyek A, meningkatkan efisiensi 20%"),
                             F("alasan_keluar", "Alasan berakhir", "text",
                               "pengunduran diri atas permintaan sendiri")],
      {"pembuka": "Yang bertanda tangan di bawah ini:",
       "penutup": "Surat ini dibuat karena {alasan_keluar} dan dapat digunakan untuk "
                  "keperluan profesional selanjutnya."},
      meta="judul", ttd=1),

    T("sk_kerja_korporat", "Keterangan Kerja (korporat)",
      "Satu paragraf narasi: periode kerja, status, dan posisi terakhir.",
      "Surat Keterangan",
      ["Kalimat pembuka menerangkan", "Identitas karyawan",
       "Paragraf masa kerja dan posisi terakhir", "Penutup"],
      [F("nama_peg", "Nama", "text", ""), F("npp", "NPP / NIK", "text", ""),
       F("alamat_org", "Alamat", "area", ""),
       F("perusahaan", "Nama perusahaan/unit", "text", ""),
       F("status_kerja", "Status kerja", "text", "Tenaga Outsourcing"),
       F("periode", "Periode kerja", "text", "07 Januari 2011 s.d. 24 Desember 2014"),
       F("posisi_akhir", "Posisi terakhir", "text", "Administrasi Umum")],
      {"pembuka": "Yang bertanda tangan di bawah ini menerangkan bahwa:",
       "penutup": TUTUP_UMUM},
      meta="judul", ttd=1),

    T("sk_pengalaman_instansi", "Keterangan Pengalaman Kerja (instansi/sekolah)",
      "Pemberi keterangan lengkap NIP & pangkat; daftar tugas bernomor; lampiran SK.",
      "Surat Keterangan Pengalaman Kerja",
      ["Identitas pemberi keterangan", "Identitas yang diterangkan",
       "Masa kerja dan jabatan", "Daftar tugas bernomor", "Lampiran", "Penutup"],
      [F("nama_ttd", "Nama pemberi", "text", ""), F("nip_ttd", "NIP pemberi", "text", ""),
       F("pangkat_ttd", "Pangkat/Gol pemberi", "text", ""),
       F("jabatan_ttd", "Jabatan pemberi", "text", "Kepala Sekolah"),
       F("instansi", "Instansi", "text", "")] +
      [F("nama_peg", "Nama", "text", ""), F("nik_peg", "NIK", "text", ""),
       F("alamat_org", "Alamat", "area", ""),
       F("masa_kerja", "Lama pengalaman kerja", "text", "1 Tahun 2 Bulan"),
       F("jabatan_peg", "Jabatan", "text", "Guru Mata Pelajaran Bahasa Inggris"),
       F("tugas_tambahan", "Tugas-tugas (satu per baris)", "area", "Guru Mapel\nWakasis"),
       F("lampiran_sk", "Lampiran", "text", "SK Pengangkatan Tenaga Honorer")],
      {"pembuka": "Saya yang bertanda tangan di bawah ini ... dengan ini menyatakan bahwa:",
       "penutup": "Demikian Surat Keterangan ini dibuat untuk dipergunakan sebagaimana "
                  "mestinya."},
      meta="judul", ttd=1),

    # ---------- D. SKTM ----------
    T("sktm_blangko", "SKTM (blangko desa dengan saksi)",
      "Tiga poin kondisi 'coret yang tidak perlu'; saksi RT & RW; verifikasi Camat.",
      "Surat Keterangan Tidak Mampu",
      ["Identitas pejabat", "Identitas pemohon", "Poin kondisi ekonomi",
       "Peruntukan", "Penutup"],
      [F("pejabat", "Pejabat", "text", "Kepala Desa ...")] + IDENT +
      [F("kondisi", "Kondisi (satu per baris)", "area",
         "Pekerjaan sehari-hari ...\nPekerjaan musiman/tetap ...\n"
         "Menderita penyakit dan membutuhkan pelayanan kesehatan"), KEPERLUAN],
      {"pembuka": "Saya yang bertanda tangan di bawah ini menerangkan dengan sesungguhnya "
                  "bahwa nama tersebut di bawah ini adalah benar masyarakat kurang mampu "
                  "dengan kondisi sebagai berikut:",
       "penutup": "Demikian surat keterangan ini dibuat dengan sebenarnya untuk digunakan "
                  "sebagai lampiran penerbitan surat keterangan miskin (SPM)."},
      meta="judul", ttd=2, ttd_label=["Saksi Ketua RT/RW", "Kepala Desa"],
      verifikasi="Camat", blangko=True, coret=True),

    T("sktm_narasi", "SKTM (narasi desa)",
      "Kalimat 'tergolong keluarga prasejahtera'; menyebut peruntukan bantuan.",
      "Surat Keterangan Tidak Mampu",
      ["Kalimat pejabat menerangkan", "Identitas warga",
       "Paragraf kondisi ekonomi keluarga", "Peruntukan bantuan", "Penutup"],
      [F("pejabat", "Pejabat", "text", "Kepala Desa ...")] + IDENT +
      [F("bantuan", "Bantuan yang dituju", "text",
         "bantuan berupa rehab/perbaikan rumah tempat tinggal")],
      {"pembuka": "Yang bertanda tangan di bawah ini {pejabat} menerangkan bahwa:",
       "penutup": "Demikian surat keterangan ini dibuat dengan sebenarnya dan diberikan "
                  "kepada yang bersangkutan untuk dapat dipergunakan sebagaimana mestinya."},
      meta="judul", ttd=1),

    T("sktm_anak", "SKTM RT (orang tua & anak)",
      "Dua blok identitas: data orang tua lalu data anak.",
      "Surat Keterangan Tidak Mampu (SKTM)",
      ["Kalimat Ketua RT menerangkan", "Identitas orang tua", "Identitas anak",
       "Pernyataan keluarga tidak mampu", "Penutup"],
      IDENT + [F("nama_anak", "Nama anak", "text", ""),
               F("ttl_anak", "Tempat/tanggal lahir anak", "text", ""),
               F("agama_anak", "Agama anak", "text", ""),
               F("pekerjaan_anak", "Pekerjaan anak", "text", "Pelajar"),
               F("alamat_anak", "Alamat anak", "area", "")],
      {"pembuka": "Yang bertanda tangan di bawah ini adalah Ketua RT ... Kelurahan ... "
                  "Dengan ini menerangkan berikut:",
       "penutup": "Alamat tersebut di atas adalah warga yang bertempat tinggal di wilayah "
                  "yang saya pimpin dan sepengetahuan kami yang bersangkutan adalah "
                  "keluarga tidak mampu. Demikianlah surat keterangan ini kami buat untuk "
                  "dipergunakan sebagaimana mestinya."},
      meta="judul", ttd=1),

    # ---------- E. kelakuan baik ----------
    T("sk_kelakuan_siswa", "Keterangan Kelakuan Baik (siswa)",
      "Menyebut bebas NAPZA; untuk mendaftar perguruan tinggi.",
      "Surat Keterangan Kelakuan Baik",
      ["Kalimat kepala sekolah menerangkan", "Identitas siswa",
       "Pernyataan kelakuan baik dan bebas NAPZA", "Peruntukan", "Penutup"],
      SISWA + [F("ttl", "Tempat, tanggal lahir", "text", ""),
               F("jk", "Jenis kelamin", "text", ""), F("agama", "Agama", "text", ""),
               F("alamat_org", "Alamat", "area", ""), KEPERLUAN],
      {"pembuka": "Dengan ini Kepala {sekolah}, menerangkan dengan sesungguhnya bahwa:",
       "penutup": "Berdasarkan pantauan dan catatan yang ada, siswa tersebut berkelakuan "
                  "baik dan tidak terlibat penyalahgunaan Narkotika, Alkohol, Psikotropika "
                  "dan Zat Adiktif (NAPZA) yang dapat merusak moral dan kesehatan. "
                  "Demikian surat keterangan ini kami buat untuk digunakan sebagai bahan "
                  "pertimbangan seperlunya."},
      meta="judul", ttd=1, tutup_tgl="ditetapkan"),

    T("sk_kelakuan_mhs", "Keterangan Berkelakuan Baik (mahasiswa)",
      "Format seperti keterangan aktif kuliah; untuk persyaratan beasiswa.",
      "Surat Keterangan Berkelakuan Baik",
      ["Kalimat pejabat menerangkan", "Identitas mahasiswa",
       "Pernyataan berkelakuan baik", "Peruntukan", "Penutup"],
      MHS + [F("ttl", "Tempat/tgl lahir", "text", ""),
             F("fakultas", "Fakultas", "text", ""),
             F("alamat_org", "Alamat", "area", ""), KEPERLUAN],
      {"pembuka": "Dekan {fakultas} dengan ini menerangkan bahwa:",
       "penutup": "Nama tersebut di atas terdaftar dan berkelakuan BAIK SEKALI dalam "
                  "perkuliahan. Demikianlah Surat Keterangan ini diberikan untuk dapat "
                  "dipergunakan sebagaimana mestinya."},
      meta="judul", ttd=1),

    T("sk_kelakuan_karyawan", "Keterangan Kelakuan Baik (karyawan, blangko)",
      "Tanpa kop; menyebut tidak terlibat NARKOBA; tembusan Arsip.",
      "Surat Keterangan Kelakuan Baik",
      ["Identitas pemberi keterangan", "Identitas karyawan",
       "Pernyataan kelakuan baik", "Penutup"],
      PENANDATANGAN_SURAT + [F("nama_peg", "Nama", "text", ""),
                             F("ttl", "Tempat, tanggal lahir", "text", ""),
                             F("jabatan_peg", "Jabatan", "text", ""),
                             F("jk", "Jenis kelamin", "text", ""),
                             F("tgl_masuk", "Tanggal masuk", "text", ""),
                             F("alamat_org", "Alamat", "area", ""), TEMBUSAN],
      {"pembuka": "Yang bertanda tangan di bawah ini: ... Menerangkan bahwa:",
       "penutup": "Bahwa selama menjadi karyawan di instansi kami, yang bersangkutan "
                  "berkelakuan baik dan tidak terlibat penyalahgunaan NARKOBA. Demikian "
                  "surat keterangan ini kami sampaikan, untuk dapat dipergunakan "
                  "sebagaimana mestinya."},
      kop=False, meta="judul", ttd=1, tembusan=True, blangko=True),

    # ---------- F. tambahan dari batch pernyataan ----------
    T("sk_belum_menikah", "Keterangan Belum Menikah",
      "Diterbitkan pejabat desa/kelurahan, berkop dan bernomor.",
      "Surat Keterangan Belum Menikah",
      ["Kalimat pejabat menerangkan", "Identitas warga",
       "Pernyataan status belum menikah", "Penutup"],
      IDENT + [F("suku", "Suku / bangsa", "text", ""),
               F("status_kawin", "Status perkawinan", "text", "Belum Kawin")],
      {"pembuka": "Yang bertanda tangan di bawah ini Kepala Desa/Lurah ... dengan ini "
                  "menerangkan bahwa:",
       "penutup": "Yang tersebut di atas menurut sepengetahuan dan penelitian kami benar "
                  "BELUM PERNAH MENIKAH sampai sekarang. Demikianlah surat keterangan ini "
                  "dibuat agar dapat dipergunakan sebagaimana mestinya."},
      meta="judul", ttd=1),

    T("sk_hilang", "Keterangan Hilang (barang inventaris)",
      "Dikeluarkan kepala instansi; sebut barang, merek, hari, pukul, tempat.",
      "Surat Keterangan Hilang",
      ["Identitas pejabat", "Uraian barang yang hilang",
       "Waktu dan tempat kejadian", "Penutup"],
      [F("nama_ttd", "Nama pejabat", "text", ""), F("nip_ttd", "NIP", "text", ""),
       F("jabatan_ttd", "Jabatan", "text", "Kepala Sekolah"),
       F("alamat_org", "Alamat", "area", ""),
       F("barang", "Barang yang hilang", "text", "Sanyo Merk Shimizu (Mesin Pompa Air)"),
       F("hari_tgl", "Hari / tanggal", "text", ""), F("waktu", "Pukul", "text", ""),
       F("tempat", "Tempat", "text", "")],
      {"pembuka": "Saya yang bertanda tangan di bawah ini: ... Menerangkan bahwa telah "
                  "kehilangan barang berupa:",
       "penutup": "Demikianlah Surat Keterangan hilang ini kami buat dengan sebenarnya dan "
                  "dapat dipergunakan sebagaimana mestinya."},
      meta="judul", ttd=1),

    T("sk_ahli_waris_blangko", "Keterangan Ahli Waris (blangko desa)",
      "Daftar ahli waris + saksi RT/RW + blok registrasi + Mengetahui Camat & Kades.",
      "Surat Keterangan Ahli Waris",
      ["Kalimat para ahli waris", "Data almarhum/almarhumah",
       "Daftar ahli waris", "Peruntukan", "Penutup"],
      [F("almarhum", "Nama almarhum/almarhumah", "text", ""),
       F("wafat", "Hari, tanggal, dan tempat wafat", "text", ""),
       F("pasangan", "Menikah dengan", "text", ""),
       F("jml_anak", "Jumlah anak", "text", "3 (tiga)"), TABEL,
       F("peruntukan", "Peruntukan", "text", "menutup dan mengambil tabungan di Bank ...")],
      {"pembuka": "Kami yang bertanda tangan di bawah ini adalah ahli waris yang sah dari "
                  "almarhum/almarhumah {almarhum}, yang meninggal dunia pada {wafat}:",
       "penutup": "Bahwa nama-nama tersebut di atas adalah para ahli waris almarhum yang "
                  "sah dan tidak ada ahli waris lainnya. Demikian Surat Keterangan Ahli "
                  "Waris ini dibuat untuk {peruntukan}."},
      meta="judul", ttd=2, ttd_label=["Saksi Ketua RT", "Saksi Ketua RW"],
      verifikasi="Camat dan Kepala Desa", registrasi=True, tabel=True, blangko=True),

    T("sk_ahli_waris_banyak", "Keterangan Ahli Waris (daftar banyak)",
      "Sampai 9 ahli waris lengkap; untuk mengambil tabungan bank; TTD bernomor.",
      "Surat Keterangan Ahli Waris",
      ["Kalimat para ahli waris", "Data almarhum", "Daftar ahli waris lengkap",
       "Peruntukan", "Penutup"],
      [F("almarhum", "Nama almarhum", "text", ""),
       F("wafat", "Hari, tanggal, jam, tempat wafat", "area", ""),
       F("pasangan", "Menikah dengan (nama, lahir)", "text", ""),
       F("jml_anak", "Jumlah anak", "text", "8 (delapan)"), TABEL,
       F("peruntukan", "Peruntukan", "text",
         "menutup dan mengambil tabungan SIMPEDES di BRI unit ...")],
      {"pembuka": "Kami yang bertanda tangan di bawah ini adalah ahli waris yang sah dari "
                  "almarhum {almarhum}:",
       "penutup": "Bahwa nama-nama tersebut di atas adalah para ahli waris yang sah dan "
                  "tidak ada ahli waris lainnya. Demikian surat keterangan ahli waris ini "
                  "dibuat untuk {peruntukan}."},
      meta="judul", ttd=2, ttd_label=["Saksi Ketua RT", "Saksi Ketua RW"],
      registrasi=True, tabel=True),

    T("sk_ahli_waris_harta", "Keterangan Ahli Waris (narasi + harta)",
      "Satu ahli waris; menyebut harta peninggalan; sampai 6 penandatangan berjenjang.",
      "Surat Keterangan Ahli Waris",
      ["Pernyataan ahli waris", "Data almarhum dan riwayat pernikahan",
       "Identitas ahli waris", "Harta peninggalan", "Penutup"],
      [F("almarhum", "Nama almarhum/almarhumah", "text", ""),
       F("wafat", "Hari, tanggal, tempat wafat", "text", ""),
       F("tempat_tinggal_akhir", "Tempat tinggal terakhir", "area", "")] + IDENT_RINGKAS +
      [F("usia", "Usia", "text", ""),
       F("harta", "Harta peninggalan", "area",
         "Sebidang tanah tercatat dalam Sertifikat Hak Milik Nomor ... atas nama ...")],
      {"pembuka": "Saya yang bertandatangan di bawah ini menyatakan dengan sesungguhnya "
                  "adalah ahli waris dari {almarhum} yang meninggal dunia pada {wafat}:",
       "penutup": "Demikian Surat Keterangan Ahli Waris ini saya buat dengan sebenarnya "
                  "tanpa ada paksaan dari pihak manapun di hadapan dua orang saksi. Apabila "
                  "di kemudian hari terjadi sesuatu, maka saya akan bertanggung jawab dan "
                  "tidak akan melibatkan Pejabat Pemerintah baik Lurah maupun Camat beserta "
                  "pengurus RT dan RW yang ikut menandatangani."},
      meta="judul", ttd=4,
      ttd_label=["Saksi 1", "Saksi 2", "Ketua RT", "Ketua RW"],
      verifikasi="Lurah dan Camat", registrasi=True, materai=True, saksi=True),
]
