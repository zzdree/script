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

## 🏷️ 2. Standarisasi Profil Fixture Resmi (Alien-AL36 & Kumastb-STL47)

Nama dan model lampu distandarkan secara bersih dan presisi:
- **Alien-AL36:** `Name = Alien-AL36`, `Manufacturer = Alien`, `Model = AL36` (File: `fixtures/Alien-AL36.zfx`)
- **Kumastb-STL47:** `Name = Kumastb-STL47`, `Manufacturer = Kumastb`, `Model = STL47` (File: `fixtures/Kumastb-STL47.zfx`)
- Keterangan teks seperti `8ch`, `8ch rgb`, atau `rgbw` dihilangkan agar tampilan list bersih (*to-the-point*).

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

### 4.3. Menu Aksi Langsung (Direct Actions — Tanpa Dropdown)
- **Preview:** Sekali klik langsung membuka pop-up **Stage Visualizer** (shortcut tersembunyi `Ctrl+P`).
- **Setting:** Sekali klik langsung membuka pop-up **Setting** (shortcut tersembunyi `Ctrl+Shift+P`).
- **Help:** Sekali klik langsung membuka pop-up **Help** (shortcut tersembunyi `F1`).
- **About:** Sekali klik langsung membuka pop-up **About**.

### 4.4. Menu `Editor` (Dieliminasi)
- Dihapus total karena fungsinya telah terwakili secara rapi di dalam `Fixture -> Fixture Editor`.

---

## 📚 5. Jendela Fixture Library (To-The-Point & Resizable)

- **Title Bar Jendela:** Langsung **`Fixture Library`**.
- **Tanpa Header & Deskripsi:** Menghapus judul dekoratif dan teks deskripsi panjang.
- **Posisi Splitter Seimbang (50:50):** Pembatas vertikal otomatis berada di tengah jendela pop-up (`220px : 220px`) agar nyaman langsung dibaca tanpa perlu digeser manual.
- **Tampilan Daftar:** Menampilkan nama resmi bersih: **`Alien-AL36`** dan **`Kumastb-STL47`**.
- **Format Footprint Inspector (Rapi dengan Tab/Spacing):**
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
  - **Open Fixture:** `Ctrl+O` (Membuka berkas `.zfx`)
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

## 🎭 7. Jendela Stage Visualizer (2D & 3D Dual-View dengan Full Controls)

- **Title Bar Jendela:** Langsung **`Stage Visualizer`**.
- **Top Bar Simetris:**
  - Sisi Kiri: Tombol switch view **`[2D Front View]`** dan **`[3D Perspective View]`**.
  - Sisi Kanan: Tombol hamburger **`[ ☰ ]`** (sejajar horizontal dengan tombol view).
- **Default View Ringan (2D First):**
  - Saat dibuka, default aktif pada **`2D Front View`** agar ringan dan cepat.
- **Clean Initial State (Panggung Kosong):**
  - Proyek baru / unpatched (0 fixture) menampilkan panggung bersih tanpa lampu tiruan/ghost.
  - Teks saat kosong: `Stage Ready • Patch fixtures in Address tab to visualize lighting`.
- **Auto Center-Aligned (Vertikal & Horizontal):**
  - Lampu tertata rapi simetris di tengah panggung secara horizontal dan vertikal.
  - Panjang bentangan truss dan drop cable otomatis beradaptasi dengan jumlah fixture.
  - Label hanya menampilkan nama fixture saja (*e.g., Alien-AL36*).

### 7.1. Kontrol Mouse & Seleksi Fixture
- **Di 2D Front View:**
  - Klik kiri: memilih fixture (*select*).
  - **Shift + Klik Kiri:** Multi-selection beberapa fixture secara bersamaan.
  - **Mouse tidak dapat menggeser posisi lampu** (mencegah tata letak rusak tak sengaja).
  - Posisi lampu hanya diatur melalui **Pivot Position** di drawer kanan.
- **Di 3D Perspective View:**
  - **Klik Kiri Tahan (Inverted Orbit):** Memutar kamera mengelilingi panggung (*yaw* & *pitch*) dengan arah inverted natural tanpa limit sudut buatan.
  - **Klik Kiri Lepas:** Memilih fixture (*select*) atau Shift+Klik untuk multi-selection.
  - **Klik Kanan Tahan (Pan/Move):** Menggeser posisi kamera horizontal dan vertikal.
  - **Scroll Wheel (Zoom with Limit):** Zoom in dan zoom out dengan batas jarak aman (*clamped 200 s.d. 1200*) agar kamera tidak hilang atau menembus lantai.
  - **Klik Tengah:** Netral (*no action*).
  - **Default Kamera 3D:** Sudut pandang lurus dari depan tepat di tengah eye-level (`yaw=0.0`, `pitch=0.0`).

### 7.2. Model Realistis PAR LED 3D & Lensa (Beam Angle)
- **Struktur 3D PAR LED:**
  - Coupler / C-clamp gantung pada pipa truss.
  - U-yoke bracket baja dengan knurled tightening knobs di sisi kiri-kanan.
  - Silinder tabung lampu dengan garis heatsink cooling fins di belakang.
  - Front bezel dengan **matrix multi-cell LED lenses** (array lingkaran titik emitter LED konsentris bercahaya).
  - **Beam Angle Slider (15°–60°):** Mengatur lebar sebaran lensa sorot lampu secara dinamis di udara dan di lantai panggung.

### 7.3. Sidebar Drawer Hamburger `[ ☰ ]` (Kanan Atas)
- Default awal: **Tertutup (Hidden)** agar panggung lega. Dibuka dengan klik ikon `☰`.
- Kontrol di dalam Drawer:
  - **Tab 3D:**
    - `Reset Camera`: Standby warna abu-abu (`#333844`), saat diklik memberikan kilatan hijau (`#16a34a`) dan kamera kembali ke posisi depan lurus eye-level.
    - `Haze FX`: Saklar toggle bersih tanpa label teks `:on` (hijau `#16a34a` jika ON, abu-abu `#333844` jika OFF). Default: **OFF**.
    - `FIXTURE POSITION`: 3 Pivot (X, Y, Z) dengan slider horizontal + spinbox yang dapat digeser bebas. Nilai otomatis membaca offset fixture yang diselect.
    - `FIXTURE ROTATION` (3D only): Rot X (Tilt -90° s.d. +90°), Rot Y (Pan -180° s.d. +180°), Rot Z (Roll).
    - `BEAM SPREAD`: Slider sudut sebaran lensa (15° s.d. 60°).
    - `ALIGNMENT`: Tombol `[Align Horizontal]` dan `[Align Vertical]`.
  - **Tab 2D:**
    - `FIXTURE POSITION`: 2 Pivot (X, Y) dengan slider + spinbox.
    - `ALIGNMENT`: Tombol `[Align Horizontal]` dan `[Align Vertical]`.
    - **Sinkronisasi 2D & 3D:** Nilai Pivot X dan Pivot Y saling terhubung secara real-time.

---

## ⚙️ 8. Jendela Setting (Network & Art-Net Configuration)

- **Akses:** Direct action dari menu bar atas (`Setting`).
- **Title Bar:** Langsung **`Setting`**.
- **Tanpa Header/Deskripsi:** Langsung ke konfigurasi target.
- **Grup Target Interface:**
  - **Preset (Tanda Strip Pendek `-`):**
    - `127.0.0.1 - Localhost (SITL QLC+)`
    - `192.168.4.1 - ESP32 AP Direct`
    - `255.255.255.255 - Limited Broadcast (Auto-Detect)`
    - Subnet Broadcast router terdeteksi otomatis (misal: `192.168.1.255 - Subnet Broadcast (WiFi Router)`)
    - `Custom IP`
  - **IP Address:** Input alamat IP (custom / editable).
  - **Universe:** Dropdown angka **`0`, `1`, `2`, `3`**.
  - **UDP Port:** Default `6454`.
  - **FPS:** Spinbox frame rate 44 FPS.
- **Tabel Scanned Interfaces:**
  - Header kolom: **`Name`** dan **`Address`**.
- **Tombol Bawah:**
  - `Refresh` (Warna biru `#2563eb`)
  - `Save` (Warna hijau `#16a34a`)
  - `Cancel` (Warna standar console)

---

## ❓ 9. Jendela Help & About (Direct Pop-Up & Rapi)

### 9.1. Jendela Help
- **Akses:** Direct action dari menu bar atas (`Help` / `F1`).
- **Title Bar:** Langsung **`Help`**.
- **Tabel Shortcuts:** Header kolom **`Action / Function`** dan **`Key`**.
- **Read-Only:** Tabel tidak bisa diedit.
- **Tombol:** `Close`.

### 9.2. Jendela About
- **Akses:** Direct action dari menu bar atas (`About`).
- **Title Bar:** Langsung **`About`**.
- **Layout Lega (720x560):** Area konten scrollable yang luas sehingga baris `Description` dan `Research Title` tampil penuh dan nyaman dibaca tanpa terpotong.
- **Tombol:** `Close`.

---

## 🌐 10. Audit 100% Full Bahasa Inggris (Console-Standard Interface)

Seluruh teks antarmuka, dialog konfirmasi, pesan kesalahan, judul tab, tombol kontrol, dan tabel di seluruh modul `ui/` telah distandarisasi ke dalam Bahasa Inggris murni berstandar industri lighting console:
- Menu: `File`, `Fixture`, `Preview`, `Setting`, `Help`, `About`
- Workspace Tabs: `Address`, `Analyze`, `Result`, `Perform`, `Page`, `Mixer`
- Actions: `UNDO`, `REDO`, `CLEAR PATCH`, `PATCH 4x ALIEN (GIA)`, `PATCH 1x KUMA (BENCH)`
- Performance: `Live Show Playlist`, `Section Cues & Stage Lighting Timing`, `GENERATE EXECUTORS`
- Visualizer: `2D Front View`, `3D Perspective View`, `Reset Camera`, `Haze FX`, `FIXTURE POSITION`, `FIXTURE ROTATION`, `Align Horizontal`, `Align Vertical`
- Settings: `Setting`, `Target Interface`, `Scanned Interfaces`, `Name`, `Address`, `Refresh`, `Save`, `Cancel`
- Help & About: `Shortcuts`, `About`, `Close`
