# Rencana Eksekusi FASE 6 — Pengujian Lapangan GIA Deliksari

**Sistem:** ZZLUXORA v10 (`zzdree/zzluxora-v10` @ `7c566d9`) + firmware `artnet_dmx_final.ino`
**Lokasi:** Gereja GIA Deliksari, Semarang
**Perangkat:** ESP32 DevKit V1 + MAX485 + LCD 16x2 I2C; 4 unit Alien AL36 (DMX 1/17/33/49)
**Dokumen ini:** urutan teknis yang dapat dieksekusi, melengkapi checklist pada `script_test_protocols.md` bagian 6.

> **Prasyarat status:** perangkat keras saat ini dipinjam rekan untuk kegiatan panggung. Seluruh langkah uji fisik menunggu perangkat kembali. Langkah 1 (pra-terbang) dan 6 (installer Windows) dapat dijalankan tanpa perangkat keras.

---

## 0. Ringkasan Urutan Eksekusi

| # | Tahap | Perangkat keras? | Estimasi |
|---|---|---|---|
| 1 | Pra-terbang: regresi SITL + verifikasi perangkat lunak | Tidak | 1 jam |
| 2 | Bring-up ESP32 (flash, SoftAP, `/status`) | Ya | 1 jam |
| 3 | Uji penerimaan paket & patch firmware penghitung | Ya | 2 jam |
| 4 | Pengukuran latensi end-to-end | Ya | 2 jam |
| 5 | Pengukuran packet loss | Ya | 1 jam |
| 6 | Build installer Windows 11 (Acer Swift 3) | Tidak | 2 jam |
| 7 | Uji black-box 24 kasus + uji kanal optik | Ya | 3 jam |
| 8 | Sesi responden (setelah semua keputusan dospem) | Ya | 4 jam |

---

## 1. Pra-Terbang (Tanpa Perangkat Keras)

Jalankan sebelum menyentuh perangkat keras, agar sesi di gereja tidak terbuang untuk kesalahan perangkat lunak.

```bash
cd /home/zzdree/ANDREAS/zzluxora_v10
python3 -m unittest discover -s tests -p "test_*.py"      # harus 74 lulus

# Uji peluncuran GUI dan alur Analyze MANUAL satu kali:
# klik Analyze pada satu lagu, pastikan tidak ada AttributeError dan
# statistik hasil muncul. (Bug pemanggilan load_audio_file pada 15 Okt 2026
# membuat jalur ini gagal sebelum diperbaiki.)
python3 main.py
```

Regresi SITL ke QLC+ (per instruksi `CLAUDE.md` proyek skripsi):

```bash
# Terminal 1: jalankan QLC+ v4 dengan workspace loopback Art-Net
qlc+4   # buka showfiles/zzluxora_test.qxw, aktifkan Art-Net input 127.0.0.1:6454

# Terminal 2: streaming gelombang fader 43 FPS dari ZZLUXORA
python3 tools/qlc_bridge_test.py
# Verifikasi fader QLC+ bergerak mengikuti gelombang.
```

**Lulus bila:** 74 test OK, alur Analyze GUI selesai tanpa error, dan fader QLC+ bergerak.

---

## 2. Bring-Up ESP32

```bash
# 2.1. Flash firmware (build platformio atau esptool sesuai toolchain yang dipakai)
#      Catat versi + hash firmware untuk CSV. Tandai firmware yang dipakai:
sha256sum artnet_projects/artnet_dmx_final.ino

# 2.2. Setelah boot, node membuka SoftAP "ARTNET-DMX" di 192.168.4.1.
#      Sambungkan laptop ke SSID tersebut (kata sandi: lihat catatan akses terbatas, JANGAN di CSV).

# 2.3. Verifikasi node hidup dan melaporkan status nyata:
curl -s http://192.168.4.1/status
# CATATAN: pada mode AP, handler /status saat ini mengembalikan nilai
# hardcoded ("ip":"192.168.4.1","status":"Connected"). Untuk bring-up yang
# benar, patch handler AP agar melaporkan WiFi.softAPIP() dan jumlah station.
# Lihat langkah 3.3.

# 2.4. Verifikasi LCD 16x2 menampilkan status terbaca.
```

---

## 3. Uji Penerimaan Paket & Patch Firmware Penghitung

Protokol (§2.2) menuntut packet loss dihitung dari **paket valid yang benar-benar diterima firmware**, bukan dari status UI. Firmware saat ini tidak memiliki penghitung. Tambahkan patch berikut.

### 3.1. Patch penghitung paket

Tambahkan variabel global dan naikkan pada handler UDP:

```c
// --- global, dekat variabel lain ---
static volatile uint32_t artnet_rx_count = 0;

// --- di dalam ArtNetUdp handler, saat paket valid diterima ---
artnet_rx_count++;
```

Ekspos di JSON `/status` (mode RUN maupun AP):

```c
json += "\"rx_count\":" + String(artnet_rx_count) + ",";
```

### 3.2. Verifikasi penghitung

```bash
# Kirim N paket terkendali dari laptop, lalu baca penghitung node.
python3 main.py --cli --ip 192.168.4.1 --duration 5.0
curl -s http://192.168.4.1/status | grep -o '"rx_count":[0-9]*'
# Bandingkan dengan jumlah paket yang dikirim. Selisih = packet loss nyata.
```

### 3.3. Patch /status mode AP agar jujur

Ganti nilai hardcoded pada handler AP dengan nilai nyata:

```c
String json = "{";
json += "\"ip\":\"" + WiFi.softAPIP().toString() + "\",";
json += "\"wifi\":\"" + String(WiFi.softAPSSID()) + "\",";
json += "\"stations\":" + String(WiFi.softAPgetStationNum()) + ",";
json += "\"rx_count\":" + String(artnet_rx_count) + ",";
json += "\"status\":\"" + String(WiFi.status() == WL_CONNECTED ? "STA" : "AP") + "\"";
json += "}";
```

**Lulus bila:** `curl /status` pada mode AP melaporkan jumlah station > 0 setelah laptop bergabung, membuktikan laptop benar-benar tersambung, bukan hanya AP menyala.

---

## 4. Pengukuran Latensi End-to-End

Protokol (§2.1) mensyaratkan definisi operasional yang dapat dipertanggungjawabkan: **waktu kirim paket sampai lampu merespons**. Bab 3 memakai ambang < 100 ms untuk H3.

### 4.1. Metode yang direkomendasikan

| Komponen | Alat | Catatan |
|---|---|---|
| t0 (paket dikirim) | Timestamp monotonic di sisi pengirim (`tx_host_monotonic_ns`) | Sudah ada di aplikasi |
| t1 (lampu merespons) | Kamera ponsel **slow-motion 240 fps** (resolusi 4,17 ms/frame) | Cukup untuk ambang 100 ms |
| Sinkronisasi | Rekam layar laptop + lampu dalam SATU klip | Menghilangkan kebutuhan sinkronisasi jam |

**Prosedur:**
1. Arahkan kamera sehingga **layar laptop** (menampilkan tombol Blackout/GO+) dan **lampu** terlihat dalam satu frame.
2. Mulai rekam slow-motion.
3. Picu transisi (mis. Blackout → ON) sambil merekam.
4. Hitung selisih frame antara perubahan piksel di layar dan perubahan cahaya lampu.
5. Konversi: `latensi_ms = selisih_frame × 4,17`.

**Batasan yang wajib dicatat:** resolusi 4,17 ms membatasi presisi. Jika hasil mendekati ambang 100 ms, gunakan fotodioda + osiloskop untuk presisi lebih tinggi. Jika tidak tersedia, **nyatakan latensi sebagai "terukur pada resolusi 4,17 ms"** dan jangan mengklaim presisi lebih halus.

### 4.2. Titik ukur alternatif (jika fotodioda tersedia)

Isi kolom `rx_to_dmx_ms` dan `dmx_marker_daq_ns` pada CSV hanya jika marker benar-benar diukur pada pencatat waktu yang sama dengan fotodioda. Jika tidak, biarkan `NA`.

---

## 5. Pengukuran Packet Loss

1. Jalankan streaming stabil selama durasi tetap (mis. 60 detik).
2. Baca `rx_count` node sebelum dan sesudah; selisih = paket diterima.
3. Hitung paket terkirim dari sisi pengirim (jumlah `send_frame()` sukses).
4. Isi kolom `run_tx_count`, `run_rx_unique_count`, `run_loss_count`, `run_loss_rate_pct` pada CSV.
5. Olah dengan `tools/analyze_field_data.py`:

```bash
python3 tools/analyze_field_data.py path/ke/measurement.csv
# Menghasilkan Tabel 4.14 siap salin; NA dihitung sebagai tidak terukur, bukan nol.
```

**Catatan kejujuran:** bila `rx_count` firmware tidak dapat diamati, nyatakan packet loss **tidak terukur**, bukan nol.

---

## 6. Build Installer Windows 11 (Acer Swift 3)

Dapat dikerjakan paralel tanpa perangkat keras.

### 6.1. Di laptop Acer Swift 3 (Windows)

```powershell
# Sinkronkan source
cd D:\andreas\script
git pull origin main
cd ..\zzluxora_v10
git pull origin main

# Siapkan lingkungan
py -3.11 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt pyinstaller

# Build satu berkas
pyinstaller --name ZZLUXORA `
  --windowed `
  --icon ui\assets\logo_zz.ico `
  --add-data "ui\assets;ui\assets" `
  --add-data "fixtures;fixtures" `
  --add-data "showfiles;showfiles" `
  --hidden-import PySide6.QtSvg `
  --noconfirm `
  main.py
```

### 6.2. Verifikasi build

```powershell
.\dist\ZZLUXORA\ZZLUXORA.exe
# Uji: aplikasi terbuka tanpa konsol, logo muncul di taskbar, tab Address tampil,
# dan patch 4x ALIEN (GIA) tersedia.
```

### 6.3. Kemas installer (Inno Setup)

Bungkus folder `dist\ZZLUXORA\` menjadi `ZZLUXORA-Setup-v10.exe` dengan skrip Inno Setup standar. Sertakan VC++ Redistributable bila diperlukan oleh build PySide6.

**Catatan:** `.venv` tidak dibuat di repo Linux ini, karena PyInstaller harus dijalankan pada Windows agar menghasilkan `.exe` yang benar.

---

## 7. Uji Black-Box 24 Kasus & Uji Kanal Optik

1. Jalankan seluruh 24 kasus FB-01 s.d. FB-24 (`script_test_protocols.md` bagian 3) pada versi aplikasi/firmware yang dicatat.
2. Catat hasil aktual dan status pada **Tabel 4.11** Bab 4 (kini 24 baris, selaras dengan protokol).
3. Rekap pada **Tabel 4.12** per kelompok (Aplikasi/patch, Audio/hasil, Showfile/Perform, Output/jaringan).
4. Uji kanal optik: kirim nilai rendah terkendali (dimmer dan R/G/B) ke setiap fixture satu per satu pada kondisi aman tanpa responden; catat fixture, alamat, nilai target, tampilan node/DMX, dan observasi cahaya. Verifikasi blackout dan pemulihan.

> **Penting:** jangan gunakan kasus FB-21 (play-gated) sebagai bukti dari status UI saja. Gunakan `tcpdump` pada loopback untuk membuktikan paket benar-benar berhenti saat PLAY nonaktif. Catat juga bahwa mode CLI `main.py --cli` mengirim tanpa gate (mode diagnostik), berbeda dari pengirim GUI.

---

## 8. Sesi Responden

Dijalankan **hanya setelah** seluruh keputusan pada `script_konsultasi_pembimbing.md` disetujui dosen pembimbing, terutama:
- pemilihan 3–5 lagu uji (dan memutuskan apakah bahan sintetis boleh dipakai atau perlu lagu asli),
- unit analisis dan agregasi rating,
- alpha dan aturan uji H1/H2/H3.

Urutan mengikuti `script_test_protocols.md` §6.1 poin 5–7.

---

## 9. Kriteria Selesai FASE 6

- [ ] 74 unit test lulus + alur Analyze GUI terverifikasi manual
- [ ] Firmware ter-flash dengan hash tercatat; `/status` melaporkan station & rx_count nyata
- [ ] Packet loss terukur dari penghitung firmware (bukan nol asumsi)
- [ ] Latensi terukur dengan metode dan resolusi yang dicatat
- [ ] 4 unit Alien AL36 merespons kanal dengan benar pada DMX 1/17/33/49
- [ ] Installer `ZZLUXORA-Setup-v10.exe` ter-build dan terverifikasi di Windows 11
- [ ] 24 kasus black-box tercatat pada Tabel 4.11
- [ ] CSV pengukuran diolah dengan `tools/analyze_field_data.py`
- [ ] Seluruh keputusan dospem disetujui sebelum sesi responden

---

*Disusun 15 Oktober 2026 sebagai pelengkap `script_test_protocols.md`. Semua langkah yang bergantung perangkat keras menunggu perangkat kembali dari peminjaman.*
