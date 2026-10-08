# Model Matematis: Pemetaan Fitur Audio ke RGBW

### Formalisme Kanonik Implementasi ZZLUXORA v10

> **Catatan Versi (7 Oktober 2026).** Seluruh formalisme pada dokumen ini telah diselaraskan 1:1 dengan **kode sumber kebenaran** ZZLUXORA v10, yaitu `core/emotion_model.py` dan `core/color_engine.py`, serta dengan perumusan pada Bab II dan Bab III naskah. Versi lama dokumen ini — domain *Valence–Arousal* $[0, 1]$, rona warna (*hue*) *piecewise* per kuadran dengan ambang $0{,}5$, bobot Arousal $0{,}40/0{,}35/0{,}25$, serta Valence berbasis rasio energi chroma mayor dengan pemetaan $S = 0{,}6A + 0{,}4|2V - 1|$ dan $V_{hsv} = \max(0{,}5\,\text{RMS} + 0{,}5A;\ 0{,}10)$ — **diarsipkan** dan tidak lagi digunakan, mengikuti keputusan kanonik 7 Oktober 2026: **formalisme mengikuti implementasi v10**.

---

## Overview Pipeline

```
Audio File → STFT & Ekstraksi Fitur → Normalisasi → (V, A) polar → HSV → RGB → RGBW → Scene/Chase → DMX512 (Art-Net)
```

---

## [1] Ekstraksi Fitur Audio

Analisis dilakukan oleh mesin STFT dan ekstraktor fitur milik sendiri (`core/fft_engine.py` dan `core/feature_extractor.py`) dengan parameter baku berikut: $f_s = 22.050\text{ Hz}$, $N = 2048$, $H = 512$ (overlap 75 %), sehingga $\Delta f = f_s/N \approx 10{,}77\text{ Hz}$, $\Delta t_{\text{hop}} = H/f_s \approx 23{,}22\text{ ms}$, dan laju frame $43{,}07\text{ FPS}$.

| Fitur | Fungsi implementasi v10 | Deskripsi |
|-------|------------------------|-----------|
| STFT | `STFTEngine.compute_stft()` | Transformasi Fourier jendela geser + Hann window |
| RMS Energy | `STFTEngine.compute_rms_energy()` | Energi rata-rata per frame (loudness) |
| Spectral Centroid | `STFTEngine.compute_spectral_centroid()` | "Kecerahan" timbre (titik pusat massa frekuensi) |
| Chroma 12-semitone | `FeatureExtractor.extract_chroma()` | Distribusi energi kelas nada C s.d. B |
| Tempo/BPM | `FeatureExtractor.estimate_tempo_bpm()` | Estimasi tempo via autokorelasi *onset envelope* |
| Mode polaritas | `EmotionModel.compute_mode_ratio()` | Polaritas modus Mayor/Minor (Krumhansl–Schmuckler) |

### 1.1 STFT Diskrit

$$X[m, k] = \sum_{n=0}^{N-1} x[n + mH] \cdot w[n] \cdot e^{-j \frac{2\pi}{N} kn} \tag{1}$$

dengan fungsi *Hann window*

$$w[n] = 0{,}5 \left[ 1 - \cos\left( \frac{2\pi n}{N-1} \right) \right], \quad 0 \le n \le N-1 \tag{2}$$

dan *magnitude spectrogram* $|X[m, k]| = \sqrt{\text{Re}^2 + \text{Im}^2}$.

### 1.2 Root Mean Square (RMS Energy)

$$\text{RMS}[m] = \sqrt{ \frac{1}{N} \sum_{n=0}^{N-1} \left| x[n + mH] \cdot w[n] \right|^2 } \tag{3}$$

### 1.3 Spectral Centroid

$$\text{Centroid}[m] = \frac{\sum_{k=0}^{N/2} f_k \cdot |X[m, k]|}{\sum_{k=0}^{N/2} |X[m, k]|}, \quad f_k = \frac{k \cdot f_s}{N} \tag{4}$$

### 1.4 Chroma 12-Semitone

Setiap bin $k$ dipetakan ke kelas nada kromatik melalui nomor nada MIDI $p(f_k) = 12\log_2(f_k/440) + 69$ dan operasi modulo 12, dengan bobot lonceng Gauss di sekitar pusat semitone:

$$\text{Chroma}[c, k] \mathrel{+}= \exp\left( -\frac{1}{2} \left( \frac{p(f_k) - \text{round}(p(f_k))}{0{,}5} \right)^{\!2} \right), \quad c = \text{round}(p(f_k)) \bmod 12 \tag{5}$$

hanya untuk rentang musikal $30\text{ Hz} \le f_k \le 4000\text{ Hz}$. Setiap baris filterbank dinormalisasi terhadap jumlah elemennya, kemudian vektor chroma dinormalisasi terhadap norma Euclidean per frame:

$$\hat{\mathbf{Chroma}}[m] = \frac{\mathbf{Chroma}[m]}{\|\mathbf{Chroma}[m]\|_2} \tag{6}$$

### 1.5 Estimasi Tempo

Tempo global $B$ (BPM) diestimasi dari puncak autokorelasi *envelope* ketukan pada rentang pencarian 60–180 BPM, kemudian di-*clamp*:

$$B = \text{clip}(B,\ 50,\ 190) \tag{7}$$

---

## [2] Normalisasi Fitur

Implementasi v10 memakai **normalisasi terhadap nilai maksimum pada keseluruhan lagu** (bukan rentang min–maks tetap), dengan penguncian hasil ke rentang $[0, 1]$:

$$\text{RMS}_{\text{norm}} = \text{clip}\!\left( \frac{\text{RMS}[m]}{\max_{m}\text{RMS}[m]},\ 0,\ 1 \right) \tag{8}$$

$$\text{SC}_{\text{norm}} = \text{clip}\!\left( \frac{\text{Centroid}[m]}{\max_{m}\text{Centroid}[m]},\ 0,\ 1 \right) \tag{9}$$

Untuk tempo, normalisasi linier ke skor $[-1, 1]$ dilakukan pada tahap perhitungan Arousal dengan jendela $[50, 170]$ (lihat Persamaan (14)). Semua masukan ter-normalisasi yang diterima model afektif berada pada rentang $[0, 1]$.

---

## [3] Perhitungan Valence & Arousal (Model Afektif Russell)

Domain kanonik: $V, A \in [-1{,}0,\ +1{,}0]$, di mana $V = -1$ (khidmat/sedih) s.d. $+1$ (sukacita/tinggi), dan $A = -1$ (tenang) s.d. $+1$ (energik). Nilai dipotong ke rentang tersebut pada akhir perhitungan.

### 3.1 Bobot Fitur (Default Implementasi `emotion_model.py`)

| Domain | $w_1$ | $w_2$ | $w_3$ |
|--------|-------|-------|-------|
| **Valence** | $0{,}50$ — `mode_ratio` (polaritas modus) | $0{,}30$ — `spectral_centroid` (kecerahan timbre) | $0{,}20$ — `mfcc_contrast` (tekstur harmonik) |
| **Arousal** | $0{,}50$ — `rms_energy` (loudness) | $0{,}30$ — `tempo_bpm` (kecepatan ketukan) | $0{,}20$ — `onset_strength` (transien perkusif) |

### 3.2 Polaritas Modus (Krumhansl–Schmuckler)

Profil tonal Krumhansl–Schmuckler untuk Mayor dan Minor:

$$\mathbf{T}_{\text{major}} = [6{,}35;\ 2{,}23;\ 3{,}48;\ 2{,}33;\ 4{,}38;\ 4{,}09;\ 2{,}52;\ 5{,}19;\ 2{,}39;\ 3{,}66;\ 2{,}29;\ 2{,}88] \tag{10}$$

$$\mathbf{T}_{\text{minor}} = [6{,}33;\ 2{,}68;\ 3{,}52;\ 5{,}38;\ 2{,}60;\ 3{,}53;\ 2{,}54;\ 4{,}75;\ 3{,}98;\ 2{,}69;\ 3{,}34;\ 3{,}17] \tag{11}$$

Kedua profil dan vektor chroma dinormalisasi terhadap norma Euclidean, lalu dikorelasikan terhadap **seluruh 12 transposisi** (geseran circular). Diperoleh korelasi maksimum $\rho_{\text{maj}}$ dan $\rho_{\text{min}}$, sehingga skor polaritas modus menjadi

$$\text{Mode}_{\text{polarity}} = \frac{\rho_{\text{maj}} - \rho_{\text{min}}}{\rho_{\text{maj}} + \rho_{\text{min}}}, \qquad \text{Mode}_{\text{score}} = \text{clip}\!\left( 2 \cdot \text{Mode}_{\text{polarity}},\ -1,\ 1 \right) \tag{12}$$

dengan nilai $0{,}0$ bila penyebut mendekati nol atau vektor chroma tidak valid (bukan 12 dimensi). Skor $+1$ menandakan modus Mayor dominan dan $-1$ menandakan modus Minor dominan.

### 3.3 Pemetaan Skor Masukan $[0, 1] \to [-1, 1]$

$$\text{score}(x) = 2 \cdot \text{clip}(x,\ 0,\ 1) - 1 \tag{13}$$

berlaku untuk $\text{SC}_{\text{norm}}$, $\text{RMS}_{\text{norm}}$, $\text{MFCC}_{\text{norm}}$, dan $\text{Onset}_{\text{norm}}$, sedangkan tempo dinormalisasi secara linier:

$$\text{Tempo}_{\text{score}} = 2 \cdot \frac{\text{clip}(B,\ 50,\ 170) - 50}{120} - 1 \tag{14}$$

### 3.4 Valence dan Arousal

$$V = \text{clip}\!\left( 0{,}50 \cdot \text{Mode}_{\text{score}} + 0{,}30 \cdot \text{score}(\text{SC}_{\text{norm}}) + 0{,}20 \cdot \text{score}(\text{MFCC}_{\text{norm}}),\ -1,\ 1 \right) \tag{15}$$

$$A = \text{clip}\!\left( 0{,}50 \cdot \text{score}(\text{RMS}_{\text{norm}}) + 0{,}30 \cdot \text{Tempo}_{\text{score}} + 0{,}20 \cdot \text{score}(\text{Onset}_{\text{norm}}),\ -1,\ 1 \right) \tag{16}$$

> **Catatan implementasi.** Pemanggilan pada `core/feature_extractor.py` kini meneruskan seluruh parameter fitur secara aktif: `rms_norm`, `centroid_norm`, `chroma_12`, `tempo_bpm`, `onset_norm` (dari *spectral flux envelope*), dan `mfcc_norm` (kontras 12 koefisien Mel-cepstral). Seluruh komponen bobot ($0{,}50$, $0{,}30$, $0{,}20$) beroperasi penuh pada alur analisis berjalan, dengan nilai cadangan (*fallback*) $0{,}5$ bila data frame audio hening atau tidak terdefinisi.

### 3.5 Interpretasi Kuadran V–A

Batas kuadran adalah **tanda** $V$ dan $A$ (ambang $0{,}0$, bukan $0{,}5$), sebagaimana terimplementasi pada properti `EmotionCoordinate.quadrant` (`core/models.py`):

| Kuadran | Kondisi | Label implementasi | Karakter |
|---------|---------|--------------------|----------|
| Q1 | $V \ge 0$ dan $A \ge 0$ | `Q1_PRAISE_HIGH` | Praise, energik |
| Q2 | $V < 0$ dan $A \ge 0$ | `Q2_INTENSE_REVERENCE` | Intens, dramatis |
| Q3 | $V < 0$ dan $A < 0$ | `Q3_DEEP_WORSHIP` | Khidmat, kontemplatif |
| Q4 | $V \ge 0$ dan $A < 0$ | `Q4_PEACE_INTIMACY` | Damai, tenang |

---

## [4] Pemetaan $(V, A) \to$ HSV (Representasi Polar)

Ruang afektif dua dimensi dipetakan ke HSV secara **polar** (bukan *piecewise* per kuadran), persis seperti `ColorEngine.emotion_to_hsv()`:

### 4.1 Rona (*Hue*) — $0^\circ$–$360^\circ$

$$H = \left( \frac{180^\circ}{\pi} \cdot \text{atan2}(A,\ V) + 360^\circ \right) \bmod 360^\circ \tag{17}$$

di mana $V$ dan $A$ terlebih dahulu di-*clip* ke $[-1, 1]$. Karena fungsi `atan2`, pemetaan kuadran afektif ke interval rona secara eksak adalah:

| Kuadran | Tanda $(V, A)$ | Interval $H$ | Sektor roda HSV standar |
|---------|----------------|--------------|--------------------------|
| Q1 | $(+, +)$ | $0^\circ \le H < 90^\circ$ | Merah → kuning (hangat) |
| Q2 | $(-, +)$ | $90^\circ \le H < 180^\circ$ | Kuning → hijau |
| Q3 | $(-, -)$ | $180^\circ \le H < 270^\circ$ | Hijau → biru (dingin) |
| Q4 | $(+, -)$ | $270^\circ \le H < 360^\circ$ | Biru → magenta → merah |

### 4.2 Saturasi (*Saturation*) — $0$–$1$

Saturasi sebanding dengan jarak titik afektif dari pusat netral $(0, 0)$:

$$S = \text{clip}\!\left( \frac{\sqrt{V^2 + A^2}}{\sqrt{2}},\ 0{,}2,\ 1{,}0 \right) \tag{18}$$

Lantai $S_{\min} = 0{,}2$ menjaga warna tetap memiliki rona meskipun emosi mendekati netral (pusat $V{=}A{=}0$ menghasilkan $S = 0{,}2$).

### 4.3 Kecerahan (*Value*) — $0$–$1$

$$V_{hsv} = \text{clip}\!\left( \text{RMS}_{\text{norm}} \cdot D_{\text{master}},\ 0,\ 1 \right) \tag{19}$$

di mana $D_{\text{master}} \in [0, 1]$ adalah *master dimmer*. Kecerahan murni berasal dari energi akustik frame (RMS), bukan dari kombinasi RMS dan Arousal.

---

## [5] HSV $\to$ RGB (Foley & van Dam)

Konversi mengikuti algoritma standar dengan $h$ dalam derajat, $s, v \in [0, 1]$:

$$C = v \cdot s, \qquad X = C \cdot \left( 1 - \left| \left( \frac{h}{60^\circ} \right) \bmod 2 - 1 \right| \right), \qquad m = v - C \tag{20}$$

Nilai $(R_1, G_1, B_1)$ ditentukan berdasarkan sektor $h$:

$$
(R_1, G_1, B_1) = \begin{cases}
(C, X, 0) & \text{jika } 0^\circ \le h < 60^\circ \\
(X, C, 0) & \text{jika } 60^\circ \le h < 120^\circ \\
(0, C, X) & \text{jika } 120^\circ \le h < 180^\circ \\
(0, X, C) & \text{jika } 180^\circ \le h < 240^\circ \\
(X, 0, C) & \text{jika } 240^\circ \le h < 300^\circ \\
(C, 0, X) & \text{jika } 300^\circ \le h < 360^\circ
\end{cases} \tag{21}
$$

Nilai akhir 8-bit (dibulatkan dan di-*clamp* ke $[0, 255]$):

$$R = \text{round}\big((R_1 + m) \cdot 255\big), \quad G = \text{round}\big((G_1 + m) \cdot 255\big), \quad B = \text{round}\big((B_1 + m) \cdot 255\big) \tag{22}$$

Notasi sektor berbasis $H' = H/60^\circ$ yang dipakai pada Bab II ekuivalen dengan Persamaan (20)–(21).

---

## [6] RGB $\to$ RGBW Fisik dan Output DMX

### 6.1 Dekomposisi 4-Kanal Physical RGBW

Lampu PAR LED RGBW memiliki emitor *White* tersendiri. Mengekstrak komponen putih bersama dari RGB menjaga kromatisitas tetap persis sambil memakai emitor putih berkecepatan tinggi (*anti-washout*):

$$W = \min(R, G, B) \tag{23}$$

$$R' = R - W, \qquad G' = G - W, \qquad B' = B - W \tag{24}$$

Operasi di atas dijalankan pada nilai 8-bit hasil Persamaan (22).

### 6.2 Output DMX

$$\text{DMX}[R, G, B, W] = \text{round}\big( [R',\ G',\ B',\ W] \cdot d \big), \quad d = \text{clip}(\text{dimmer},\ 0,\ 1) \tag{25}$$

*Grand Master* fader berlaku sebagai penskalaan linier pada buffer DMX:

$$\text{DMX}_{\text{out}}[ch] = \text{round}\!\left( \text{raw}[ch] \cdot \frac{M}{255} \right), \qquad M \in [0, 255] \tag{26}$$

sehingga penskalaan kecerahan tidak dilakukan dua kali: $D_{\text{master}}$ pada Persamaan (19) menyetel *Value*, sedangkan $M$ pada Persamaan (26) menyetel keluaran fader/DMX.

---

## [7] Tabel Rule-Based Mapping Eksplisit

Tabel berikut merupakan aturan pemetaan eksplisit yang menjadi dasar sistem ZZLUXORA. Setiap aturan merujuk pada referensi penelitian yang telah dipublikasikan.

### 7.1 Pemetaan Fitur Audio $\to$ Valence–Arousal

| No | Fitur Audio | Rentang/Kondisi | Dampak pada $V$–$A$ | Dasar Referensi |
|----|------------|-----------------|---------------------|-----------------|
| 1 | BPM lambat 60–90 | $\text{Tempo}_{\text{score}} = -0{,}83$ s.d. $-0{,}33$ | $A \downarrow$ | Juslin & Laukka (2003): tempo lambat $\to$ *low arousal* [31] |
| 2 | BPM sedang 90–120 | $\text{Tempo}_{\text{score}} = -0{,}33$ s.d. $+0{,}17$ (nol pada $B = 110$) | $A \approx$ netral | Eerola & Vuoskoski (2011) [25] |
| 3 | BPM cepat 120–170 | $\text{Tempo}_{\text{score}} = +0{,}17$ s.d. $+1{,}00$ | $A \uparrow$ | Juslin & Laukka (2003): tempo cepat $\to$ *high arousal* [31] |
| 4 | $\text{RMS}_{\text{norm}} < 0{,}1$ (pelan) | $\text{score} < -0{,}80$ | $A \downarrow$, $V_{hsv} \downarrow$ | Juslin & Laukka (2003): *loudness* rendah $\to$ *low arousal* [31] |
| 5 | $\text{RMS}_{\text{norm}} > 0{,}8$ (keras) | $\text{score} > +0{,}60$ | $A \uparrow$, $V_{hsv} \uparrow$ | Juslin & Laukka (2003): *loudness* tinggi $\to$ *high arousal* [31] |
| 6 | Korelasi profil Mayor dominan | $\text{Mode}_{\text{score}} > 0$ | $V \uparrow$ | Palmer *et al.* (2013): modus mayor $\to$ valence positif [24] |
| 7 | Korelasi profil Minor dominan | $\text{Mode}_{\text{score}} < 0$ | $V \downarrow$ | Palmer *et al.* (2013): modus minor $\to$ valence negatif [24] |
| 8 | SC rendah (timbre gelap) | $\text{score}(\text{SC}_{\text{norm}}) < 0$ | $V \downarrow$ (hue bergeser melalui Persamaan (17)) | Lindborg (2021): frekuensi rendah $\to$ warna hangat [10] |
| 9 | SC tinggi (timbre cerah) | $\text{score}(\text{SC}_{\text{norm}}) > 0$ | $V \uparrow$ (hue bergeser melalui Persamaan (17)) | Lindborg (2021): frekuensi tinggi $\to$ warna dingin [10] |
| 10 | Onset strength tinggi | $\text{score}(\text{Onset}_{\text{norm}}) > 0$ | $A \uparrow$, transisi cepat | Juslin & Laukka (2003): artikulasi cepat $\to$ arousal tinggi [31] |

### 7.2 Pemetaan $V$–$A \to$ Warna (HSV Polar)

Interval hue pada tabel berikut **diturunkan secara kritis** dari Persamaan (17); kolom referensi merujuk pada dasar psikologis asosiasi emosi–warna, bukan pada rentang derajat tertentu.

| No | Kuadran $V$–$A$ | Karakter | Interval Hue (Persamaan (17)) | Warna Visual | Dasar Asosiasi Emosi–Warna |
|----|-----------------|----------|-------------------------------|--------------|-----------------|
| 1 | $V \ge 0,\ A \ge 0$ (Q1) | Praise/energik | $0^\circ$–$90^\circ$ | Merah, oranye, kuning | Palmer (2013): musik cepat + mayor $\to$ emosi positif, asosiasi warna hangat [24] |
| 2 | $V < 0,\ A \ge 0$ (Q2) | Intens/dramatis | $90^\circ$–$180^\circ$ | Kuning-hijau, hijau, cyan | Palmer (2013): musik intens $\to$ emosi intens, warna tersaturasi [24] |
| 3 | $V < 0,\ A < 0$ (Q3) | Kontemplatif | $180^\circ$–$270^\circ$ | Cyan, biru, indigo | Palmer (2013): musik lambat + minor $\to$ emosi tenang, warna dingin [24] |
| 4 | $V \ge 0,\ A < 0$ (Q4) | Damai/tenang | $270^\circ$–$360^\circ$ | Ungu, magenta, merah redup | Lindborg (2021): musik tenang $\to$ emosi lembut [10] |

*Saturasi* mengikuti jarak $\sqrt{V^2+A^2}$ (Persamaan (18)) dan *value* mengikuti RMS (Persamaan (19)), sehingga lagu tenang otomatis menghasilkan warna dengan saturasi terkendali dan kecerahan rendah.

### 7.3 Pemetaan Fitur Audio $\to$ Parameter Lighting

| No | Fitur Audio | Rentang | Parameter Lighting | Nilai (implementasi v10) | Dasar |
|----|------------|---------|--------------------|--------------------------|-------|
| 1 | $\text{RMS}_{\text{norm}}$ rendah | $0$–$0{,}2$ | $V_{hsv}$ (skala 8-bit $= v \times 255$) | $0$–$51$ | Persamaan (19) dan (22) |
| 2 | $\text{RMS}_{\text{norm}}$ sedang | $0{,}4$–$0{,}6$ | $V_{hsv}$ (skala 8-bit $= v \times 255$) | $102$–$153$ | Persamaan (19) dan (22) |
| 3 | $\text{RMS}_{\text{norm}}$ tinggi | $0{,}8$–$1{,}0$ | $V_{hsv}$ (skala 8-bit $= v \times 255$) | $204$–$255$ | Persamaan (19) dan (22) |
| 4 | Jarak $\sqrt{V^2+A^2}$ besar | $r \to \sqrt{2}$ | Saturasi $S$ | $\to 1{,}0$ (maksimum) | Persamaan (18) |
| 5 | Jarak $\sqrt{V^2+A^2}$ kecil | $r \to 0$ | Saturasi $S$ | $0{,}2$ (lantai) | Persamaan (18) |
| 6 | SC rendah (timbre gelap) | $\text{score} < 0 \Rightarrow V \downarrow$ | Hue | Pada $A > 0$: $H$ bergeser menuju $90^\circ$ | Persamaan (15) dan (17) |
| 7 | SC tinggi (timbre cerah) | $\text{score} > 0 \Rightarrow V \uparrow$ | Hue | Pada $A > 0$: $H$ bergeser menuju $0^\circ$ | Persamaan (15) dan (17) |

---

## [8] Aturan Transisi Chase / Crossfade

Implementasi v10 memakai *cosine S-curve crossfading* antar *cue*, bukan ambang durasi per-BPM.

### 8.1 Interpolasi Crossfade

Progress waktu $p \in [0, 1]$ dihitung dari elapsed terhadap durasi *fade*, kemudian faktor pencampuran:

$$p = \min\!\left(1,\ \frac{t_{\text{elapsed}}}{t_{\text{fade}}}\right), \qquad \alpha = \frac{1}{2}\left( 1 - \cos(\pi p) \right) \tag{27}$$

$$\text{DMX}[ch] = \text{round}\big( \text{DMX}_{\text{start}}[ch] + \big( \text{DMX}_{\text{target}}[ch] - \text{DMX}_{\text{start}}[ch] \big) \cdot \alpha \big) \tag{28}$$

*Tick* crossfade berjalan setiap $23\text{ ms}$ (selaras dengan laju $43{,}07\text{ FPS}$). *Snap* instan dipakai bila $t_{\text{fade}} \le 0{,}05\text{ s}$ atau *cue* bertipe *flash*.

### 8.2 Pembangkitan *Section Cue* Berbasis Kuadran

*Section cues* (Intro/Verse/Chorus/Bridge/Ending) dibangkitkan dari palet warna hasil analisis dan label kuadran (`ui/panels/perform_tab.py`):

| Kuadran | Kelompok | `fade_in` (s) | `chase_rate` | Karakter |
|---------|----------|---------------|--------------|----------|
| Q3/Q4 (Worship) | Intro $\to$ Ending | $3{,}0 \to 3{,}0$ | $0{,}5$–$1{,}2$ | Reverensi dalam, rasio *white* tinggi |
| Q1/Q2 (Praise) | Intro $\to$ Ending | $1{,}5 \to 0{,}5$ | $1{,}0$–$2{,}5$ | Energi tinggi, warna jenuh, *chase* cepat |

### 8.3 Pola Multi-Fixture

1. **All On:** Semua *fixture* sama — untuk bagian energik.
2. **Running:** Satu *fixture* bergantian per *beat* — untuk *praise*.
3. **Gradient:** Kecerahan menurun *fixture* $1 \to N$ — untuk bagian tenang.
4. **Center-Out:** Tengah terang, sisi redup — untuk transisi.

---

## [9] Contoh Perhitungan Satu Frame (Karakter Worship)

Seluruh angka berikut **dihitung dengan menjalankan mesin v10** (`EmotionModel.evaluate_frame()` dan `ColorEngine`) terhadap masukan ilustratif berikut (nilai fitur diwarisi dari contoh versi lama dokumen ini, sedangkan hasil akhir dihitung ulang dengan formalisme kanonik):

| Masukan | Nilai |
|---------|-------|
| $\text{RMS}_{\text{norm}}$ | $0{,}143$ |
| $\text{SC}_{\text{norm}}$ | $0{,}289$ |
| $B$ (BPM) | $73$ |
| Chroma (mayor, 12 dimensi) | $[1{,}0;\ 0{,}1;\ 0{,}1;\ 0{,}1;\ 0{,}9;\ 0{,}1;\ 0{,}1;\ 0{,}8;\ 0{,}1;\ 0{,}1;\ 0{,}1;\ 0{,}1]$ |
| `onset_norm`, `mfcc_norm` | $0{,}500$ (contoh ilustrasi bernilai netral) |

**Langkah 1 — Skor masukan:**

- $\text{Mode}_{\text{score}} = 0{,}0574$ (Persamaan (12))
- $\text{score}(\text{SC}_{\text{norm}}) = 2(0{,}289) - 1 = -0{,}4220$
- $\text{score}(\text{RMS}_{\text{norm}}) = 2(0{,}143) - 1 = -0{,}7140$
- $\text{Tempo}_{\text{score}} = 2\frac{73 - 50}{120} - 1 = -0{,}6167$
- $\text{score}(\text{Onset}_{\text{norm}}) = \text{score}(\text{MFCC}_{\text{norm}}) = 2(0{,}5) - 1 = 0$ (ilustrasi masukan netral)

**Langkah 2 — Valence & Arousal:**

$$V = 0{,}50(0{,}0574) + 0{,}30(-0{,}4220) + 0 = -0{,}0979$$

$$A = 0{,}50(-0{,}7140) + 0{,}30(-0{,}6167) + 0 = -0{,}5420$$

$\Rightarrow$ **Kuadran Q3** (`Q3_DEEP_WORSHIP`) — khidmat/kontemplatif, sesuai karakter *worship*.

**Langkah 3 — HSV polar:**

- $H = \text{atan2}(-0{,}5420;\ -0{,}0979) \Rightarrow 259{,}76^\circ$ (sektor biru–magenta)
- $S = \text{clip}\!\left(\sqrt{0{,}0979^2 + 0{,}5420^2}/\sqrt{2}\right) = 0{,}3895$
- $V_{hsv} = 0{,}143$

**Langkah 4 — RGB $\to$ RGBW:**

- RGB $= (27,\ 22,\ 36)$
- $W = \min = 22 \Rightarrow R' = 5,\ G' = 0,\ B' = 14$
- **Output DMX: $R=5,\ G=0,\ B=14,\ W=22$** — putih redup kebiruan, sesuai karakter *worship*.

**Referensi mapping yang digunakan:**
- BPM $73$ (lambat) $\to$ *low arousal* $\to$ warna tenang [31]
- Modus mayor lemah-positif ($\text{Mode}_{\text{score}} = 0{,}0574$) $\to$ valence mendekati netral $\to$ warna lembut [24]
- $\text{SC}_{\text{norm}}$ rendah ($\text{score} = -0{,}422$) $\to$ Valence turun $\to$ warna cenderung lembut/gelap [10]

---

## [10] Parameter Tunable (Default Implementasi v10)

| Parameter | Default | Sumber kode | Pengaruh |
|-----------|---------|-------------|----------|
| $w_{V}$ (mode, centroid, MFCC) | $0{,}50,\ 0{,}30,\ 0{,}20$ | `EmotionModel.w_valence` | Komposisi Valence |
| $w_{A}$ (RMS, tempo, onset) | $0{,}50,\ 0{,}30,\ 0{,}20$ | `EmotionModel.w_arousal` | Komposisi Arousal |
| Jendela tempo | $[50,\ 170] \to [-1,\ 1]$ | `evaluate_frame()` | Sensitivitas tempo |
| Clamp tempo | $[50,\ 190]$ BPM | `estimate_tempo_bpm()` | Batas estimasi BPM |
| $S_{\min}$ | $0{,}2$ | `emotion_to_hsv()` | Lantai saturasi |
| $D_{\text{master}}$ | $1{,}0$ | `process_frame()` | Skala *Value* |
| $N,\ H,\ f_s$ | $2048,\ 512,\ 22050$ | `STFTEngine` | Resolusi STFT / $43{,}07\text{ FPS}$ |
| Tick crossfade | $23\text{ ms}$ | `_crossfade_timer` | Kelancaran transisi |

---

> **Penutup — Arsip Versi Lama.** Persamaan dan tabel versi sebelumnya (domain $V$–$A$ $[0, 1]$, *hue* *piecewise* per kuadran dengan ambang $0{,}5$, bobot Arousal $0{,}40/0{,}35/0{,}25$, serta normalisasi min–maks tetap ala `librosa`) telah diarsipkan dan digantikan sepenuhnya oleh formalisme kanonik di atas, mengikuti keputusan kanonik **7 Oktober 2026 — implementasi ZZLUXORA v10**. Angka-angka pada dokumen ini berasal langsung dari `core/emotion_model.py`, `core/color_engine.py`, `core/feature_extractor.py`, `core/fft_engine.py`, `core/models.py`, `ui/main_window.py`, dan `ui/panels/perform_tab.py`.
