---
name: dsp-math
description: Panduan penulisan perumusan matematis Digital Signal Processing (DSP), Fast Fourier Transform (FFT), STFT, dan konversi format rumus LaTeX ke Word OMML / MathML untuk naskah skripsi teknik.
---

# DSP Math — Formulasi Sinyal & Notasi Rumus Ilmiah

Panduan perumusan matematis pemrosesan sinyal audio digital dan penulisan persamaan ilmiah baku agar tidak berformat teks mentah (*raw plain text*) di naskah Microsoft Word (`.docx`).

## 1. Konversi Format Rumus: Dari Teks Mentah ke Word Math (OMML)
Masalah pada proposal `v3` adalah penulisan rumus masih berupa raw text / raw latex tanpa blok formula terformat, misalnya:
`RMS = \sqrt{\frac{1}{N} \sum_{i=1}^N x_i^2}`

### Solusi Pembuatan File Word (.docx):
Ketika menyusun dokumen Word secara terprogram (misal via Python):
1. **Gunakan Elemen XML OMML (Office Math Markup Language):**
   - Tag `<m:oMath>` dan `<m:oMathPara>` di dalam namespace `http://schemas.openxmlformats.org/officeDocument/2006/math`.
   - Atau menggunakan pustaka `latex2mathml` / converter OMML sehingga persamaan otomatis terdeteksi sebagai blok rumus resmi Microsoft Word (terpusat, bernomor di kanan, font Cambria Math).
2. **Alternatif Gambar Persamaan Beresolusi Tinggi:**
   - Render rumus LaTeX ke format SVG vektor transparan atau PNG 300 DPI lalu sisipkan ke dokumen dengan penomoran rapi:
     $$\text{Persamaan } (2.1)$$

## 2. Bank Rumus Standar Proyek Skripsi ZZLUXORA

### 2.1 Discrete Fourier Transform (DFT)
$$X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j \frac{2\pi}{N} kn} = \sum_{n=0}^{N-1} x[n] \left[ \cos\left(\frac{2\pi kn}{N}\right) - j \sin\left(\frac{2\pi kn}{N}\right) \right]$$

### 2.2 Short-Time Fourier Transform (STFT Diskrit)
$$X[m, k] = \sum_{n=0}^{N-1} x[n + mH] \cdot w[n] \cdot e^{-j \frac{2\pi}{N} kn}$$
dengan fungsi Hann window:
$$w[n] = 0{,}5 \left[ 1 - \cos\left( \frac{2\pi n}{N-1} \right) \right], \quad 0 \le n \le N-1$$

### 2.3 Spectral Centroid (Titik Pusat Massa Frekuensi)
$$\text{Centroid}[m] = \frac{\sum_{k=0}^{N/2} f_k \cdot |X[m, k]|}{\sum_{k=0}^{N/2} |X[m, k]|}, \quad f_k = \frac{k \cdot f_s}{N}$$

### 2.4 Root Mean Square (RMS Energy)
$$\text{RMS}[m] = \sqrt{ \frac{1}{N} \sum_{n=0}^{N-1} \left| x[n + mH] \cdot w[n] \right|^2 }$$

### 2.5 Dekomposisi 4-Kanal Physical RGBW
$$\begin{aligned}
W &= \min(R, G, B) \\
R' &= R - W \\
G' &= G - W \\
B' &= B - W \\
\text{Output DMX} &= \text{round}\left( [R', G', B', W] \cdot 255 \cdot V_{\text{master}} \right)
\end{aligned}$$
