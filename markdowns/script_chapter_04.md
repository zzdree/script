# BAB 4 HASIL DAN PEMBAHASAN

Bab ini menyajikan hasil pengujian dan pembahasan sistem ZZLUXORA. Sebagian tabel telah terisi dengan bukti perangkat lunak yang terverifikasi; data pengujian lapangan, hasil pengukuran perangkat keras, dan tanggapan responden belum dimasukkan. Setiap penanda yang tersisa harus diganti hanya setelah bukti pengujian atau dokumen pendukung tersedia. Target sampel bukan jumlah responden aktual.

**Daftar penanda status yang dipakai pada Bab 4:**

| Penanda | Makna |
|---|---|
| **[TERVERIFIKASI SOFTWARE]** | Dibuktikan oleh pengujian unit dan/atau pengujian loopback pada perangkat lunak. Tidak melibatkan perangkat keras fisik. |
| **[VERIFIKASI LAPANGAN]** | Menunggu pengujian pada perangkat keras fisik di lokasi. |
| **[BELUM DIUKUR]** | Nilai numerik belum tersedia karena pengukuran belum dilakukan. |
| **[BELUM DIISI]** / **[BELUM DIPILIH]** | Sel belum diisi karena keputusan atau pemilihan belum ditetapkan. |
| **[BELUM DIUJI]** / **[BELUM DINILAI]** | Kasus uji belum dijalankan. |
| **[BELUM DIHITUNG]** | Statistik belum dihitung karena data sumber belum lengkap. |

Status **[TERVERIFIKASI SOFTWARE]** menyatakan kebenaran pada tataran perangkat lunak saja dan tidak boleh dibaca sebagai keberhasilan integrasi perangkat keras.

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
| 1 | Prapemrosesan dan STFT/FFT | Pemuatan multi-format; segmentasi frame geser $N=2048$, $H=512$; pembobotan Hann; transformasi FFT melalui `np.fft.rfft`; laju analisis $43{,}07$ frame per detik | Terverifikasi perangkat lunak: `tests/test_fft_engine.py` (3 uji) dan `tests/test_audio_loader.py` (3 uji). Bukti: commit `48ca2bd`, 74/74 uji lulus |
| 2 | Ekstraksi fitur akustik | RMS energy (Parseval), spectral centroid, Chroma 12-semitone, 13 MFCC (40 Mel + DCT-II), spectral flux, onset strength ternormalisasi, estimasi tempo autokorelasi FFT pada rentang $[50, 190]$ BPM | Terverifikasi perangkat lunak: `tests/test_feature_extractor.py` (9 uji). Bukti: commit `48ca2bd`, 74/74 uji lulus |
| 3 | Model *valence-arousal* dan pemetaan HSV | Bobot $V = 0{,}50/0{,}30/0{,}20$ (mode, centroid, MFCC); bobot $A = 0{,}50/0{,}30/0{,}20$ (RMS, tempo, onset); polaritas mode 12 transposisi Krumhansl-Schmuckler; pemetaan $(V,A) \to (H,S)$ melalui `atan2` dengan lantai saturasi $S \ge 0{,}2$ | Terverifikasi perangkat lunak: `tests/test_emotion_model.py` (2 uji); contoh perhitungan `script_math_model.md` [9] direproduksi langsung dari mesin pada masukan yang sama |
| 4 | Dekomposisi RGBW algoritmik serta generator *scene/chase* | Dekomposisi 4-kanal fisik $W=\min(R,G,B)$, $R'=R-W$, $G'=G-W$, $B'=B-W$; pembangkitan scene/chase berbasis segmen dan tempo | Terverifikasi perangkat lunak: `tests/test_color_engine.py` (2 uji). Bukti: commit `48ca2bd`, 74/74 uji lulus |
| 5 | Antarmuka dan pengirim Art-Net | Enam tab workspace; paket ArtDmx 530 byte (Universe 0, port 6454); transmisi ter-gate tombol Play; blackout atomik; antarmuka patch DMX | Terverifikasi perangkat lunak: `tests/test_ui_components.py` (40 uji) dan `tests/test_artnet_sender.py` (2 uji). Bukti: commit `48ca2bd`, 74/74 uji lulus |

Catatan: status "Terverifikasi perangkat lunak" menyatakan bahwa modul lulus pengujian unit dan pengujian pengulangan pada perangkat lunak, bukan bahwa modul telah divalidasi pada perangkat keras fisik. Validasi perangkat keras tetap berstatus **[VERIFIKASI LAPANGAN]** pada §4.2.

**Gambar 4.1** Diagram Arsitektur Implementasi Terverifikasi Rantai Pemrosesan Sinyal Audio ZZLUXORA v10, dari Modul AudioLoader hingga ArtNetSender, Disusun dari Berkas Nyata pada Direktori `core/`.

> Gambar 4.1 dibangkitkan secara terprogram oleh `tools/make_chapter4_figures.py` dari berkas yang benar-benar ada di repositori perangkat lunak, bukan digambar ulang sebagai ilustrasi. Karena itu gambar ini tidak dapat memuat modul atau parameter yang tidak ada di kode; bila kode berubah, gambar dibangkitkan ulang dan ikut berubah.

### 4.1.2 Hasil Ekstraksi Fitur Audio

Dengan parameter rancangan Bab 3, laju hop STFT dihitung sebesar $f_s/H = 22.050/512 \approx 43{,}07$ frame per detik. Nilai tersebut adalah laju pembaruan frame pada perhitungan STFT secara teoretis. Nilai itu tidak menunjukkan *frame rate* komputasi aktual dan tidak dapat digunakan untuk menyimpulkan laju *refresh* DMX. Laju aktual DMX, bila akan dilaporkan, memerlukan pengukuran tersendiri dan metode yang disetujui.

Protokol penelitian merencanakan pemilihan 3–5 lagu dari 10 berkas kandidat. **Sepuluh berkas kandidat yang tersedia saat ini bersifat sintetis**, dibangkitkan oleh `zzluxora_v10/tools/generate_benchmark_audio.py` (durasi seragam 12,00 detik, 22.050 Hz, mono), dan dipakai untuk pengujian perangkat lunak, bukan sebagai rekaman lagu rohani yang sesungguhnya. Materi sintetis ini tidak memadai untuk penilaian persepsi pengguna. Oleh karena itu, untuk keperluan H₁ dan sajian pada subbab ini, materi uji harus berupa rekaman lagu rohani nyata yang dipilih dan disetujui pembimbing; identitas serta izin pemakaian materi dicatat. Judul dan bagian lagu yang benar-benar dipakai masih perlu diverifikasi dan disetujui; daftar kandidat tidak berarti seluruh 10 lagu telah diuji. Hasil fitur hanya diisi untuk lagu yang akhirnya dipilih dan dianalisis. Tabel menyediakan lima slot; **hapus baris slot yang tidak dipakai setelah jumlah lagu final ditetapkan** (3, 4, atau 5 lagu).

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

**Tabel 4.4** Hasil Uji Pengulangan Keluaran Algoritmik

Uji dijalankan pada perangkat lunak dengan masukan dan setelan identik, sebanyak tiga pengulangan per berkas. Perbedaan keluaran diperiksa pada tiga ringkasan: jumlah frame, jumlah RMS, jumlah spectral centroid, dan RGBW frame pertama.

| No. | Berkas dan setelan masukan | Jumlah pengulangan | Perbedaan keluaran yang teramati | Bukti/log |
|---|---|---|---|---|
| 1 | `NDC_Worship_-_Bapa_Yang_Kekal.wav`, STFTEngine($f_s=22050$, $N=2048$, $H=512$), EmotionModel bobot bawaan | 3 | 0 (identik bit-for-bit; 513 frame; RMS 354,536054; centroid 136141,287305; RGBW frame pertama $(33,0,37,104)$) | `tools/export_correlation.py --repeats 3`, commit `48ca2bd` |
| 2 | Berkas lagu terpilih berikutnya | [BELUM DIISI setelah pemilihan lagu final] | [BELUM DIUKUR] | Perintah reproduksi sama seperti baris 1 |
| 3 | Berkas lagu terpilih berikutnya | [BELUM DIISI setelah pemilihan lagu final] | [BELUM DIUKUR] | Perintah reproduksi sama seperti baris 1 |

Uji keluaran algoritmik ini membuktikan bahwa pipeline pemrosesan bersifat deterministik pada masukan identik. Uji ini **bukan** pengukuran lapangan dan tidak menyatakan apa pun tentang respons lampu fisik.

**Tabel 4.5** Korelasi Fitur Audio dan Keluaran Algoritmik

| Fitur audio | Dimmer | R algoritmik | G algoritmik | B algoritmik | W algoritmik |
|---|---|---|---|---|---|
| BPM | tidak terdefinisi | tidak terdefinisi | tidak terdefinisi | tidak terdefinisi | tidak terdefinisi |
| RMS energy | tidak terdefinisi | $+0{,}163$ | $+0{,}289$ | $-0{,}946$ | $+0{,}992$ |
| *Spectral centroid* | tidak terdefinisi | $+0{,}274$ | $-0{,}503$ | $+0{,}236$ | $-0{,}160$ |

Nilai pada tabel ini dihitung dari keluaran perangkat lunak untuk berkas `NDC_Worship_-_Bapa_Yang_Kekal.wav` melalui `tools/export_correlation.py` (commit `48ca2bd`), dengan unit analisis satu frame STFT ($n = 513$ frame). Sel bertanda **tidak terdefinisi** dijelaskan sebagai berikut:

1. **BPM** merupakan nilai skalar per lagu, bukan nilai per frame. Korelasi Pearson antar-frame antara BPM dan kanal keluaran tidak bermakna karena vektor BPM konstan pada satu lagu. Bila korelasi BPM diperlukan, perhitungan harus dilakukan pada tingkat antarlagu (satu titik data per lagu), bukan antar-frame.
2. **Dimmer** pada keluaran `ColorRGBW` selalu bernilai $1{,}0$ (lihat `ColorEngine.process_frame`); kecerahan sesungguhnya dibawa oleh komponen Value pada ruang HSV, bukan oleh medan dimmer. Karena itu korelasinya terhadap fitur audio selalu tidak terdefinisi.

Korelasi terkuat yang teramati adalah antara RMS energy dan kanal putih algoritmik ($r = +0{,}992$) serta antara RMS energy dan kanal biru algoritmik ($r = -0{,}946$). Nilai ini menunjukkan hubungan matematis antara kenyaringan dan keluaran kanal, dan **tidak** menyatakan bahwa kanal putih atau biru telah diverifikasi pada lampu fisik. Tabel ini mengisi korelasi fitur audio terhadap kanal keluaran algoritmik; korelasi pada butir yang sama juga disebut pada Bab 3 sebagai metode yang direncanakan.

### 4.1.4 Keluaran Valence-Arousal, HSV, dan RGBW Algoritmik

Tabel 4.6 disediakan untuk menyajikan keluaran perangkat lunak berdasarkan segmen lagu yang dianalisis. Tabel menyediakan lima slot; **hapus baris slot yang tidak dipakai setelah jumlah lagu final ditetapkan**. Istilah **RGBW algoritmik** di sini merujuk pada empat nilai yang dihasilkan oleh model perangkat lunak. Nilai tersebut tidak membuktikan bahwa lampu fisik menghasilkan kanal putih terpisah.

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

**Tabel 4.7** Bukti Integrasi Sistem

| Jalur yang direncanakan | Titik yang perlu diverifikasi | Status aktual | Bukti/log |
|---|---|---|---|
| ZZLUXORA ke QLC+ melalui *virtual adapter*/loopback | Alamat tujuan, port, Universe, paket diterima dan perubahan kanal | Terverifikasi perangkat lunak (SITL loopback) | `tools/qlc_bridge_test.py --duration 5 --fixture alien` ke penerima UDP `127.0.0.1:6454`; 112 paket ArtDmx diterima, 105 nomor urut unik, urutan awal monotonik dari 1, blackout akhir mengembalikan seluruh kanal ke 0. Commit `48ca2bd` |
| ZZLUXORA ke ESP32 melalui Wi-Fi/*hotspot* | Alamat tujuan, koneksi, penerimaan paket di firmware | [BELUM DIUJI] | [BELUM DIISI] |
| ESP32 ke keluaran DMX512 melalui MAX485 | Sinyal DMX dan nilai kanal yang teramati | [BELUM DIUJI] | [BELUM DIISI] |
| Keluaran DMX ke setiap fixture fisik | Profil, mode kanal, alamat, perubahan cahaya dan blackout | [VERIFIKASI LAPANGAN] | [BELUM DIISI] |

Baris pertama hanya membuktikan jalur perangkat lunak ke penerima UDP pada mesin yang sama (*loopback*). Baris ini **tidak** membuktikan paket diterima ESP32, tidak membuktikan keluaran DMX512, dan tidak membuktikan lampu fisik merespons. Ketiga jalur tersebut berstatus belum diuji pada berkas ini.

Catatan teknis: pada sesi uji ini ditemukan bahwa berkas showfile GIA (`gia_deliksari_alien_4x.zlx`) masih menyimpan `target_ip` bernilai `127.0.0.1`, sehingga sebelum pengujian lapangan tujuan harus diubah ke alamat node aktual (misalnya SoftAP `192.168.4.1`) dan diverifikasi pada penerima, bukan diasumsikan.

Catatan pengukuran: perdana nomor urut ArtDmx pada sesi ini dimulai dari nilai 1, sesuai perbaikan pada `core/artnet_sender.py` (commit `7c566d9`). Sebelum perbaikan, penghitung dimulai dari 0, sementara nilai 0 pada medan Sequence Art-Net berarti "sequence disabled", sehingga paket pertama tidak valid. Pengujian lanjutan perlu memastikan tidak ada dua pengirim yang berbagi port/UDP yang sama dalam satu sesi, karena hal itu dapat menampilkan nomor urut yang tampak tidak monotonik pada penerima.

**Gambar 4.4** Topologi Jalur Pengukuran, Memisahkan Jalur Virtual *Software-in-the-Loop* yang Telah Terverifikasi Perangkat Lunak dari Jalur Fisik ESP32 dan Fixture yang Belum Diuji.

> Gambar 4.4 memisahkan kedua jalur secara visual agar batas bukti tidak terbaca ambigu: jalur A (kiri) memuat angka hasil pengujian loopback yang tercatat, sedangkan jalur B (kanan) memuat hal-hal yang masih harus diukur di lokasi. Tanda panah putus-putus pada jalur B menandai langkah yang belum diverifikasi. Gambar ini juga dibangkitkan oleh `tools/make_chapter4_figures.py`.

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

Baris mengikuti 24 kasus uji pada protokol pengujian (`script_test_protocols.md` §3, kode FB-01 s.d. FB-24). Kolom hasil dan status diisi hanya setelah kasus benar-benar dijalankan pada versi aplikasi/firmware yang dicatat.

| ID | Fitur/kasus uji | Hasil yang diharapkan | Hasil aktual | Status | Bukti |
|---|---|---|---|---|---|
| FB-01 | Peluncuran aplikasi | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-02 | Muat profil `.zfx` valid | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-03 | Profil `.zfx` tidak valid | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-04 | Patch satu fixture | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-05 | Patch cepat GIA 4x | [TETAPKAN SESUAI PROFIL YANG DIVERIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-06 | Undo/redo patch | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-07 | Muat audio valid | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-08 | Audio tidak didukung/rusak | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-09 | Analisis audio | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-10 | Validitas tampilan hasil | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-11 | Analisis ulang deterministik | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-12 | Ekspor ke Perform | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-13 | Muat showfile `.zlx` GIA | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-14 | Simpan dan muat ulang `.zlx` | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-15 | Perform GO+ | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-16 | Perform PREV | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-17 | Crossfade | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-18 | Page/executor | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-19 | Mixer kanal DMX | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-20 | Grand Master dan reset | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-21 | Play-gated dan Stop | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-22 | Blackout | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-23 | Loopback QLC+ | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |
| FB-24 | ESP32 dan empat fixture | [TETAPKAN SESUAI SPESIFIKASI] | [BELUM DIUJI] | [BELUM DINILAI] | [BELUM DIISI] |

**Tabel 4.12** Templat Rekapitulasi Hasil *Black-Box Testing*

Penyebut persentase Pass adalah jumlah kasus FB yang benar-benar dijalankan (maksimum 24), bukan jumlah kasus yang direncanakan. Kasus yang tidak dijalankan diberi status N/A beserta alasannya dan tidak dihitung sebagai Fail.

| Kelompok fitur | Jumlah kasus yang dijalankan | Pass | Fail | N/A beserta alasan | Persentase Pass |
|---|---:|---:|---:|---|---:|
| Aplikasi dan patch (FB-01 s.d. FB-06) | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIISI] | [BELUM DIHITUNG] |
| Audio dan hasil (FB-07 s.d. FB-12) | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIISI] | [BELUM DIHITUNG] |
| Showfile dan Perform (FB-13 s.d. FB-18) | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIISI] | [BELUM DIHITUNG] |
| Output dan jaringan (FB-19 s.d. FB-24) | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIISI] | [BELUM DIHITUNG] |
| Semua kasus yang dijalankan | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIHITUNG] | [BELUM DIISI] | [BELUM DIHITUNG] |

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
