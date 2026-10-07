# 🎓 ZZLUXORA: Audio-Reactive Lighting Research & Thesis Ecosystem

> **Tugas Akhir / Skripsi Sarjana Teknik Komputer**  
> **Judul:** *"Rancang Bangun Sistem Audio-Reactive Lighting Design Berbasis Analisis Mood Lagu Rohani dengan Pemetaan Warna HSV-RGBW dan Protokol Art-Net DMX512"*  
> **Peneliti:** Andreas Restuawanta Christwara (`NIM: 5312422036`)  
> **Dosen Pembimbing:** Mario Norman Syah, S.Pd., M.Eng. (`NIP: 199304212024061001`)  
> **Institusi:** Program Studi Teknik Komputer, Jurusan Teknik Elektro, Fakultas Teknik, Universitas Negeri Semarang (UNNES)

---

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/GUI-PySide6%20%2F%20Qt6-41CD52?style=flat-square&logo=qt&logoColor=white)
![Art-Net](https://img.shields.io/badge/Protocol-Art--Net_DMX512_(UDP_6454)-orange?style=flat-square)
![Hardware](https://img.shields.io/badge/Hardware-ESP32_DevKit_V1_%2B_MAX485-E7352C?style=flat-square&logo=espressif&logoColor=white)
![Status](https://img.shields.io/badge/Status-Public_Showcase-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-Proprietary_(All_Rights_Reserved)-red?style=flat-square)

---

## 📑 Daftar Isi
1. [Ringkasan Eksekutif & Latar Belakang](#-1-ringkasan-eksekutif--latar-belakang)
2. [Pipeline Komputasi & Model Matematika](#-2-pipeline-komputasi--model-matematika)
3. [Arsitektur Hardware & Firmware ESP32](#-3-arsitektur-hardware--firmware-esp32)
4. [Katalog & Struktur Direktori Berkas](#-4-katalog--struktur-direktori-berkas)
5. [Metodologi Penelitian & Pengujian](#-5-metodologi-penelitian--pengujian)
6. [Daftar Pustaka & Literatur Utama](#-6-daftar-pustaka--literatur-utama)
7. [Hak Cipta & Kerahasiaan](#-7-hak-cipta--kerahasiaan)

---

## 📋 1. Ringkasan Eksekutif & Latar Belakang

Pencahayaan panggung (*stage lighting design*) pada kebaktian gereja modern memegang peranan vital dalam membangun atmosfer peribadatan dan memperdalam penghayatan jemaat. Dinamika ibadah umumnya terbagi menjadi dua suasana kontras:
* **Segmen Pujian (*Praise*):** Musik berirama cepat (*upbeat/high tempo*), membutuhkan pencahayaan dinamis, saturasi warna cerah (*warm/vibrant*), serta pergerakan lampu yang energik.
* **Segmen Penyembahan (*Worship*):** Musik bertempo lambat (*slow tempo/ambient*), membutuhkan pencahayaan bernuansa teduh, warna kontemplatif (*cool/calm*), dan transisi lembut (*smooth fading*).

### Permasalahan yang Dihadapi:
1. **Human Delay & Fatigue:** Operator pencahayaan manual sering mengalami keterlambatan respons visual saat lagu mengalami transisi mendadak (*drop/chorus*).
2. **Inkonsistensi Nuansa Warna:** Pemilihan warna manual kerap tidak selaras dengan struktur tangga nada (mayor/minor) dan pesan emosional lagu.
3. **Keterbatasan Operator Ahli:** Kebutuhan operator pencahayaan profesional yang terlatih sering kali sulit dipenuhi di gereja-gereja lokal.

### Solusi Penelitian (ZZLUXORA):
Penelitian ini merancang dan membangun **ZZLUXORA**, sebuah sistem otomasi pencahayaan cerdas (*Audio-Reactive Stage Lighting*) yang mengintegrasikan komputasi **Music Information Retrieval (MIR)**, pemodelan emosi **Valence-Arousal (Russell Circumplex Model)**, algoritma konversi warna **HSV ➔ RGB ➔ Physical RGBW**, serta komunikasi jaringan berkecepatan tinggi via **Art-Net DMX512 (UDP 6454)** ke mikrokontroler **ESP32**.

---

## 🔬 2. Pipeline Komputasi & Model Matematika

Sistem memproses berkas audio lagu rohani melalui 6 tahapan komputasi berurutan:

```text
+-----------------------------------------------------------------------------------------+
|                              PIPELINE SISTEM ZZLUXORA                                   |
+-----------------------------------------------------------------------------------------+
  [1] AUDIO INPUT       : File Audio Lagu Rohani (.wav / .mp3 / .flac)
          │
          ▼
  [2] MIR EXTRACTION    : Ekstraksi Fitur Akustik Komputasional (Librosa):
                          • RMS Energy          : Intensitas energi rata-rata (Loudness)
                          • Tempo / BPM         : Kecepatan ketukan dan deteksi onset
                          • Spectral Centroid   : Titik berat spektrum frekuensi (Kecerahan Timbre)
                          • Chroma STFT         : Distribusi 12 nada kromatik (Major vs Minor)
                          • MFCC (13 Koef.)     : Karakteristik tekstur dan timbre vokal/instrumen
          │
          ▼
  [3] NORMALISASI       : Min-Max Feature Scaling ke rentang [0.0, 1.0]:
                          x_norm = (x - x_min) / (x_max - x_min)
          │
          ▼
  [4] MODEL AFEKTIF     : Pemetaan ke Koordinat 2D Valence-Arousal (Russell):
                          • Valence (V) = f(Chroma_Major_Ratio, Spectral_Centroid, MFCC)
                          • Arousal (A) = f(RMS_Energy, Tempo_BPM, Onset_Strength)
          │
          ▼
  [5] COLOR CONVERSION  : Transformasi Ruang Warna Cross-Modal:
                          • (Valence, Arousal) ➔ Hue (0° - 360°), Saturation (0 - 1)
                          • RMS Energy ➔ Dimmer / Value (0 - 1)
                          • HSV ➔ RGB ➔ Physical 4-Channel RGBW
          │
          ▼
  [6] DMX TRANSMISSION  : Pengemasan Frame Paket ArtDmx (Universe 0)
                          ➔ UDP Broadcast (Port 6454) ➔ ESP32 Node ➔ MAX485 DMX512
+-----------------------------------------------------------------------------------------+
```

### Algoritma Dekomposisi 4-Kanal Physical RGBW:
Untuk memanfaatkan kanal *White* murni pada lampu PAR LED panggung dan mencegah warna menjadi pudar (*washout*):

```text
W = min(R, G, B)
R' = R - W
G' = G - W
B' = B - W
Output Final = [R', G', B', W] * Master_Intensity
```

---

## ⚡ 3. Arsitektur Hardware & Firmware ESP32

Sistem menggunakan node mikrokontroler mandiri berbasis **ESP32 DevKit V1** yang terhubung ke jaringan Wi-Fi lokal untuk menerima paket Art-Net dan mengubahnya menjadi sinyal serial diferensial standar DMX512 (RS-485).

### Spesifikasi Teknis Perangkat Keras:
| Komponen | Spesifikasi & Fungsi |
| :--- | :--- |
| **Mikrokontroler** | ESP32 DevKit V1 (Dual-Core 240 MHz, 520 KB SRAM, Wi-Fi 802.11 b/g/n) |
| **DMX Transceiver** | MAX485 Module (Half-Duplex RS-485 Differential Transceiver) |
| **Koneksi UART** | Hardware Serial UART2 (`TX = GPIO 17`, `RX = GPIO 16`, `DE/RE = GPIO 4`) |
| **Protokol DMX512** | Laju Baud 250.000 bps, 8 Data Bits, 2 Stop Bits (*Break* 88 µs, *MAB* 8 µs) |
| **Status Display** | LCD 16x2 dengan modul I2C Backpack (`SDA = GPIO 21`, `SCL = GPIO 22`) |
| **Fitur Firmware** | Dual-Buffer FreeRTOS Mutexing, Captive Portal Web UI, Auto-Reconnect |

---

## 📁 4. Katalog & Struktur Direktori Berkas

```text
SCRIPT/
├── 📂 script_projects/        <- Naskah Skripsi Lengkap Microsoft Word (.docx) & Pedoman FT UNNES
│   ├── script_andreas_v1.docx     <- Draf awal proposal skripsi
│   ├── script_andreas_v2.docx     <- Draf revisi bab 1-3
│   ├── script_andreas_v3.docx     <- Naskah skripsi terstruktur bab 1-3
│   ├── script_guide.pdf           <- Buku Pedoman Penulisan Skripsi Fakultas Teknik UNNES
│   ├── script_nafi.docx           <- Referensi komparasi format naskah skripsi
│   └── script_nanda.pdf           <- Referensi pengujian skripsi terdahulu
│
├── 📂 script_references/      <- Gudang Literatur Jurnal Ilmiah Internasional (MIR & Affective Model)
│   ├── Bock_2021_Beat_Tempo_MultiTask.pdf    <- Ekstraksi tempo & beat tracking multi-task neural network
│   ├── Castellon_2021_Audio_Language_MIR.pdf <- Pemrosesan sinyal representasi audio MIR
│   ├── Guo_2022_Multimodal_Music_Emotion.pdf <- Pengenalan emosi musik multimodal
│   ├── Hung_2022_Audio_Benchmark.pdf         <- Tolok ukur representasi audio & klasifikasi fitur
│   ├── Li_2024_FFA-BiGRU_Music_Emotion.pdf   <- Klasifikasi mood musik berbasis BiGRU & Attention
│   ├── Won_2021_CNN_Music_Tagging.pdf        <- Arsitektur CNN untuk evaluasi audio tagging
│   └── ESP32_Technical_Reference_Manual.pdf  <- Datasheet & manual teknis mikrokontroler ESP32
│
├── 📂 artnet_projects/        <- Firmware Mikrokontroler Node ESP32 + MAX485 Transceiver
│   ├── artnet_dmx_final.ino       <- Firmware final ESP32 Art-Net receiver to DMX512 driver
│   ├── artnet_dmx_prompt.txt      <- Dokumentasi rekayasa rancangan firmware
│   └── artnet_dmx_v1-v4.txt       <- Riwayat iterasi kode firmware pengujian
│
├── 📂 image_references/       <- Diagram Skema Arsitektur Sistem, Flowchart, & Hardware Wiring
│   ├── image_01.png               <- Diagram Blok Arsitektur Komputasi Sistem
│   ├── image_02.png               <- Flowchart Alur Pemrosesan Fitur Musik ke Frame DMX
│   ├── image_03.png               <- Skema Rangkaian Wiring Hardware ESP32 & MAX485
│   ├── image_04.png               <- Diagram Koordinat Emosi Valence-Arousal
│   └── image_05.png               <- Screenshot Antarmuka Pengujian Aplikasi ZZLUXORA
│
├── 📂 markdowns/              <- Naskah Lengkap Bab 1-3, Model Matematika, PRD, & Panduan Bimbingan
│   ├── script_titles.md           <- Lembar judul resmi skripsi, identitas, & kata kunci
│   ├── script_chapter_01.md       <- Naskah Lengkap BAB 1 (Latar Belakang, Rumusan, Tujuan, Manfaat)
│   ├── script_chapter_02.md       <- Naskah Lengkap BAB 2 (Kajian Pustaka, Landasan Teori, Hipotesis)
│   ├── script_chapter_03.md       <- Naskah Lengkap BAB 3 (Metode Penelitian 4D/ADDIE, Prosedur Uji)
│   ├── script_math_model.md       <- Penjabaran Formula Matematis Ekstraksi Fitur & Transformasi Warna
│   ├── script_questionnaires.md   <- Kuesioner Pengujian Ahli Sistem & Uji Usability (SUS)
│   ├── script_plans.md            <- Jadwal & Rencana Timeline Pengerjaan Skripsi
│   ├── script_references.md       <- Daftar Pustaka Standar IEEE / APA
│   ├── app_prd.md                 <- Product Requirements Document (PRD) Sistem ZZLUXORA
│   ├── app_plan.md / app_upgrade.md <- Rancangan Upgrade Arsitektur Aplikasi
│   └── artnet_dmx_review.md       <- Hasil Audit Review Komunikasi Protokol Art-Net
│
├── 📂 notes/                  <- Catatan Bimbingan Dosen & Riwayat Evaluasi Proposal
│   ├── feedback_v1.txt / v2.txt   <- Catatan Masukan Dosen Pembimbing
│   └── prompt_v1-v4.docx          <- Arsip naskah ide prompt riset
│
├── 📄 LICENSE                <- Lisensi Proprietary & Perlindungan Hak Cipta Skripsi\n└── 📄 README.md              <- Dokumentasi resmi repositori riset skripsi
```

---

## 🧪 5. Metodologi Penelitian & Pengujian

Penelitian ini menggunakan metode **Research and Development (R&D)** dengan pendekatan model pengembangan sistem terstruktur:

1. **Pengujian Fungsionalitas Audio Engine:** Menguji akurasi deteksi ketukan (*beat tracking*) dan nilai *spectral centroid* terhadap variasi genre lagu rohani.
2. **Pengujian Kinerja Jaringan (*Latency Test*):** Mengukur waktu propagasi paket Art-Net UDP melalui Wi-Fi hingga output DMX fisik (target latensi < 40 ms untuk responsivitas visual *real-time*).
3. **Pengujian Penerimaan Pengguna (*User Acceptance Test*):** Evaluasi antarmuka dan kemudahan penggunaan menggunakan instrumen **System Usability Scale (SUS)** kepada operator gereja dan praktisi *lighting*.

---

## 📚 6. Daftar Pustaka & Literatur Utama

1. **Böck, S., & Davies, M. E. (2021).** *Deconstruct, Compose, Predict: Beat and Downbeat Tracking with Multi-Task Learning.* Journal of New Music Research.
2. **Castellon, R., Donahue, C., & Liang, P. (2021).** *Towards Transfer Learning for Audio Language Models in Music Information Retrieval.* IEEE Transactions on Audio, Speech, and Language Processing.
3. **Guo, X., et al. (2022).** *Multimodal Music Emotion Recognition Using Audio and Lyrics.* ACM Multimedia.
4. **Li, Y., & Zhang, J. (2024).** *Music Emotion Classification Based on FFA-BiGRU with Feature Attention Mechanism.* IEEE Access.
5. **Won, M., Ferraro, A., Choi, K., & Serra, X. (2021).** *Evaluation of CNN-based Models for Music Auto-Tagging.* ISMIR.

---

## 🔒 7. Hak Cipta & Kerahasiaan

```text
HAK CIPTA TERPELIHARA (C) 2026 ANDREAS RESTUAWANTA CHRISTWARA.
PROGRAM STUDI TEKNIK KOMPUTER, JURUSAN TEKNIK ELEKTRO,
FAKULTAS TEKNIK, UNIVERSITAS NEGERI SEMARANG (UNNES).

SELURUH NASKAH DOKUMEN, FIRMWARE, DAN DATA PENELITIAN INI BERSIFAT
RAHASIA (PROPRIETARY / PRIVATE RESEARCH ARCHIVE).
```
