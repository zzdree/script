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

### Berkas Naskah & Status Iterasi:
- **Naskah Eksisting (v3):** `script_projects/script_andreas_v3.docx` (draf awal yang dipresentasikan ke dospem).
- **Naskah Proposal Mutakhir (v4) — STATUS: TUNTAS 100%:**
  - File: `script_projects/script_andreas_v4.docx` (2.58 MB, 555 paragraf).
  - Dilengkapi 8 gambar ilmiah resmi (monokrom IEEE standard, anti-slop) yang dihasilkan melalui 9Router.
  - Memuat 20 persamaan matematis bernomor resmi dalam font Cambria Math murni.
  - Memuat 33 daftar pustaka berstandar IEEE lengkap dengan sitasi dalam teks.
  - Bersih total dari pecahan rumus mentah (0 raw formula artifacts) dan tanpa kotak ASCII.
  - Telah mengintegrasikan Dosen Pembimbing resmi: Mario Norman Syah, S.Pd., M.Eng. (NIP: 199304212024061001).
- **Target Selanjutnya (v5):** Naskah lengkap Skripsi Bab 1 s.d. Bab 5 setelah implementasi aplikasi ZZLUXORA v10 dan pengujian lapangan di Gereja GIA Deliksari Semarang.

### PR Dosen Pembimbing (Mario Norman Syah, S.Pd., M.Eng.) — STATUS: TERSELESAIKAN:
> **"Disuruh belajar lagi tentang FFT, ngulitin lagi lah, terus menjabarkan lengkap di proposal."**

PR ini telah dikuliti secara matematis dan dijabarkan tuntas pada Bab 2 dan Bab 3 naskah v4:
1. **Dasar Matematika Fourier Transform:**
   - Diskritisasi sinyal $x[n] = x(n/f_s)$, kriteria Nyquist-Shannon ($f_s = 22.050\text{ Hz}, f_{\text{Nyquist}} = 11.025\text{ Hz}$).
   - Discrete Fourier Transform (DFT), simetri konjugat Hermitian $X[N-k] = X^*[k]$, kompleksitas $\mathcal{O}(N^2)$.
   - Fast Fourier Transform (FFT) Cooley-Tukey Radix-2 Decimation-in-Time (DIT) divide-and-conquer, twiddle factor $W_N^k$, butterfly operation, kompleksitas $\mathcal{O}(N \log_2 N)$ (akselerasi 186.2x, efisiensi 99.46%).
2. **Short-Time Fourier Transform (STFT):**
   - Penanganan sinyal musik non-stasioner via sliding windowing ($N=2048, H=512$, overlap 75%).
   - Pembobotan Hann Window $w[n] = \sin^2(\pi n / (N-1))$ meredam spectral leakage hingga $-31.5\text{ dB}$.
   - Resolusi frekuensi $\Delta f \approx 10.77\text{ Hz}$, waktu perbaruan $\Delta t_{\text{hop}} \approx 23.22\text{ ms}$, menghasilkan laju tepat $43.07\text{ FPS}$ yang sinkron alami dengan laju transmisi fisik DMX512 (44 FPS).
   - Prinsip Ketidakpastian Heisenberg-Gabor $\Delta t \cdot \Delta f \ge \frac{1}{4\pi}$.
3. **Ekstraksi Fitur Spektral (MIR):**
   - RMS Energy (Parseval's theorem) untuk dinamika master dimmer.
   - Spectral Centroid (center of mass frekuensi) untuk kecerahan timbre.
   - Chroma STFT (12-semitone pitch class profile C s.d. B) untuk tonalitas akord Mayor (sukacita/praise) vs Minor (khidmat/worship).
   - MFCC (13 koefisien via 40 Mel filterbanks + DCT-II) untuk tekstur instrumen akustik vs elektrik.
   - Spectral Flux untuk onset detection dan beat tracking.
4. **Daftar 8 Gambar Resmi Naskah Proposal v4:**
   - Gambar 2.1: Diagram Proses Segmentasi Jendela Geser STFT & Mitigasi Spectral Leakage Hann Window.
   - Gambar 2.2: Pemetaan Afektif 2D Valence-Arousal (Russell) ke Koordinat Warna Pencahayaan Panggung.
   - Gambar 2.3: Perbandingan Pencampuran Warna RGB Konvensional vs. Algoritma Dekomposisi 4-Kanal Physical RGBW.
   - Gambar 2.4: Diagram Kerangka Berpikir Penelitian Sistem Audio-Reactive Lighting ZZLUXORA.
   - Gambar 3.1: Diagram Alur Komputasi End-to-End Sistem ZZLUXORA (Audio to DMX).
   - Gambar 3.2: Skematik Rangkaian Elektronika Hardware Modul Node ESP32 + MAX485 + LCD + XLR.
   - Gambar 3.3: Diagram Alir Arsitektur Firmware ESP32 Dual-Core FreeRTOS (Core 0 UDP WiFi vs Core 1 DMX Driver).
   - Gambar 3.4: Denah Tata Letak Panggung, Pengkabelan DMX512 Daisy-Chain, WiFi Art-Net, & Responden di GIA Deliksari.

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
