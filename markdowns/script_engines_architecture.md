# 🎛️ ARSITEKTUR LENGKAP 6 SUB-ENGINE SISTEM ZZLUXORA
## Landasan Matematis, Algoritmik, dan Alur Komputasi End-to-End
### Dokumen Rujukan Akademik Skripsi S1 Teknik Komputer FT UNNES

> **Peneliti:** Andreas Restuawanta Christwara (`NIM: 5312422036`)  
> **Dosen Pembimbing:** Mario Norman Syah, S.Pd., M.Eng. (`NIP: 199304212024061001`)  
> **Konteks:** Pedoman komprehensif untuk presentasi dan asistensi kepada Dosen Pembimbing mengenai cara kerja sistem ZZLUXORA yang terdiri dari **6 sub-engine komputasi terintegrasi**.

---

## 🌟 IKHTISAR: ZZLUXORA BUKAN HANYA FFT!

Sistem ZZLUXORA bukanlah sekadar kalkulator FFT sederhana, melainkan sebuah **arsitektur terintegrasi multi-disiplin** yang menghubungkan 6 sub-engine berurutan:

```text
[ AUDIO LAGU ROHANI (.wav / .mp3) ]
             │
             ▼
┌────────────────────────────────────────────────────────┐
│ ENGINE 1: PREPROCESSING & DISKRITISASI AUDIO           │
│ - Resampling 22.050 Hz (Nyquist limit 11.025 Hz)       │
│ - Stereo to Mono Downmix float32 [-1.0, 1.0]           │
└────────────────────────────┬───────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│ ENGINE 2: STFT & COOLEY-TUKEY RADIX-2 FFT              │
│ - Sliding Windowing (N = 2048, H = 512, Overlap 75%)   │
│ - Hann Windowing w[n] (Meredam Leakage hingga -31.5 dB)│
│ - O(N log2 N) FFT -> Matriks Kompleks X[m, k]          │
│ - Laju Pembaruan 43.07 FPS (Sinkron DMX512 44 FPS)     │
└────────────────────────────┬───────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│ ENGINE 3: EKSTRAKSI FITUR AKUSTIK SPEKTRAL (MIR)       │
│ - RMS Energy (Parseval Loudness Envelope)              │
│ - Spectral Centroid (Center of Mass Timbre Brightness) │
│ - Chroma STFT 12-Semitone (Tonalitas Mayor vs Minor)   │
│ - MFCC 13 Koefisien (Tekstur Timbre Vokal/Instrumen)   │
│ - Spectral Flux & Beat Tracker (BPM & Onset Timing)    │
└────────────────────────────┬───────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│ ENGINE 4: PEMODELAN AFEKTIF RUSSELL 2D PLANE           │
│ - Valence (V) in [-1.0, +1.0]: Sukacita vs Khidmat     │
│ - Arousal (A) in [-1.0, +1.0]: Energetik vs Tenang     │
│ - Klasifikasi Kuadran Ibadah (Praise Q1 vs Worship Q3) │
└────────────────────────────┬───────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│ ENGINE 5: CROSS-MODAL COLOR & PHYSICAL RGBW ENGINE     │
│ - Polar Map: Hue H = atan2(A, V), Saturation S = r/√2  │
│ - Value/Dimmer = RMS_norm * Master_Fader               │
│ - HSV -> Standard sRGB [0 - 255]                       │
│ - Dekomposisi 4-Kanal: W = min(R,G,B), R'=R-W, G'=G-W  │
│   (Mencegah Desaturasi / Washout pada PAR LED)         │
└────────────────────────────┬───────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│ ENGINE 6: JARINGAN ART-NET 4 & HARDWARE ESP32 DMX512   │
│ - Pengemasan Paket Biner ArtDmx 530 Byte (Port 6454)   │
│ - Transmisi UDP Broadcast/Unicast 43 FPS               │
│ - ESP32 Dual-Core FreeRTOS Receiver (Core 0 UDP WiFi)  │
│ - Hardware Serial UART2 Driver MAX485 (Core 1 DMX512)  │
└────────────────────────────┬───────────────────────────┘
                             │
                             ▼
[ LAMPU PAR LED PANGGUNG GEREJA GIA DELIKSARI BERGERAK OTOMATIS ]
```

---

## 🔬 1. ENGINE 1: PREPROCESSING & DISKRITISASI AUDIO

### 1.1 Masukan Sinyal Fisik
Sinyal audio dari file lagu rohani (.mp3 atau .wav) didekode menjadi sinyal audio digital terkuantisasi linear PCM float32.

### 1.2 Downmixing Stereo ke Mono
Sinyal audio kebaktian umumnya diproduksi dalam format stereo 2-kanal ($x_L(t)$ dan $x_R(t)$). Untuk analisis spektral yang konsisten dan bebas fase interferensi, kedua kanal digabungkan menjadi sinyal mono:
$$x[n] = \frac{x_L[n] + x_R[n]}{2}$$

### 1.3 Resampling & Kriteria Nyquist-Shannon
Frekuensi pencuplikan diubah ke laju standar MIR $f_s = 22.050\text{ Hz}$.
Berdasarkan teorema Nyquist:
$$f_{\text{Nyquist}} = \frac{f_s}{2} = \frac{22050}{2} = 11.025\text{ Hz}$$
- Nada terendah instrumen musik panggung (C0 / Sub-bass): $\approx 16{,}35\text{ Hz}$.
- Nada piano tertinggi (C8): $4.186\text{ Hz}$.
- Rentang vokal manusia: $80\text{ Hz} - 1.200\text{ Hz}$.
Dengan batas $11.025\text{ Hz}$, seluruh nada dasar musik dan harmonik ke-2 serta ke-3 tertangkap utuh tanpa distorsi aliasing, sekaligus menghemat beban pemrosesan hingga $50\%$ dibanding menggunakan $44.100\text{ Hz}$.

---

## ⚡ 2. ENGINE 2: STFT & COOLEY-TUKEY RADIX-2 FFT

### 2.1 Mengapa Musik Butuh STFT?
Sinyal musik bersifat **non-stasioner** (frekuensi dan energi berubah dari detik ke detik). Jika dianalisis dengan FFT biasa sepanjang 4 menit, kita hanya mengetahui frekuensi apa yang ada, tetapi tidak tahu **kapan frekuensi itu berbunyi**.
Oleh karena itu digunakan **Short-Time Fourier Transform (STFT)** yang memotong sinyal menjadi jendela-jendela kecil yang bergeser (*sliding window*).

### 2.2 Parameter Segmentasi & Resolusi
- Panjang Jendela Transformasi ($N$): **2048 sampel** ($\approx 92{,}88\text{ ms}$).
- Jarak Pergeseran Frame ($H$): **512 sampel** ($\approx 23{,}22\text{ ms}$, terjadi tumpang-tindih/*overlap* $75\%$).
- Lebar Pita per Bin Frekuensi ($\Delta f$):
  $$\Delta f = \frac{f_s}{N} = \frac{22050}{2048} \approx 10{,}77\text{ Hz per bin}$$
- Interval Waktu Perbaruan ($\Delta t_{\text{hop}}$):
  $$\Delta t_{\text{hop}} = \frac{H}{f_s} = \frac{512}{22050} \approx 23{,}22\text{ ms}$$
- **Laju Frame Visual:**
  $$\text{FPS} = \frac{1}{\Delta t_{\text{hop}}} = \frac{22050}{512} \approx 43{,}07\text{ frame per detik (fps)}$$

> **SINKRONISASI KRUSIAL:** Standar transmisi fisik DMX512-A adalah **44 paket per detik**. Pemilihan $H=512$ menghasilkan **43,07 FPS**, yang secara alami sinkron dengan refresh rate kabel DMX tanpa perlu buffer tambahan!

### 2.3 Mitigasi Spectral Leakage via Hann Window
Pemotongan frame secara mendadak menimbulkan diskontinuitas yang membocorkan energi frekuensi (*spectral leakage*). Untuk mencegahnya, sinyal dikalikan dengan **Hann Window**:
$$w[n] = 0{,}5 \left[ 1 - \cos\left(\frac{2\pi n}{N-1}\right) \right] = \sin^2\left(\frac{\pi n}{N-1}\right), \quad 0 \le n \le N-1$$
Hann window meredam kebocoran spektral hingga **-31,5 dB** (jauh lebih bersih dibanding rectangular window yang hanya -13 dB).

### 2.4 Formulasi Diskrit STFT
$$X[m, k] = \sum_{n=0}^{N-1} x[n + mH] \cdot w[n] \cdot e^{-j \frac{2\pi}{N} kn}$$
di mana $m$ adalah indeks waktu frame dan $k \in \{0, 1, \dots, 1024\}$ adalah indeks bin frekuensi positif.

### 2.5 Kecepatan Algoritma FFT Cooley-Tukey Radix-2
Dengan membagi deret genap dan ganjil secara rekursif (*butterfly operation*):
- Kompleksitas DFT biasa: $\mathcal{O}(N^2) = 2048^2 = 4.194.304$ operasi.
- Kompleksitas FFT Cooley-Tukey: $\mathcal{O}(N \log_2 N) = 2048 \times 11 = 22.528$ operasi.
- **Hasil:** Algoritma FFT berjalan **186,2 kali lebih cepat** (menghemat $99{,}46\%$ beban CPU), sehingga evaluasi STFT per frame selesai dalam waktu kurang dari **1 milidetik**!

---

## 📊 3. ENGINE 3: EKSTRAKSI FITUR AKUSTIK SPEKTRAL (MIR)

Dari matriks kompleks STFT $X[m, k]$, diekstraksi 5 fitur utama:

### 3.1 RMS Energy (Intensitas & Volume)
Berdasarkan Teorema Parseval, energi sinyal per frame dihitung sebagai:
$$\text{RMS}[m] = \sqrt{ \frac{1}{N} \sum_{n=0}^{N-1} |x[n + mH] \cdot w[n]|^2 }$$
Dinormalisasi ke $[0.0, 1.0]$. Fitur ini langsung mengendalikan **Master Dimmer** lampu panggung (ketika musik tenang, lampu meredup lembut; ketika musik mencapai chorus puncak, lampu bersinar terang).

### 3.2 Spectral Centroid (Kecerahan Timbre / Brightness)
Titik pusat massa dari spektrum frekuensi audio pada frame ke-$m$:
$$\text{Centroid}[m] = \frac{\sum_{k=0}^{1024} f_k \cdot |X[m, k]|}{\sum_{k=0}^{1024} |X[m, k]|}, \quad f_k = \frac{k \cdot f_s}{N}$$
- Centroid rendah (< 1500 Hz): Suara berat, hangat, tebal (bass/drum dominan) $\to$ warna tenang, kontemplatif.
- Centroid tinggi (> 3000 Hz): Suara tajam, terang, cerah (simbal/vokal sopran dominan) $\to$ warna terang, hangat tersaturasi.

### 3.3 Chroma STFT (12 Kelas Nada Kromatik & Mayor vs Minor)
Memproyeksikan 1025 bin FFT ke dalam 12 kelas nada musik barat:
$$\{C, C\sharp, D, D\sharp, E, F, F\sharp, G, G\sharp, A, A\sharp, B\}$$
Menggunakan rumus nada MIDI:
$$p = 12 \log_2\left(\frac{f_k}{440}\right) + 69, \quad c = \text{round}(p) \pmod{12}$$
Vektor Chroma 12 dimensi dikorelasikan dengan template Krumhansl-Schmuckler:
- Korelasi Mayor tinggi $\to$ Lagu bernuansa sukacita/praise $\to$ **Valence positif ($V > 0$)**.
- Korelasi Minor tinggi $\to$ Lagu bernuansa teduh/worship $\to$ **Valence negatif ($V < 0$)**.

### 3.4 Mel-Frequency Cepstral Coefficients (MFCC)
Menangkap amplop spektral (*timbre texture*) menggunakan 40 filterbank Mel segitiga dan *Discrete Cosine Transform* (DCT-II):
$$\text{MFCC}[m, l] = \sum_{b=1}^{40} \log(\tilde{S}[m, b]) \cdot \cos\left( \frac{\pi l (b - 0{,}5)}{40} \right), \quad l = 0, \dots, 12$$
Koefisien MFCC membedakan instrumen akustik (piano/gitar akustik pada lagu *worship*) dari instrumen distorsi (gitar elektrik/drum pada lagu *praise*).

### 3.5 Onset Detection & Beat Tracking
Menghitung fungsi kebaruan spektral (*spectral flux*):
$$\text{SF}[m] = \sum_{k=0}^{1024} \max(0, |X[m, k]| - |X[m-1, k]|)$$
Puncak nilai SF mendeteksi hentakan ketukan (*beat attack*), yang digunakan untuk sinkronisasi tempo pergantian *scene* dan laju *chase* pencahayaan.

---

## 🎭 4. ENGINE 4: PEMODELAN AFEKTIF RUSSELL 2D PLANE

Fitur-fitur akustik dipetakan ke dalam koordinat 2 dimensi model *Circumplex of Affect* (Russell, 1980):
- **Valence ($V$) $\in [-1.0, +1.0]$:** Tingkat kesenangan (Sedih/Khidmat $\leftrightarrow$ Bahagia/Sukacita).
- **Arousal ($A$) $\in [-1.0, +1.0]$:** Tingkat intensitas energi (Tenang/Relaks $\leftrightarrow$ Bersemangat/Dinamis).

### 4.1 Formulasi Matematis Pembobotan
$$V = w_1 \cdot \text{Mode}_{\text{ratio}} + w_2 \cdot \text{Centroid}_{\text{norm}} + w_3 \cdot \text{MFCC}_{\text{norm}}$$
$$A = w_4 \cdot \text{RMS}_{\text{norm}} + w_5 \cdot \text{Tempo}_{\text{norm}} + w_6 \cdot \text{Onset}_{\text{norm}}$$
dengan $\sum w_i = 1.0$ untuk masing-masing dimensi.

### 4.2 Pemetaan Kuadran dalam Konteks Ibadah Gereja:
| Kuadran | Rentang $(V, A)$ | Segmen Ibadah | Karakter Musik | Nuansa Pencahayaan |
| :---: | :---: | :---: | :---: | :---: |
| **Q1 (Praise High)** | $V > 0, A > 0$ | Pujian (*Praise*) | Upbeat, cepat (120-160 BPM), akord Mayor | Warna hangat cerah (Kuning, Gold, Amber, Merah), transisi cepat |
| **Q2 (Intense Reverence)** | $V < 0, A > 0$ | Doa Peperangan / Puncak Seruan | Cepat, bertenaga, akord Minor dramatis | Magenta pekat, Crimson, Amber pekat, gerakan tegas |
| **Q3 (Deep Worship)** | $V < 0, A < 0$ | Penyembahan Mendalam | Lambat (60-80 BPM), akord Minor/Suspended | Biru laut dalam (*Deep Blue*), Ungu kontemplatif, transisi sangat lembut |
| **Q4 (Peace & Intimacy)** | $V > 0, A < 0$ | Saat Teduh / Berkat | Lambat, akustik lembut, akord Mayor tenang | Putih hangat (*Warm White*), Cyan lembut, Biru muda teduh |

---

## 🎨 5. ENGINE 5: CROSS-MODAL COLOR & PHYSICAL RGBW ENGINE

### 5.1 Pemetaan Afektif ke Ruang Warna HSV
Berdasarkan penelitian lintas-modal Palmer *et al.* (2013) dan Lindborg (2021):
- **Hue ($H$):** Sudut polar koordinat emosi:
  $$H = \left( \text{atan2}(A, V) \cdot \frac{180^\circ}{\pi} + 360^\circ \right) \pmod{360^\circ}$$
- **Saturation ($S$):** Jarak radial dari titik pusat (intensitas emosi):
  $$S = \frac{\sqrt{V^2 + A^2}}{\sqrt{2}} \in [0.0, 1.0]$$
- **Value ($V_{\text{lum}}$):** Kenyaringan audio dikalikan fader utama:
  $$V_{\text{lum}} = \text{RMS}_{\text{norm}} \cdot V_{\text{master}} \in [0.0, 1.0]$$

### 5.2 Algoritma Dekomposisi 4-Kanal Physical RGBW (Anti-Washout)
Lampu PAR LED panggung memiliki 4 kanal pemancar LED terpisah: *Red, Green, Blue,* dan *White*.
Jika nilai RGB murni (misal $R=255, G=200, B=200$) langsung ditambah kanal White $W=255$, warna akan mengalami pemudaran parah (*color washout*) menjadi putih kabur.

Untuk mempertahankan kemurnian kromatik sekaligus memanfaatkan efisiensi chip LED White:
$$\begin{aligned}
W &= \min(R, G, B) \\
R' &= R - W \\
G' &= G - W \\
B' &= B - W \\
\text{Output Final DMX} &= \text{round}\left( [R', G', B', W] \cdot V_{\text{master}} \right)
\end{aligned}$$

- Jika warna murni tersaturasi penuh (misal Merah 255, 0, 0): $W = \min(255, 0, 0) = 0$, $R'=255$. Emiter White padam, LED Merah menyala maksimal.
- Jika warna pastel lembut (misal Pink 255, 100, 100): $W = 100$, $R'=155, G'=0, B'=0$. Bagian abu-abu putih diproduksi oleh fosfor LED White yang efisien, sedangkan selisih warnanya diproduksi oleh LED Merah. Hasilnya warna pastel yang sangat jernih tanpa distorsi.

---

## 🌐 6. ENGINE 6: JARINGAN ART-NET 4 & HARDWARE ESP32 DMX512

### 6.1 Format Paket Biner ArtDmx 530 Byte
Protokol Art-Net 4 mengemas 512 kanal DMX ke dalam paket UDP datagram (Port 6454):

| Offset Byte | Panjang | Deskripsi | Nilai Tetap |
| :---: | :---: | :--- | :--- |
| **0 s.d. 7** | 8 Byte | Header Identifikasi Protokol | `b"Art-Net\x00"` |
| **8 s.d. 9** | 2 Byte | OpCode (OpOutput / OpDmx) | `0x5000` (Little-Endian: `0x00, 0x50`) |
| **10 s.d. 11** | 2 Byte | Protocol Version | `14` (Big-Endian: `0x00, 0x0E`) |
| **12** | 1 Byte | Sequence Number | `0x01` s.d. `0xFF` |
| **13** | 1 Byte | Physical Port | `0x00` |
| **14** | 1 Byte | Sub-Universe (Port-Address Low) | `0x00` (Universe 0) |
| **15** | 1 Byte | Net (Port-Address High) | `0x00` (Net 0) |
| **16 s.d. 17** | 2 Byte | DMX Data Length | `512` (Big-Endian: `0x02, 0x00`) |
| **18 s.d. 529** | 512 Byte | Payload Nilai Kanal DMX512 | Deret data 0–255 kanal 1 s.d. 512 |

Total ukuran paket: **18 byte header + 512 byte data = 530 byte**.

### 6.2 Arsitektur Firmware ESP32 Node (Dual-Core FreeRTOS)
Mikrokontroler ESP32 DevKit V1 membagi beban kerja secara mandiri pada dua inti prosesor Tensilica LX6 240 MHz:
- **Core 0 (Network Task):** Menjalankan stack WiFi (Mode SoftAP `192.168.4.1` atau Station), mendengarkan socket UDP port 6454, menerima paket Art-Net, dan menyalin data ke *double-buffer* aman (*mutex protected*).
- **Core 1 (DMX Hardware Driver Task):** Mengontrol Hardware Serial UART2 (`GPIO 17 TX, GPIO 16 RX, GPIO 4 DE/RE`) yang terhubung ke transceiver RS-485 MAX485. Mengirimkan sinyal fisik standar DMX512:
  - *Break signal* $\ge 88\ \mu\text{s}$ (Low).
  - *Mark-After-Break (MAB)* $\ge 8\ \mu\text{s}$ (High).
  - *Start Code* `0x00` + 512 byte data pada laju **250.000 baud (8N2)**.
- **Fail-safe Auto-Blackout:** Jika koneksi WiFi terputus atau tidak ada paket Art-Net selama lebih dari 10 detik, ESP32 otomatis memadamkan lampu untuk mencegah lampu menyala liar saat ibadah.

---

## 🎯 RINGKASAN UNTUK ASISTENSI DENGAN DOSEN PEMBIMBING

Jika Pak Mario Norman Syah menanyakan mekanisme sistem, peneliti dapat memaparkan intisari berikut:
1. **Bukan hanya FFT:** FFT hanyalah mesin pengubah domain pada Engine 2. Sistem ini adalah sebuah rantai komputasi lengkap (*closed-loop audio-to-light pipeline*) yang mengintegrasikan 6 sub-engine dari sampel sinyal digital hingga radiasi foton lampu LED.
2. **Sinkronisasi Ilmiah FPS:** Pemilihan hop size $H=512$ pada sampling $22.050\text{ Hz}$ menghasilkan laju tepat **$43{,}07\text{ FPS}$**, yang sinkron dengan laju transmisi fisik **DMX512 (44 FPS)**.
3. **Penyelesaian Masalah Nyata:** Di gereja lokal (seperti GIA Deliksari), sistem ini menyelesaikan keterbatasan operator manual, menghadirkan konsistensi visual lagu pujian vs penyembahan, dan memperdalam pengalaman peribadatan jemaat dalam merasakan hadirat Tuhan Yesus.
