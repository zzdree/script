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
- **Repositori Software:** `https://github.com/zzdree/zzluxora-v10.git` (Folder: `/home/zzdree/ANDREAS/zzluxora_v10/`)

### Riwayat & Rencana Rilis:
- Repositori GitHub lama: `zzdree/zzluxora-v7`, `zzdree/zzluxora-v8`, `zzdree/zzluxora-v8.5`, `zzdree/zzluxora-v9`.
- **Evaluasi User:** Versi **v7** memiliki basis tata letak/konsep yang paling disukai pengguna, namun fungsionalitasnya belum berjalan sempurna.
- **Target Rilis Mutakhir:** **ZZLUXORA v10** (Fresh development & clean modular architecture).

### Status Implementasi Software ZZLUXORA v10:
1. **Fase 1: Engine System / Core First — STATUS: TUNTAS 100% & TERVERIFIKASI**
   - Zero-GUI Pure Python/NumPy core engine di `core/`:
     - Pipeline FFT (Cooley-Tukey Radix-2 DIT) & STFT (Hann Windowing, $f_s = 22.050\text{ Hz}$, $N=2048$, $H=512$, $43.07\text{ FPS}$).
     - Ekstraksi 5 fitur spektral: RMS Energy (Parseval), Spectral Centroid, Chroma STFT 12-semitone (C s.d. B), MFCC (13 koefisien), dan Spectral Flux (Onset Detection/Beat Tracking).
     - Pemetaan afektif Russell 2D Plane ($V, A \in [-1.0, 1.0]$) dengan klasifikasi kuadran ibadah (Q1 Praise vs Q3 Deep Worship).
     - Konversi ruang warna cross-modal: $(V, A) \to (H, S)$ ➔ Dimmer $V_{\text{lum}} = \text{RMS}_{\text{norm}}$ ➔ HSV ke sRGB ➔ Dekomposisi Physical 4-Kanal RGBW ($W = \min(R,G,B)$, $R'=R-W$, $G'=G-W$, $B'=B-W$) anti-washout.
     - Art-Net 4 DMX512 UDP packet generator (530 byte paket biner: 18B header little-endian opcode + 512B payload, Universe 0, Port 6454).
     - Seluruh 11 unit test standar (`tests/test_*.py`) lulus 100%.

2. **Fase 2: UI/UX Console Panggung (GrandMA3 & QLC+ Style) — STATUS: TUNTAS & MODULAR**
   - Dibangun menggunakan **PySide6 / PyQt6** berbasis `feedback_v1.txt` dan `feedback_v2.txt`.
   - **Tanpa Splashscreen:** Konsol langsung terbuka seketika (*instant launch*) tanpa jeda splashscreen.
   - **Arsitektur Modular (`ui/`):**
     - `styles.py`: Industrial dark theme (`#0e1013`), token warna kanal DMX, dan master QSS.
     - `icons.py`: Generator ikon SVG prosedural (lampu panggung, hamburger, play/pause, blackout).
     - `main_window.py`: Header bar terintegrasi, menu bar File/View/Help, indikator Art-Net, tombol play/pause toggle, dan tombol Master Blackout (reset fader ke 0).
     - `sidebar.py`: Navigasi hamburger responsif dengan indikator aktif.
     - `panels/address_tab.py`: Grid DMX 512 kanal (24 kolom horizontal, auto-patch sekuensial, inspektor kanal).
     - `panels/analyze_tab.py`: Core skripsi audio analyzer dengan grafik bidang afektif Russell 2D live dan progress bar saintifik.
     - `panels/scenes_tab.py` & `chase_tab.py`: Pemetaan cue terstruktur lagu (Verse, Chorus, Bridge) dan BPM timing engine.
     - `panels/page_tab.py`: Tombol virtual executor playback langsung panggung.
     - `panels/mixer_tab.py`: 513 slider fader fisik industri (1 Master Dimmer + 512 DMX channels 0–255).
     - `panels/preview_tab.py`: Visualizer panggung 2D tampak depan dengan rendering cahaya PAR LED dinamis (RGBW glow) dan draggable fixtures.
     - `panels/output_tab.py`: Pengaturan jaringan Art-Net UDP 6454 (Localhost, ESP32 AP 192.168.4.1, Custom IP).
     - `panels/fixture_editor.py` & `fixture_list.py`: Editor profil lampu JSON dan drawer perpustakaan lampu.

---

## ⚡ 5. Arsitektur Hardware Prototipe

- **File Firmware:** `artnet_projects/artnet_dmx_final.ino`
- **Spesifikasi Perangkat:**
  - Board: ESP32 DevKit V1 (Dual-Core Tensilica LX6 240 MHz).
  - Transceiver RS-485: MAX485 Module via Hardware Serial UART2 (`TX = GPIO 17`, `RX = GPIO 16`, `DE/RE = GPIO 4`).
  - Indikator Status: LCD 16x2 I2C (`SDA = GPIO 21`, `SCL = GPIO 22`).
  - Jaringan: Wi-Fi Station Mode & SoftAP Captive Portal (`192.168.4.1`).
  - Output Fisik: DMX512-A standard (250.000 baud, 8N2, Break $\ge 88\ \mu\text{s}$, MAB $\ge 8\ \mu\text{s}$).
- **Status Saat Ini:** Hardware fisik sedang dipinjam rekan untuk kegiatan panggung, sehingga pengujian aktif dialihkan ke lingkungan simulasi **Software-in-the-Loop (SITL)** menggunakan QLC+.

---

## 🎛️ 6. Lingkungan Simulasi QLC+ (Dual-Version Setup di Linux Mint)

Untuk memungkinkan pengujian visual fader bergerak secara *real-time* tanpa hardware fisik, sistem Linux Mint telah dikonfigurasi dengan dua instalasi QLC+ resmi yang berdampingan:

### Perintah Terminal:
- `qlc+4` atau `qlcplus4`: Menjalankan **QLC+ v4.14.4 (Latest Stable)** — native C++ Qt Widgets, sangat ringan dan stabil untuk live show.
- `qlc+5` atau `qlcplus5`: Menjalankan **QLC+ v5.2.2 (Latest Beta)** — modern QML dengan visualizer 3D panggung terpadu (terpasang di `/opt/qlcplus5/`).
- `qlcplus`: Memunculkan pesan pengingat agar pengguna wajib menyertakan nomor versi (`qlc+4` atau `qlc+5`).

### Berkas Menu Start / App Library:
1. 💡 **Q Light Controller Plus v4**
2. 💡 **Q Light Controller Plus v5**
3. 🛠️ **Fixture Definition Editor**

### Pipeline Pengujian Software-in-the-Loop (SITL):
- **Template Workspace:** `/home/zzdree/ANDREAS/zzluxora_test.qxw` (memuat 4 unit PAR LED RGBW kanal 1-16, Art-Net loopback `127.0.0.1:6454` Universe 1 dengan Passthrough aktif).
- **Skrip Jembatan Loopback:** `/home/zzdree/ANDREAS/zzluxora_v10/tools/qlc_bridge_test.py` (mentransmisikan gelombang fader 43 FPS ke QLC+ Simple Desk dan Virtual Console).

---

## 🔄 7. Konfigurasi Lingkungan Kerja (2 Laptop Multi-Agent Setup)

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

## 🛠️ 8. Prinsip Kerja & Panduan Interaksi Claude

1. **Komunikasi:** Gunakan Bahasa Indonesia yang ramah, jelas, terstruktur, dan berwawasan teknis mendalam.
2. **Kualitas Akademis:** Naskah skripsi harus menggunakan bahasa baku akademik sesuai kaidah PUEBI, EYD V, dan pedoman resmi Fakultas Teknik UNNES.
3. **Rigorous Mathematics:** Setiap perumusan FFT, STFT, dan konversi warna harus dijabarkan variabelnya secara gamblang dan presisi (siap dicantumkan pada naskah skripsi).
4. **Verifikasi Sebelum Klaim:** Pastikan setiap file, referensi, atau instruksi dicek keberadaannya secara nyata di dalam sistem file sebelum memberikan kesimpulan.
