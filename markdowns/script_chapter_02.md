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

*Digital Signal Processing* (DSP) merupakan cabang ilmu rekayasa komputasi yang menangani representasi, transformasi, dan ekstraksi informasi dari sinyal-sinyal dalam domain digital. Dalam konteks penelitian ini, DSP menjadi pilar utama untuk mengekstraksi fitur-fitur akustik dan harmonik dari berkas audio lagu rohani. Sub-bidang yang secara khusus mendasari ekstraksi informasi musikal ini adalah *Music Information Retrieval* (MIR), yang mengkaji teknik komputasi untuk mengenali ritme, melodi, harmoni, timbre, dan dinamika struktural dari rekaman audio musik [2][4][21].

#### a. Diskritisasi Sinyal Audio dan Kriteria Nyquist-Shannon

Sinyal suara fisik yang dihasilkan oleh instrumen musik dan vokal penyembahan merupakan gelombang tekanan udara mekanik kontinu $x(t)$ dalam domain waktu kontinu ($t \in \mathbb{R}$). Ketika ditangkap oleh transduser mikrofon dan dikuantisasi oleh *Analog-to-Digital Converter* (ADC), sinyal dicuplik pada interval waktu periodik $T_s$ (detik), menghasilkan deret diskrit $x[n]$:

$$x[n] = x(n \cdot T_s) = x\left(\frac{n}{f_s}\right), \quad n \in \mathbb{Z}$$

di mana $n$ adalah indeks sampel diskrit ($n = 0, 1, 2, \dots, L-1$ dengan $L$ adalah total panjang sampel) dan $f_s = \frac{1}{T_s}$ adalah frekuensi pencuplikan (*sampling rate*) dalam satuan Hertz (Hz). Berdasarkan Teorema Kriteria Nyquist-Shannon, agar deret diskrit $x[n]$ mampu merekonstruksi sinyal analog asli tanpa mengalami distorsi lipatan frekuensi (*aliasing*), frekuensi pencuplikan harus memenuhi:

$$f_s \ge 2 \cdot f_{\max}$$

di mana $f_{\max}$ adalah komponen frekuensi tertinggi yang dikandung oleh sinyal audio. Spektrum pendengaran manusia mencakup rentang $20\text{ Hz}$ hingga $20.000\text{ Hz}$. Pada sistem audio CD standar digunakan $f_s = 44.100\text{ Hz}$. Namun, dalam standar komputasi MIR dan pustaka Librosa [21], sinyal audio di-*downsample* ke frekuensi standar $f_s = 22.050\text{ Hz}$. Dengan $f_s = 22.050\text{ Hz}$, frekuensi batas Nyquist adalah:

$$f_{\text{Nyquist}} = \frac{f_s}{2} = 11.025\text{ Hz}$$

Batas frekuensi $11.025\text{ Hz}$ ini terbukti sangat memadai untuk merepresentasikan nada dasar (*fundamental frequency* $f_0$) instrumen musik panggung (rentang nada piano dan vokal manusia berkisar antara $27{,}5\text{ Hz}$ hingga $4.200\text{ Hz}$) serta harmonik dominan instrumen musik, sekaligus menghemat beban komputasi CPU dan memori hingga $50\%$ dibandingkan pemrosesan pada laju $44.100\text{ Hz}$.

#### b. Discrete Fourier Transform (DFT) dan Kompleksitas Komputasi

Sinyal audio dalam domain waktu $x[n]$ hanya merepresentasikan fluktuasi amplitudo terhadap waktu, sehingga tidak mampu memperlihatkan kandungan nada dan spektrum frekuensi yang menyusun lagu tersebut. Untuk mengubah sinyal dari domain waktu ke domain frekuensi, digunakan *Discrete Fourier Transform* (DFT).

Untuk suatu blok sinyal diskrit sepanjang $N$ sampel ($n = 0, 1, \dots, N-1$), DFT mentransformasikan sampel waktu ke dalam spektrum frekuensi diskrit $X[k]$ yang berupa deret bilangan kompleks:

$$X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j \frac{2\pi}{N} kn}, \quad k = 0, 1, \dots, N-1$$

Berdasarkan identitas Euler $e^{-j\theta} = \cos(\theta) - j\sin(\theta)$, formulasi DFT dapat diuraikan secara eksplisit menjadi komponen riil dan imajiner:

$$X[k] = \sum_{n=0}^{N-1} x[n] \cos\left(\frac{2\pi kn}{N}\right) - j \sum_{n=0}^{N-1} x[n] \sin\left(\frac{2\pi kn}{N}\right)$$

di mana:
- $j = \sqrt{-1}$ adalah unit bilangan imajiner.
- $k$ adalah indeks komponen frekuensi diskrit (*frequency bin*).
- $N$ adalah ukuran blok transformasi (*transform size* / *frame length*).
- Komponen riil $\text{Re}(X[k]) = \sum_{n=0}^{N-1} x[n] \cos\left(\frac{2\pi kn}{N}\right)$.
- Komponen imajiner $\text{Im}(X[k]) = -\sum_{n=0}^{N-1} x[n] \sin\left(\frac{2\pi kn}{N}\right)$.

Karena sampel audio $x[n]$ merupakan nilai riil murni ($x[n] \in \mathbb{R}$), spektrum DFT memiliki sifat simetri konjugat Hermitian:

$$X[N - k] = X^*[k]$$

di mana tanda $*$ menyatakan konjugat kompleks. Konsekuensi dari sifat simetri ini adalah bahwa nilai magnitudo spektrum di atas indeks $N/2$ merupakan cerminan persis dari spektrum di bawah $N/2$ ($|X[N-k]| = |X[k]|$). Oleh karena itu, dalam komputasi ekstraksi fitur audio, kita hanya perlu menghitung dan menganalisis sebanyak:

$$N_{\text{bins}} = \frac{N}{2} + 1$$

komponen frekuensi positif independen, mulai dari bin $k = 0$ (komponen DC / frekuensi $0\text{ Hz}$) hingga bin $k = N/2$ (frekuensi Nyquist $f_s/2$).

Ditinjau dari kompleksitas algoritma, untuk menghitung setiap bin $k$ dari persamaan definisi langsung diperlukan $N$ perkalian kompleks dan $N-1$ penjumlahan kompleks. Karena terdapat $N$ buah bin yang harus dihitung, total operasi perhitungan DFT langsung adalah:

$$\text{Kompleksitas DFT} = \mathcal{O}(N^2)$$

Jika panjang frame yang digunakan adalah $N = 2048$ sampel, maka satu kali evaluasi DFT langsung membutuhkan $2048^2 = 4.194.304$ operasi perkalian kompleks. Jika dalam 1 detik sinyal terdapat 43 frame audio, maka sistem harus melakukan lebih dari 180 juta operasi perkalian per detik hanya untuk transformasi dasar. Kompleksitas sebesar ini akan memicu *bottleneck* komputasi dan latensi tinggi yang tidak dapat diterima pada aplikasi pengendalian pencahayaan panggung *real-time*.

#### c. Algoritma Fast Fourier Transform (FFT) Cooley-Tukey Radix-2

Untuk mengatasi inefisiensi komputasi DFT langsung, sistem memanfaatkan algoritma *Fast Fourier Transform* (FFT) yang dirumuskan oleh J. W. Cooley dan J. W. Tukey pada tahun 1965 [5]. Algoritma ini mengeksploitasi periodisitas dan simetri dari faktor fase (*twiddle factor*) $W_N = e^{-j \frac{2\pi}{N}}$ melalui pendekatan *divide-and-conquer* berbasis desimasi waktu (*Decimation-in-Time* / DIT).

Dengan mengasumsikan panjang frame $N$ adalah bilangan genap kelipatan dua ($N = 2^p$), deret penjumlahan $n$ pada DFT dipecah menjadi dua kelompok:
1. Sub-deret indeks genap ($n = 2m$, dengan $m = 0, 1, \dots, \frac{N}{2}-1$)
2. Sub-deret indeks ganjil ($n = 2m+1$, dengan $m = 0, 1, \dots, \frac{N}{2}-1$)

Substitusi ke dalam persamaan DFT menghasilkan:

$$X[k] = \sum_{m=0}^{\frac{N}{2}-1} x[2m] \cdot e^{-j \frac{2\pi}{N} k(2m)} + \sum_{m=0}^{\frac{N}{2}-1} x[2m+1] \cdot e^{-j \frac{2\pi}{N} k(2m+1)}$$

$$X[k] = \sum_{m=0}^{\frac{N}{2}-1} x[2m] \cdot e^{-j \frac{2\pi}{N/2} km} + W_N^k \sum_{m=0}^{\frac{N}{2}-1} x[2m+1] \cdot e^{-j \frac{2\pi}{N/2} km}$$

$$X[k] = E[k] + W_N^k \cdot O[k]$$

di mana:
- $E[k]$ adalah DFT berukuran $N/2$ dari sampel-sampel genap (*Even*).
- $O[k]$ adalah DFT berukuran $N/2$ dari sampel-sampel ganjil (*Odd*).
- $W_N^k = e^{-j \frac{2\pi k}{N}}$ adalah *twiddle factor*.

Memanfaatkan sifat periodisitas $E[k + N/2] = E[k]$, $O[k + N/2] = O[k]$, dan relasi simetri $W_N^{k + N/2} = -W_N^k$, kedua bagian spektrum dapat dihitung secara simultan melalui operasi kupu-kupu (*butterfly operation*):

$$\begin{cases}
X[k] &= E[k] + W_N^k \cdot O[k] \\
X\left[k + \frac{N}{2}\right] &= E[k] - W_N^k \cdot O[k]
\end{cases} \quad \text{untuk } k = 0, 1, \dots, \frac{N}{2} - 1$$

Melalui rekursi sebanyak $\log_2 N$ tahapan, algoritma FFT Cooley-Tukey berhasil mereduksi kompleksitas komputasi secara drastis menjadi:

$$\text{Kompleksitas FFT} = \mathcal{O}(N \log_2 N)$$

Pada ukuran frame $N = 2048$ sampel, algoritma FFT hanya membutuhkan:

$$N \log_2 N = 2048 \times 11 = 22.528 \text{ operasi dasar}$$

Dibandingkan dengan DFT langsung ($4.194.304$ operasi), algoritma FFT Cooley-Tukey memberikan **faktor percepatan sebesar 186,2 kali lipat** atau memangkas beban komputasi sebesar **$99{,}46\%$**. Efisiensi komputasi ini sangat krusial agar sistem ZZLUXORA dapat mengekstrak seluruh spektrum frekuensi audio secara instan (< 5 ms per frame) tanpa membebani prosesor komputer kontrol pencahayaan.

#### d. Karakteristik Sinyal Musik Non-Stasioner dan Short-Time Fourier Transform (STFT)

Meskipun FFT sangat efisien, penerapan FFT standar secara langsung terhadap keseluruhan durasi berkas lagu rohani (misalnya sebuah lagu berdurasi 4 menit) tidak dapat digunakan untuk pengendalian pencahayaan panggung. Hal ini disebabkan oleh sifat fisik sinyal musik:

1. **Sinyal Musik Bersifat Non-Stasioner:**
   Komposisi lagu rohani memiliki struktur dinamika yang terus berubah terhadap waktu (terdiri dari bagian *intro*, bait/*verse*, jembatan/*bridge*, reff/*chorus*, dan penutup). Kandungan frekuensi, harmoni akord, kenyaringan, dan tempo musik berganti dari detik ke detik.
2. **Ketiadaan Lokalisasi Waktu pada FFT Global:**
   FFT standar mengintegrasikan seluruh sinyal dari awal hingga akhir lagu, sehingga spektrum yang dihasilkan hanya memperlihatkan *frekuensi apa saja yang muncul di sepanjang lagu*, namun **sama sekali tidak memiliki informasi mengenai kapan frekuensi tersebut terjadi**.
3. **Kebutuhan Sinkronisasi Pencahayaan Panggung:**
   Tata cahaya panggung menuntut respons visual yang sinkron detik demi detik mengikuti dinamika lagu (misalnya saat lagu berpindah dari *verse* yang tenang ke *drop chorus* yang bertenaga).

Oleh karena itu, transformasi yang wajib digunakan untuk analisis musik adalah **Short-Time Fourier Transform (STFT)**, yang membagi sinyal audio menjadi jendela-jendela waktu pendek (*sliding frames*) dan mengevaluasi FFT pada masing-masing jendela tersebut.

#### e. Fungsi Windowing dan Mitigasi Spectral Leakage

Dalam komputasi STFT, pemotongan sinyal audio menjadi segmen-segmen frame pendek secara matematis ekuivalen dengan mengalikan sinyal $x[n]$ dengan suatu fungsi pembobotan (*window function*) $w[n]$.

Jika frame dipotong menggunakan jendela persegi (*Rectangular Window*):

$$w_{\text{rect}}[n] = \begin{cases} 1, & 0 \le n \le N-1 \\ 0, & \text{lainnya} \end{cases}$$

Di domain frekuensi, perkalian ini setara dengan operasi konvolusi sinyal dengan fungsi $\text{sinc}(f) = \frac{\sin(\pi f)}{\pi f}$. Pemotongan mendadak pada batas awal dan akhir frame menimbulkan diskontinuitas artifisial tajam pada sinyal. Akibatnya, energi frekuensi dari suatu nada murni akan menyebar dan bocor ke bin-bin frekuensi tetangga di sekitarnya dalam bentuk puncak sampingan (*sidelobes*) yang tinggi. Fenomena kebocoran ini dikenal sebagai **Spectral Leakage**.

Kebocoran spektral sangat merugikan sistem pencahayaan panggung karena menyebabkan deteksi harmoni nada dan ekstraksi fitur *Chroma* menjadi tidak akurat (nada mayor dan minor menjadi bias akibat tercemar frekuensi palsu). Untuk meredam *spectral leakage*, amplitudo sinyal pada tepi frame harus diturunkan secara mulus (*tapering*) menuju nol. Pada sistem ZZLUXORA, digunakan fungsi jendela **Hann (Hanning) Window** [21]:

$$w[n] = 0{,}5 \left[ 1 - \cos\left( \frac{2\pi n}{N - 1} \right) \right] = \sin^2\left( \frac{\pi n}{N - 1} \right), \quad 0 \le n \le N-1$$

Fungsi Hann memiliki nilai $w[0] = w[N-1] = 0$ dan puncak $w[(N-1)/2] = 1$. Keunggulan akustik fungsi Hann adalah mampu meredam *sidelobe level* hingga **-31,5 dB** (jauh lebih baik dibandingkan *rectangular window* yang hanya memiliki peredaman -13 dB), sehingga menghasilkan pemisahan puncak frekuensi nada yang bersih dan meminimalkan bias pada analisis harmoni lagu.

#### f. Formulasi Diskrit STFT dan Konversi Parameter Fisik

Dengan menggabungkan fungsi pembobotan Hann window dan algoritma FFT Cooley-Tukey, formulasi matematis STFT diskrit yang diimplementasikan pada komputasi perangkat lunak ZZLUXORA didefinisikan sebagai:

$$X[m, k] = \sum_{n=0}^{N-1} x[n + m \cdot H] \cdot w[n] \cdot e^{-j \frac{2\pi}{N} kn}$$

di mana:
- $m \in \{0, 1, \dots, M-1\}$ adalah **indeks frame waktu** ($M$ adalah total frame dalam lagu).
- $k \in \left\{0, 1, \dots, \frac{N}{2}\right\}$ adalah **indeks bin frekuensi**.
- $N$ adalah panjang jendela analisis (*Window Length* / *FFT size*), ditetapkan bernilai **2048 sampel**.
- $H$ adalah jarak pergeseran antar jendela (*Hop Length* / *Stride*), ditetapkan bernilai **512 sampel** (terjadi *overlap* sebesar $75\%$).
- $w[n]$ adalah fungsi jendela Hann sepanjang $N$.
- $x[n + m \cdot H]$ adalah segmen sinyal audio pada jendela waktu ke-$m$.

Hasil transformasi STFT adalah sebuah matriks bilangan kompleks $X[m, k]$ berdimensi $\left( \frac{N}{2} + 1 \right) \times M$ yang menghubungkan koordinat sel diskrit $(m, k)$ dengan besaran fisik nyata di dunia nyata:

1. **Waktu Fisik ($t_m$) dalam Detik:**
   $$t_m = \frac{m \cdot H}{f_s}$$
2. **Frekuensi Fisik ($f_k$) dalam Hertz:**
   $$f_k = \frac{k \cdot f_s}{N}$$
3. **Lebar Pita per Bin Frekuensi ($\Delta f$):**
   $$\Delta f = \frac{f_s}{N} = \frac{22050}{2048} \approx 10{,}7666\text{ Hz}$$
4. **Interval Perbaruan Waktu Antar Frame ($\Delta t_{\text{hop}}$):**
   $$\Delta t_{\text{hop}} = \frac{H}{f_s} = \frac{512}{22050} \approx 0{,}02322\text{ detik} = 23{,}22\text{ ms}$$

Laju pembaruan data visual (*frame rate*) yang dihasilkan oleh algoritma adalah:

$$\text{FPS} = \frac{1}{\Delta t_{\text{hop}}} = \frac{22050}{512} \approx 43{,}07\text{ frame per detik (fps)}$$

Nilai **43,07 FPS** ini secara presisi selaras dengan laju penyegaran transmisi fisik standar **DMX512-A (44 frame per detik)**, sehingga data pencahayaan dapat langsung dialirkan ke lampu PAR LED panggung tanpa membutuhkan interpolasi atau penahanan buffer tambahan, menghasilkan transisi visual yang sangat halus (*smooth fading*) dan bebas getaran (*visual stepping*).

#### g. Prinsip Ketidakpastian Waktu-Frekuensi (Heisenberg-Gabor Limit)

Dalam pemrosesan sinyal waktu-frekuensi berlaku batasan fundamental fisika yang dikenal sebagai **Prinsip Ketidakpastian Gabor**:

$$\Delta t \cdot \Delta f \ge \frac{1}{4\pi}$$

Prinsip ini menegaskan bahwa kita tidak dapat memperoleh resolusi waktu yang sangat tinggi dan resolusi frekuensi yang sangat tinggi secara simultan menggunakan satu ukuran jendela STFT konstan:
- **Jika ukuran jendela $N$ terlalu besar (misalnya $N = 8192$):** Resolusi frekuensi menjadi sangat tinggi ($\Delta f \approx 2{,}69\text{ Hz}$), mempermudah pembedaan nada bass, namun resolusi waktu memburuk secara drastis ($\Delta t \approx 371\text{ ms}$). Akibatnya, hentakan ketukan drum dan transien musik menjadi kabur dan terlambat dideteksi lebih dari 0,3 detik.
- **Jika ukuran jendela $N$ terlalu kecil (misalnya $N = 256$):** Resolusi waktu sangat tajam ($\Delta t \approx 11{,}6\text{ ms}$), namun resolusi frekuensi sangat kasar ($\Delta f \approx 86{,}13\text{ Hz}$), sehingga sistem tidak dapat membedakan nada-nada musik yang berdekatan dan gagal menganalisis akord mayor/minor.

Penetapan parameter $f_s = 22.050\text{ Hz}$, $N = 2048$, dan $H = 512$ pada sistem ZZLUXORA merupakan titik kompromi optimal (*golden mean*) yang terbukti secara empiris dan teoretis mampu membedakan harmoni akord musik ($\Delta f \approx 10{,}77\text{ Hz}$) sekaligus mendeteksi ketukan musik dengan latensi rendah ($\Delta t_{\text{hop}} \approx 23{,}22\text{ ms}$), berada jauh di bawah ambang batas persepsi keterlambatan visual mata manusia (< 40 ms).

#### h. Penurunan Fitur Akustik Spektral Berbasis Spektrum FFT

Matriks hasil STFT $X[m, k]$ merupakan representasi bilangan kompleks $X[m, k] = \text{Re}(X[m, k]) + j\,\text{Im}(X[m, k])$. Dari matriks ini diturunkan fitur-fitur akustik spektral yang menjadi input bagi model afektif pencahayaan panggung:

1. **Magnitude Spectrogram dan Power Spectrogram:**
   Magnitudo spektrum mengukur amplitudo absolut dari setiap komponen frekuensi:
   $$|X[m, k]| = \sqrt{\text{Re}(X[m, k])^2 + \text{Im}(X[m, k])^2}$$
   Sedangkan spektrum daya (*Power Spectrogram*) mengukur daya energi sinyal pada frame ke-$m$:
   $$S[m, k] = |X[m, k]|^2$$

2. ***Root Mean Square* (RMS) Energy:**
   RMS Energy merepresentasikan kenyaringan (*loudness*) dan intensitas daya dinamika lagu pada frame ke-$m$. Berdasarkan Teorema Parseval, total energi dalam domain waktu setara dengan total energi dalam domain frekuensi:
   $$\text{RMS}[m] = \sqrt{ \frac{1}{N} \sum_{n=0}^{N-1} \left| x[n + mH] \cdot w[n] \right|^2 }$$
   Nilai RMS ini kemudian dinormalisasi ke skala $[0{,}0, 1{,}0]$ dan dipetakan secara linier sebagai pengatur intensitas **Master Dimmer** lampu panggung:
   $$\text{RMS}_{\text{norm}}[m] = \frac{\text{RMS}[m] - \text{RMS}_{\min}}{\text{RMS}_{\max} - \text{RMS}_{\min}}$$

3. ***Spectral Centroid* (Kecerahan Timbre / Brightness):**
   *Spectral Centroid* merupakan titik pusat massa (*center of mass*) dari spektrum frekuensi audio pada frame ke-$m$. Nilai centroid menunjukkan apakah energi frekuensi lagu didominasi oleh rentang frekuensi rendah (karakter instrumen bass/drum, bernuansa hangat dan berat) atau frekuensi tinggi (karakter instrumen simbal/gitar melodi/vokal tinggi, bernuansa cerah dan tajam). Formulasi matematis eksak berbasis bin frekuensi FFT:
   $$\text{Centroid}[m] = \frac{\sum_{k=0}^{N/2} f_k \cdot |X[m, k]|}{\sum_{k=0}^{N/2} |X[m, k]|} = \frac{\sum_{k=0}^{N/2} \left( \frac{k \cdot f_s}{N} \right) \cdot |X[m, k]|}{\sum_{k=0}^{N/2} |X[m, k]|}$$
   di mana $f_k$ adalah frekuensi fisik bin ke-$k$ dan $|X[m, k]|$ adalah bobot magnitudo spektral. Pada sistem ZZLUXORA, nilai centroid dinormalisasi dan dihubungkan ke koordinat Arousal serta rona warna (*Hue*). Nilai centroid tinggi memicu warna-warna cerah tersaturasi (*vibrant gold/amber/white*), sedangkan centroid rendah memicu warna kontemplatif (*cool deep blue/purple*).

4. ***Chroma STFT* (Pitch Class Profile 12-Semitone):**
   Fitur *Chroma* memproyeksikan seluruh energi spektral frekuensi FFT ke dalam 12 kelas nada kromatik musik barat:
   $$\text{Chroma} = \{C, C\sharp, D, D\sharp, E, F, F\sharp, G, G\sharp, A, A\sharp, B\}$$
   Hubungan antara frekuensi kontinu $f$ dengan nomor nada MIDI $p$ mengikuti skala logaritmik sama rata (*equal temperament* dengan acuan nada $A_4 = 440\text{ Hz}$ pada indeks MIDI 69):
   $$p(f) = 12 \cdot \log_2\left( \frac{f}{440} \right) + 69$$
   Setiap bin frekuensi $k$ memiliki frekuensi fisik $f_k = \frac{k \cdot f_s}{N}$. Kelas nada kromatik $c \in \{0, 1, \dots, 11\}$ ditentukan melalui operasi modulo 12:
   $$c(k) = \text{round}(p(f_k)) \pmod{12}$$
   Energi pada kelas nada $c$ pada frame ke-$m$ dihitung dengan mengintegrasikan magnitudo seluruh bin FFT yang bersesuaian:
   $$\text{Chroma}[m, c] = \sum_{k \in \mathcal{K}_c} |X[m, k]|$$
   Vektor Chroma 12 dimensi $\mathbf{Chroma}[m]$ dikorelasikan dengan template profil tonal Krumhansl-Schmuckler untuk tangga nada Mayor ($\mathbf{T}_{\text{major}}$) dan Minor ($\mathbf{T}_{\text{minor}}$) guna mengevaluasi polaritas tangga nada lagu:
   $$\rho_{\text{major}} = \text{corr}(\mathbf{Chroma}[m], \mathbf{T}_{\text{major}}), \quad \rho_{\text{minor}} = \text{corr}(\mathbf{Chroma}[m], \mathbf{T}_{\text{minor}})$$
   Korelasi mayor yang lebih tinggi ($\rho_{\text{major}} > \rho_{\text{minor}}$) mengindikasikan suasana sukacita (*happy/uplifting*) dan menghasilkan nilai **Valence positif ($V > 0$)**, sedangkan korelasi minor yang dominan mengindikasikan suasana khidmat dan menghasilkan nilai **Valence negatif ($V < 0$)**.

5. ***Mel-Frequency Cepstral Coefficients* (MFCC):**
   MFCC mengekstraksi amplop spektral (*spectral envelope*) yang merepresentasikan karakteristik tekstur timbre suara vokal dan instrumen berdasarkan respons pendengaran telinga manusia. Spektrum daya FFT $S[m, k]$ disaring menggunakan $B = 40$ filter segitiga pada skala Mel ($m_{\text{mel}} = 2595 \log_{10}(1 + f/700)$), ditransformasikan ke skala logaritmik, lalu didekorelasikan melalui *Discrete Cosine Transform* (DCT-II):
   $$\text{MFCC}[m, l] = \sum_{b=1}^B \log(\tilde{S}[m, b]) \cdot \cos\left( \frac{\pi l (b - 0{,}5)}{B} \right), \quad l = 0, 1, \dots, 12$$
   13 koefisien MFCC pertama diambil untuk membedakan tekstur instrumen akustik (piano/gitar akustik pada lagu *worship*) dari instrumen berdistorsi (gitar elektrik/drum pada lagu *praise*).

6. ***Onset Detection* dan *Beat Tracking*:**
   *Onset Detection* mengidentifikasi titik awal transien serangan nada (*attack*) dengan menghitung fungsi kebaruan spektral (*spectral flux*) dari spektrum FFT:
   $$\text{SF}[m] = \sum_{k=0}^{N/2} \max(0, |X[m, k]| - |X[m-1, k]|)$$
   Titik puncak fungsi kebaruan ini menunjukkan terjadinya hentakan ketukan (*beat*) atau pergantian akord, yang digunakan oleh sistem ZZLUXORA sebagai pemicu pergantian *scene* dan *chase step* pencahayaan panggung secara otomatis.

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

Temuan-temuan ini menjadi dasar ilmiah bagi penyusunan tabel *rule-based mapping* eksplisit yang digunakan dalam sistem ZZLUXORA. Setiap aturan pemetaan merujuk pada referensi penelitian yang telah dipublikasikan.

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

*Art-Net* merupakan protokol komunikasi yang dikembangkan oleh *Artistic Licence Engineering Ltd.* untuk mentransmisikan data DMX512 melalui jaringan UDP/IP [16]. *Art-Net* menggunakan *port* 6454 dan mendukung hingga 32.768 *universe* DMX. Dalam penelitian ini, *Art-Net* digunakan sebagai *transport layer* untuk mengirimkan data pencahayaan dari aplikasi ZZLUXORA ke modul ESP32 melalui jaringan WiFi.

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

1. Menerima data *Art-Net* dari ZZLUXORA sebagai *Input Universe* melalui *virtual adapter*.
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
