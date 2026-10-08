# BAB 4 HASIL DAN PEMBAHASAN

Bab ini menyajikan hasil pengujian dan pembahasan sistem ZZLUXORA. Naskah yang tersedia masih berupa templat; data pengujian lapangan, hasil pengukuran, dan tanggapan responden belum dimasukkan. Setiap penanda **[BELUM DIUKUR]**, **[BELUM DIISI]**, dan **[VERIFIKASI LAPANGAN]** harus diganti hanya setelah bukti pengujian atau dokumen pendukung tersedia. Target sampel bukan jumlah responden aktual.

Pemetaan pembahasan mengikuti rumusan masalah pada Bab 1 §1.3 dan hipotesis pada Bab 3 §3.5. Rumusan masalah ketiga mencakup seluruh pengukuran teknis, persepsi kesesuaian pencahayaan, dan *usability*. Karena itu, latensi, *packet loss*, serta hasil *black-box* dibahas di §4.3, bukan ditempatkan sebagai hasil Rumusan Masalah Kedua. Tabel 4.1 merangkum pemetaan tersebut.

**Tabel 4.1** Pemetaan Rumusan Masalah dan Hipotesis ke dalam Bab 4

| Rumusan Masalah | Cakupan | Subbab hasil | Hipotesis terkait |
|---|---|---|---|
| 1. Perancangan sistem analisis audio STFT/FFT dan pemetaan otomatis ke parameter pencahayaan HSV-RGBW | Rancangan alur sistem, fitur audio, pemetaan afektif dan warna | 4.1 | Tidak ada hipotesis statistik khusus |
| 2. Integrasi keluaran ZZLUXORA dengan PAR LED melalui Art-Net DMX512, ESP32, dan jaringan nirkabel | Arsitektur integrasi serta verifikasi jalur perangkat lunak dan perangkat keras | 4.2 | Tidak ada hipotesis statistik khusus |
| 3. Kinerja sistem: aspek teknis (*end-to-end latency*, *packet loss*, *black-box*), kesesuaian pencahayaan, dan *usability* | Hasil teknis, validitas/reliabilitas instrumen, persepsi, dan SUS | 4.3 | H₁: kesesuaian; H₂: SUS; H₃: *latency*; pembahasan hipotesis dirujuk pada 4.4 |

## 4.1 Hasil Pengujian dan Pembahasan Rumusan Masalah Pertama

### 4.1.1 Rancangan dan Implementasi Sistem *Audio-Reactive Lighting Design*

Alur yang dirancang untuk ZZLUXORA mencakup pemuatan berkas audio, prapemrosesan, STFT berbasis FFT, ekstraksi fitur akustik, pemodelan *valence-arousal*, transformasi warna HSV, konversi ke RGB, dekomposisi nilai RGBW algoritmik, serta pembentukan *scene* dan *chase*. Uraian ini menjelaskan rancangan pada Bab 3, bukan pernyataan bahwa seluruh fungsi telah lolos pengujian. Status setiap modul dan bukti verifikasinya perlu dicatat pada Tabel 4.2.

**Tabel 4.2** Modul ZZLUXORA dan Bukti Verifikasi

| No. | Modul/tahap | Fungsi sesuai rancangan | Status implementasi dan bukti |
|---|---|---|---|
| 1 | Prapemrosesan dan STFT/FFT | [LENGKAPI BERDASARKAN IMPLEMENTASI] | [BELUM DIVERIFIKASI] |
| 2 | Ekstraksi fitur akustik | [LENGKAPI BERDASARKAN IMPLEMENTASI] | [BELUM DIVERIFIKASI] |
| 3 | Model *valence-arousal* dan pemetaan HSV | [LENGKAPI BERDASARKAN IMPLEMENTASI] | [BELUM DIVERIFIKASI] |
| 4 | Dekomposisi RGBW algoritmik serta generator *scene/chase* | [LENGKAPI BERDASARKAN IMPLEMENTASI] | [BELUM DIVERIFIKASI] |
| 5 | Antarmuka dan pengirim Art-Net | [LENGKAPI BERDASARKAN IMPLEMENTASI] | [BELUM DIVERIFIKASI] |

**Gambar 4.1** [BELUM DIISI: diagram arsitektur berdasarkan implementasi yang diverifikasi]

### 4.1.2 Hasil Ekstraksi Fitur Audio

Dengan parameter rancangan Bab 3, laju hop STFT dihitung sebesar $f_s/H = 22.050/512 \approx 43{,}07$ frame per detik. Nilai tersebut adalah laju pembaruan frame pada perhitungan STFT secara teoretis. Nilai itu tidak menunjukkan *frame rate* komputasi aktual dan tidak dapat digunakan untuk menyimpulkan laju *refresh* DMX. Laju aktual DMX, bila akan dilaporkan, memerlukan pengukuran tersendiri dan metode yang disetujui.

Protokol penelitian merencanakan pemilihan 3–5 lagu dari 10 berkas kandidat. Judul dan bagian lagu yang benar-benar dipakai masih perlu diverifikasi dan disetujui; daftar kandidat tidak berarti seluruh 10 lagu telah diuji. Hasil fitur hanya diisi untuk lagu yang akhirnya dipilih dan dianalisis.

**Tabel 4.3** Hasil Ekstraksi Fitur pada Lagu Terpilih

| No. lagu terpilih | Nama berkas/segmen | BPM | RMS rata-rata | *Spectral centroid* rata-rata (Hz) | Tonalitas/fitur terkait | *Onset strength* rata-rata |
|---|---|---|---|---|---|---|
| 1 | [BELUM DIPILIH] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] |
| 2 | [BELUM DIPILIH] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] |
| 3 | [BELUM DIPILIH] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] |
| 4 | [BELUM DIPILIH] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] |
| 5 | [BELUM DIPILIH] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] |

**Gambar 4.2** [BELUM DIISI: contoh visualisasi analisis dari lagu yang benar-benar dipilih]

### 4.1.3 Verifikasi Pemetaan Fitur Audio

Bab 3 merumuskan uji pengulangan untuk memeriksa apakah masukan dan setelan yang sama menghasilkan keluaran algoritmik yang sama. Rumusan tersebut menjelaskan metode yang direncanakan, bukan hasil uji deterministik yang telah diperoleh. Bab 3 juga menyebut korelasi Pearson antara fitur audio dan kanal keluaran. Nilai korelasi perlu dihitung dari data yang benar-benar direkam; korelasi tidak dengan sendirinya membuktikan ketepatan persepsi warna. Unit analisis dan agregasi data untuk korelasi perlu dijelaskan sebelum hasil ditafsirkan.

**Tabel 4.4** Templat Uji Pengulangan Keluaran Algoritmik

| No. | Berkas dan setelan masukan | Jumlah pengulangan | Perbedaan keluaran yang teramati | Bukti/log |
|---|---|---|---|---|
| 1 | [BELUM DIISI] | [BELUM DIUJI] | [BELUM DIUKUR] | [BELUM DIISI] |
| 2 | [BELUM DIISI] | [BELUM DIUJI] | [BELUM DIUKUR] | [BELUM DIISI] |
| 3 | [BELUM DIISI] | [BELUM DIUJI] | [BELUM DIUKUR] | [BELUM DIISI] |

**Tabel 4.5** Templat Korelasi Fitur Audio dan Keluaran Algoritmik

| Fitur audio | Dimmer | R algoritmik | G algoritmik | B algoritmik | W algoritmik |
|---|---|---|---|---|---|
| BPM | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] |
| RMS energy | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] |
| *Spectral centroid* | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] |

### 4.1.4 Keluaran Valence-Arousal, HSV, dan RGBW Algoritmik

Tabel 4.6 disediakan untuk menyajikan keluaran perangkat lunak berdasarkan segmen lagu yang dianalisis. Istilah **RGBW algoritmik** di sini merujuk pada empat nilai yang dihasilkan oleh model perangkat lunak. Nilai tersebut tidak membuktikan bahwa lampu fisik menghasilkan kanal putih terpisah.

Profil Alien AL36 yang dicantumkan pada dokumen penelitian memiliki delapan kanal: dimmer, R, G, B, kanal kosong, program, speed, dan kanal kosong; profil itu tidak mencantumkan kanal putih khusus. Kesesuaian model, mode kanal pada unit fisik, serta pemetaan nilai W algoritmik ke fixture harus ditetapkan melalui **[VERIFIKASI LAPANGAN]**. Sebelum verifikasi dan pengujian optik dilakukan, naskah tidak menyatakan bahwa keluaran RGBW fisik telah diuji.

**Tabel 4.6** Templat Keluaran Afektif dan Pemetaan Warna per Lagu Terpilih

| No. lagu terpilih | Berkas/segmen | Rata-rata V | Rata-rata A | Kuadran/HSV | RGBW algoritmik | Pemetaan ke kanal Alien AL36 |
|---|---|---|---|---|---|---|
| 1 | [BELUM DIPILIH] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [VERIFIKASI LAPANGAN] |
| 2 | [BELUM DIPILIH] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [VERIFIKASI LAPANGAN] |
| 3 | [BELUM DIPILIH] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [VERIFIKASI LAPANGAN] |
| 4 | [BELUM DIPILIH] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [VERIFIKASI LAPANGAN] |
| 5 | [BELUM DIPILIH] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [VERIFIKASI LAPANGAN] |

**Gambar 4.3** [BELUM DIISI: visualisasi koordinat V-A dari data analisis yang tersimpan]

### 4.1.5 Pembahasan Rumusan Masalah Pertama

[ BELUM DIISI SETELAH DATA TERSEDIA: bahas bukti implementasi, hasil ekstraksi, hasil uji pengulangan, korelasi, dan keluaran afektif. Bedakan keluaran algoritmik dengan pengamatan lampu fisik. Jangan menyatakan konsistensi atau kesesuaian empiris sebelum tabel terkait terisi dan diverifikasi. ]

## 4.2 Hasil Pengujian dan Pembahasan Rumusan Masalah Kedua

### 4.2.1 Integrasi ZZLUXORA, Art-Net, dan ESP32

Rancangan integrasi menghubungkan keluaran aplikasi ke tujuan Art-Net melalui jaringan, kemudian ke penerima ESP32 dan antarmuka DMX512. Jalur virtual ke QLC+ dan jalur menuju perangkat keras merupakan kondisi pengujian yang berbeda. Hasil pada QLC+ hanya menjadi bukti jalur simulasi yang benar-benar diamati; hasil tersebut tidak membuktikan paket diterima ESP32 atau lampu fisik merespons.

**Tabel 4.7** Templat Bukti Integrasi Sistem

| Jalur yang direncanakan | Titik yang perlu diverifikasi | Status aktual | Bukti/log |
|---|---|---|---|
| ZZLUXORA ke QLC+ melalui *virtual adapter*/loopback | Alamat tujuan, port, Universe, paket diterima dan perubahan kanal | [BELUM DIUJI] | [BELUM DIISI] |
| ZZLUXORA ke ESP32 melalui Wi-Fi/*hotspot* | Alamat tujuan, koneksi, penerimaan paket di firmware | [BELUM DIUJI] | [BELUM DIISI] |
| ESP32 ke keluaran DMX512 melalui MAX485 | Sinyal DMX dan nilai kanal yang teramati | [BELUM DIUJI] | [BELUM DIISI] |
| Keluaran DMX ke setiap fixture fisik | Profil, mode kanal, alamat, perubahan cahaya dan blackout | [VERIFIKASI LAPANGAN] | [BELUM DIISI] |

**Gambar 4.4** [BELUM DIISI: topologi jalur yang benar-benar digunakan, tandai jalur virtual dan fisik secara terpisah]

### 4.2.2 Profil Fixture dan Batas Keluaran Fisik

Pengujian integrasi perlu mencatat model dan mode kanal setiap fixture, alamat DMX, Universe, serta hasil pengujian kanal per unit. Untuk Alien AL36, profil yang tersedia menunjukkan kanal dimmer/R/G/B serta kanal kosong, program, dan speed, tanpa kanal putih khusus. Oleh sebab itu, penyebutan RGBW pada keluaran algoritmik tidak boleh disamakan dengan penerimaan empat kanal RGBW oleh unit Alien AL36. Konfigurasi aktual, pemetaan kanal dan respons optik setiap fixture berstatus **[VERIFIKASI LAPANGAN]** sampai ada catatan inspeksi dan bukti uji.

**Tabel 4.8** Templat Verifikasi Profil dan Keluaran Fixture

| Unit/identitas fixture | Model dan mode kanal aktual | Alamat/Universe | Kanal yang diuji | Respons aktual per kanal | Bukti |
|---|---|---|---|---|---|
| 1 | [VERIFIKASI LAPANGAN] | [BELUM DIISI] | [BELUM DIUJI] | [BELUM DIUJI] | [BELUM DIISI] |
| 2 | [VERIFIKASI LAPANGAN] | [BELUM DIISI] | [BELUM DIUJI] | [BELUM DIUJI] | [BELUM DIISI] |
| 3 | [VERIFIKASI LAPANGAN] | [BELUM DIISI] | [BELUM DIUJI] | [BELUM DIUJI] | [BELUM DIISI] |
| 4 | [VERIFIKASI LAPANGAN] | [BELUM DIISI] | [BELUM DIUJI] | [BELUM DIUJI] | [BELUM DIISI] |

### 4.2.3 Pembahasan Rumusan Masalah Kedua

[ BELUM DIISI SETELAH VERIFIKASI: jelaskan tingkat integrasi yang benar-benar dibuktikan dan batasnya. Pisahkan bukti simulasi, penerimaan ESP32, keluaran DMX, serta respons fixture. Jangan menyatakan integrasi fisik berhasil hanya dari status pada aplikasi atau hasil QLC+. ]

## 4.3 Hasil Pengujian dan Pembahasan Rumusan Masalah Ketiga

Rumusan masalah ketiga mencakup bukti kinerja teknis dan evaluasi pengguna. Bagian ini menampung hasil uji instrumen, *black-box*, latensi, *packet loss*, kesesuaian pencahayaan, dan SUS. Semua hasil tetap berupa templat sampai data mentah, prosedur, serta bukti pendukung tersedia.

### 4.3.1 Validitas Konten dan Reliabilitas Instrumen

Bab 3 merencanakan penelaahan validitas konten oleh dosen pembimbing dan penghitungan Cronbach's Alpha dengan acuan α ≥ 0,6. Nilai validitas dan reliabilitas belum tersedia untuk diisikan. Reliabilitas SUS dan instrumen kesesuaian pencahayaan dilaporkan terpisah karena keduanya mengukur konstruk yang berbeda.

**Tabel 4.9** Templat Hasil Penelaahan Validitas Konten

| Instrumen/versi | Penelaah | Aspek yang ditelaah | Catatan/revisi berdasarkan bukti | Status dan tanggal persetujuan |
|---|---|---|---|---|
| SUS | [BELUM DIISI] | [BELUM DIISI] | [BELUM DIISI] | [BELUM DIVERIFIKASI] |
| Kesesuaian pencahayaan | [BELUM DIISI] | [BELUM DIISI] | [BELUM DIISI] | [BELUM DIVERIFIKASI] |

**Tabel 4.10** Templat Hasil Reliabilitas Instrumen

| Instrumen/konstruk | N aktual | Jumlah butir | Aturan pengodean/agregasi | Cronbach's Alpha | Acuan Bab 3 | Interpretasi setelah persetujuan |
|---|---:|---:|---|---:|---|---|
| SUS | [BELUM DIUKUR] | 10 | [BELUM DITETAPKAN] | [BELUM DIHITUNG] | α ≥ 0,6 | [BELUM DITAFSIRKAN] |
| Kesesuaian pencahayaan | [BELUM DIUKUR] | 6 | [PERLU PERSETUJUAN DOSEN PEMBIMBING: tetapkan unit analisis dan cara menangani penilaian berulang untuk 3–5 lagu] | [BELUM DIHITUNG] | α ≥ 0,6 | [BELUM DITAFSIRKAN] |

[PERLU PERSETUJUAN DOSEN PEMBIMBING: pastikan versi instrumen, pengodean butir, unit analisis, dan agregasi rating kesesuaian lintas lagu sebelum menghitung atau menafsirkan koefisien reliabilitas.]

### 4.3.2 Hasil Uji Fungsional *Black-Box*

Bab 3 menetapkan penyajian *black-box testing* secara deskriptif berdasarkan *test case*, hasil yang diharapkan, hasil aktual, dan status Pass/Fail. Tabel 4.11 dan 4.12 merupakan templat pencatatan, bukan laporan uji yang sudah dilaksanakan. Cantumkan kasus yang benar-benar dijalankan beserta versi perangkat lunak/firmware dan bukti uji.

**Tabel 4.11** Templat Hasil *Black-Box Testing*

| No. | Fitur/kasus uji | Hasil yang diharapkan | Hasil aktual | Status | Bukti |
|---|---|---|---|---|---|
| 1 | Pemuatan berkas audio dan penanganan input | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| 2 | Analisis audio dan keluaran algoritmik | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| 3 | Pengiriman Art-Net ke QLC+ | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| 4 | Pengiriman Art-Net ke ESP32 | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| 5 | Konfigurasi fixture dan kanal | [TETAPKAN SESUAI PROFIL YANG DIVERIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| 6 | Konektivitas ESP32/Wi-Fi/*captive portal* | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |

**Tabel 4.12** Templat Rekapitulasi Hasil *Black-Box Testing*

| Kelompok fitur | Jumlah kasus yang dijalankan | Pass | Fail | N/A beserta alasan | Persentase Pass |
|---|---:|---:|---:|---|---:|
| Semua kasus yang dilaporkan | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIISI] | [BELUM DIHITUNG] |

Persentase Pass dihitung mengikuti rumus pada Bab 3 §3.9.1.b dan penyebutnya harus konsisten dengan kasus yang benar-benar dijalankan. Laporkan kasus N/A beserta alasannya; jangan memberi status Pass berdasarkan spesifikasi saja.

### 4.3.3 Hasil Pengukuran *End-to-End Latency* dan *Packet Loss*

Bab 3 menggunakan ambang $<100$ ms untuk H₃ dan meminta statistik deskriptif latensi. Dalam templat ini, 100 ms disebut **kriteria penerimaan penelitian yang direncanakan**, bukan standar *real-time* universal. Definisi operasional Bab 3 merujuk waktu pengiriman paket hingga lampu merespons. Pengukuran hanya dapat dilaporkan sebagai *end-to-end* bila titik awal dan respons lampu terukur dengan metode yang dapat dipertanggungjawabkan; keterbatasan alat dan sinkronisasi waktu harus dicatat.

Latensi diukur dan dicatat pada bagian ini saja. Pembahasan H₃ di §4.4.3 merujuk ke hasil pada §4.3.3 tanpa menyalin nilai pengukuran. Jika pengukuran yang sah tidak dapat dilakukan, tulis **tidak terukur** dan jangan menyimpulkan H₃.

**Tabel 4.13** Templat Statistik Deskriptif *End-to-End Latency*

| Kondisi uji | Metode/titik ukur dan bukti | n valid | Rata-rata (ms) | Simpangan baku (ms) | Minimum (ms) | Maksimum (ms) | Perbandingan deskriptif dengan 100 ms |
|---|---|---:|---:|---:|---:|---:|---|
| [BELUM DIISI] | [BELUM DIVERIFIKASI] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DIUKUR] | [BELUM DITAFSIRKAN] |

[PERLU PERSETUJUAN DOSEN PEMBIMBING: Bab 3 mencantumkan statistik deskriptif dan ambang, tetapi belum menetapkan statistik utama untuk mengoperasionalkan H₃. Tetapkan aturan interpretasi sebelum menyimpulkan dan sebelum melihat hasil. Interval kepercayaan tidak ditetapkan di Bab 3; jangan menambahkan atau menafsirkannya sebagai metode yang telah disetujui.]

**Tabel 4.14** Templat Rekapitulasi *Packet Loss*

| Kondisi/sesi | Durasi dan laju kirim | Paket unik terkirim | Paket valid diterima | *Packet loss* terukur (%) | Bukti penerimaan di ESP32 |
|---|---|---:|---:|---:|---|
| [BELUM DIISI] | [BELUM DIISI] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIISI] |

Bab 3 tidak menetapkan ambang lulus untuk *packet loss*. Laporkan jumlah paket, metode pencatatan pada penerima, durasi, dan kondisi pengujian. Jika paket valid yang diterima firmware tidak dapat diamati, nyatakan metrik sebagai **tidak terukur**, bukan nol.

### 4.3.4 Target Rekrutmen dan Karakteristik Responden

Bab 3 merencanakan sampel 25 orang dari jemaat/*Youth* GIA Deliksari. Jumlah tersebut merupakan target/rencana yang perlu dikonfirmasi, bukan jumlah peserta aktual. Isi tabel setelah perekrutan, persetujuan partisipasi, dan pengumpulan data dilakukan. Laporkan jumlah aktual serta karakteristik anonim sesuai data yang benar-benar diperoleh.

**Tabel 4.15** Templat Karakteristik Responden

| Karakteristik | Kategori | Jumlah aktual | Persentase |
|---|---|---:|---:|
| Jumlah responden yang direkrut | Target Bab 3: 25; target perlu dikonfirmasi | [BELUM DIHITUNG] | [BELUM DIHITUNG] |
| Peran | [TETAPKAN SESUAI DATA DAN KRITERIA YANG DISETUJUI] | [BELUM DIHITUNG] | [BELUM DIHITUNG] |
| Usia | [KATEGORI SESUAI DATA DAN PERSETUJUAN ETIK] | [BELUM DIHITUNG] | [BELUM DIHITUNG] |

### 4.3.5 Hasil Penilaian Kesesuaian Pencahayaan

Kuesioner Bab 3 memuat enam butir skala Likert 1–5 untuk setiap lagu yang diamati. Protokol merencanakan pemilihan 3–5 lagu dari 10 kandidat; pilihan akhir masih **[BELUM DIPILIH]**. Baris berikut menunjukkan slot lagu terpilih 1–5, bukan bukti bahwa lima lagu atau sepuluh kandidat telah digunakan. Hapus slot yang tidak dipakai setelah pilihan final ditetapkan.

**Tabel 4.16** Templat Skor Kesesuaian Pencahayaan per Lagu Terpilih

| No. lagu terpilih | Judul/segmen terverifikasi | Jumlah penilaian valid | Rata-rata skor | Simpangan baku |
|---|---|---:|---:|---:|
| 1 | [BELUM DIPILIH] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] |
| 2 | [BELUM DIPILIH] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] |
| 3 | [BELUM DIPILIH] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] |
| 4 | [BELUM DIPILIH] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] |
| 5 | [BELUM DIPILIH] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] |

**Tabel 4.17** Templat Rata-rata Skor per Butir Kesesuaian

| No. | Pernyataan sesuai instrumen | Rata-rata skor |
|---|---|---:|
| 1 | Warna pencahayaan sesuai dengan karakter lagu ini. | [BELUM DIHITUNG] |
| 2 | Tingkat kecerahan (*brightness*) pencahayaan sesuai dengan energi lagu. | [BELUM DIHITUNG] |
| 3 | Perpindahan/transisi antar-*scene* terasa halus dan sesuai dengan ritme lagu. | [BELUM DIHITUNG] |
| 4 | Pencahayaan yang dihasilkan mendukung suasana ibadah saat lagu ini dimainkan. | [BELUM DIHITUNG] |
| 5 | Dinamika pencahayaan (perubahan warna dan *brightness*) mengikuti perubahan ritme dan energi lagu. | [BELUM DIHITUNG] |
| 6 | Secara keseluruhan, pencahayaan ini cocok untuk lagu rohani yang sedang dimainkan. | [BELUM DIHITUNG] |

[PERLU PERSETUJUAN DOSEN PEMBIMBING: Bab 3 menyebut penghitungan rata-rata dari seluruh responden dan seluruh lagu serta *one-sample t-test* terhadap 3,0, tetapi belum menjelaskan unit analisis dan perlakuan terhadap pengukuran berulang per responden/per lagu. Tetapkan aturan agregasi enam butir dan beberapa lagu sebelum uji H₁.]

### 4.3.6 Hasil *System Usability Scale* (SUS)

SUS dihitung per responden menurut rumus yang dijelaskan pada Bab 3 §3.9.2.a. Tabel 4.18 adalah templat statistik deskriptif. Isi jumlah peserta valid dan skor dari formulir aktual; angka 25 tetap berstatus target sampai perekrutan selesai. Perbandingan terhadap 68 disajikan secara deskriptif, tanpa uji inferensial H₂ yang tidak ditetapkan pada Bab 3.

**Tabel 4.18** Templat Statistik Deskriptif Skor SUS

| Statistik | Hasil aktual |
|---|---:|
| Responden dengan data SUS valid | [BELUM DIHITUNG] |
| Rata-rata skor SUS | [BELUM DIHITUNG] |
| Simpangan baku | [BELUM DIHITUNG] |
| Minimum | [BELUM DIHITUNG] |
| Maksimum | [BELUM DIHITUNG] |
| Acuan pembanding Bab 3 | 68 |
| Selisih rata-rata terhadap acuan, setelah agregasi disetujui | [BELUM DIHITUNG] |

[PERLU PERSETUJUAN DOSEN PEMBIMBING: tetapkan agregasi skor responden untuk H₂ dan putuskan apakah interval kepercayaan akan dilaporkan. Bab 3 tidak menetapkan metode inferensial maupun interval kepercayaan untuk H₂. Kategori SUS juga perlu aturan batas yang tidak tumpang tindih sebelum dilaporkan, karena rentang pada Bab 3 menempatkan skor 68 pada lebih dari satu kategori.]

### 4.3.7 Pembahasan Rumusan Masalah Ketiga

[ BELUM DIISI SETELAH DATA TERSEDIA: interpretasikan hasil *black-box*, latensi dan *packet loss* dengan batas bukti yang dicatat, lalu bahas skor kesesuaian dan SUS. Bedakan pembandingan deskriptif terhadap kriteria yang direncanakan dari uji inferensial. Jangan menyatakan keberhasilan atau signifikansi tanpa dasar metode dan hasil yang disetujui. ]

## 4.4 Pembahasan Hipotesis Penelitian

Pembahasan hipotesis menunggu data yang valid dan keputusan analisis yang diperlukan. Bab 3 menyebut *one-sample t-test* untuk H₁, tetapi belum menetapkan alpha, unit analisis, dan pengolahan rating berulang. Bab 3 tidak menetapkan uji inferensial untuk H₂ atau H₃. Karena itu, bagian ini tidak menggunakan *p-value* atau keputusan “H₀ diterima/ditolak” untuk mengisi kekosongan metode.

### 4.4.1 Hipotesis 1: Kesesuaian Pencahayaan

H₀ dan H₁ dirumuskan pada Bab 3 §3.5. Metode *one-sample t-test* terhadap nilai 3,0 disebut pada Bab 3 §3.9.2.b. Sebelum menjalankannya, perlu persetujuan atas alpha, unit analisis, dan agregasi enam butir lintas responden serta 3–5 lagu. Sampai keputusan dan data tersedia, tidak ada *p-value* atau keputusan hipotesis yang dapat dilaporkan.

[PERLU PERSETUJUAN DOSEN PEMBIMBING: tetapkan alpha, unit analisis, agregasi rating berulang, serta aturan pelaporan/interpretasi sebelum uji H₁.]

### 4.4.2 Hipotesis 2: *Usability* Sistem

H₂ membandingkan skor SUS dengan acuan 68 sebagaimana dirumuskan pada Bab 3 §3.5. Hasil deskriptif yang relevan berada pada §4.3.6. Bab 3 tidak menetapkan uji inferensial atau interval kepercayaan untuk H₂; oleh sebab itu bagian ini tidak menambahkan uji, *p-value*, atau keputusan menerima/menolak hipotesis.

[PERLU PERSETUJUAN DOSEN PEMBIMBING: konfirmasi unit/agregasi skor SUS untuk pembandingan deskriptif dan apakah interval kepercayaan akan digunakan.]

### 4.4.3 Hipotesis 3: *End-to-End Latency*

H₃ dirumuskan dengan kriteria $<100$ ms pada Bab 3 §3.5. Hasil ukur dan statistik deskriptif dicatat hanya pada §4.3.3. Bagian ini merujuk ke §4.3.3 tanpa mengulang angka latensi. Bab 3 belum memilih statistik utama untuk menyimpulkan H₃ atau menetapkan interval kepercayaan; jangan menyebut H₃ terpenuhi/tidak terpenuhi sebelum aturan tersebut disetujui dan hasil ukur valid tersedia.

[PERLU PERSETUJUAN DOSEN PEMBIMBING: tetapkan statistik utama/aturan deskriptif untuk membandingkan H₃ dengan 100 ms; Bab 3 tidak menetapkan interval kepercayaan.]
