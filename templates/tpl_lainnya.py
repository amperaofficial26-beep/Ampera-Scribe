"""Jenis pelengkap: Edaran, Pengumuman, Memo, Pengantar, Berita Acara."""
from .common import F, T, TABEL, TEMBUSAN, POIN, ACARA, DASAR, IDENT_RINGKAS

# ----------------------------------------------------------------- EDARAN
EDARAN = [
    T("edaran_rt", "Edaran Gotong Royong (RT/RW)",
      "Judul + baris 'Tentang' + topik di tengah; daftar lokasi bernomor.",
      "Surat Edaran",
      ["Tentang", "Kalimat pemberitahuan kegiatan",
       "Daftar lokasi/acara bernomor", "Harapan kehadiran", "Penutup"],
      ACARA + [F("tentang", "Tentang", "text", "GOTONG ROYONG"),
               F("wilayah", "Wilayah", "text", "WARGA RT 009 / RW 06"),
               F("lokasi_kerja", "Lokasi yang dikerjakan (satu per baris)", "area",
                 "Sekitar rumah masing-masing\nSarana umum (jalan, gorong-gorong)\n"
                 "Ramah tamah"),
               F("alasan", "Alasan/latar", "text",
                 "menjaga kebersihan dan kesehatan masyarakat")],
      {"pembuka": "Kami beritahukan kepada {wilayah}, akan diadakan kerja bakti untuk "
                  "{alasan}. Kami sebagai pengurus RT mengharapkan semua warga ikut "
                  "berpartisipasi dalam kegiatan tersebut. Adapun acara dan tempat:",
       "penutup": "Demikian surat edaran dan pemberitahuan ini demi kenyamanan dan "
                  "kebersamaan warga. Atas perhatian dan partisipasinya kami sampaikan "
                  "terima kasih."},
      meta="judul", ttd=1, tentang=True),

    T("edaran_tindak_lanjut", "Edaran Tindak Lanjut Instruksi",
      "Menindaklanjuti surat instansi atasan; paragraf inti dicetak tebal; tembusan.",
      "Surat Edaran",
      ["Salam", "Rujukan surat yang ditindaklanjuti", "Instruksi inti (dicetak tebal)",
       "Penutup"],
      [DASAR, F("instruksi", "Instruksi inti", "area",
                "kami meminta para Ketua RT untuk menghimbau seluruh warga melaksanakan "
                "kerja bakti serentak pada Hari Minggu, pukul 07.30 WIB"),
       F("tujuan_edaran", "Ditujukan kepada", "text", "Para Ketua RT di lingkungan RW"),
       TEMBUSAN],
      {"pembuka": "Menindaklanjuti {dasar}, maka:",
       "penutup": "Demikian surat edaran ini kami sampaikan, atas kerja sama dan "
                  "perhatian kami ucapkan terima kasih."},
      salam="islami", ttd=1, tembusan=True, verifikasi="Mengetahui", tebal_inti=True),
]

# ------------------------------------------------------------- PENGUMUMAN
PENGUMUMAN = [
    T("peng_hasil_seleksi", "Pengumuman Hasil Seleksi",
      "Dua tabel: daftar seluruh peserta, lalu daftar yang lulus.",
      "Pengumuman",
      ["Dasar dan konteks seleksi", "Tabel daftar peserta",
       "Tabel daftar yang lulus", "Ucapan selamat dan penutup"],
      [F("kegiatan_seleksi", "Nama seleksi", "area",
         "Hasil Tes Wawancara Seleksi Tim Penulis Buku Pendidikan"),
       F("tgl_seleksi", "Tanggal pelaksanaan", "text", ""),
       F("jml_lulus", "Jumlah yang lulus", "text", "3 orang"),
       TABEL, F("tabel2", "Tabel kedua (yang lulus)", "area",
                "No | Nama | Tempat Tugas\n1 | ... | ...")],
      {"pembuka": "Berdasarkan hasil {kegiatan_seleksi} yang dilaksanakan pada "
                  "{tgl_seleksi} dengan peserta:",
       "penutup": "Demikianlah pengumuman ini kami sampaikan. Selamat kepada peserta yang "
                  "telah lulus. Terima kasih atas partisipasi dan kerjasama dari seluruh "
                  "peserta."},
      meta="judul", ttd=1, tabel=True, tanpa_tujuan=True),

    T("peng_perubahan_harga", "Pengumuman Perubahan Harga",
      "Blangko; daftar perubahan harga dari-menjadi.",
      "Surat Pengumuman Perubahan Harga Barang",
      ["Kalimat pembuka alasan perubahan", "Daftar perubahan harga bernomor",
       "Penjelasan peningkatan mutu", "Penutup"],
      [F("alasan", "Alasan perubahan", "area",
         "banyak beredarnya produk barang yang sama di pasaran luas"),
       F("daftar_harga", "Daftar harga (produk | dari | menjadi)", "area",
         "Produk A | Rp 10.000 | Rp 12.000"),
       F("mulai_berlaku", "Mulai berlaku", "text", "")],
      {"pembuka": "Sehubungan dengan {alasan}, maka terhitung sejak tanggal "
                  "dikeluarkannya pengumuman ini, produk kami mengalami perubahan harga. "
                  "Perubahan harga tersebut adalah sebagai berikut:",
       "penutup": "Perubahan harga ini diikuti dengan peningkatan mutu agar konsumen "
                  "semakin yakin dengan produk kami. Jika konsumen mendapatkan harga yang "
                  "tidak sesuai dengan label harga yang tertera dalam setiap kemasan, "
                  "diharap dapat melaporkannya kepada kami."},
      kop=False, meta="judul", ttd=1, blangko=True, tanpa_tujuan=True),
]

# ------------------------------------------------------------------- MEMO
MEMO = [
    T("memo_internal", "Memo Internal Perusahaan",
      "Header Tanggal/Dari/Kepada/Tembusan/Subyek; tabel; dua penandatangan.",
      "Internal Memo",
      ["Paragraf instruksi", "Tabel rincian", "Keterangan masa berlaku/review"],
      [F("dari", "Dari", "text", "Direksi PT ..."),
       F("kepada", "Kepada", "text", "Seluruh Staff"),
       F("tembusan_memo", "Tembusan", "text", "HRD, Semua Kepala Divisi"),
       F("subyek", "Subyek", "text", "Pemberitahuan Perubahan Jam Kerja"),
       F("mulai_berlaku", "Mulai berlaku", "text", ""),
       F("review", "Masa review", "text", "3 bulan ke depan"), TABEL],
      {"pembuka": "Dengan surat ini kami infokan perubahan {subyek} yang diberlakukan "
                  "mulai {mulai_berlaku} kepada setiap divisi untuk meningkatkan kinerja "
                  "yang lebih baik lagi:",
       "penutup": "Perubahan ini hanya sementara dan akan kami review ulang {review}."},
      meta="memo", ttd=2, ttd_label=["Komisaris", "Direktur"], tabel=True,
      tanpa_tujuan=True),
]

# --------------------------------------------------------------- PENGANTAR
PENGANTAR = [
    T("pengantar_keputusan", "Pengantar Penyampaian Keputusan",
      "Surat singkat pengantar penyampaian salinan keputusan; ada field Sifat.",
      "Penyampaian Keputusan",
      ["Rujukan keputusan yang disampaikan", "Permintaan tindak lanjut", "Penutup"],
      [F("keputusan", "Keputusan yang disampaikan (nomor, tanggal, tentang)", "area",
         "Keputusan Menteri Dalam Negeri Nomor ... tanggal ... tentang ..."),
       F("tindak_lanjut", "Tindak lanjut yang diminta", "area",
         "agar salinan keputusan tersebut disampaikan kepada masing-masing yang "
         "bersangkutan untuk dipergunakan sebagaimana mestinya")],
      {"pembuka": "Berkenaan dengan telah ditetapkannya {keputusan}, dengan hormat "
                  "diharapkan {tindak_lanjut}.",
       "penutup": "Demikian untuk menjadi maklum."},
      ttd=1, sifat=True, an=True),
]

# ------------------------------------------------------------ BERITA ACARA
BERITA_ACARA = [
    T("ba_rapat_bantuan", "Berita Acara Rapat/Musyawarah",
      "Musyawarah dengan perhitungan dana dan daftar barang; empat penandatangan.",
      "Berita Acara",
      ["Waktu dan tempat", "Pihak yang hadir", "Agenda musyawarah",
       "Perhitungan dana", "Hasil musyawarah", "Penutup"],
      ACARA + [F("agenda_ba", "Agenda musyawarah", "text",
                 "Sosialisasi Dana Bantuan Siswa Miskin (BSM)"),
               F("pihak", "Pihak yang hadir (satu per baris)", "area",
                 "Komite Sekolah\nOrang tua/wali siswa penerima\nTokoh masyarakat"),
               F("perhitungan", "Perhitungan dana", "area",
                 "100 siswa x Rp 180.000 = Rp 18.000.000"),
               F("hasil", "Hasil musyawarah (satu per baris)", "area", ""),
               F("daftar_barang", "Daftar barang (satu per baris)", "area",
                 "Baju Seragam\nBuku Tulis\nSepatu")],
      {"pembuka": "Pada hari ini, {hari_tgl}, bertempat di {tempat}, telah dilaksanakan "
                  "musyawarah tentang {agenda_ba} yang dihadiri oleh:",
       "penutup": "Demikian berita acara ini kami buat bersama dalam keadaan sehat jasmani "
                  "dan rohani tanpa ada paksaan dari pihak manapun untuk dipergunakan "
                  "sebagaimana mestinya."},
      meta="judul", ttd=4,
      ttd_label=["Mengetahui Kepala Sekolah", "Pengelola", "Kepala Desa", "Ketua Komite"]),
]
