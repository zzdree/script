# Proposal Skripsi ZZLIGHT-Luxora — Implementation Plan (Revisi v3)

## Konteks
**Mahasiswa:** Andreas Restuawanta Christwara (NIM 5312422036)  
**Prodi:** Teknik Komputer, Jurusan Teknik Elektro, UNNES  
**Jalur:** Skripsi (Penelitian)  
**Target:** Menyusun dokumen proposal untuk diajukan ke dosen pembimbing

**Fokus Penelitian:** Rule-Based Audio Feature Mapping untuk Lighting Control  
**Judul Final:** "Implementasi Rule-Based Audio Feature Mapping untuk Sistem Lighting Design RGBW Otomatis dengan Protokol Art-Net DMX512"

---

## Deliverables Overview

| # | Deliverable | Output File |
|---|------------|-------------|
| 1 | BAB 1 — Pendahuluan | `script_01.md` |
| 2 | BAB 2 — Kajian Pustaka | `script_02.md` |
| 3 | BAB 3 — Metode Penelitian | `script_03.md` |
| 4 | Model Matematis + Tabel Mapping Eksplisit | `script_math_model.md` |
| 5 | Referensi (IEEE) | `script_references.md` |
| 6 | Kuesioner (SUS + Kesesuaian Pencahayaan) | `script_questionnaire.md` |
| 7 | Dokumen DOCX Final | `script_andreas_v3.docx` |

---

## Keputusan Desain Penelitian

### Framing Utama
- **BUKAN** mood detection / mood recognition / AI-based emotion classification
- **MELAINKAN** Rule-Based Audio Feature Mapping: pemetaan deterministik dari fitur audio ke parameter pencahayaan RGBW berdasarkan aturan eksplisit dan model matematis

### Terminologi yang Digunakan
| ✅ Boleh | ❌ Tidak Boleh |
|---------|---------------|
| Pemetaan fitur audio | Mood detection |
| Karakteristik audio | Akurasi mood |
| Kesesuaian persepsi pengguna | Prediksi mood |
| Konsistensi rule-based mapping | Akurasi emosi |
| Tingkat penerimaan pengguna | Klasifikasi emosi |
| Respon visual | AI mood recognition |

### Segmentasi Lagu
- **TIDAK** menggunakan segmentasi otomatis verse/chorus/bridge (MIR tingkat lanjut, risiko tinggi)
- **MENGGUNAKAN** beat tracking dan onset detection saja (librosa)
- Perubahan scene berbasis beat dan onset strength, bukan struktur lagu

### Pengujian
- **Responden:** 25 orang (anggota Youth + jemaat Gereja GIA Deliksari)
- **Instrumen:** 2 saja → SUS + Kesesuaian Pencahayaan (UAT dihapus)
- **Variabel dependen:** 3 kategori:
  - **Teknis:** End-to-end latency, packet loss rate, black-box test pass rate
  - **Visual:** Skor kesesuaian pencahayaan (Likert 1-5)
  - **Usability:** Skor SUS (0-100)

### Detail Teknis
- Double buffering, spinlock, core affinity → cukup ditulis "sinkronisasi data" di proposal, detail masuk BAB 4 implementasi
- Donasi gereja → dipindahkan ke Kata Pengantar, bukan di BAB 1

---

## 1. BAB 1 — Pendahuluan (`script_01.md`)

### Struktur

#### 1.1 Latar Belakang
**Alur: Umum → Khusus → Masalah → Solusi**

| Paragraf | Topik | Sumber |
|----------|-------|--------|
| 1 | Peran pencahayaan dalam ibadah gereja modern | Referensi kontekstual |
| 2 | Tantangan lighting design di gereja kecil | Pengalaman peneliti |
| 3 | Korelasi karakteristik audio dengan parameter visual | Palmer (2013), Lindborg (2021) |
| 4 | Teknologi Art-Net, DMX512, ESP32, QLC+ | [14]-[17] |
| 5 | Gap: belum ada sistem audio-to-lighting + Art-Net + affordable | Literature gap |
| 6 | Solusi: ZZLIGHT-Luxora + modul ARTNET-DMX | Peneliti |

> Paragraf donasi/motivasi pribadi dipindahkan ke Kata Pengantar

#### 1.2 Batasan Masalah
- Input: file audio (.mp3/.wav) lagu rohani
- Analisis: rule-based audio feature mapping (bukan ML/AI)
- Deteksi dinamika: beat tracking dan onset detection (bukan segmentasi verse/chorus)
- Pemetaan: model matematis HSV → RGBW
- Output: DRGBW per scene/chase
- Transmisi: Art-Net via virtual adapter/WiFi
- Hardware: ESP32 → MAX485 → XLR → PAR LED RGBW
- Pengujian: GIA Deliksari, 25 responden

#### 1.3 Rumusan Masalah
1. Bagaimana merancang dan membangun sistem audio-reactive lighting design?
2. Bagaimana mengintegrasikan output pencahayaan via Art-Net DMX512?
3. Bagaimana kinerja sistem dari aspek teknis (latency, packet loss, fungsionalitas), kesesuaian pencahayaan, dan usability?

#### 1.4 Tujuan Penelitian
- Sesuai rumusan masalah

#### 1.5 Manfaat Penelitian
- Teoretis + Praktis (tanpa donasi)

#### 1.6 Kebaruan Penelitian
- Rule-based, HSV-RGBW, lagu rohani, end-to-end, pengguna awam

---

## 2. BAB 2 — Kajian Pustaka (`script_02.md`)

### Struktur

#### 2.1 Tinjauan Pustaka
- 2.1.1 Penelitian audio-reactive lighting systems
- 2.1.2 Penelitian korelasi fitur audio dengan parameter visual
- 2.1.3 Penelitian korespondensi lintas-modal musik-warna
- 2.1.4 Penelitian IoT lighting control
- 2.1.5 Posisi Penelitian

#### 2.2 Landasan Teori
- 2.2.1 DSP/MIR (FFT, STFT, fitur audio, beat tracking, onset detection)
  - **TANPA** segmentasi verse/chorus/bridge
- 2.2.2 Psikologi Persepsi Musik dan Warna (Circumplex, V-A, Lindborg, Palmer)
- 2.2.3 Model Warna dan Pemetaan Matematis (HSV, RGB, RGBW)
- 2.2.4 Lampu PAR LED RGBW
- 2.2.5 Art-Net dan DMX512
- 2.2.6 ESP32 (tanpa detail spinlock/double-buffering)
- 2.2.7 QLC+

#### 2.3 Kerangka Berpikir
- Pipeline tanpa segmentasi verse/chorus

#### 2.4 Hipotesis Teoritis

---

## 3. BAB 3 — Metode Penelitian (`script_03.md`)

### Struktur

#### 3.3 Subjek Penelitian
- **25 responden** (Youth + jemaat GIA Deliksari)
- Purposive sampling

#### 3.4 Variabel Penelitian (DIPANGKAS)
**Variabel Dependen — 3 Kategori:**

| Kategori | Variabel | Satuan |
|----------|----------|--------|
| Teknis | End-to-End Latency | ms |
| Teknis | Packet Loss Rate | % |
| Teknis | Black-box Test Pass Rate | % |
| Visual | Skor Kesesuaian Pencahayaan | Skala 1-5 |
| Usability | Skor SUS | 0-100 |

#### 3.7 Teknik Pengumpulan Data
- Black-box testing + latency measurement
- Kuesioner SUS (10 item standar)
- Kuesioner Kesesuaian Pencahayaan (6 item)
- **TANPA** UAT

---

## 4. Model Matematis (`script_math_model.md`)

### Pipeline
```
Audio File → Ekstraksi Fitur → Normalisasi → V-A → HSV → RGB → RGBW → DRGBW
```

### Tabel Mapping Eksplisit (BARU — senjata sidang)
Tabel lengkap: fitur audio → range → dampak V-A → HSV → warna visual → referensi

### Rules Chase/Transisi (DIREVISI)
- Berbasis beat tracking dan onset strength
- TANPA referensi verse/chorus/bridge

---

## 5. Kuesioner (`script_questionnaire.md`)

### 2 Instrumen:
1. **SUS** — 10 item standar
2. **Kesesuaian Pencahayaan** — 6 item (reframed dari "mood" ke "karakteristik audio/pencahayaan")

---

## Open Questions (Resolved)

| # | Pertanyaan | Keputusan |
|---|-----------|-----------|
| 1 | Judul final | "Implementasi Rule-Based Audio Feature Mapping untuk Sistem Lighting Design RGBW Otomatis dengan Protokol Art-Net DMX512" |
| 2 | Segmentasi lagu | Beat tracking + onset detection saja |
| 3 | Jumlah responden | 25 orang |
| 4 | Instrumen kuesioner | SUS + Kesesuaian Pencahayaan (UAT dihapus) |
| 5 | Tabel mapping | Dibuat dengan referensi Palmer (2013), Lindborg (2021), dll. |
| 6 | DOCX generation | Setelah semua .md di-review dan di-approve |

> [!WARNING]
> File `script_andreas_v1.docx` dan `script_andreas_v2.docx` **tidak akan diubah**. Output baru → `script_andreas_v3.docx`.
