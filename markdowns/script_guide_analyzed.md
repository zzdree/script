# Analisis Panduan TA UNNES 2024 — Jalur SKRIPSI

## ✅ Keputusan: Jalur SKRIPSI

**Definisi Skripsi (UNNES)**: Laporan hasil penelitian kualitatif, kuantitatif, atau campuran, yang ditulis oleh mahasiswa dan dipertanggungjawabkan melalui mekanisme ujian sebagai salah satu persyaratan untuk memperoleh gelar sarjana.

**Konsekuensi**: Anda tidak hanya membangun sistem, tapi harus **meneliti** sesuatu dari sistem tersebut — misalnya menguji efektivitas, mengukur performa, atau menganalisis akurasi.

---

## 🎯 Rekomendasi Judul Skripsi

> **"Rancang Bangun Aplikasi Pembangkit Scene Lighting RGBW Berbasis Analisis Audio Lagu Rohani dengan Integrasi Protokol Art-Net"**

Alternatif:
1. "Rancang Bangun Sistem Otomasi Lighting Design Berbasis Analisis Sinyal Audio untuk Pengendalian Lampu RGBW melalui Protokol Art-Net"
2. "Pengembangan Aplikasi Audio-Reactive Lighting Controller dengan Output RGBW dan Transmisi Art-Net untuk Kegiatan Ibadah"

---

## 📐 Sistematika Penulisan Skripsi (BAB 3 Panduan UNNES)

### A. Proposal Skripsi (spasi 1,15)

**Bagian Awal:**
1. Sampul (soft cover, warna fakultas)
2. Halaman Judul
3. Persetujuan Pembimbing
4. Daftar Isi
5. Daftar Tabel / Gambar / Istilah (jika ada)

**Bagian Utama:**
```
BAB 1. PENDAHULUAN
  1.1 Latar Belakang
  1.2 Batasan Masalah
  1.3 Rumusan Masalah
  1.4 Tujuan Penelitian
  1.5 Manfaat Penelitian
  1.6 Kebaruan Penelitian

BAB 2. KAJIAN PUSTAKA
  2.1 Tinjauan Pustaka
  2.2 Landasan Teoretik
  2.3 Kerangka Berpikir
  2.4 Hipotesis Teoretis (bila ada)

BAB 3. METODE PENELITIAN
  3.1 Pendekatan, Jenis, dan Prosedur Penelitian
  3.2 Lokasi dan Waktu Penelitian
  3.3 Subjek Penelitian / Sampel dan Populasi
  3.4 Variabel Penelitian dan Definisi Operasional
  3.5 Hipotesis Statistik (bila ada)
  3.6 Data dan Sumber Data
  3.7 Teknik Pengumpulan Data
  3.8 Teknik Keabsahan Data
  3.9 Teknik Analisis Data
  3.10 Etika Penelitian (bila ada)
```

**Bagian Akhir:**
- Daftar Pustaka
- Lampiran Biodata Penulis
- Lampiran SK Pembimbing
- Lampiran Instrumen

### B. Laporan Skripsi (spasi 1,5)

Sama seperti proposal, ditambah:
- BAB 4. HASIL DAN PEMBAHASAN
- BAB 5. PENUTUP (Simpulan & Saran)
- Pengesahan Tim Penguji
- Pernyataan Keaslian (materai 10.000)
- Moto dan Persembahan
- Abstrak & Abstract (English)

---

## 🔬 Framing Penelitian untuk Skripsi

Karena skripsi = penelitian, Anda perlu membingkai proyek ini sebagai penelitian. Berikut contoh framing:

### Rumusan Masalah (contoh):
1. Bagaimana merancang dan membangun aplikasi yang dapat menghasilkan scene lighting RGBW secara otomatis berdasarkan analisis audio lagu rohani?
2. Bagaimana mengintegrasikan output scene lighting dari aplikasi ke protokol Art-Net untuk pengendalian lampu secara real-time?
3. Bagaimana performa sistem yang dibangun ditinjau dari aspek akurasi mapping audio-ke-warna, latency pengiriman Art-Net, dan kepuasan pengguna?

### Tujuan Penelitian (contoh):
1. Merancang dan membangun aplikasi pembangkit scene lighting RGBW berbasis analisis audio
2. Mengimplementasikan integrasi protokol Art-Net untuk transmisi data lighting secara real-time
3. Menguji performa sistem dari aspek fungsionalitas, latency, dan usability

### Variabel Penelitian (contoh):
- **Variabel Independen**: Fitur audio (frekuensi, energi, tempo/BPM)
- **Variabel Dependen**: Nilai RGBW scene, latency Art-Net, kepuasan pengguna

### Metode Pengujian (contoh):
1. **Pengujian Fungsional**: Black-box testing (semua fitur berjalan sesuai spesifikasi)
2. **Pengujian Performa**: Latency Art-Net (ms), throughput paket, sinkronisasi audio-to-light
3. **Pengujian Usability**: Kuesioner SUS (System Usability Scale) ke tim lighting gereja

---

## 📐 Format Penulisan

| Aspek | Proposal | Laporan |
|-------|----------|---------|
| Font | Times New Roman 12pt | Times New Roman 12pt |
| Spasi | **1,15** | **1,5** |
| Perataan | Justify (rata kiri-kanan) | Justify |
| Kertas | A4, satu kolom | A4, satu kolom |
| Margin | Kiri 4cm, Kanan 3cm, Atas 3cm, Bawah 3cm | Sama |
| Sitasi | IEEE (rekomendasikan untuk Tekkom) | IEEE |
| Ref Manager | Mendeley / Zotero / EndNote | Sama |

---

## ✅ Checklist Langkah Awal

### Fase 1: Administrasi
- [ ] Pastikan sudah **≥110 SKS**, semua MK wajib tanpa nilai E
- [ ] Pastikan sudah lulus MK prasyarat (statistika, metpen, dll.) minimal C
- [ ] Siapkan **KHS semester sebelumnya**

### Fase 2: Pengajuan Topik
- [ ] Tentukan judul final (diskusikan dengan calon dospem)
- [ ] Ajukan **usulan topik** ke koordinator prodi
- [ ] Tunggu verifikasi **tim verifikator prodi**
- [ ] Tunggu persetujuan **koorprodi**
- [ ] Koorprodi usulkan **SK Pembimbing** ke Dekan
- [ ] Dekan terbitkan **SK Pembimbing**

### Fase 3: Penyusunan Proposal
- [ ] Serahkan SK Pembimbing ke dosen pembimbing
- [ ] Cantumkan **mata kuliah TA** di KRS
- [ ] Mulai tulis proposal sesuai sistematika di atas
- [ ] Bimbingan proposal **minimal 4 kali** (catat di Sitedi)
- [ ] Dosen menyetujui proposal

### Fase 4: Pelaksanaan Penelitian
- [ ] Bangun aplikasi (audio analysis + scene generator + Art-Net)
- [ ] Lakukan pengujian (fungsional, performa, usability)
- [ ] Kumpulkan data hasil pengujian

### Fase 5: Penulisan Laporan
- [ ] Tulis BAB 4 (Hasil dan Pembahasan) berdasarkan data
- [ ] Tulis BAB 5 (Simpulan dan Saran)
- [ ] Bimbingan total **minimal 12 kali** (catat di Sitedi)
- [ ] Siapkan **draf artikel ilmiah** (tidak wajib publish, tapi harus ada)
- [ ] Cek **similarity level ≤ 25%**

### Fase 6: Sidang
- [ ] Naskah disetujui pembimbing untuk diujikan
- [ ] Selesaikan administrasi yudisium
- [ ] Ujian di depan tim penguji (minimal lulus **B** = 71-80)

---

## ⚠️ Catatan Penting

1. **Bimbingan wajib dicatat di Sitedi** — http://apps.unnes.ac.id/23
2. **Draf artikel ilmiah** harus dilampirkan meskipun tidak wajib dipublikasikan
3. **Revisi** setelah ujian harus selesai dalam **90 hari kalender**
4. Jika tidak lulus, bisa ujian ulang **maksimal 2 kali** selama masa studi
5. Penilaian: **Isi (60%)** + **Sikap Ilmiah (40%)**
