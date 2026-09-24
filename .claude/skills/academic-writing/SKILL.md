---
name: academic-writing
description: Panduan penulisan naskah akademis skripsi/tesis standar Fakultas Teknik Universitas Negeri Semarang (UNNES), sitasi IEEE numerik, struktur bab 1-3, perumusan kebaruan, dan tata bahasa baku ilmiah.
---

# Academic Writing — Standar Skripsi FT UNNES (Teknik Komputer)

Panduan operasional penyusunan naskah proposal dan skripsi ilmiah di lingkungan Program Studi Teknik Komputer, Jurusan Teknik Elektro, Fakultas Teknik UNNES.

## 1. Aturan Tata Tulis & Tipografi Resmi (Pedoman FT UNNES)
- **Kertas:** A4 ($210\text{ mm} \times 297\text{ mm}$), $80\text{ gram}$.
- **Margin Halaman (4-3-3-3):**
  - Kiri (*Left*): **4 cm** (ruang penjilidan naskah).
  - Atas (*Top*): **3 cm**.
  - Kanan (*Right*): **3 cm**.
  - Bawah (*Bottom*): **3 cm**.
- **Font & Ukuran:** Times New Roman ukuran 12pt (teks utama), 10pt (keterangan tabel/gambar), 14pt tebal (*Bold*) untuk judul bab.
- **Spasi:**
  - Teks paragraf utama: **1.5 spasi**.
  - Judul bab, subbab, kutipan langsung > 4 baris, judul tabel, dan judul gambar: **1.0 spasi (single)**.
  - Spasi antar paragraf: 0 pt after/before (indentasi baris pertama $1\text{ cm}$ atau $1{,}27\text{ cm}$).
- **Penomoran Halaman:**
  - Halaman awal (Judul, Pengesahan, Abstrak, Daftar Isi): angka romawi kecil (i, ii, iii, ...) di bawah tengah.
  - Halaman Bab I s.d. Daftar Pustaka: angka arab (1, 2, 3, ...) di kanan atas, kecuali halaman pertama tiap Bab diletakkan di bawah tengah.

## 2. Sistematika Naskah Proposal (Bab I s.d. Bab III)
### BAB I: PENDAHULUAN
- **1.1 Latar Belakang:** Dimulai dari fenomena umum $\to$ urgensi panggung ibadah gereja $\to$ masalah human delay & inkonsistensi operator $\to$ solusi komputasi cerdas audio-reactive $\to$ gap riset terdahulu.
- **1.2 Batasan Masalah:** Menegaskan ruang lingkup (format audio, ruang warna RGBW PAR LED, protokol Art-Net UDP, board ESP32).
- **1.3 Rumusan Masalah:** Dirumuskan dalam kalimat tanya yang terukur dan dapat diuji.
- **1.4 Tujuan Penelitian:** Menjawab rumusan masalah secara langsung.
- **1.5 Manfaat Penelitian:** Dibagi menjadi Manfaat Teoretis (pengembangan ilmu MIR & affective computing) dan Manfaat Praktis (bagi operator gereja dan industri panggung).
- **1.6 Kebaruan Penelitian (*State-of-the-Art*):** Tabel perbandingan sistematis dengan penelitian terdahulu yang menonjolkan orisinalitas riset.

### BAB II: KAJIAN PUSTAKA
- **2.1 Tinjauan Pustaka:** Ringkasan kritis paper terdahulu (bukan sekadar daftar resume), memetakan posisi penelitian saat ini.
- **2.2 Landasan Teori:** Teori matematis dan teknis yang mendalam:
  - Digital Signal Processing (DSP) & Music Information Retrieval (MIR).
  - Fast Fourier Transform (FFT) & Short-Time Fourier Transform (STFT) secara mendalam.
  - Ekstraksi Fitur Musik: RMS Energy, Spectral Centroid, Chroma STFT, MFCC.
  - Model Emosi Musik 2D Russell (Valence-Arousal).
  - Konversi Ruang Warna Cross-Modal (HSV $\to$ RGB $\to$ RGBW 4-Channel).
  - Protokol Jaringan Art-Net 4 & Standar Kelistrikan DMX512-A (RS-485).
  - Mikrokontroler ESP32 DevKit V1 & Transceiver MAX485.
- **2.3 Kerangka Berpikir:** Diagram alur konseptual pemecahan masalah dari input audio hingga aksi lampu panggung.
- **2.4 Hipotesis Penelitian:** Pernyataan ilmiah teruji mengenai performa latensi (< 40 ms) dan korelasi afektif warna.

### BAB III: METODE PENELITIAN
- **3.1 Pendekatan & Prosedur Penelitian:** Research and Development (R&D) menggunakan metode prototyping / ADDIE.
- **3.2 Lokasi & Waktu:** Laboratorium pribadi & pengujian lapangan di GIA Deliksari Semarang.
- **3.3 Objek Penelitian:** Dataset lagu rohani (praise & worship) berformat .wav/.mp3.
- **3.4 Alat & Bahan:** Spesifikasi laptop pengembang, mikrokontroler ESP32, MAX485, PAR LED RGBW, Python 3.10+, Librosa, PySide6.
- **3.5 Alur Penelitian:** Flowchart detail tahapan riset dari studi pustaka hingga evaluasi.
- **3.6 Perancangan Sistem:** Diagram blok arsitektur hardware, firmware FreeRTOS, dan software pipeline ZZLUXORA.
- **3.7 Prosedur Pengujian:**
  - Pengujian Black-Box (fungsionalitas fitur).
  - Pengujian Latensi Jaringan (Art-Net UDP round-trip time).
  - Pengujian Akurasi Pemetaan Emosi (korelasi expert review).
  - Pengujian Usability (System Usability Scale / SUS kepada operator lighting).

## 3. Standar Sitasi & Daftar Pustaka (IEEE Numerik)
- Di dalam teks menggunakan tanda kurung siku: `...sebagaimana diteliti oleh Li et al. [1].` atau `...algoritma FFT Cooley-Tukey [4][5].`
- Daftar Pustaka diurutkan secara numerik berdasarkan urutan kemunculan pertama kali di dalam naskah.
- Setiap referensi wajib mencantumkan penulis, judul paper dalam tanda kutip, nama jurnal/prosiding bercetak miring, volume, nomor, halaman, tahun, dan DOI/URL valid.
