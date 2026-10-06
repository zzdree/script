# 🎛️ Feedback ZZLUXORA — v4 (Precision Console Polish & To-The-Point UX)

- **Sumber:** User Review & Feedback v4 (Penyempurnaan Presisi UI/UX, Anti-Overengineering, Full Control Visualizer & 100% English Interface)
- **Referensi:** grandMA2 & grandMA3 onPC Console, QLC+ v4 & v5 Fixture Definition Editor & 3D Stage
- **Dokumentasi:** Terstruktur, Rapi, Standar Rekayasa Perangkat Lunak Senior (Lead Architect)
- **Tanggal:** 6 Oktober 2026

---

## 📌 1. Format Berkas & Ekstensi Eksklusif (.zfx & .zlx)

Aplikasi ZZLUXORA secara ketat hanya membaca dan mengelola **dua ekstensi berkas eksklusif**:
1. **`.zfx` (ZZLUXORA Fixture Profile):** Format profil lampu panggung. Aplikasi **hanya** menerima berkas berekstensi `.zfx` (tidak bisa mengimpor atau membuka berkas `.json`, meskipun struktur dalamnya berupa serialisasi JSON).
2. **`.zlx` (ZZLUXORA Showfile Project):** Format pertunjukan dan showfile panggung lengkap.
- Seluruh dialog `QFileDialog` (Open, Save, Save As) pada Fixture Editor maupun Main Window dibatasi secara ketat hanya memfilter berkas `.zfx` dan `.zlx`.

---

## 🏷️ 2. Standarisasi Profil Fixture Resmi (Alien AL36 & Kumastb STL47)

Nama manufaktur dan model lampu distandarkan secara bersih dan presisi:
- **Alien AL36:** `Manufacturer = Alien`, `Model = AL36` (File: `fixtures/Alien-AL36.zfx`)
- **Kumastb STL47:** `Manufacturer = Kumastb`, `Model = STL47` (File: `fixtures/Kumastb-STL47.zfx`)
- Keterangan teks seperti `8ch`, `8ch rgb`, atau `rgbw` dihilangkan agar tampilan list dan inspektor bersih (*to-the-point*).

---

## 🖥️ 3. Window Title Bar Presisi

- **Nama Aplikasi:** `ZZLUXORA`
- **Status Saat Baru Dibuka (Cold Launch / Proyek Baru):**
  - Judul window: `ZZLUXORA [Untitled.zlx]`
- **Status Setelah Memuat atau Menyimpan Showfile:**
  - Menampilkan alamat berkas lengkap (*full file path*): `ZZLUXORA [alamat file]`
  - Contoh: `ZZLUXORA [/home/zzdree/ANDREAS/zzluxora_v10/showfiles/demo_church_worship.zlx]`

---

## 🧭 4. Main Menu Bar Bersih (Clean QMenuBar)

Menu bar dirampingkan, tidak bertele-tele (*to-the-point*), dan bebas dari *over-engineering*:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ File    Fixture    Preview    Setting    Help    About                                           │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.1. Menu `File` (Dropdown Minimalis)
Hanya memuat 4 aksi inti:
- **Open Project:** `Ctrl+O` (Membuka dialog file explorer / Thunar untuk memilih file `.zlx`)
- **Save Project:** `Ctrl+S` (Menyimpan proyek saat ini)
- **Save As Project:** `Ctrl+Shift+S` (Menyimpan proyek dengan nama/lokasi baru)
- **Exit:** `Alt+F4` (Keluar dari aplikasi)

### 4.2. Menu `Fixture` (Dropdown 2 Menu Inti)
Mengonsolidasikan seluruh fungsi fixture menjadi 2 menu langsung:
- **Fixture Library:** `Ctrl+F` (Membuka jendela pop-up *Fixture Library*)
- **Fixture Editor:** `Ctrl+E` (Membuka jendela pop-up *Fixture Editor*)

### 4.3. Menu `Preview` (Direct Action — Tanpa Dropdown)
- Sekali klik langsung membuka jendela pop-up **Stage Visualizer**.
- Shortcut `Ctrl+P` tersembunyi (tetap aktif secara global di aplikasi tanpa mengotori menu).

### 4.4. Menu `Setting` (Direct Action — Tanpa Dropdown)
- Sekali klik langsung membuka dialog pop-up **Settings**.
- Shortcut `Ctrl+Shift+P` tersembunyi.

### 4.5. Menu `Editor` (Dieliminasi)
- Dihapus total karena fungsinya telah terwakili secara rapi di dalam `Fixture -> Fixture Editor`.

---

## 📚 5. Jendela Fixture Library (To-The-Point & Resizable)

- **Title Bar Jendela:** Langsung **`Fixture Library`**.
- **Tanpa Header & Deskripsi:** Menghapus judul dekoratif dan teks deskripsi panjang.
- **Posisi Splitter Seimbang (50:50):** Pembatas vertikal diletakkan di tengah window (`220px : 220px`) agar nyaman dilihat langsung tanpa perlu digeser manual.
- **Tampilan Daftar:** Menampilkan `Manufacturer | Model` bersih (misal: `Alien | AL36`, `Kumastb | STL47`).
- **Format Footprint Inspector:**
  ```text
  Model       : AL36
  Manufacture : Alien
  Channel     : 8
  ------------------------------------
  01 | Dimmer (Dimmer)
  02 | Red (Red)
  03 | Green (Green)
  04 | Blue (Blue)
  05 | Empty (Empty)
  06 | Program (Program)
  07 | Speed (Speed)
  08 | Emptz (Empty)
  ```
- **Tombol Aksi Bawah:**
  - `RELOAD` (Warna hijau solid `#16a34a`)
  - `CLOSE` (Warna standar console)

---

## 🛠️ 6. Jendela Fixture Definition Editor (QLC+ Aligned)

- **Title Bar Jendela:** Langsung **`Fixture Editor`** (atau `Fixture Editor [nama_file.zfx]`).
- **Menu Bar `File` (Dropdown Mandiri):**
  - **New Fixture:** `Ctrl+N` (Mereset form ke template awal)
  - **Open Fixture:** `Ctrl+O` (Dialog file explorer berkas `.zfx`)
  - **Save Fixture:** `Ctrl+S` (Menyimpan berkas `.zfx`)
  - **Save As Fixture:** `Ctrl+Shift+S` (Menyimpan sebagai `.zfx` baru)
  - **Close:** `Alt+F5` (Menutup editor fixture)

- **Form Header Kosongan (Default):**
  - **Model:** Input teks kosong `""`
  - **Manufacture:** Input teks kosong `""`
  - **Channel:** Spinbox angka default `4`

- **Tabel Pemetaan Kanal (Channel Footprint):**
  - **Channel:** Format angka 2-digit berpading nol: `01`, `02`, `03`, `04`, dst.
  - **Label:** Teks custom bebas diketik (*Red, Green, Blue, Dimmer, Pan, Tilt, dll*).
  - **Type:** Dropdown combo box lengkap berstandar QLC+ (*Dimmer, Red, Green, Blue, White, Amber, UV, Cyan, Magenta, Yellow, Strobe, Shutter, Pan, Tilt, Color Macro, Gobo, Prism, Program, Speed, Effect, Maintenance, Empty*).

- **Tombol Aksi Bawah:**
  - `Save` (Warna hijau solid `#16a34a`)
  - `Close` (Warna standar console)

---

## 🎭 7. Jendela Stage Visualizer (2D & 3D Dual-View dengan Full Mouse Control)

- **Title Bar Jendela:** Langsung **`Stage Visualizer`**.
- **Tanpa Header & Tombol Close Bawah:** Area panggung luas maksimal.
- **Default View Ringan (2D First):**
  - Saat dibuka, default aktif pada **`2D Front View`** (Tab index 0) agar ringan dan cepat.
  - Pilihan Tab: **`2D Front View`** dan **`3D Perspective View`**.
- **Clean Initial State (Panggung Kosong):**
  - Proyek baru / unpatched (0 fixture) menampilkan panggung bersih tanpa lampu tiruan/ghost.
  - Teks saat kosong: `Stage Ready • Patch fixtures in Address tab to visualize lighting`.
- **Auto Center-Aligned (Vertikal & Horizontal):**
  - Lampu tertata rapi simetris di tengah panggung secara horizontal dan vertikal.
  - Panjang bentangan truss dan drop cable otomatis beradaptasi dengan jumlah fixture.
  - Label hanya menampilkan nama fixture saja (*e.g., Alien AL36 #1*).

### 7.1. Kontrol Mouse & Posisi Fixture
- **Di 2D Front View:**
  - Klik kiri: memilih fixture (*select*).
  - **Mouse tidak dapat menggeser posisi lampu** (mencegah tata letak rusak tak sengaja).
  - Posisi lampu hanya diatur melalui **Pivot Position** di drawer kanan.
- **Di 3D Perspective View:**
  - **Klik Kiri Tahan (Inverted Orbit):** Memutar kamera mengelilingi panggung (*yaw* & *pitch*) dengan arah inverted natural.
  - **Klik Kiri Lepas (Select):** Memilih fixture tanpa memindahkan posisinya.
  - **Klik Kanan Tahan (Pan/Move):** Menggeser posisi kamera horizontal dan vertikal.
  - **Scroll Wheel (Zoom with Limit):** Zoom in dan zoom out dengan batas jarak aman (*clamped 250 s.d. 1100*) agar kamera tidak hilang atau menembus lantai.
  - **Klik Tengah:** Netral (*no action*).
  - **Default Kamera 3D:** Sudut pandang lurus dari depan (*front-facing perspective*, `yaw=0.0`, `pitch=16°`).

### 7.2. Sidebar Drawer Hamburger `[ ☰ ]` (Kanan Atas)
- Default awal: **Tertutup (Hidden)** agar panggung lega. Dibuka dengan klik ikon `☰`.
- Tanpa label "Control Panel", langsung aksi to-the-point:
  - **Tab 3D:**
    - `Reset Camera`: Tombol standby warna abu-abu (`#333844`), saat diklik memberikan kilatan hijau (`#16a34a`) dan kamera kembali ke posisi depan.
    - `Haze FX`: Saklar toggle default **OFF** (abu-abu `#333844`, teks `Haze FX: OFF`). Saat ON menjadi hijau (`#16a34a`, teks `Haze FX: ON`).
    - `FIXTURE POSITION`: 3 Pivot (X, Y, Z) dengan kombinasi slider horizontal + spinbox yang dapat digeser kanan-kiri.
  - **Tab 2D:**
    - `FIXTURE POSITION`: 2 Pivot (X, Y) dengan slider + spinbox.
    - **Sinkronisasi 2D & 3D:** Nilai Pivot X dan Pivot Y saling terhubung secara real-time.

---

## ⚙️ 8. Jendela Settings (Network & Art-Net Configuration)

- **Akses:** Direct action dari menu bar atas (`Setting`).
- **Title Bar:** Langsung **`Settings`**.
- **Tanpa Header/Deskripsi:** Langsung ke konfigurasi target.
- **Grup Target:**
  - **Preset (Tanda Strip Pendek `-`):**
    - `127.0.0.1 - Localhost (SITL QLC+)`
    - `192.168.4.1 - ESP32 AP Mode`
    - `255.255.255.255 - Subnet Broadcast`
    - `Custom IP`
  - **IP Address:** Input alamat IP (custom / editable).
  - **Universe:** Dropdown pilihan angka `0`, `1`, `2`, `3`.
  - **UDP Port:** Default `6454`.
  - **FPS:** Spinbox `44` (Frame rate transmisi DMX).
- **Tabel Scanned Interfaces:**
  - Header kolom: **`Name`** dan **`Address`**.
- **Tombol Bawah:**
  - `Scan Interfaces` (Memindai ulang adapter lokal)
  - `Save` (Warna hijau `#16a34a`)
  - `Cancel` (Warna standar console)

---

## 🌐 9. Audit 100% Full Bahasa Inggris (Console-Standard Interface)

Seluruh teks antarmuka, dialog konfirmasi, pesan kesalahan, judul tab, tombol kontrol, dan tabel di seluruh modul `ui/` telah distandarisasi ke dalam Bahasa Inggris murni:
- Dialog: `"Open Project"`, `"Save Project"`, `"Save As Project"`, `"Exit"`
- Workspace Tabs: `Address`, `Analyze`, `Result`, `Perform`, `Page`, `Mixer`
- Actions: `UNDO`, `REDO`, `CLEAR PATCH`, `PATCH 4x ALIEN (GIA)`, `PATCH 1x KUMA (BENCH)`
- Audio: `Select Audio File`, `Import Audio from YouTube`, `Track ready`, `Audio analysis failed`
- Metrics: `Song Title`, `Estimated Tempo`, `Duration & STFT Frames`, `RMS Energy`, `Spectral Centroid`, `Chroma STFT & Tonality`, `Valence`, `Arousal`, `Worship Mood`
- Performance: `Live Show Playlist`, `Section Cues & Stage Lighting Timing`, `GENERATE EXECUTORS`
- Visualizer: `2D Front View`, `3D Perspective View`, `Reset Camera`, `Haze FX: ON/OFF`, `FIXTURE POSITION`
- Settings: `Settings`, `Target`, `Preset`, `Universe`, `FPS`, `Scanned Interfaces`, `Name`, `Address`
- Credentials: `About Developer & System`, `Author / Researcher`, `Thesis Advisor`
