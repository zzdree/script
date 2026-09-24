# 🎓 CLAUDE.md — Panduan Konteks & Direktif Proyek Skripsi ZZLUXORA

Dokumen ini adalah **single source of truth** dan instruksi operasional untuk Claude Code dalam mendampingi pengerjaan skripsi, riset komputasi audio, dan pengembangan perangkat lunak **ZZLUXORA**.

---

## 📌 1. Identitas Akademik & Penelitian

- **Peneliti:** Andreas Restuawanta Christwara (`NIM: 5312422036`)
- **Dosen Pembimbing:** Mario Norman Syah, S.Pd., M.Eng. (`NIP: 199304212024061001`)
- **Institusi:** Program Studi S1 Teknik Komputer, Jurusan Teknik Elektro, Fakultas Teknik, Universitas Negeri Semarang (UNNES)
- **Judul Skripsi:** 
  > *"Rancang Bangun Sistem Audio-Reactive Lighting Design Berbasis Analisis Mood Lagu Rohani dengan Pemetaan Warna HSV-RGBW dan Protokol Art-Net DMX512"*
- **Repositori Utama:** `https://github.com/zzdree/script.git` (Branch: `main`)
- **Workspace Dev Saat Ini:** `/home/zzdree/ANDREAS/script/`

---

## 🎯 2. Status Skripsi & Target Naskah

### Berkas Naskah Eksisting & Target Iterasi:
- **Draf Eksisting (v3):** `script_projects/script_andreas_v3.docx` (Bab 1, 2, dan 3 yang telah dipresentasikan ke Dosen Pembimbing).
- **Target Selanjutnya (v4):** Membuat naskah **`script_andreas_v4.docx`** yang telah merevisi dan menyempurnakan seluruh catatan bimbingan.

### PR Utama dari Dosen Pembimbing (Mario Norman Syah, S.Pd., M.Eng.):
> **"Disuruh belajar lagi tentang FFT, ngulitin lagi lah, terus menjabarkan lengkap di proposal."**

Claude wajib mendalami, menguliti secara matematis, dan menguraikan secara komprehensif teori serta implementasi:
1. **Dasar Matematika Fourier Transform:**
   - Continuous Fourier Transform (CFT) ➔ Discrete Fourier Transform (DFT) ➔ Fast Fourier Transform (FFT, algoritma Cooley-Tukey $\mathcal{O}(N \log N)$).
2. **Short-Time Fourier Transform (STFT):**
   - Fenomena non-stasioner pada sinyal musik.
   - Analisis Windowing (Fungsi Hamming, Hanning, Blackman) untuk meminimalkan *spectral leakage*.
   - Parameter komputasi: Sampling Rate ($f_s$), Frame Size / Window Length ($N$), Hop Length / Stride ($H$), serta kompromi resolusi waktu vs. resolusi frekuensi (*Gabor limit / uncertainty principle*).
3. **Representasi Spektogram & Ekstraksi Fitur Musik (MIR):**
   - Perhitungan Bin Frekuensi: $f(k) = \frac{k \cdot f_s}{N}$.
   - Magnitude Spectrum & Power Spectrum.
   - **Root Mean Square (RMS) Energy:** Perhitungan intensitas energi sinyal per frame.
   - **Spectral Centroid:** Titik berat spektrum frekuensi (indikator kecerahan timbre/brightness) yang diturunkan langsung dari FFT.
   - **Chroma STFT / Chromagram:** Proyeksi energi spektral ke 12 kelas nada kromatik (C, C#, D, ..., B) untuk identifikasi harmoni (Mayor vs Minor).
   - **Mel-Frequency Cepstral Coefficients (MFCC):** Filterbank skala Mel berbasis persepsi pendengaran manusia + Discrete Cosine Transform (DCT).
4. **Penjabaran dalam Naskah:**
   - Menuliskan rumus matematis formal, penjelasan variabel, dan interpretasi visual pada **Bab 2 (Kajian Pustaka / Landasan Teori)** dan **Bab 3 (Metodologi Penelitian / Rancang Bangun)**.

---

## 📚 3. Referensi Format & Standar Penulisan

Dalam menyusun naskah dan dokumen skripsi, Claude wajib merujuk pada:

1. **Pedoman Resmi UNNES:**
   - `script_projects/script_guide.pdf` — Buku Pedoman Penulisan Skripsi Fakultas Teknik UNNES (format margin, font, spasi, penomoran bab/subbab, tabel, gambar, sitasi APA/IEEE).
2. **Komparasi Format Skripsi Final Teman (Benchmark Struktur & Bahasa):**
   - `script_projects/script_elang_final.docx`
   - `script_projects/script_nafi_final.docx`
   - `script_projects/script_nanda_chapter_1_2_3.pdf`
   - `script_projects/script_naufal_final.docx`
   *Catatan:* Ambil dan pelajari **pola format, sistematika penulisan, gaya bahasa akademis baku, dan kelengkapan bab**, bukan menyalin isi kontennya.
3. **Pengelolaan Daftar Pustaka (Dapus):**
   - Ekstrak seluruh sumber literatur dari `script_andreas_v3.docx`.
   - Unduh dan kumpulkan berkas PDF sumber primer ke folder `script_references/`.
   - Tambahkan referensi jurnal internasional terkini (IEEE, ACM, ISMIR, Elsevier) terkait MIR, FFT, dan affective computing untuk naskah `v4`.
4. **Folder Naskah & Catatan:**
   - `markdowns/` dan `notes/`: Digunakan sebagai ruang kerja drafting/re-develop teks sebelum dikompilasi ke format Word `.docx`.

---

## 💻 4. Arsitektur Software ZZLUXORA

**ZZLUXORA** adalah aplikasi pengontrol pencahayaan panggung pementasan dan ibadah berbasis analisis audio pintar.

### Riwayat & Rencana Rilis:
- Repositori GitHub saat ini: `zzdree/zzluxora-v7`, `zzdree/zzluxora-v8`, `zzdree/zzluxora-v8.5`, `zzdree/zzluxora-v9`.
- **Evaluasi User:** Versi **v7** memiliki basis tata letak/konsep yang paling disukai pengguna, namun fungsionalitasnya belum berjalan sempurna.
- **Target Rilis Berikutnya:** **ZZLUXORA v10** (fresh development & clean architecture).

### Strategi & Tahapan Pengembangan Software:
1. **Fase 1: Engine System / Core First (Fokus Utama Saat Ini)**
   - Pembangunan Audio Engine komputasional murni:
     - Pipeline FFT (Cooley-Tukey Radix-2 DIT) & STFT (Hann Windowing, $f_s = 22.050\text{ Hz}$, $N=2048$, $H=512$).
     - Ekstraksi 4 fitur spektral utama: RMS Energy, Spectral Centroid, Chroma STFT (12-semitone pitch classes), dan MFCC (13 koefisien).
     - Pemetaan afektif Russell 2D Plane (Valence-Arousal).
     - Konversi ruang warna: $(V, A) \to (H, S)$ ➔ Dimmer $V_{\text{lum}} = \text{RMS}_{\text{norm}}$ ➔ HSV ke RGB ➔ Physical 4-Kanal RGBW ($W = \min(R,G,B)$, $R'=R-W$, $G'=G-W$, $B'=B-W$).
     - Art-Net 4 DMX512 UDP packet generator (Universe 0, Port 6454, target output 43 FPS).
2. **Fase 2: UI/UX Console Panggung (GrandMA3 & QLC+ Style)**
   - Disiapkan sembari mengonsep tata letak (bisa menggunakan Figma / mockups visual).
   - Mengacu pada `notes/feedback_v2.txt` dan koleksi visual di `image_references/`.
   - Layout modular: Header bar, Status Art-Net + Blackout, Grid DMX Address (maks 24 kolom), Mixer 513 Fader (Master + 512 DMX), Tab Analyze, Tab Scenes/Chase, Visualizer 2D PAR LED, dan Fixture Editor.

---

## ⚡ 5. Arsitektur Hardware Prototipe

- **File Firmware:** `artnet_projects/artnet_dmx_final.ino`
- **Spesifikasi Perangkat:**
  - Board: ESP32 DevKit V1 (Dual-Core Tensilica LX6 240 MHz).
  - Transceiver RS-485: MAX485 Module via Hardware Serial UART2 (`TX = GPIO 17`, `RX = GPIO 16`, `DE/RE = GPIO 4`).
  - Indikator Status: LCD 16x2 I2C (`SDA = GPIO 21`, `SCL = GPIO 22`).
  - Jaringan: Wi-Fi Station Mode & SoftAP Captive Portal (`192.168.4.1`).
  - Output Fisik: DMX512-A standard (250.000 baud, 8N2, Break $\ge 88\ \mu\text{s}$, MAB $\ge 8\ \mu\text{s}$).
- **Status:** Hardware ini **sudah tuntas dan berfungsi** sebagai prototipe fisik / jembatan skripsi ke lampu nyata.

---

## 🔄 6. Konfigurasi Lingkungan Kerja (2 Laptop Multi-Agent Setup)

| Parameter | Laptop Dev (Aktif Saat Ini) | Laptop Utama (Server Room) |
| :--- | :--- | :--- |
| **Model / Nama** | ASUS VivoBook X407MA | Acer Swift 3 (`swift356g`) |
| **OS** | Linux Mint | Windows 10/11 |
| **Direktori Project** | `/home/zzdree/ANDREAS/script/` | `D:\andreas\script\` |
| **Peran Utama** | Penulisan naskah, riset, Python coding | Sinkronisasi data drive, build executable `.exe` / installer |
| **Jaringan & Router** | Terhubung via **9router (decolua)** | Terhubung via **9router (decolua)** |
| **Agent CLI** | `claude` CLI & `agy` CLI | `claude` CLI & `agy` CLI |

### ⚠️ Aturan Disiplin Sinkronisasi Git:
1. **GitHub sebagai Single Source of Truth:**
   - Semua perubahan di laptop ini **wajib di-commit dan di-push ke GitHub** (`zzdree/script`, branch `main`).
   - Di laptop utama, pembaruan data **wajib dilakukan via `git pull origin main`** di `D:\andreas\script`.
2. **Larangan Keras:**
   - **JANGAN PERNAH** menimpa/copy-paste folder project secara manual antar laptop! Hal ini dapat merusak direktori `.git` dan memicu konflik data yang sulit dipulihkan.

---

## 🛠️ 7. Prinsip Kerja & Panduan Interaksi Claude

1. **Komunikasi:** Gunakan Bahasa Indonesia yang ramah, jelas, terstruktur, dan berwawasan teknis mendalam.
2. **Kualitas Akademis:** Naskah skripsi harus menggunakan bahasa baku akademik sesuai kaidah PUEBI, EYD V, dan pedoman resmi Fakultas Teknik UNNES.
3. **Rigorous Mathematics:** Setiap perumusan FFT, STFT, dan konversi warna harus dijabarkan variabelnya secara gamblang dan presisi (siap dicantumkan pada naskah skripsi).
4. **Verifikasi Sebelum Klaim:** Pastikan setiap file, referensi, atau instruksi dicek keberadaannya secara nyata di dalam sistem file sebelum memberikan kesimpulan.
