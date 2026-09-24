# 🔬 BEDAH MATEMATIS & TEORITIS FFT (FAST FOURIER TRANSFORM) DAN STFT
## Landasan Komputasi Pemrosesan Sinyal Audio Digital untuk Sistem ZZLUXORA
### Dokumen Rekayasa & Suplemen Resmi Skripsi S1 Teknik Komputer FT UNNES

> **Peneliti:** Andreas Restuawanta Christwara (`NIM: 5312422036`)  
> **Dosen Pembimbing:** Khoirudin Fathoni, S.T., M.T. (`NIP: 19900929292015041001`)  
> **Tujuan Dokumen:** Memenuhi instruksi pendalaman teori dan perumusan matematis komprehensif mengenai *Fast Fourier Transform* (FFT) dan *Short-Time Fourier Transform* (STFT) sebagai fondasi ilmiah ekstraksi fitur musik pada naskah proposal **`script_andreas_v4.docx`** (Bab II dan Bab III).

---

## 📑 DAFTAR ISI ANALISIS
1. [Representasi Sinyal Audio Diskrit & Batas Nyquist-Shannon](#1-representasi-sinyal-audio-diskrit--batas-nyquist-shannon)
2. [Discrete Fourier Transform (DFT): Fondasi Matematis & Analisis Kompleksitas](#2-discrete-fourier-transform-dft-fondasi-matematis--analisis-kompleksitas)
3. [Algoritma Fast Fourier Transform (FFT) Cooley-Tukey Radix-2](#3-algoritma-fast-fourier-transform-fft-cooley-tukey-radix-2)
4. [Karakteristik Sinyal Musik Non-Stasioner & Urgensi STFT](#4-karakteristik-sinyal-musik-non-stasioner--urgensi-stft)
5. [Analisis Windowing & Mitigasi Fenomena Spectral Leakage](#5-analisis-windowing--mitigasi-fenomena-spectral-leakage)
6. [Formulasi Diskrit Short-Time Fourier Transform (STFT)](#6-formulasi-diskrit-short-time-fourier-transform-stft)
7. [Prinsip Ketidakpastian Waktu-Frekuensi (Gabor Limit)](#7-prinsip-ketidakpastian-waktu-frekuensi-gabor-limit)
8. [Penurunan Fitur Akustik Spektral Berbasis Spektrum FFT](#8-penurunan-fitur-akustik-spektral-berbasis-spektrum-fft)
   - 8.1 Magnitude Spectrum & Power Spectrum
   - 8.2 Root Mean Square (RMS) Energy
   - 8.3 Spectral Centroid (Kecerahan Timbre / Brightness)
   - 8.4 Chroma STFT (Pitch Class Profile 12-Semitone)
   - 8.5 Mel-Frequency Cepstral Coefficients (MFCC)
9. [Pipeline Integrasi ke Model Emosi Russell & Protokol Art-Net DMX512](#9-pipeline-integrasi-ke-model-emosi-russell--protokol-art-net-dmx512)

---

## 1. Representasi Sinyal Audio Diskrit & Batas Nyquist-Shannon

Sinyal suara fisik yang dihasilkan oleh instrumen musik maupun vokal dalam lagu rohani merupakan gelombang mekanik kontinu bertekanan udara $x(t)$ dalam domain waktu kontinu ($t \in \mathbb{R}$). Ketika ditangkap oleh transduser mikrofon dan diproses oleh sistem komputasi digital, sinyal analog tersebut harus melalui proses kuantisasi dan pencuplikan (*sampling*) oleh *Analog-to-Digital Converter* (ADC).

### 1.1 Persamaan Diskritisasi
Sinyal audio kontinu $x(t)$ disampling pada interval waktu periodik $T_s$ (dalam detik), menghasilkan deret diskrit $x[n]$:
$$x[n] = x(n \cdot T_s) = x\left(\frac{n}{f_s}\right), \quad n \in \mathbb{Z}$$
di mana:
- $n$ adalah indeks sampel diskrit ($n = 0, 1, 2, \dots, L-1$ dengan $L$ adalah total sampel audio).
- $T_s$ adalah periode sampling (*sampling interval*).
- $f_s = \frac{1}{T_s}$ adalah frekuensi sampling (*sampling rate*) dalam Hertz (Hz).

### 1.2 Teorema Kriteria Nyquist-Shannon
Agar sinyal diskrit $x[n]$ dapat merepresentasikan seluruh informasi frekuensi dari sinyal analog asli tanpa mengalami distorsi distorsi aliasing (*frequency folding*), frekuensi sampling $f_s$ harus memenuhi:
$$f_s \ge 2 \cdot f_{\max}$$
di mana $f_{\max}$ adalah frekuensi tertinggi yang terkandung di dalam sinyal audio.

Batas frekuensi pendengaran manusia berkisar antara $20\text{ Hz}$ hingga $20.000\text{ Hz}$ ($20\text{ kHz}$). Pada sistem audio CD standar digunakan $f_s = 44.100\text{ Hz}$, sedangkan pada komputasi *Music Information Retrieval* (MIR) dan pustaka Librosa, sinyal sering di-*downsample* ke $f_s = 22.050\text{ Hz}$. Dengan $f_s = 22.050\text{ Hz}$, frekuensi Nyquist adalah:
$$f_{\text{Nyquist}} = \frac{f_s}{2} = 11.025\text{ Hz}$$
Frekuensi ini sudah sangat mencukupi untuk mencakup seluruh frekuensi dasar (*fundamental frequency* $f_0$) instrumen musik panggung (piano, gitar, bass, vokal manusia berkisar antara $27{,}5\text{ Hz}$ hingga $4.200\text{ Hz}$) serta harmonik dominan pertama hingga ketiga, sekaligus mereduksi beban komputasi sebesar $50\%$.

---

## 2. Discrete Fourier Transform (DFT): Fondasi Matematis & Analisis Kompleksitas

Untuk menganalisis komponen nada, harmoni, dan timbre lagu, sinyal dalam domain waktu $x[n]$ (yang hanya menunjukkan fluktuasi amplitudo terhadap waktu) harus ditransformasikan ke dalam domain frekuensi (yang menunjukkan spektrum kandungan frekuensi).

### 2.1 Definisi Matematis DFT
Untuk suatu blok sinyal diskrit $x[n]$ dengan panjang $N$ sampel ($n = 0, 1, \dots, N-1$), *Discrete Fourier Transform* (DFT) mendefinisikan transformasi ke dalam deret bilangan kompleks $X[k]$:

$$X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j \frac{2\pi}{N} kn}, \quad k = 0, 1, \dots, N-1$$

Berdasarkan rumus Euler:
$$e^{-j \theta} = \cos(\theta) - j \sin(\theta)$$
maka persamaan DFT dapat diuraikan secara eksplisit menjadi komponen riil dan imajiner:

$$X[k] = \sum_{n=0}^{N-1} x[n] \cos\left(\frac{2\pi kn}{N}\right) - j \sum_{n=0}^{N-1} x[n] \sin\left(\frac{2\pi kn}{N}\right)$$

di mana:
- $j = \sqrt{-1}$ adalah unit bilangan imajiner.
- $k$ adalah indeks frekuensi diskrit (*frequency bin*).
- $N$ adalah jumlah titik transformasi (*transform length* / *frame length*).
- Komponen riil $\text{Re}(X[k]) = \sum_{n=0}^{N-1} x[n] \cos\left(\frac{2\pi kn}{N}\right)$.
- Komponen imajiner $\text{Im}(X[k]) = -\sum_{n=0}^{N-1} x[n] \sin\left(\frac{2\pi kn}{N}\right)$.

### 2.2 Sifat Simetri Konjugat pada Sinyal Audio Riil
Karena sampel audio $x[n]$ merupakan nilai riil murni ($x[n] \in \mathbb{R}$), spektrum DFT memiliki sifat simetri konjugat Hermitian:
$$X[N - k] = X^*[k]$$
di mana $*$ melambangkan konjugat kompleks. Konsekuensinya:
- Nilai magnitude bin frekuensi di atas $N/2$ adalah cerminan dari bin di bawah $N/2$:
  $$|X[N - k]| = |X[k]|$$
- Oleh karena itu, dalam aplikasi praktis pemrosesan audio panggung, kita hanya perlu menghitung dan menganalisis sebanyak:
  $$N_{\text{bins}} = \frac{N}{2} + 1$$
  yaitu dari bin $k = 0$ (komponen DC / frekuensi $0\text{ Hz}$) hingga bin $k = N/2$ (frekuensi Nyquist $f_s/2$).

### 2.3 Analisis Kompleksitas Komputasi DFT Langsung
Untuk menghitung satu nilai bin $X[k]$ secara langsung dari definisi:
- Diperlukan $N$ perkalian kompleks antara sampel $x[n]$ dengan *twiddle factor* $e^{-j \frac{2\pi}{N} kn}$.
- Diperlukan $N - 1$ penjumlahan kompleks.

Karena terdapat $N$ nilai $k$ yang harus dihitung, total operasi perhitungan langsung adalah:
$$\text{Kompleksitas DFT} = \mathcal{O}(N^2)$$

#### Implikasi Kinerja pada Sistem Real-Time:
Jika sebuah frame audio memiliki panjang $N = 2048$ sampel:
$$\text{Operasi DFT} = 2048^2 = 4.194.304 \text{ operasi perkalian kompleks per frame}$$
Jika dalam 1 detik audio terdapat 43 frame yang harus diproses, sistem membutuhkan lebih dari **180 juta operasi perkalian per detik** hanya untuk transformasi Fourier dasar. Komputasi seberat ini akan menyebabkan *buffer underrun*, lonjakan penggunaan CPU, dan keterlambatan visual (*latency delay*) di atas 100 ms pada sistem pencahayaan panggung.

---

## 3. Algoritma Fast Fourier Transform (FFT) Cooley-Tukey Radix-2

Untuk mengatasi hambatan kompleksitas $\mathcal{O}(N^2)$, digunakan algoritma **Fast Fourier Transform (FFT)** yang dipublikasikan oleh J. W. Cooley dan J. W. Tukey pada tahun 1965. Algoritma ini mengeksploitasi periodisitas dan simetri dari faktor fase (*twiddle factor*) $W_N = e^{-j \frac{2\pi}{N}}$ dengan pendekatan *divide-and-conquer* (Radix-2 Decimation-in-Time / DIT).

### 3.1 Penurunan Matematis Dekomposisi DIT
Asumsikan panjang frame $N$ merupakan bilangan pangkat dua ($N = 2^p$, misal $N = 512, 1024, 2048$). Kita dapat memecah penjumlahan deret $n$ menjadi dua kelompok:
1. Indeks genap: $n = 2m$, dengan $m = 0, 1, \dots, \frac{N}{2} - 1$
2. Indeks ganjil: $n = 2m + 1$, dengan $m = 0, 1, \dots, \frac{N}{2} - 1$

Substitusikan ke persamaan DFT:
$$X[k] = \sum_{m=0}^{\frac{N}{2}-1} x[2m] \cdot e^{-j \frac{2\pi}{N} k(2m)} + \sum_{m=0}^{\frac{N}{2}-1} x[2m+1] \cdot e^{-j \frac{2\pi}{N} k(2m+1)}$$

Sederhanakan eksponen pada suku genap:
$$e^{-j \frac{2\pi}{N} k(2m)} = e^{-j \frac{2\pi}{N/2} km}$$

Dan uraikan eksponen pada suku ganjil:
$$e^{-j \frac{2\pi}{N} k(2m+1)} = e^{-j \frac{2\pi}{N} k} \cdot e^{-j \frac{2\pi}{N/2} km} = W_N^k \cdot e^{-j \frac{2\pi}{N/2} km}$$

Dengan demikian, persamaan DFT berukuran $N$ terbagi menjadi dua buah DFT berukuran $N/2$:
$$X[k] = E[k] + W_N^k \cdot O[k]$$

di mana:
- $E[k] = \sum_{m=0}^{\frac{N}{2}-1} x[2m] \cdot e^{-j \frac{2\pi}{N/2} km}$ adalah DFT dari sub-deret genap (*Even*).
- $O[k] = \sum_{m=0}^{\frac{N}{2}-1} x[2m+1] \cdot e^{-j \frac{2\pi}{N/2} km}$ adalah DFT dari sub-deret ganjil (*Odd*).
- $W_N^k = e^{-j \frac{2\pi k}{N}}$ adalah *twiddle factor*.

### 3.2 Sifat Periodisitas & Operasi Kupu-Kupu (*Butterfly Calculation*)
Karena $E[k]$ dan $O[k]$ adalah DFT periodik berukuran $N/2$, maka:
$$E\left[k + \frac{N}{2}\right] = E[k], \quad O\left[k + \frac{N}{2}\right] = O[k]$$

Sedangkan untuk *twiddle factor*:
$$W_N^{k + N/2} = e^{-j \frac{2\pi (k + N/2)}{N}} = e^{-j \frac{2\pi k}{N}} \cdot e^{-j \pi} = -W_N^k$$

Hubungan ini menghasilkan pasangan komputasi simetris yang sangat efisien yang dikenal sebagai **Butterfly Operation**:
$$\begin{cases}
X[k] &= E[k] + W_N^k \cdot O[k] \\
X\left[k + \frac{N}{2}\right] &= E[k] - W_N^k \cdot O[k]
\end{cases} \quad \text{untuk } k = 0, 1, \dots, \frac{N}{2} - 1$$

### 3.3 Perbandingan Efisiensi DFT vs FFT
Proses dekomposisi ini diulang secara rekursif sebanyak $\log_2 N$ tahapan (*stages*). Pada setiap tahap dilakukan $N$ operasi dasar.
$$\text{Kompleksitas FFT} = \mathcal{O}(N \log_2 N)$$

| Parameter Panjang Frame ($N$) | Operasi DFT $\mathcal{O}(N^2)$ | Operasi FFT $\mathcal{O}(N \log_2 N)$ | Faktor Percepatan (*Speedup Factor*) |
| :---: | :---: | :---: | :---: |
| **512** | 262.144 | 4.608 | **56,9 kali lebih cepat** |
| **1024** | 1.048.576 | 10.240 | **102,4 kali lebih cepat** |
| **2048** (Standar ZZLUXORA) | 4.194.304 | 22.528 | **186,2 kali lebih cepat** |
| **4096** | 16.777.216 | 49.152 | **341,3 kali lebih cepat** |

**Kesimpulan Ilmiah:** Penggunaan algoritma FFT mereduksi beban komputasi hingga **99,46%** pada frame 2048 sampel, memungkinkan sistem ZZLUXORA mengekstraksi seluruh fitur audio secara instan dengan waktu komputasi < 5 ms per frame.

---

## 4. Karakteristik Sinyal Musik Non-Stasioner & Urgensi STFT

Meskipun FFT sangat efisien, penerapan FFT standar secara langsung terhadap keseluruhan berkas lagu rohani (misal berdurasi 4 menit) memiliki kelemahan fatal:

1. **Sinyal Musik Bersifat Non-Stasioner:**
   Komposisi musik terdiri dari struktur temporal yang dinamis (bagian *intro*, bait/*verse*, refrain/*chorus*, jembatan/*bridge*, dan penutup/*ending*). Karakteristik frekuensi, tangga nada, intensitas volume, dan instrumen berubah secara drastis dari detik ke detik.
2. **Kehilangan Lokalisasi Waktu:**
   FFT standar menghitung integral/penjumlahan terhadap seluruh rentang waktu dari $t=0$ hingga $t=T_{\text{lagu}}$. Akibatnya, spektrum FFT hanya memberi tahu *frekuensi apa saja yang ada di dalam lagu*, namun **tidak dapat memberi tahu kapan frekuensi tersebut muncul**.
3. **Kebutuhan Sistem Lighting Panggung:**
   Pencahayaan panggung membutuhkan respons visual yang berubah mengikuti ketukan dan suasana detik demi detik. Jika lagu beralih dari suasana teduh (*verse*) ke puncak pujian yang meledak (*drop chorus*), sistem pencahayaan harus mendeteksi perubahan tersebut secara instan.

Oleh karena itu, transformasi yang wajib digunakan adalah **Short-Time Fourier Transform (STFT)**.

---

## 5. Analisis Windowing & Mitigasi Fenomena Spectral Leakage

Dalam STFT, sinyal audio dipotong-potong menjadi potongan-potongan pendek (*frames*). Secara matematis, pemotongan ini setara dengan mengalikan sinyal $x[n]$ dengan sebuah fungsi bobot yang disebut **Window Function** $w[n]$.

### 5.1 Fenomena Spectral Leakage
Jika frame dipotong menggunakan jendela persegi (*Rectangular Window*):
$$w_{\text{rect}}[n] = \begin{cases} 1, & 0 \le n \le N-1 \\ 0, & \text{lainnya} \end{cases}$$

Di domain frekuensi, fungsi persegi setara dengan konvolusi sinyal dengan fungsi $\text{sinc}(f) = \frac{\sin(\pi f)}{\pi f}$. Pemotongan mendadak pada tepi frame menciptakan diskontinuitas artifisial tajam pada batas sinyal. Akibatnya, energi frekuensi dari suatu nada murni akan "bocor" ke bin-bin frekuensi di sekitarnya yang membentuk puncak-puncak sampingan besar (*high sidelobes*). Fenomena ini disebut **Spectral Leakage**.

*Spectral leakage* menyebabkan deteksi nada akord dan ekstraksi Chroma STFT menjadi bias dan kabur, karena energi nada mayor/minor tercampur dengan frekuensi harmonik palsu.

### 5.2 Fungsi Hann (Hanning) Window pada ZZLUXORA
Untuk meredam *spectral leakage*, amplitudo sinyal pada tepi frame harus diturunkan secara halus (*tapering*) menuju nol. Pada sistem ZZLUXORA, digunakan fungsi jendela **Hann (Hanning) Window**:

$$w[n] = 0{,}5 \left[ 1 - \cos\left( \frac{2\pi n}{N - 1} \right) \right] = \sin^2\left( \frac{\pi n}{N - 1} \right), \quad 0 \le n \le N-1$$

#### Karakteristik Akustik Hann Window:
- Nilai di kedua ujung frame: $w[0] = w[N-1] = 0$.
- Nilai di tengah frame: $w[(N-1)/2] = 1$.
- Meredam *sidelobe level* hingga **-31,5 dB** (jauh lebih baik dibanding *rectangular window* yang hanya -13 dB).
- Memberikan kompromi optimal antara pencegahan kebocoran spektral dan ketajaman puncak frekuensi nada utama.

---

## 6. Formulasi Diskrit Short-Time Fourier Transform (STFT)

### 6.1 Persamaan Matematis Diskrit STFT
Dengan menggabungkan konsep *sliding window* berbobot Hann dan algoritma FFT, formulasi matematis STFT diskrit yang diimplementasikan pada komputasi perangkat lunak didefinisikan sebagai:

$$X[m, k] = \sum_{n=0}^{N-1} x[n + m \cdot H] \cdot w[n] \cdot e^{-j \frac{2\pi}{N} kn}$$

di mana:
- $m \in \{0, 1, \dots, M-1\}$ adalah **indeks frame waktu** ($M$ adalah total frame dalam lagu).
- $k \in \left\{0, 1, \dots, \frac{N}{2}\right\}$ adalah **indeks bin frekuensi**.
- $N$ adalah panjang jendela analisis (*Window Length* / *FFT size*), bernilai $2048$ sampel.
- $H$ adalah jarak pergeseran antar frame (*Hop Length* / *Stride*), bernilai $512$ sampel.
- $w[n]$ adalah fungsi jendela Hann berukuran $N$.
- $x[n + m \cdot H]$ adalah segmen sinyal audio yang sedang dianalisis pada jendela ke-$m$.

### 6.2 Konversi ke Satuan Fisik Waktu dan Frekuensi
Matriks STFT $X[m, k]$ berukuran $\left( \frac{N}{2} + 1 \right) \times M$ memetakan setiap sel koordinat $(m, k)$ ke satuan fisik nyata:

1. **Waktu Fisik ($t_m$) dalam Detik:**
   $$t_m = \frac{m \cdot H}{f_s}$$
2. **Frekuensi Fisik ($f_k$) dalam Hertz:**
   $$f_k = \frac{k \cdot f_s}{N}$$
3. **Lebar Pita per Bin Frekuensi ($\Delta f$):**
   $$\Delta f = \frac{f_s}{N} = \frac{22050}{2048} \approx 10{,}7666\text{ Hz}$$
4. **Interval Waktu Pembaruan Frame ($\Delta t_{\text{hop}}$):**
   $$\Delta t_{\text{hop}} = \frac{H}{f_s} = \frac{512}{22050} \approx 0{,}02322\text{ detik} = 23{,}22\text{ ms}$$

Frame rate output visual yang dihasilkan adalah:
$$\text{FPS} = \frac{1}{\Delta t_{\text{hop}}} = \frac{22050}{512} \approx 43{,}07\text{ frame per detik (fps)}$$

Nilai **43 fps** ini identik dan sinkron sempurna dengan standar laju transmisi maksimum paket **DMX512-A fisik (44 fps)**, memastikan transisi fader lampu PAR LED panggung berlangsung sangat mulus (*ultra-smooth crossfading*) tanpa adanya efek getaran visual (*visual stepping/jittering*).

---

## 7. Prinsip Ketidakpastian Waktu-Frekuensi (Gabor Limit)

Dalam analisis sinyal waktu-frekuensi berlaku batas fundamental fisika yang dikenal sebagai **Prinsip Ketidakpastian Heisenberg-Gabor**:
$$\Delta t \cdot \Delta f \ge \frac{1}{4\pi}$$

Keterbatasan ini menyatakan bahwa kita tidak dapat memperoleh resolusi waktu yang sangat tinggi dan resolusi frekuensi yang sangat tinggi secara bersamaan menggunakan satu jendela transformasi STFT konstan:

1. **Jika Ukuran Window $N$ Terlalu Besar (misal $N = 8192$):**
   - Resolusi frekuensi sangat tinggi ($\Delta f = 22050 / 8192 \approx 2{,}69\text{ Hz}$), sangat mudah membedakan nada-nada rendah di frekuensi bass.
   - Namun resolusi waktu sangat buruk ($\Delta t = 8192 / 22050 \approx 371\text{ ms}$). Transien ketukan drum, petikan senar, dan hentakan irama akan buram dan terlambat dideteksi lebih dari 0,3 detik.
2. **Jika Ukuran Window $N$ Terlalu Kecil (misal $N = 256$):**
   - Resolusi waktu sangat tajam ($\Delta t = 256 / 22050 \approx 11{,}6\text{ ms}$), deteksi *onset* ketukan drum sangat presisi.
   - Namun resolusi frekuensi sangat kasar ($\Delta f = 22050 / 256 \approx 86{,}13\text{ Hz}$). Pada frekuensi bass dan nada tengah, jarak antar seminada (*semitone*) kurang dari $10\text{ Hz}$ sehingga sistem tidak dapat membedakan nada C, D, E, dan akord Mayor vs Minor.

### Rationale Pemilihan Parameter pada ZZLUXORA:
Dengan menetapkan $f_s = 22.050\text{ Hz}$, $N = 2048$, dan $H = 512$:
- **Resolusi Frekuensi:** $\Delta f \approx 10{,}77\text{ Hz}$ cukup untuk menganalisis akord dan pusat energi instrumen vokal/gitar.
- **Resolusi Waktu Efektif:** Hop step $23{,}22\text{ ms}$ memberikan respons deteksi *beat/transient* dengan latensi jauh di bawah ambang batas deteksi keterlambatan mata manusia ($< 40\text{ ms}$).

---

## 8. Penurunan Fitur Akustik Spektral Berbasis Spektrum FFT

Matriks hasil STFT $X[m, k]$ merupakan representasi bilangan kompleks:
$$X[m, k] = |X[m, k]| \cdot e^{j \phi[m, k]}$$

Seluruh fitur musik utama dalam sistem ZZLUXORA diekstraksi langsung dari nilai spektrum ini:

### 8.1 Magnitude Spectrogram & Power Spectrogram
Magnitude spektrum mengukur amplitudo absolut dari setiap komponen frekuensi pada frame waktu ke-$m$:
$$|X[m, k]| = \sqrt{\text{Re}(X[m, k])^2 + \text{Im}(X[m, k])^2}$$

Sedangkan Power Spectrogram $S[m, k]$ mengukur daya energi sinyal:
$$S[m, k] = |X[m, k]|^2$$

---

### 8.2 Root Mean Square (RMS) Energy
RMS Energy merepresentasikan kenyaringan (*loudness*) dan intensitas tenaga musik pada setiap frame waktu $m$. Berdasarkan **Teorema Parseval**, total energi dalam domain waktu setara dengan total energi dalam domain frekuensi FFT:

$$\text{RMS}[m] = \sqrt{ \frac{1}{N} \sum_{n=0}^{N-1} |x[n + mH] \cdot w[n]|^2 }$$

Nilai ini kemudian dinormalisasi ke rentang $[0{,}0, 1{,}0]$:
$$\text{RMS}_{\text{norm}}[m] = \frac{\text{RMS}[m] - \text{RMS}_{\min}}{\text{RMS}_{\max} - \text{RMS}_{\min}}$$

**Peran dalam Lighting:** Nilai $\text{RMS}_{\text{norm}}[m]$ dihubungkan langsung ke parameter **Master Dimmer** lampu PAR LED. Bagian lagu yang tenang memiliki nilai RMS rendah (lampu meredup lembut), sedangkan saat puncak lagu (*refrain/chorus*), nilai RMS mendekati 1,0 (lampu menyala maksimal).

---

### 8.3 Spectral Centroid (Kecerahan Timbre / Brightness)
Spectral Centroid menunjukkan titik pusat massa (*center of mass*) dari spektrum frekuensi audio pada frame ke-$m$. Secara fisika, fitur ini menunjukkan apakah energi audio didominasi oleh frekuensi rendah (*bass/drum kick*) atau frekuensi tinggi (*cymbal, gitar melodi, vokal tinggi*).

#### Rumus Matematis:
$$\text{Centroid}[m] = \frac{\sum_{k=0}^{N/2} f_k \cdot |X[m, k]|}{\sum_{k=0}^{N/2} |X[m, k]|} = \frac{\sum_{k=0}^{N/2} \left( \frac{k \cdot f_s}{N} \right) \cdot |X[m, k]|}{\sum_{k=0}^{N/2} |X[m, k]|}$$

di mana:
- $f_k$ adalah frekuensi fisik dari bin ke-$k$ dalam Hertz.
- $|X[m, k]|$ adalah bobot magnitude pada bin ke-$k$.
- Pembilang adalah perkalian berbobot frekuensi terhadap magnitudenya.
- Penyebut adalah total magnitudo energi pada frame tersebut.

#### Interpretasi Akustik & Visual:
- **Nilai Centroid Rendah (< 1.500 Hz):** Musik bernuansa tebal, berat, dominan instrumen bass/cello, tempo tenang $\to$ dipetakan ke koordinat Arousal rendah dan warna kontemplatif (*cool blue/deep purple*).
- **Nilai Centroid Tinggi (> 3.000 Hz):** Musik bernuansa cerah (*bright*), tajam, banyak instrumen brass/perkusi $\to$ dipetakan ke koordinat Arousal tinggi dan warna energetik (*bright amber/yellow/white*).

---

### 8.4 Chroma STFT (Pitch Class Profile 12-Semitone)
Fitur Chroma memproyeksikan seluruh energi spektral frekuensi FFT ke dalam 12 kelas nada kromatik barat (*12 semitone pitch classes*):
$$\text{Chroma} = \{C, C\sharp, D, D\sharp, E, F, F\sharp, G, G\sharp, A, A\sharp, B\}$$
tanpa mempedulikan oktaf nada tersebut. 

#### Mekanisme Pemetaan dari Bin FFT ke Kelas Nada:
Hubungan antara frekuensi kontinu $f$ dengan nomor nada MIDI $p$ mengikuti skala logaritmik sama rata (*equal temperament* dengan acuan nada $A_4 = 440\text{ Hz}$ pada MIDI 69):
$$p(f) = 12 \cdot \log_2\left( \frac{f}{440} \right) + 69$$

Setiap bin frekuensi FFT $k$ memiliki frekuensi $f_k = \frac{k \cdot f_s}{N}$. Nilai nada kromatik $c \in \{0, 1, \dots, 11\}$ ditentukan oleh modulo 12:
$$c(k) = \text{round}(p(f_k)) \pmod{12}$$

Energi pada kelas nada $c$ pada frame $m$ dihitung dengan menjumlahkan magnitudo seluruh bin FFT yang bersesuaian:
$$\text{Chroma}[m, c] = \sum_{k \in \mathcal{K}_c} |X[m, k]|$$
di mana $\mathcal{K}_c$ adalah himpunan bin FFT yang terpetakan ke kelas nada $c$.

#### Analisis Modalitas Mayor vs Minor untuk Valence:
Vektor Chroma 12 dimensi $\mathbf{Chroma}[m]$ dikorelasikan dengan template profil tonal Krumhansl-Schmuckler untuk tangga nada Mayor ($\mathbf{T}_{\text{major}}$) dan Minor ($\mathbf{T}_{\text{minor}}$):
$$\rho_{\text{major}} = \text{corr}(\mathbf{Chroma}[m], \mathbf{T}_{\text{major}}), \quad \rho_{\text{minor}} = \text{corr}(\mathbf{Chroma}[m], \mathbf{T}_{\text{minor}})$$
- Jika $\rho_{\text{major}} > \rho_{\text{minor}}$: Musik cenderung berkarakter sukacita (*happy/uplifting*), menghasilkan nilai **Valence positif ($V > 0$)**.
- Jika $\rho_{\text{minor}} \ge \rho_{\text{major}}$: Musik cenderung berkarakter sendu/khidmat (*solemn/sad*), menghasilkan nilai **Valence negatif ($V < 0$)**.

---

### 8.5 Mel-Frequency Cepstral Coefficients (MFCC)
MFCC mengekstraksi amplop spektral (*spectral envelope*) yang merepresentasikan tekstur timbre vokal dan instrumen, disesuaikan dengan kurva persepsi pendengaran telinga manusia.

Tahapan komputasi dari spektrum FFT:
1. **Perhitungan Power Spectrum FFT:** $S[m, k] = |X[m, k]|^2$.
2. **Transformasi ke Skala Frekuensi Mel:**
   $$m_{\text{mel}} = 2595 \cdot \log_{10}\left(1 + \frac{f}{700}\right)$$
3. **Penerapan Triangular Filterbank:** Mengalikan spektrum daya dengan $B$ buah filter segitiga Mel ($B = 40$ filter):
   $$\tilde{S}[m, b] = \sum_{k=0}^{N/2} S[m, k] \cdot H_b[k], \quad b = 1, 2, \dots, B$$
4. **Transformasi Logaritmik:** Merefleksikan persepsi kenyaringan logaritmik manusia:
   $$\tilde{L}[m, b] = \log(\tilde{S}[m, b] + \epsilon)$$
5. **Discrete Cosine Transform (DCT-II):** Merekolerasikan energi antar filterbank:
   $$\text{MFCC}[m, l] = \sum_{b=1}^B \tilde{L}[m, b] \cdot \cos\left( \frac{\pi l (b - 0{,}5)}{B} \right), \quad l = 0, 1, \dots, 12$$

13 koefisien MFCC pertama diambil untuk membedakan karakteristik instrumen akustik (gitar akustik/piano pada lagu *worship*) dengan instrumen elektrik/distorsi (gitar listrik/drum pada lagu *praise*).

---

## 9. Pipeline Integrasi ke Model Emosi Russell & Protokol Art-Net DMX512

Setelah fitur-fitur berbasis FFT diekstraksi pada setiap frame $m$, seluruh nilai disatukan dalam model afektif dan dialirkan ke lampu panggung melalui protokol Art-Net DMX512:

```text
[ AUDIO LAGU (.wav/.mp3) ]
          │
          ▼
[ SAMPLING & WINDOWING ]
  fs = 22.050 Hz, N = 2048, H = 512, Hann Window w[n]
          │
          ▼
[ KOMPUTASI FAST FOURIER TRANSFORM (FFT) ]
  X[m, k] = FFT(x[n + mH] * w[n])  --> Kompleksitas O(N log N)
          │
          ▼
[ EKSTRAKSI FITUR SPEKTRAL ]
  ├─ RMS Energy          --> Indikator Loudness
  ├─ Spectral Centroid   --> Indikator Kecerahan Timbre
  ├─ Chroma STFT         --> Deteksi Tangga Nada (Mayor vs Minor)
  └─ MFCC (13 Koefisien) --> Karakteristik Tekstur Timbre
          │
          ▼
[ MODEL AFEKTIF RUSSELL (VALENCE-AROUSAL 2D PLANE) ]
  • Valence (V)  = w1*(Mayor/Minor Ratio) + w2*(Centroid_norm) + w3*(MFCC_1)  [-1.0 s/d +1.0]
  • Arousal (A)  = w4*(RMS_norm) + w5*(Tempo_norm) + w6*(Onset_Strength)      [-1.0 s/d +1.0]
          │
          ▼
[ TRANSFORMASI RUANG WARNA CROSS-MODAL ]
  • Hue (H)        = (atan2(A, V) * 180 / PI + 360) mod 360  [0° - 360°]
  • Saturation (S) = sqrt(V^2 + A^2) / sqrt(2)                [0.0 - 1.0]
  • Dimmer / Val   = RMS_norm * Master_Fader                  [0.0 - 1.0]
  • HSV --> Standard RGB [0 - 255]
          │
          ▼
[ DEKOMPOSISI 4-KANAL PHYSICAL RGBW (PAR LED) ]
  W   = min(R, G, B)
  R'  = R - W
  G'  = G - W
  B'  = B - W
  Output Kanal = [R', G', B', W] * Dimmer
          │
          ▼
[ TRANSMISI NETWORK ART-NET 4 UDP (PORT 6454) ]
  OpOutput / ArtDmx Packet (Universe 0)
  Broadcast / Unicast 43 FPS ke ESP32 Node (192.168.4.1)
          │
          ▼
[ MIKROKONTROLER ESP32 + MAX485 TRANSCEIVER ]
  Hardware UART2 Driver (250.000 bps, 8N2)
          │
          ▼
[ LAMPU PAR LED PANGGUNG REAL-TIME DMX512 ]
```

---

## 📌 Catatan Penyesuaian Naskah Proposal v4 (Bab II & Bab III):
1. **Bab II (Subbab 2.2.1):** Gantilah penjelasan FFT 3 kalimat lama dengan penurunan matematis dari Bagian 1, 2, 3, 5, 6, dan 8 pada dokumen ini.
2. **Bab II (Subbab 2.2.1 Butir b):** Cantumkan perumusan matematis eksak untuk RMS, Spectral Centroid (integrasi frekuensi bin), dan Chroma STFT (modulo 12 semitone).
3. **Bab III (Subbab 3.6 / 3.9):** Masukkan spesifikasi parameter FFT ($f_s = 22.050\text{ Hz}, N = 2048, H = 512$, Hann Window) serta justifikasi keselarasan 43 fps dengan standar laju transmisi DMX512.
