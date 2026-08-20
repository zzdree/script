# BAB 2 KAJIAN PUSTAKA

## 2.1 Tinjauan Pustaka

Bagian ini menyajikan tinjauan terhadap penelitian-penelitian terdahulu yang relevan dengan topik penelitian, meliputi sistem *audio-reactive lighting*, korelasi fitur audio dengan parameter visual, korespondensi lintas-modal musik-warna, dan sistem pencahayaan cerdas berbasis IoT. Tinjauan ini bertujuan untuk mengidentifikasi posisi penelitian dan kontribusi kebaruan yang ditawarkan.

### 2.1.1 Penelitian Sistem *Audio-Reactive Lighting*

Perkembangan teknologi pengendalian pencahayaan panggung telah melahirkan berbagai sistem yang mampu merespons sinyal audio secara otomatis. Dalam konteks profesional, perangkat lunak seperti *SoundSwitch* dan *Lightjams* menyediakan fitur sinkronisasi pencahayaan dengan musik melalui analisis *beat* secara *real-time*. Namun, sistem-sistem tersebut umumnya bersifat komersial dengan biaya lisensi tinggi dan tidak dirancang khusus untuk konteks ibadah gereja.

Penelitian terbaru menunjukkan pergeseran dari pendekatan *rule-based* tradisional menuju model generatif berbasis *deep learning* untuk otomasi pencahayaan panggung. Meskipun demikian, pendekatan *rule-based* tetap menjadi standar untuk banyak aplikasi *real-time* karena keandalan dan biaya komputasi yang rendah. Penelitian ini memilih pendekatan *rule-based* dengan pertimbangan transparansi, kemudahan pengujian, dan kesesuaian dengan perangkat keras terbatas.

### 2.1.2 Penelitian Korelasi Fitur Audio dengan Parameter Visual

Li, Liu, dan Xue (2024) mengembangkan model FFA-BiGRU (*Feature Fusion Attention–Bidirectional Gated Recurrent Unit*) untuk klasifikasi emosi musik menggunakan fitur spasial-temporal [1]. Penelitian tersebut menunjukkan bahwa kombinasi fitur audio seperti MFCC, *chroma*, dan *spectral features* mampu merepresentasikan karakteristik emosional musik dengan baik. Chaki *et al.* (2023) melakukan pengenalan emosi musik menggunakan *supervised machine learning* dan membuktikan bahwa fitur audio konvensional masih efektif sebagai basis klasifikasi [7]. Guo, Li, dan Chen (2022) mengusulkan metode multimodal yang mengombinasikan beberapa fitur dalam satu *classifier* [8].

Berbeda dengan penelitian-penelitian tersebut yang menggunakan pendekatan *machine learning*, penelitian ini mengadopsi pendekatan *rule-based* yang memetakan fitur audio ke parameter pencahayaan melalui model matematis deterministik tanpa memerlukan proses *training* model, sehingga lebih mudah diimplementasikan dan diverifikasi secara objektif.

### 2.1.3 Penelitian Korespondensi Musik-Warna

Palmer *et al.* (2013) membuktikan bahwa asosiasi warna terhadap musik dimediasi oleh emosi secara konsisten lintas-budaya, di mana musik bertempo cepat dan bermodus mayor diasosiasikan dengan warna-warna cerah, tersaturasi, dan hangat, sedangkan musik bertempo lambat dan bermodus minor diasosiasikan dengan warna-warna gelap, desaturasi, dan dingin [24]. Lindborg (2021) memperkuat temuan ini dengan menunjukkan bahwa asosiasi warna terhadap musik dimediasi oleh emosi dan sebagian dimodulasi oleh sinestesia [10]. Temuan-temuan ini menjadi landasan ilmiah bahwa pemetaan fitur audio ke parameter warna memiliki basis psikologis yang valid dan dapat diimplementasikan secara sistematis.

Saari *et al.* (2021) mengembangkan komputasi semantik adaptif-genre untuk anotasi *mood* musik, yang menunjukkan bahwa fitur audio dapat digunakan untuk mengestimasi dimensi emosional musik [9]. Juslin dan Laukka (2003) menunjukkan bahwa tempo, *loudness*, dan modus merupakan parameter utama yang secara konsisten digunakan untuk mengekspresikan emosi dalam musik, dan pola ini paralel dengan ekspresi emosi dalam suara manusia [31]. Temuan-temuan ini menjadi fondasi bagi pengembangan tabel *rule-based mapping* dalam penelitian ini.

### 2.1.4 Penelitian Sistem Pencahayaan Cerdas Berbasis IoT

Ardiatma dan Soewito (2023) mengembangkan sistem pencahayaan *indoor* berbasis IoT yang mengendalikan LED dengan suhu warna berbeda berdasarkan aktivitas pengguna [11]. Hung, Lin, dan Chen (2024) merancang sistem LED dengan *color mixing* yang lebih seragam, relevan dengan pencampuran warna RGBW [12]. Ma (2024) meneliti integrasi IoT dalam sistem LED cerdas dengan fokus pada efisiensi energi [13].

Maier, Sharp, dan Vagapov (2021) melakukan analisis komparatif ESP32 untuk implementasi IoT, membuktikan keunggulan ESP32 dalam hal konektivitas WiFi, performa *dual-core*, dan *cost-effectiveness* [14]. Penelitian-penelitian ini mendukung pemilihan ESP32 sebagai mikrokontroler utama dalam modul *ARTNET-DMX*.

### 2.1.5 Posisi Penelitian

Berdasarkan tinjauan pustaka di atas, posisi penelitian ini berada pada konteks integrasi tiga domain keilmuan: (1) *Digital Signal Processing* dan *Music Information Retrieval* untuk ekstraksi fitur audio; (2) psikologi persepsi untuk pemetaan fitur audio ke warna; dan (3) sistem *embedded* dan protokol jaringan untuk pengendalian pencahayaan. Tabel 2.1 menyajikan perbandingan penelitian terdahulu dengan penelitian ini.

**Tabel 2.1 Perbandingan Penelitian Terdahulu dengan Penelitian Ini**

| No | Peneliti (Tahun) | Topik | Metode | Perbedaan dengan Penelitian Ini |
|----|-----------------|-------|--------|-------------------------------|
| 1 | Li *et al.* (2024) [1] | Klasifikasi emosi musik | *Deep learning* (FFA-BiGRU) | Penelitian ini menggunakan *rule-based*, bukan DL |
| 2 | Chaki *et al.* (2023) [7] | Pengenalan emosi musik | *Supervised ML* | Penelitian ini tanpa proses *training* model |
| 3 | Palmer *et al.* (2013) [24] | Asosiasi warna-musik | Eksperimen psikologi | Penelitian ini mengimplementasikan pemetaan ke sistem nyata |
| 4 | Lindborg (2021) [10] | Asosiasi warna-musik | Eksperimen psikologi | Penelitian ini mengimplementasikan pemetaan ke sistem nyata |
| 5 | Ardiatma & Soewito (2023) [11] | IoT LED control | Berbasis aktivitas | Penelitian ini berbasis analisis fitur audio |
| 6 | Maier *et al.* (2021) [14] | ESP32 untuk IoT | Analisis komparatif | Penelitian ini menggunakan ESP32 untuk Art-Net DMX |
| 7 | **Penelitian ini** | *Audio-reactive lighting* untuk ibadah | *Rule-based* HSV-RGBW + *Art-Net* | Integrasi *end-to-end* khusus lagu rohani |

---

## 2.2 Landasan Teori

### 2.2.1 Pemrosesan Sinyal Audio Digital (DSP/*MIR*)

*Digital Signal Processing* (DSP) merupakan cabang ilmu yang mempelajari pemrosesan sinyal dalam domain digital, termasuk sinyal audio. Dalam konteks penelitian ini, DSP digunakan untuk mengekstraksi fitur-fitur bermakna dari *file* audio lagu rohani. Disiplin terkait, yaitu *Music Information Retrieval* (MIR), secara khusus menangani pengambilan informasi dari data musik, meliputi aspek ritme, harmoni, timbre, dan struktur [2][4].

#### a. *Fast Fourier Transform* (FFT) dan *Short-Time Fourier Transform* (STFT)

FFT merupakan algoritma efisien untuk menghitung *Discrete Fourier Transform* (DFT) yang mengubah sinyal audio dari domain waktu ke domain frekuensi. STFT merupakan pengembangan FFT yang membagi sinyal menjadi segmen-segmen pendek (*window*) dan menerapkan FFT pada setiap segmen, menghasilkan representasi waktu-frekuensi yang disebut spektrogram. Secara matematis, STFT didefinisikan sebagai:

$$STFT\{x(t)\}(\tau, \omega) = \int_{-\infty}^{\infty} x(t) \cdot w(t - \tau) \cdot e^{-j\omega t} \, dt$$

di mana $x(t)$ adalah sinyal audio, $w(t)$ adalah fungsi *window* (misalnya Hann *window*), $\tau$ adalah waktu, dan $\omega$ adalah frekuensi angular [21].

#### b. Fitur Audio

Berikut adalah fitur-fitur audio yang diekstraksi dalam penelitian ini:

1. **Tempo/BPM (*Beats Per Minute*):** Kecepatan ketukan musik per menit. Lagu *praise* umumnya memiliki tempo tinggi (120–180 BPM), sedangkan lagu *worship* bertempo rendah (60–100 BPM) [5].

2. ***RMS Energy*:** Akar kuadrat rata-rata (*Root Mean Square*) dari amplitudo sinyal, merepresentasikan kenyaringan atau energi keseluruhan lagu.
$$RMS = \sqrt{\frac{1}{N} \sum_{i=1}^{N} x_i^2}$$

3. ***Spectral Centroid*:** Titik pusat massa spektrum frekuensi, merepresentasikan "kecerahan" (*brightness*) suara. Nilai tinggi menunjukkan dominasi frekuensi tinggi.
$$SC = \frac{\sum_{k=1}^{K} f(k) \cdot |X(k)|^2}{\sum_{k=1}^{K} |X(k)|^2}$$
di mana $f(k)$ adalah frekuensi bin ke-$k$ dan $X(k)$ adalah magnitudo DFT pada bin ke-$k$ [21].

4. **MFCC (*Mel-Frequency Cepstral Coefficients*):** Koefisien cepstral berbasis skala Mel yang merepresentasikan karakteristik timbre suara. Umumnya diambil 13 koefisien pertama [1][2].

5. ***Chroma Features*:** Representasi distribusi energi pada 12 kelas nada kromatik (C, C#, D, ..., B), merepresentasikan konten harmoni dan tonalitas lagu.

6. ***Onset Detection*:** Deteksi titik-titik awal setiap nada atau ketukan baru dalam sinyal audio. Dalam penelitian ini, *onset detection* digunakan untuk menentukan titik perubahan *scene* pencahayaan berdasarkan perubahan dinamika audio [5].

7. ***Beat Tracking*:** Pelacakan posisi ketukan (*beat*) dalam sinyal audio untuk sinkronisasi transisi pencahayaan dengan ritme musik. *Beat tracking* menjadi dasar utama penentuan waktu pergantian *scene* dan kecepatan *chase* [5].

### 2.2.2 Psikologi Persepsi Musik dan Warna

#### a. Model *Circumplex of Affect* (Russell, 1980)

Model *Circumplex of Affect* yang dikemukakan oleh James A. Russell (1980) merupakan kerangka psikologis fundamental yang mengorganisasikan pengalaman emosional dalam ruang dua dimensi [23]:

- ***Valence* (sumbu horizontal):** Merepresentasikan tingkat kesenangan (*pleasantness*) emosi, dari negatif (sedih, marah) hingga positif (senang, damai).
- ***Arousal* (sumbu vertikal):** Merepresentasikan tingkat intensitas atau aktivasi emosional, dari rendah (tenang, mengantuk) hingga tinggi (bersemangat, tegang).

Setiap emosi dapat direpresentasikan sebagai titik koordinat (*V*, *A*) dalam ruang dua dimensi ini. Dalam konteks penelitian ini, model *Valence-Arousal* digunakan sebagai representasi antara (*intermediate representation*) untuk menjembatani fitur audio dengan parameter warna — bukan sebagai klaim deteksi emosi, melainkan sebagai kerangka matematis untuk mengorganisasikan pemetaan fitur audio [7][9].

#### b. Korelasi Fitur Audio dengan Warna

Penelitian Palmer *et al.* (2013) menunjukkan bahwa asosiasi warna terhadap musik dimediasi oleh emosi secara lintas-budaya [24]. Temuan utama yang relevan dengan penelitian ini:

| Karakteristik Audio | Asosiasi Warna | Referensi |
|---------------------|---------------|-----------|
| Tempo cepat, modus mayor | Warna cerah, tersaturasi, hangat (kuning, merah) | Palmer *et al.* (2013) [24] |
| Tempo lambat, modus minor | Warna gelap, desaturasi, dingin (biru, hijau) | Palmer *et al.* (2013) [24] |
| Energi tinggi (*loudness*) | Warna gelap, tersaturasi, merah | Palmer *et al.* (2013) [24] |
| Frekuensi rendah dominan | Warna hangat (*warm*) | Lindborg (2021) [10] |
| Frekuensi tinggi dominan | Warna dingin (*cool*) | Lindborg (2021) [10] |

Temuan-temuan ini menjadi dasar ilmiah bagi penyusunan tabel *rule-based mapping* eksplisit yang digunakan dalam sistem ZZLIGHT-Luxora. Setiap aturan pemetaan merujuk pada referensi penelitian yang telah dipublikasikan.

### 2.2.3 Model Warna dan Pemetaan Matematis

#### a. Ruang Warna HSV (*Hue, Saturation, Value*)

Model warna HSV memisahkan informasi warna menjadi tiga komponen:
- ***Hue* (H):** Jenis warna, dinyatakan dalam derajat (0°–360°).
- ***Saturation* (S):** Kejenuhan warna, dari 0 (abu-abu) hingga 1 (warna penuh).
- ***Value* (V):** Kecerahan, dari 0 (gelap/hitam) hingga 1 (terang).

Model HSV dipilih sebagai jembatan antara fitur audio dan warna karena lebih intuitif dibandingkan model RGB untuk merepresentasikan persepsi warna manusia. Perubahan karakteristik audio dapat dipetakan secara langsung ke komponen *Hue* (jenis warna), *Saturation* (intensitas warna), dan *Value* (kecerahan) [12].

#### b. Konversi HSV ke RGB

Konversi dari HSV ke RGB menggunakan algoritma standar (Foley dan van Dam) sebagai berikut:

$$C = V \times S$$
$$H' = \frac{H}{60°}$$
$$X = C \times (1 - |H' \bmod 2 - 1|)$$
$$m = V - C$$

Kemudian, nilai $(R_1, G_1, B_1)$ ditentukan berdasarkan sektor $H'$:

$$
(R_1, G_1, B_1) = \begin{cases}
(C, X, 0) & \text{jika } 0 \leq H' < 1 \\
(X, C, 0) & \text{jika } 1 \leq H' < 2 \\
(0, C, X) & \text{jika } 2 \leq H' < 3 \\
(0, X, C) & \text{jika } 3 \leq H' < 4 \\
(X, 0, C) & \text{jika } 4 \leq H' < 5 \\
(C, 0, X) & \text{jika } 5 \leq H' < 6
\end{cases}
$$

Nilai akhir RGB:
$$R = (R_1 + m) \times 255, \quad G = (G_1 + m) \times 255, \quad B = (B_1 + m) \times 255$$

#### c. Penambahan Kanal *White* (RGBW)

Lampu PAR LED RGBW memiliki kanal *white* terpisah yang menghasilkan cahaya putih murni. Untuk mengekstraksi komponen *white* dari nilai RGB:

$$W = \min(R, G, B)$$
$$R' = R - W, \quad G' = G - W, \quad B' = B - W$$

Pendekatan ini menghasilkan warna yang lebih kaya dan cahaya putih yang lebih alami dibandingkan pencampuran RGB murni.

#### d. Normalisasi Fitur Audio

Normalisasi *min-max* digunakan untuk menskala setiap fitur audio ke rentang [0, 1]:

$$x_{norm} = \frac{x - x_{min}}{x_{max} - x_{min}}$$

Rentang referensi ditentukan berdasarkan karakteristik lagu rohani (misalnya BPM: 60–180, *RMS*: 0.01–0.5, *Spectral Centroid*: 500–5000 Hz). Nilai hasil normalisasi di-*clip* ke rentang [0, 1] untuk menghindari nilai di luar batas.

### 2.2.4 Lampu PAR LED RGBW

Lampu PAR LED (*Parabolic Aluminized Reflector Light-Emitting Diode*) RGBW merupakan *fixture* pencahayaan panggung yang menggunakan LED dengan empat warna: *Red*, *Green*, *Blue*, dan *White*. Setiap warna dikendalikan melalui kanal DMX tersendiri dengan rentang nilai 0–255.

Konfigurasi *fixture* yang digunakan dalam penelitian ini adalah 8 kanal per lampu:

| Kanal | Fungsi | Rentang |
|-------|--------|---------|
| CH1 | *Dimmer* (intensitas keseluruhan) | 0–255 |
| CH2 | *Red* | 0–255 |
| CH3 | *Green* | 0–255 |
| CH4 | *Blue* | 0–255 |
| CH5 | — (*empty*) | — |
| CH6 | *Program* (efek bawaan) | 0–255 |
| CH7 | *Speed* (kecepatan efek) | 0–255 |
| CH8 | — (*empty*) | — |

Pencampuran warna pada PAR LED RGBW menggunakan prinsip *additive color mixing*, di mana kombinasi intensitas dari keempat LED menghasilkan warna tampilan akhir [12].

### 2.2.5 Protokol *Art-Net* dan DMX512

#### a. Standar DMX512

DMX512 (*Digital Multiplex* 512) merupakan standar komunikasi serial yang ditetapkan oleh ANSI/ESTA (standar ANSI E1.11-2008) untuk pengendalian peralatan pencahayaan panggung [17]. Protokol ini mentransmisikan data secara unidireksional melalui antarmuka RS-485 dengan kecepatan 250 kbps, mendukung hingga 512 kanal (*channel*) dalam satu *universe*. Setiap kanal merepresentasikan satu parameter kontrol (misalnya intensitas *dimmer*) dengan resolusi 8-bit (0–255).

#### b. Protokol *Art-Net*

*Art-Net* merupakan protokol komunikasi yang dikembangkan oleh *Artistic Licence Engineering Ltd.* untuk mentransmisikan data DMX512 melalui jaringan UDP/IP [16]. *Art-Net* menggunakan *port* 6454 dan mendukung hingga 32.768 *universe* DMX. Dalam penelitian ini, *Art-Net* digunakan sebagai *transport layer* untuk mengirimkan data pencahayaan dari aplikasi ZZLIGHT-Luxora ke modul ESP32 melalui jaringan WiFi.

Struktur paket *Art-Net* (*ArtDmx*) terdiri dari: *header* identifikasi ("Art-Net\0"), *OpCode* (0x5000), nomor *universe*, panjang data, dan 512 byte data DMX.

### 2.2.6 Mikrokontroler ESP32

ESP32 merupakan mikrokontroler yang dikembangkan oleh Espressif Systems dengan arsitektur *dual-core* Xtensa LX6, dilengkapi modul WiFi 802.11 b/g/n dan Bluetooth terintegrasi [14][15]. Spesifikasi utama ESP32 DevKit V1 yang relevan dengan penelitian ini:

| Parameter | Spesifikasi |
|-----------|-------------|
| Prosesor | *Dual-core* Xtensa LX6, 240 MHz |
| WiFi | 802.11 b/g/n, 2.4 GHz |
| GPIO | 34 *pin* |
| UART | 3 *port* (UART0, UART1, UART2) |
| Memori | 520 KB SRAM, 4 MB Flash |
| Tegangan Operasi | 3.3V (input VIN 5V) |

Dalam penelitian ini, ESP32 berfungsi sebagai *Art-Net node* yang menerima paket *Art-Net* melalui WiFi dan mengonversinya menjadi sinyal DMX512 melalui modul MAX485 (RS-485 *transceiver*). Implementasi menggunakan teknik sinkronisasi data untuk menjaga kestabilan modul *Art-Net* DMX pada kecepatan *refresh* yang memadai. Detail teknis implementasi sinkronisasi disajikan pada BAB 4.

### 2.2.7 QLC+ (*Open-Source Lighting Control*)

QLC+ (*Q Light Controller Plus*) merupakan perangkat lunak *open-source* untuk pengendalian pencahayaan panggung yang mendukung berbagai protokol termasuk DMX512, *Art-Net*, dan sACN [22]. Dalam arsitektur sistem penelitian ini, QLC+ berfungsi sebagai *intermediary* opsional:

1. Menerima data *Art-Net* dari ZZLIGHT-Luxora sebagai *Input Universe* melalui *virtual adapter*.
2. Meneruskan data tersebut sebagai *Output Universe* melalui *Art-Net* ke modul ESP32 melalui jaringan WiFi/*hotspot*.

QLC+ menyediakan fitur tambahan seperti *fixture editor*, *scene* manual, dan visualisasi yang memungkinkan operator melakukan penyesuaian manual jika diperlukan.

---

## 2.3 Kerangka Berpikir

Kerangka berpikir penelitian ini didasarkan pada asumsi bahwa fitur-fitur audio suatu lagu rohani dapat diekstraksi secara kuantitatif dan dipetakan ke parameter pencahayaan RGBW melalui model matematis *rule-based* yang transparan dan terukur. Pemetaan ini didasarkan pada temuan penelitian Palmer *et al.* (2013) dan Lindborg (2021) mengenai korelasi sistematis antara karakteristik audio dan persepsi warna. Berikut adalah alur kerangka berpikir secara konseptual:

```
┌─────────────────┐
│   Audio Input   │  File audio lagu rohani (.mp3/.wav)
│   (.mp3/.wav)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Ekstraksi     │  BPM, RMS, Spectral Centroid, MFCC,
│   Fitur Audio   │  Chroma, Onset Detection, Beat Tracking
│   (librosa)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Normalisasi   │  Min-Max Scaling [0, 1]
│   Fitur         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Perhitungan   │  Rule-based weighted sum
│   Valence &     │  berdasarkan fitur audio
│   Arousal       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Pemetaan      │  V-A → H (jenis warna)
│   V-A → HSV     │  V-A → S (kejenuhan)
│   (Rule-Based)  │  V-A → V (kecerahan)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Konversi      │  Algoritma standar Foley & van Dam
│   HSV → RGB     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Ekstraksi     │  W = min(R,G,B)
│   White Channel │  R'=R-W, G'=G-W, B'=B-W
│   RGB → RGBW    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Pembangkitan  │  Berdasarkan beat tracking &
│   Scene & Chase │  onset detection
│   (DRGBW)       │  + rules BPM/RMS → timing transisi
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Pengiriman    │  UDP port 6454
│   Art-Net       │  Universe 0, 512 channel
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│Virtual │ │ WiFi/  │
│Adapter │ │Hotspot │
│→ QLC+  │ │→ ESP32 │
└───┬────┘ └───┬────┘
    │          │
    ▼          ▼
┌────────┐ ┌────────┐
│Art-Net │ │MAX485  │
│→ ESP32 │ │→ DMX   │
└───┬────┘ └───┬────┘
    │          │
    └────┬─────┘
         │
         ▼
┌─────────────────┐
│   PAR LED RGBW  │  4 unit (pengujian)
│   via DMX512    │  8 channel per fixture
└─────────────────┘
```

Berdasarkan kerangka berpikir di atas, sistem yang dibangun menghubungkan domain audio (*input*) dengan domain visual (*output*) melalui serangkaian transformasi matematis yang dapat diuji dan diverifikasi secara objektif. Penilaian akhir kesesuaian dilakukan melalui dua pendekatan: (1) uji objektif berupa konsistensi dan determinisme pemetaan serta korelasi statistik antara fitur audio dan nilai RGBW, dan (2) uji subjektif berupa persepsi pengguna terhadap kesesuaian pencahayaan dengan karakteristik lagu.

---

## 2.4 Hipotesis Teoritis

Berdasarkan kajian pustaka dan kerangka berpikir yang telah diuraikan, hipotesis teoritis dalam penelitian ini adalah sebagai berikut:

1. Fitur-fitur audio lagu rohani (BPM, *RMS energy*, *spectral centroid*, *chroma features*) dapat dipetakan secara sistematis ke parameter pencahayaan RGBW melalui model matematis *rule-based* berbasis ruang warna HSV, dengan dasar referensi korelasi musik-warna dari Palmer *et al.* (2013) dan Lindborg (2021).
2. Sistem *audio-reactive lighting* yang dibangun mampu menghasilkan *scene* dan *chase* pencahayaan yang dipersepsikan sesuai dengan karakteristik audio lagu rohani oleh pengguna.
3. Integrasi protokol *Art-Net* DMX512 melalui jaringan nirkabel (WiFi/*hotspot*) ke modul ESP32 mampu mengendalikan lampu PAR LED RGBW dengan *latency* yang dapat diterima untuk penggunaan ibadah secara *real-time*.
