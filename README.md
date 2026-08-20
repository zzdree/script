# 🎓 SCRIPT: Dokumen Naskah Skripsi & Riset Penelitian ZZLUXORA

> **Tugas Akhir / Skripsi:** Rancang Bangun Sistem Audio-Reactive Lighting Design Berbasis Analisis Mood Lagu Rohani dengan Pemetaan Warna HSV-RGBW dan Protokol Art-Net DMX512  
> **Penulis:** Andreas Restuawanta Christwara (NIM: 5312422036)  
> **Program Studi:** Teknik Komputer, Jurusan Teknik Elektro, Fakultas Teknik, Universitas Negeri Semarang (UNNES)

![Status](https://img.shields.io/badge/Status-Private_Research_Backup-red?style=flat-square)
![Hardware](https://img.shields.io/badge/Hardware-ESP32%20%2B%20MAX485-E7352C?style=flat-square&logo=espressif&logoColor=white)
![Protocol](https://img.shields.io/badge/Protocol-Art--Net%20DMX512-orange?style=flat-square)
![Institution](https://img.shields.io/badge/Institution-Universitas%20Negeri%20Semarang-blue?style=flat-square)

---

## 📖 Deskripsi Repositori

Repositori ini merupakan **penyimpanan terpusat (*backup repository*)** untuk seluruh dokumen naskah skripsi, paper literatur jurnal ilmiah, firmware perangkat keras (*hardware*), diagram sistem, dan catatan penelitian untuk tugas akhir sarjana teknik komputer.

---

## 📁 Struktur Direktori & Cakupan File

`	ext
SCRIPT/
├── 📂 script_projects/     <- Naskah Dokumen Skripsi Microsoft Word (.docx) & Pedoman Resmi UNNES
│   ├── script_andreas_v5_6.docx  <- Naskah Revisi Skripsi Final Terkini (Lengkap Gambar & Bab 1-3)
│   ├── script_andreas_v1-v5.docx <- Riwayat draf naskah skripsi sebelumnya
│   └── pedoman_skripsi_ft_unnes.pdf <- Buku Pedoman Penulisan Skripsi FT UNNES
│
├── 📂 script_references/   <- Gudang Literatur 21+ Paper Jurnal Ilmiah (MIR, Mood Audio, DMX)
│   ├── 02_castellon_2021_codified_audio.pdf
│   ├── 03_won_2021_cnn_music_tagging.pdf
│   ├── 04_hung_2022_benchmark_free_sound.pdf
│   ├── 05_bock_2021_tempo_beat.pdf
│   └── 06_fuentes_2021_music_structure.pdf (dan referensi lainnya)
│
├── 📂 artnet_projects/     <- Source Code & Firmware Mikrokontroler ESP32
│   └── artnet_dmx_final.ino      <- Firmware ESP32 Art-Net receiver to DMX512 MAX485 driver
│
├── 📂 image_references/    <- Diagram Arsitektur, Flowchart Program, & Skema Hardware
│   ├── diagram_1_arsitektur.png  <- Diagram Blok Arsitektur Sistem Lengkap
│   ├── diagram_2_alur_program.png <- Flowchart Alur Pemrosesan Audio ke DMX
│   ├── diagram_3_esp32.png       <- Skema Pengkabelan ESP32 + MAX485 + LCD 16x2
│   └── gambar_1_screenshot_app.png <- Screenshot Antarmuka Aplikasi GUI
│
├── 📂 markdowns/           <- Naskah Markdown Bab 1–3, Formula Matematika, PRD, & Panduan
│   ├── BAB_1_PENDAHULUAN.md
│   ├── BAB_2_LANDASAN_TEORI.md
│   ├── BAB_3_METODE_PENELITIAN.md
│   ├── RANCANGAN_MATEMATIKA_AUDIO_LIGHTING.md
│   └── PRD_ZZLUXORA.md
│
└── 📂 notes/               <- Catatan Evaluasi Bimbingan & Draf Prompt Pengembangan
`

---

## ⚡ Firmware Hardware ESP32 (rtnet_projects/)

Firmware mikrokontroler (rtnet_dmx_final.ino) berjalan pada modul **ESP32 DevKit V1**:
- **Penerima Art-Net UDP:** Mendengarkan paket data ArtDmx pada port standar 6454 (Universe 0).
- **Driver DMX512 Fisik:** Transceiver MAX485 pada pin UART2 (TX=17, RX=16, EN=4) dengan laju baud 250 kbps (2 stop bits).
- **Dual-Buffer Frame Safety:** Menggunakan ufferA dan ufferB bergantian via FreeRTOS mutexing untuk mencegah *flicker* atau frame tearing.
- **Captive Portal Configuration:** Web Server bawaan untuk konfigurasi SSID Wi-Fi dan universe tanpa perlu re-flash kode.
- **Display Status:** LCD 16x2 I2C untuk monitoring FPS frame rate, IP address, dan status koneksi secara *real-time*.

---

## 📜 Lisensi & Hak Cipta

Seluruh dokumen naskah, data penelitian, dan firmware ini merupakan karya asli tugas akhir sarjana milik **Andreas Restuawanta Christwara (@zzdree)** - Program Studi Teknik Komputer, Universitas Negeri Semarang (UNNES).
