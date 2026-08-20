# Model Matematis: Pemetaan Fitur Audio ke RGBW

## Overview Pipeline

```
Audio File → Ekstraksi Fitur → Normalisasi [0,1] → V-A → HSV → RGB → RGBW → Scene/Chase → DRGBW
```

---

## [1] Ekstraksi Fitur Audio (librosa)

| Fitur | Fungsi librosa | Deskripsi |
|-------|---------------|-----------|
| Tempo/BPM | `librosa.beat.tempo()` | Kecepatan ketukan per menit |
| RMS Energy | `librosa.feature.rms()` | Energi rata-rata (loudness) |
| Spectral Centroid | `librosa.feature.spectral_centroid()` | "Kecerahan" suara |
| MFCC (13 koef.) | `librosa.feature.mfcc(n_mfcc=13)` | Karakteristik timbre |
| Chroma | `librosa.feature.chroma_stft()` | Distribusi 12 nada kromatik |
| Onset Strength | `librosa.onset.onset_strength()` | Kekuatan perubahan nada |
| Beat Frames | `librosa.beat.beat_track()` | Posisi setiap beat |

### Chroma Major Ratio
```python
major_indices = [0, 2, 4, 5, 7, 9, 11]
chroma_mean = np.mean(chroma, axis=1)
major_energy = np.sum(chroma_mean[major_indices])
chroma_major_ratio = major_energy / np.sum(chroma_mean)
```

---

## [2] Normalisasi Min-Max

$$x_{norm} = \frac{x - x_{min}}{x_{max} - x_{min}}$$

Clipping: $x_{norm} = \text{clip}(x_{norm}, 0, 1)$

| Fitur | x_min | x_max | Keterangan |
|-------|-------|-------|------------|
| BPM | 60 | 180 | Worship ~60-100, Praise ~100-180 |
| RMS | 0.01 | 0.50 | Volume rendah – tinggi |
| Spectral Centroid | 500 | 5000 | Hz, gelap – cerah |
| MFCC1 | -300 | 100 | Koefisien pertama |
| Onset Rate | 0.5 | 8.0 | Onset per detik |
| Chroma Major | 0.0 | 1.0 | Rasio energi nada mayor |

---

## [3] Perhitungan Valence & Arousal (Rule-Based)

### Arousal
$$A = 0.40 \cdot BPM_{norm} + 0.35 \cdot RMS_{norm} + 0.25 \cdot OnsetRate_{norm}$$

### Valence
$$V = 0.50 \cdot ChromaMajor_{norm} + 0.30 \cdot SC_{norm} + 0.20 \cdot (1 - |MFCC1_{norm} - 0.5| \times 2)$$

### Interpretasi Kuadran V-A

| Kuadran | V | A | Karakter | Contoh Lagu |
|---------|---|---|----------|-------------|
| Q1 | > 0.5 | > 0.5 | Praise, energik | "Way Maker" (chorus) |
| Q2 | ≤ 0.5 | > 0.5 | Intens, dramatis | "Revelation Song" (bridge) |
| Q3 | ≤ 0.5 | ≤ 0.5 | Kontemplatif | "What A Beautiful Name" (verse) |
| Q4 | > 0.5 | ≤ 0.5 | Damai, tenang | "10.000 Reasons" (worship) |

---

## [4] Pemetaan V-A → HSV

### Hue (H) — 0°–360°

$$H_{base} = \begin{cases}
30 + (V - 0.5) \times 60 & V > 0.5, A > 0.5 \text{ → warm (kuning/amber)} \\
270 + (0.5 - V) \times 120 & V \leq 0.5, A > 0.5 \text{ → ungu/magenta} \\
200 + (0.5 - V) \times 120 & V \leq 0.5, A \leq 0.5 \text{ → biru/indigo} \\
150 + (V - 0.5) \times 100 & V > 0.5, A \leq 0.5 \text{ → hijau/cyan}
\end{cases}$$

Koreksi chroma: $H = H_{base} + (ChromaPeak - 6) \times 5°$

### Saturation (S) — 0–1
$$S = 0.6 \cdot A + 0.4 \cdot |2V - 1|$$

### Value (V_hsv) — 0–1
$$V_{hsv} = \max(0.5 \cdot RMS_{norm} + 0.5 \cdot A, \; 0.10)$$

---

## [5] HSV → RGB (Foley & van Dam)

$$C = V_{hsv} \times S, \quad H' = \frac{H}{60°}, \quad X = C \times (1 - |H' \bmod 2 - 1|), \quad m = V_{hsv} - C$$

Berdasarkan sektor $H'$:

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

Nilai akhir: $R = R_1 + m$, $G = G_1 + m$, $B = B_1 + m$

---

## [6] RGB → RGBW

$$W = \min(R, G, B)$$
$$R' = R - W, \quad G' = G - W, \quad B' = B - W$$

Output 8-bit:
$$D_{out} = \text{round}(V_{hsv} \times 255), \quad R_{out} = \text{round}(R' \times 255), \quad G_{out} = \text{round}(G' \times 255)$$
$$B_{out} = \text{round}(B' \times 255), \quad W_{out} = \text{round}(W \times 255)$$

---

## [7] Tabel Rule-Based Mapping Eksplisit

Tabel berikut merupakan aturan pemetaan eksplisit yang menjadi dasar sistem ZZLIGHT-Luxora. Setiap aturan merujuk pada referensi penelitian yang telah dipublikasikan.

### 7.1 Pemetaan Fitur Audio → Valence-Arousal

| No | Fitur Audio | Range | Dampak pada V-A | Dasar Referensi |
|----|------------|-------|-----------------|-----------------|
| 1 | BPM 60–90 (lambat) | Low | Arousal ↓ | Juslin & Laukka (2003): tempo lambat → low arousal [31] |
| 2 | BPM 90–120 (sedang) | Mid | Arousal → | Eerola & Vuoskoski (2011) [9] |
| 3 | BPM 120–180 (cepat) | High | Arousal ↑ | Juslin & Laukka (2003): tempo cepat → high arousal [31] |
| 4 | RMS < 0.1 (pelan) | Low | Arousal ↓, V_hsv ↓ | Juslin & Laukka (2003): loudness rendah → low arousal [31] |
| 5 | RMS > 0.3 (keras) | High | Arousal ↑, V_hsv ↑ | Juslin & Laukka (2003): loudness tinggi → high arousal [31] |
| 6 | Chroma Major > 0.65 | Mayor | Valence ↑ | Palmer et al. (2013): modus mayor → valence positif [24] |
| 7 | Chroma Major < 0.45 | Minor | Valence ↓ | Palmer et al. (2013): modus minor → valence negatif [24] |
| 8 | SC < 2000 Hz (gelap) | Low | Warm color | Lindborg (2021): frek. rendah → warna hangat [10] |
| 9 | SC > 3500 Hz (cerah) | High | Cool color | Lindborg (2021): frek. tinggi → warna dingin [10] |
| 10 | Onset Rate tinggi | High | Transisi cepat | Juslin & Laukka (2003): artikulasi cepat → arousal tinggi [31] |

### 7.2 Pemetaan V-A → Warna (HSV)

| No | Kuadran V-A | Karakter | Hue Range | Warna Visual | Dasar Referensi |
|----|-------------|----------|-----------|-------------|-----------------|
| 1 | V>0.5, A>0.5 (Q1) | Praise/energik | 30°–60° | Kuning, amber, oranye | Palmer (2013): musik cepat+mayor → warna hangat, cerah [24] |
| 2 | V≤0.5, A>0.5 (Q2) | Intens/dramatis | 270°–330° | Ungu, magenta | Palmer (2013): musik intense → warna tersaturasi gelap [24] |
| 3 | V≤0.5, A≤0.5 (Q3) | Kontemplatif | 200°–260° | Biru, indigo | Palmer (2013): musik lambat+minor → warna dingin, gelap [24] |
| 4 | V>0.5, A≤0.5 (Q4) | Damai/tenang | 150°–200° | Cyan, hijau muda | Lindborg (2021): musik tenang → warna lembut [10] |

### 7.3 Pemetaan Fitur Audio → Parameter Lighting

| No | Fitur Audio | Range | Parameter Lighting | Nilai | Dasar |
|----|------------|-------|--------------------|-------|-------|
| 1 | RMS < 0.1 | Low | Dimmer | 50–100 | Brightness rendah untuk lagu pelan |
| 2 | RMS 0.1–0.3 | Mid | Dimmer | 100–200 | Brightness sedang |
| 3 | RMS > 0.3 | High | Dimmer | 200–255 | Brightness tinggi untuk lagu energik |
| 4 | Arousal > 0.5 | High | Saturation | 0.6–1.0 | Warna lebih vivid untuk lagu intens |
| 5 | Arousal ≤ 0.5 | Low | Saturation | 0.2–0.6 | Warna lebih lembut untuk lagu tenang |
| 6 | SC < 2000 Hz | Low | Hue shift | -15° (warmer) | Frekuensi rendah → hangat |
| 7 | SC > 3500 Hz | High | Hue shift | +15° (cooler) | Frekuensi tinggi → dingin |

---

## [8] Rules Chase/Transisi (Berbasis Beat & Onset)

| No | Kondisi Audio | Efek Lighting | Timing |
|----|--------------|---------------|--------|
| 1 | BPM > 120 | Chase running per beat, transisi cepat | ~500ms per scene |
| 2 | BPM 90–120 | Transisi sedang per beat | ~700ms per scene |
| 3 | BPM < 90 | Fade panjang/halus | ~1500ms per scene |
| 4 | Onset strength tinggi (> 0.7) | Transisi tajam (*snap*) | Instant |
| 5 | Onset strength rendah (< 0.3) | Fade halus (*crossfade*) | Gradual |
| 6 | Beat terdeteksi | Trigger scene change | Per beat |
| 7 | No beat (silence/intro) | Hold scene terakhir | — |

### Pola Multi-Fixture
1. **All On:** Semua fixture sama — untuk bagian energik (Arousal > 0.7)
2. **Running:** Satu fixture bergantian per beat — untuk praise (BPM > 120)
3. **Gradient:** Brightness menurun fixture 1→N — untuk bagian tenang (Arousal < 0.3)
4. **Center-Out:** Tengah terang, sisi redup — untuk transisi

---

## [9] Contoh Perhitungan: "10.000 Reasons" (Worship)

| Fitur | Raw | Norm |
|-------|-----|------|
| BPM | 73 | 0.108 |
| RMS | 0.08 | 0.143 |
| SC | 1800 | 0.289 |
| MFCC1 | -120 | 0.450 |
| Onset | 1.5 | 0.133 |
| Chroma Major | 0.72 | 0.720 |

**Arousal** = 0.40×0.108 + 0.35×0.143 + 0.25×0.133 = **0.126**
**Valence** = 0.50×0.720 + 0.30×0.289 + 0.20×0.900 = **0.627**

→ Q4 (V>0.5, A≤0.5): Damai/tenang ✅ (sesuai karakter worship)

**HSV:** H=162.7° (cyan), S=0.178, V=0.135
**RGBW output:** D=34, R=0, G=6, B=4, W=28 → Warm white redup ✅

**Referensi mapping yang digunakan:**
- BPM 73 (lambat) → low arousal → warna tenang [31]
- Chroma Major 0.72 (mayor) → valence positif → warna lembut [24]
- SC 1800 Hz (rendah) → warm hue shift [10]

---

## [10] Parameter Tunable

| Parameter | Default | Pengaruh |
|-----------|---------|----------|
| w₁–w₃ | 0.40, 0.35, 0.25 | Bobot Arousal |
| w₄–w₆ | 0.50, 0.30, 0.20 | Bobot Valence |
| α (S blend) | 0.60 | Balance saturasi |
| β (V blend) | 0.50 | Balance brightness |
| V_hsv_min | 0.10 | Min brightness |
