# BAB 3 METODE PENELITIAN

## 3.1 Pendekatan, Jenis, dan Prosedur Penelitian

### 3.1.1 Pendekatan Penelitian

Penelitian ini menggunakan pendekatan kuantitatif, yaitu pendekatan yang menekankan pada pengumpulan dan analisis data berupa angka-angka untuk menguji hipotesis dan mengukur variabel penelitian secara objektif. Data kuantitatif yang dikumpulkan meliputi nilai-nilai fitur audio (BPM, *RMS*, *spectral centroid*), nilai *output* RGBW, waktu *latency*, skor *usability* (SUS), dan skor kesesuaian pencahayaan.

### 3.1.2 Jenis Penelitian

Jenis penelitian ini adalah *Research and Development* (R&D), yaitu penelitian yang bertujuan untuk menghasilkan produk tertentu dan menguji efektivitas produk tersebut. Produk yang dihasilkan dalam penelitian ini berupa:
1. Perangkat lunak ZZLUXORA (*audio-reactive lighting design application*).
2. Modul *hardware* ARTNET-DMX berbasis ESP32.
3. Model matematis pemetaan fitur audio ke RGBW berbasis HSV.

### 3.1.3 Prosedur Penelitian

Prosedur penelitian mengikuti tahapan pengembangan sistem sebagai berikut:

1. **Studi Literatur dan Analisis Kebutuhan:** Kajian pustaka, identifikasi kebutuhan sistem, dan perancangan arsitektur.
2. **Perancangan Model Matematis:** Formulasi model pemetaan fitur audio → *Valence-Arousal* → HSV → RGBW beserta tabel *rule-based mapping* eksplisit.
3. **Pengembangan Perangkat Lunak:** Implementasi aplikasi ZZLUXORA meliputi modul analisis audio, *scene/chase generator*, dan *Art-Net sender*.
4. **Pengembangan Perangkat Keras:** Implementasi modul ARTNET-DMX (ESP32 + MAX485 + LCD I2C).
5. **Integrasi Sistem:** Pengujian konektivitas ZZLUXORA ↔ QLC+ ↔ ESP32 ↔ PAR LED.
6. **Pengujian dan Evaluasi:** Pengujian fungsional, performa, dan persepsi pengguna.
7. **Analisis Data dan Pelaporan:** Analisis statistik hasil pengujian dan penyusunan laporan.

**Alur Program ZZLUXORA (Pipeline Komputasi Audio-ke-DMX):**

```
START
  │
  ├── User memilih file audio lagu rohani (.mp3 / .wav)
  │
  ├── User mengatur konfigurasi fixture DMX
  │   (profil lampu PAR LED, start channel, posisi X/Y panggung)
  │
  ├── Klik tombol "Analyze" (Eksekusi Audio Processing Core)
  │   │
  │   ├── [1] Preprocessing Audio:
  │   │   ├── Resampling ke laju standar fs = 22.050 Hz (Nyquist = 11.025 Hz)
  │   │   └── Downmixing kanal stereo ke mono float32 [-1.0, 1.0]
  │   │
  │   ├── [2] Transformasi Domain Waktu-ke-Frekuensi:
  │   │   ├── Segmentasi frame geser: Window Size N = 2048, Hop Length H = 512 (overlap 75%)
  │   │   ├── Pembobotan Hann Window w[n] = 0.5 * (1 - cos(2*pi*n / (N-1))) (redam leakage -31.5 dB)
  │   │   └── Fast Fourier Transform (FFT Radix-2 DIT) menghasilkan matriks X[m, k] (1025 bin x M frame)
  │   │   └── Laju pembaruan frame visual: 22050 / 512 = 43.07 FPS (sinkron standar DMX512 44 FPS)
  │   │
  │   ├── [3] Ekstraksi Fitur Akustik Spektral:
  │   │   ├── RMS Energy (Parseval's theorem): Pengukur kenyaringan dinamika lagu
  │   │   ├── Spectral Centroid: Titik pusat massa frekuensi sum(f_k * |X|) / sum(|X|) (timbre brightness)
  │   │   ├── Chroma STFT (12 semitone C s.d. B via modulo 12): Tonalitas harmoni Mayor vs Minor
  │   │   ├── MFCC (13 koefisien via 40 Mel filterbanks + DCT-II): Tekstur timbre instrumen/vokal
  │   │   └── Onset Strength & Beat Tracking: Deteksi transient ketukan dan estimasi BPM tempo
  │   │
  │   ├── [4] Pemodelan Afektif Russell (Valence-Arousal 2D Plane):
  │   │   ├── Valence (V) in [-1.0, +1.0]: f(Chroma Major/Minor Ratio, Centroid_norm, MFCC)
  │   │   └── Arousal (A) in [-1.0, +1.0]: f(RMS_norm, Tempo_BPM, Onset_Strength)
  │   │
  │   ├── [5] Transformasi Ruang Warna Cross-Modal (HSV -> RGB -> RGBW):
  │   │   ├── Hue H = (atan2(A, V) * 180 / pi + 360) mod 360 (0° - 360°)
  │   │   ├── Saturation S = sqrt(V^2 + A^2) / sqrt(2) (0.0 - 1.0)
  │   │   ├── Dimmer Value = RMS_norm * Master_Fader (0.0 - 1.0)
  │   │   ├── HSV -> Standard sRGB (0 - 255)
  │   │   └── Dekomposisi 4-Kanal Physical RGBW: W = min(R,G,B), R'=R-W, G'=G-W, B'=B-W
  │   │
  │   └── [6] Pembangkitan Scene & Chase:
  │       ├── Pengelompokan segmen struktural (Verse, Chorus, Bridge)
  │       └── Penerapan aturan transisi fade & hold time berbasis BPM
  │
  ├── Tampilkan Hasil Analisis di Antarmuka
  │   ├── Visualizer 2D PAR LED tampak depan (real-time color preview)
  │   ├── Grafik Spektrogram FFT, Centroid, dan VU RMS Meter
  │   ├── Koordinat 2D Valence-Arousal Plane
  │   └── Tabel Fader Mixer 513 Slider (Master + 512 DMX channels)
  │
  ├── Transmisi Paket Art-Net 4 (UDP Port 6454)
  │   ├── Format paket biner ArtDmx 530 byte (Universe 0)
  │   ├── Opsi IP Target: Localhost 127.0.0.1, AP ESP32 192.168.4.1, atau Custom IP
  │   └── Tombol instan Blackout (reset fader ke 0)
  │
END
```

**Alur Program Modul ARTNET-DMX (ESP32):**

```
START
  │
  ├── Inisialisasi Hardware (LCD, MAX485, Serial2)
  │
  ├── Baca kredensial WiFi dari memori (Preferences)
  │
  ├── Kredensial ada?
  │   ├── Ya → Hubungkan ke WiFi → Berhasil?
  │   │       ├── Ya → Mode RUN (Art-Net Receiver aktif)
  │   │       └── Tidak → Mode AP (Captive Portal)
  │   └── Tidak → Mode AP (Captive Portal)
  │
  ├── Mode AP:
  │   ├── Buat hotspot "ARTNET-DMX"
  │   ├── DNS hijack → Captive Portal
  │   ├── WebServer: Setup page (scan WiFi, input SSID/pass)
  │   ├── Art-Net Receiver tetap aktif
  │   └── Simpan kredensial → Reboot
  │
  ├── Mode RUN:
  │   ├── Art-Net Receiver (UDP port 6454)
  │   │   ├── Parse packet Art-Net
  │   │   ├── Filter universe 0
  │   │   └── Update data DMX
  │   │
  │   ├── DMX Output Task:
  │   │   ├── Sinkronisasi data (buffer management)
  │   │   ├── Kirim BREAK + START CODE + 512 byte DMX
  │   │   ├── Auto-blackout jika no signal >10s
  │   │   └── Refresh rate sesuai standar DMX
  │   │
  │   ├── Auto-Reconnect WiFi:
  │   │   ├── Disconnect <30s → Reconnect
  │   │   └── Disconnect >30s → Reset + Reboot
  │   │
  │   └── WebServer: Monitor page (status real-time)
  │
END
```

---

## 3.2 Lokasi dan Waktu Penelitian

### 3.2.1 Lokasi Penelitian

Penelitian ini dilaksanakan di dua lokasi:

1. **Laboratorium Pribadi (Pengembangan dan Pengujian Awal):**
   - Alamat: Kontrakan Anugerah, Kelurahan Ngijo, Kecamatan Gunungpati, Kota Semarang.
   - Kegiatan: Pengembangan perangkat lunak, perakitan modul *hardware*, dan pengujian teknis awal.

2. **Lokasi Pengujian Lapangan:**
   - Alamat: Gereja GIA Deliksari, Semarang.
   - Kegiatan: Pengujian sistem secara *end-to-end* dengan lampu PAR LED RGBW, pengambilan data responden, dan evaluasi kesesuaian pencahayaan dalam konteks ibadah.

### 3.2.2 Waktu Penelitian

Penelitian ini direncanakan dilaksanakan pada bulan Juni 2026, dengan rincian waktu sebagai berikut:

| Minggu | Kegiatan |
|--------|----------|
| Minggu 1 | Finalisasi perangkat lunak dan integrasi sistem |
| Minggu 2 | Instalasi dan pengujian di Gereja GIA Deliksari |
| Minggu 3 | Pengambilan data responden (kuesioner dan observasi) |
| Minggu 4 | Analisis data dan penyusunan laporan |

---

## 3.3 Subjek Penelitian / Sampel

Subjek penelitian ini adalah 25 orang responden yang terdiri dari anggota *Youth* (pemuda) dan jemaat Gereja GIA Deliksari, Semarang. Pemilihan sampel menggunakan teknik *purposive sampling* dengan kriteria sebagai berikut:

1. Merupakan jemaat aktif Gereja GIA Deliksari.
2. Berusia 17–45 tahun.
3. Bersedia berpartisipasi dalam penelitian dan menandatangani *informed consent*.
4. Bersedia untuk mempelajari dan mengoperasikan sistem pencahayaan.

Jumlah sampel ditentukan berdasarkan rekomendasi minimum untuk pengujian *usability* yang memadai secara statistik serta kebutuhan uji parametrik (*one-sample t-test*). Pengujian ini bersifat evaluasi awal (*preliminary evaluation*) terhadap sistem yang dikembangkan. Pemilihan jemaat gereja sebagai responden didasarkan pada pertimbangan bahwa mereka merupakan pengguna potensial sistem pencahayaan di gereja. Jika sistem dapat dioperasikan dengan baik oleh pengguna awam dari kelompok ini, maka sistem dinilai memenuhi kriteria *usability* yang diharapkan.

---

## 3.4 Variabel Penelitian dan Definisi Operasional

### 3.4.1 Variabel Independen (Bebas)

Variabel independen dalam penelitian ini adalah fitur-fitur audio yang diekstraksi dari lagu rohani, meliputi:
- Tempo/BPM (*Beats Per Minute*)
- *RMS Energy*
- *Spectral Centroid*
- *Chroma Features*
- *Onset Rate*
- MFCC (*Mel-Frequency Cepstral Coefficients*)

### 3.4.2 Variabel Dependen (Terikat)

Variabel dependen dalam penelitian ini dikelompokkan menjadi tiga kategori pengujian:

**Kategori 1: Teknis**

| Variabel | Definisi Operasional | Satuan |
|----------|---------------------|--------|
| *End-to-End Latency* | Waktu dari pengiriman paket *Art-Net* hingga lampu PAR LED merespons | ms |
| *Packet Loss Rate* | Persentase paket *Art-Net* yang gagal diterima oleh modul ESP32 | % |
| *Black-box Test Pass Rate* | Persentase *test case* fungsional yang berhasil (Pass) | % |

**Kategori 2: Kesesuaian Visual**

| Variabel | Definisi Operasional | Satuan |
|----------|---------------------|--------|
| Skor Kesesuaian Pencahayaan | Tingkat kesesuaian yang dipersepsikan oleh pengguna antara pencahayaan yang dihasilkan dengan karakteristik audio lagu rohani | Skala 1–5 |

**Kategori 3: *Usability***

| Variabel | Definisi Operasional | Satuan |
|----------|---------------------|--------|
| Skor SUS | Skor *System Usability Scale* yang mengukur kemudahan penggunaan sistem | 0–100 |

### 3.4.3 Definisi Operasional

1. ***Scene*:** Satu konfigurasi pencahayaan yang terdiri dari nilai DRGBW untuk setiap lampu pada satu saat tertentu.
2. ***Chase*:** Rangkaian beberapa *scene* yang dijalankan secara berurutan dengan waktu transisi tertentu, membentuk efek pencahayaan dinamis.
3. ***Rule-Based Mapping*:** Pemetaan deterministik dari fitur audio ke parameter pencahayaan berdasarkan aturan-aturan eksplisit yang telah ditetapkan (*if-then rules* dan formula matematis), tanpa proses *training* atau *learning*. Setiap aturan didokumentasikan dalam tabel mapping dengan referensi ilmiah.
4. **Kesesuaian Pencahayaan:** Tingkat kecocokan yang dipersepsikan oleh pengguna antara warna dan dinamika pencahayaan dengan karakteristik audio lagu rohani yang didengarkan.

---

## 3.5 Hipotesis Statistik

Hipotesis statistik dalam penelitian ini dirumuskan sebagai berikut:

### Hipotesis 1: Kesesuaian Pencahayaan

- **H₀:** Tidak terdapat kesesuaian signifikan antara pencahayaan yang dihasilkan sistem dengan karakteristik audio lagu rohani berdasarkan persepsi pengguna (rata-rata skor kesesuaian ≤ 3.0).
- **H₁:** Terdapat kesesuaian signifikan antara pencahayaan yang dihasilkan sistem dengan karakteristik audio lagu rohani berdasarkan persepsi pengguna (rata-rata skor kesesuaian > 3.0).

### Hipotesis 2: *Usability* Sistem

- **H₀:** Skor SUS sistem ZZLUXORA ≤ 68 (*below average usability*).
- **H₁:** Skor SUS sistem ZZLUXORA > 68 (*above average usability*).

### Hipotesis 3: *Latency* Sistem

- **H₀:** *End-to-end latency* sistem ≥ 100 ms (tidak memenuhi standar *real-time*).
- **H₁:** *End-to-end latency* sistem < 100 ms (memenuhi standar *real-time*).

---

## 3.6 Data dan Sumber Data

### 3.6.1 Data Primer

1. Nilai *output* RGBW yang dihasilkan oleh sistem untuk setiap lagu rohani yang diuji.
2. Waktu *latency* (*end-to-end latency*).
3. Hasil pengujian *black-box testing*.
4. *Packet loss rate* pada transmisi *Art-Net*.
5. Skor kuesioner SUS dan kesesuaian pencahayaan dari responden.

### 3.6.2 Data Sekunder

1. Spesifikasi teknis ESP32 (*Technical Reference Manual*) [15].
2. Spesifikasi protokol *Art-Net 4* [16] dan standar DMX512 [17].
3. Literatur mengenai korelasi fitur audio dengan warna [10][24].
4. Dokumentasi *library* librosa [21] dan QLC+ [22].

---

## 3.7 Teknik Pengumpulan Data

Teknik pengumpulan data yang digunakan dalam penelitian ini meliputi:

### 3.7.1 Pengujian Sistem (Teknis)

1. ***Black-Box Testing*:** Pengujian fungsional seluruh fitur aplikasi ZZLUXORA dan modul ARTNET-DMX untuk memastikan setiap fungsi berjalan sesuai spesifikasi [18]. Pengujian mencakup:
   - *Input* file audio (format, ukuran, durasi)
   - Proses analisis dan *output* nilai DRGBW
   - Pengiriman *Art-Net* (ke *virtual adapter* dan ESP32)
   - Konfigurasi *fixture* (jumlah lampu, *channel mapping*)
   - Konektivitas modul ESP32 (WiFi/*hotspot*, *captive portal*)

2. **Pengukuran *Latency*:** Mengukur waktu respons *end-to-end* sistem menggunakan *timestamp logging*:
   - *Art-Net packet transmission time*
   - *End-to-end delay* (pengiriman Art-Net → lampu merespons)
   - *Packet loss rate*

### 3.7.2 Kuesioner

1. **Kuesioner SUS (*System Usability Scale*):** 10 item standar yang diadaptasi untuk konteks ZZLUXORA, menggunakan skala Likert 5 poin [19][20].
2. **Kuesioner Kesesuaian Pencahayaan:** 6 item untuk mengukur kesesuaian pencahayaan yang dihasilkan sistem dengan karakteristik audio lagu rohani, di mana responden mendengarkan lagu sambil melihat pencahayaan yang dihasilkan, kemudian menilai kesesuaiannya menggunakan skala Likert 5 poin.

### 3.7.3 Observasi

Observasi langsung terhadap proses penggunaan sistem oleh responden di Gereja GIA Deliksari, mencatat kesulitan, pertanyaan, dan reaksi spontan pengguna.

---

## 3.8 Teknik Keabsahan Data

Untuk menjamin keabsahan data, penelitian ini menggunakan teknik triangulasi pada tiga aspek:

1. **Triangulasi Teknis:** Membandingkan hasil pengujian teknis (*black-box*, *latency*, korelasi statistik) dengan spesifikasi desain sistem.
2. **Triangulasi Persepsi:** Membandingkan hasil persepsi 25 responden untuk melihat konsistensi penilaian kesesuaian pencahayaan.
3. **Triangulasi Literatur:** Membandingkan temuan penelitian dengan hasil-hasil penelitian terdahulu mengenai korelasi fitur audio dengan warna [10][24].

Validitas instrumen kuesioner diuji melalui:
- **Validitas Konten (*Content Validity*):** Instrumen dikonsultasikan dengan dosen pembimbing.
- **Reliabilitas:** Menggunakan koefisien *Cronbach's Alpha* (α ≥ 0.6 dianggap reliabel).

---

## 3.9 Teknik Analisis Data

### 3.9.1 Pengujian Objektif (Teknis)

#### a. Validasi Konsistensi Pemetaan

Validasi dilakukan untuk membuktikan bahwa pemetaan bersifat deterministik dan konsisten:

- **Uji Deterministik (*Reproducibility*):** Menjalankan analisis berulang pada *file* audio yang sama untuk membuktikan bahwa *output* DRGBW bersifat identik pada setiap eksekusi (*input* sama → *output* sama).
- **Korelasi Pearson:** Menghitung koefisien korelasi antara setiap fitur audio (BPM, RMS, *spectral centroid*) dengan setiap kanal *output* (R, G, B, W, *Dimmer*) untuk membuktikan bahwa pemetaan bersifat sistematis dan konsisten dengan tabel *rule-based mapping*.

#### b. Pengujian Fungsional (*Black-Box*)

Hasil *black-box testing* dianalisis secara deskriptif dengan format tabel: *test case*, *expected result*, *actual result*, dan status (Pass/Fail). Persentase keberhasilan dihitung:

$$\text{Persentase Keberhasilan} = \frac{\text{Jumlah Test Case Pass}}{\text{Total Test Case}} \times 100\%$$

#### c. Pengukuran *Latency*

Statistik deskriptif (rata-rata, standar deviasi, minimum, maksimum) dari *end-to-end latency* dihitung dan dibandingkan dengan *threshold* yang ditetapkan (< 100 ms untuk *real-time*).

### 3.9.2 Pengujian Subjektif (Persepsi)

#### a. Skor SUS

Skor SUS dihitung menggunakan formula standar [20]:

Untuk setiap responden:
- Item ganjil (1, 3, 5, 7, 9): skor = respons − 1
- Item genap (2, 4, 6, 8, 10): skor = 5 − respons
- Total skor = jumlah seluruh item × 2.5
- Rentang skor: 0–100

Interpretasi:
| Skor | Kategori |
|------|----------|
| > 80.3 | A (Excellent) |
| 68–80.3 | B (Good) |
| 68 | C (Average) |
| 51–68 | D (Below Average) |
| < 51 | F (Poor) |

#### b. Skor Kesesuaian Pencahayaan

Rata-rata skor kesesuaian pencahayaan dihitung dari seluruh responden dan seluruh lagu yang diuji. Uji statistik dilakukan menggunakan *one-sample t-test* terhadap nilai tengah skala (3.0) untuk membuktikan apakah kesesuaian signifikan secara statistik.

### 3.9.3 Perancangan Model Matematis & Formulasi Algoritma

Perancangan model matematis mengintegrasikan seluruh tahapan transformasi dari sampel sinyal audio diskrit hingga nilai kanal DMX512 fisik:

1. **Transformasi STFT Diskrit:**
   $$X[m, k] = \sum_{n=0}^{N-1} x[n + mH] \cdot w[n] \cdot e^{-j \frac{2\pi}{N} kn}$$
   dengan $N = 2048$, $H = 512$, $f_s = 22.050\text{ Hz}$, dan fungsi *Hann window* $w[n] = 0{,}5 [1 - \cos(2\pi n / (N-1))]$.

2. **Ekstraksi Fitur Spektral:**
   - *Root Mean Square* (RMS): $\text{RMS}[m] = \sqrt{\frac{1}{N} \sum_{n=0}^{N-1} |x[n+mH] \cdot w[n]|^2}$
   - *Spectral Centroid*: $\text{Centroid}[m] = \frac{\sum_{k=0}^{N/2} f_k |X[m, k]|}{\sum_{k=0}^{N/2} |X[m, k]|}$ di mana $f_k = \frac{k \cdot f_s}{N}$
   - *Chroma 12-Semitone*: $\text{Chroma}[m, c] = \sum_{k \in \mathcal{K}_c} |X[m, k]|$ dengan $c = \text{round}(12 \log_2(f_k / 440) + 69) \pmod{12}$

3. **Pemetaan ke Ruang Afektif 2D Russell (Valence-Arousal):**
   - $V = w_1 \cdot \text{Mode}_{\text{ratio}} + w_2 \cdot \text{Centroid}_{\text{norm}} + w_3 \cdot \text{MFCC}_{\text{norm}} \in [-1{,}0, +1{,}0]$
   - $A = w_4 \cdot \text{RMS}_{\text{norm}} + w_5 \cdot \text{Tempo}_{\text{norm}} + w_6 \cdot \text{Onset}_{\text{norm}} \in [-1{,}0, +1{,}0]$

4. **Transformasi Cross-Modal ke Parameter Warna HSV:**
   - $H = (\text{atan2}(A, V) \cdot \frac{180^\circ}{\pi} + 360^\circ) \pmod{360^\circ}$
   - $S = \frac{\sqrt{V^2 + A^2}}{\sqrt{2}} \in [0{,}0, 1{,}0]$
   - $V_{\text{lum}} = \text{RMS}_{\text{norm}} \cdot V_{\text{master}} \in [0{,}0, 1{,}0]$

5. **Dekomposisi 4-Kanal Physical RGBW Lampu Panggung:**
   $$\begin{aligned}
   W &= \min(R, G, B) \\
   R' &= R - W \\
   G' &= G - W \\
   B' &= B - W \\
   \text{DMX}[1\dots 4] &= \text{round}([R', G', B', W] \cdot 255 \cdot V_{\text{master}})
   \end{aligned}$$

Rincian tabel pemetaan *rule-based mapping* dan pembuktian matematis selengkapnya disajikan pada dokumen pendukung `script_math_model.md` dan `script_fft_deep_dive.md`.

---

## 3.10 Etika Penelitian

Penelitian ini memperhatikan aspek-aspek etika sebagai berikut:

1. ***Informed Consent*:** Seluruh responden diberikan penjelasan mengenai tujuan penelitian, prosedur yang akan diikuti, dan hak-hak mereka sebagai responden. Responden menandatangani lembar persetujuan (*informed consent*) sebelum berpartisipasi.
2. **Kerahasiaan Data:** Identitas responden dijaga kerahasiaannya. Data yang dilaporkan bersifat anonim dan hanya digunakan untuk kepentingan penelitian.
3. **Kesukarelaan:** Partisipasi bersifat sukarela. Responden berhak mengundurkan diri kapan saja tanpa konsekuensi.
4. **Tidak Merugikan (*Non-Maleficence*):** Penelitian ini tidak menimbulkan risiko fisik, psikologis, maupun finansial bagi responden.
5. **Izin Lokasi:** Penelitian di Gereja GIA Deliksari dilaksanakan atas seizin pengurus gereja.
