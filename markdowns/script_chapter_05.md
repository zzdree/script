# BAB 5 PENUTUP

Bab ini memuat simpulan dan saran. Simpulan harus menjawab tiga rumusan masalah Bab 1 §1.3 dengan merujuk hasil Bab 4 yang benar-benar telah diperoleh. Draf ini masih berupa templat dan belum menyajikan hasil pengujian lapangan. Ganti setiap penanda **[BELUM DIISI]** hanya berdasarkan data terverifikasi dan keputusan metode yang disetujui.

## 5.1 Simpulan

Simpulan berikut belum dapat difinalisasi sebelum hasil pengujian pada Bab 4 tersedia.

### 5.1.1 Simpulan Rumusan Masalah Pertama

[ BELUM DIISI: simpulkan rancangan dan status implementasi sistem berdasarkan bukti pada Bab 4 §4.1.1. Laporkan hasil ekstraksi, verifikasi pengulangan, dan keluaran afektif hanya sejauh data terukur pada §4.1.2–§4.1.4 mendukungnya. Sebut keluaran RGBW sebagai nilai algoritmik, kecuali kanal fisik telah diverifikasi. Jangan menyatakan pemetaan deterministik atau sesuai secara empiris tanpa hasil uji. ]

### 5.1.2 Simpulan Rumusan Masalah Kedua

[ BELUM DIISI: simpulkan jalur integrasi yang benar-benar diverifikasi berdasarkan Bab 4 §4.2. Bedakan QLC+/*virtual adapter*, penerimaan ESP32, keluaran DMX512, dan respons lampu fisik. Jangan menyebut uji fisik berhasil jika bukti hanya berasal dari simulasi. Konfigurasi Alien AL36 dan pemetaan kanal tetap berstatus [VERIFIKASI LAPANGAN] sampai diverifikasi. ]

### 5.1.3 Simpulan Rumusan Masalah Ketiga

[ BELUM DIISI: rangkum temuan *black-box*, *packet loss*, kesesuaian pencahayaan, dan SUS dari Bab 4 §4.3.2–§4.3.6. Untuk H₁, simpulkan hanya setelah metode dan keputusan analisis yang disetujui menghasilkan dasar yang memadai. Untuk H₂, gunakan pembandingan deskriptif yang disetujui, bukan keputusan inferensial. Untuk H₃, rujuk §4.3.3 dan §4.4.3; jangan menyalin ulang angka latensi atau menyebut kriteria terpenuhi sebelum statistik pembanding disepakati. Jumlah 25 orang adalah target/rencana, bukan jumlah aktual, sampai rekrutmen selesai. ]

## 5.2 Saran

Saran final disusun setelah penulis membandingkan hasil aktual, keterbatasan pengukuran, dan pelaksanaan penelitian. Butir berikut merupakan templat arah tindak lanjut; pertahankan atau ubah hanya jika didukung temuan dan disetujui pembimbing.

### 5.2.1 Saran bagi Pengembangan Sistem

1. [BELUM DIISI: rekomendasikan perbaikan teknis hanya jika hasil terukur pada Bab 4 menunjukkan kebutuhan, misalnya pada jalur jaringan, kehilangan paket, atau uji fungsional.]  
2. [BELUM DIISI: jika keluaran algoritmik RGBW dan kanal fisik Alien AL36 tidak sepadan, dokumentasikan pemetaan yang sesuai profil terverifikasi atau gunakan fixture dengan kanal yang memenuhi kebutuhan penelitian.]  
3. [BELUM DIISI: rumuskan perbaikan penggunaan berdasarkan observasi atau tanggapan pengguna yang benar-benar tercatat.]  
4. [BELUM DIISI: usulkan pengukuran laju refresh DMX tersendiri hanya jika diperlukan; jangan menyamakan laju hop STFT 43,07 frame per detik dengan FPS DMX.] 

### 5.2.2 Saran bagi Penelitian Lanjutan

1. Penelitian lanjutan dapat menguji sistem pada jumlah dan variasi lagu yang lebih luas setelah lagu pada penelitian ini dipilih dan dilaporkan secara transparan.  
2. Penelitian lanjutan dapat melibatkan lokasi atau kelompok pengguna tambahan. Dasar pengembangan sampel disesuaikan dengan keterbatasan dan hasil rekrutmen aktual, bukan mengasumsikan bahwa target 25 responden telah tercapai.  
3. Pengujian lanjutan dapat memperluas evaluasi perangkat keras ke model fixture dan konfigurasi kanal lain setelah profil, pemetaan kanal, serta metode pengukuran fisik diverifikasi.  
4. Pengembangan metode analisis alternatif dapat dipertimbangkan sebagai pekerjaan terpisah; efektivitasnya perlu dibandingkan melalui rancangan dan data penelitian yang ditetapkan terlebih dahulu.  
5. [BELUM DIISI: tambahkan saran lain jika keterbatasan spesifik telah ditemukan dan didukung bukti pada Bab 4.]
