# 🎛️ Feedback ZZLUXORA — v4 (Precision Console Polish & To-The-Point UX)

- **Sumber:** User Review & Feedback v4 (Penyempurnaan Presisi UI/UX, Anti-Overengineering, Full Control Visualizer & To-the-Point)
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

## 🖥️ 2. Window Title Bar Presisi

- **Nama Aplikasi:** `ZZLUXORA`
- **Status Saat Baru Dibuka (Cold Launch / Proyek Baru):**
  - Judul window: `ZZLUXORA [Untitled.zlx]`
- **Status Setelah Memuat atau Menyimpan Showfile:**
  - Menampilkan alamat berkas lengkap (*full file path*): `ZZLUXORA [alamat file]`
  - Contoh: `ZZLUXORA [/home/zzdree/ANDREAS/zzluxora_v10/showfiles/demo_church_worship.zlx]`

---

## 🧭 3. Main Menu Bar Bersih (Clean QMenuBar)

Menu bar dirampingkan, tidak bertele-tele (*to-the-point*), dan bebas dari *over-engineering*:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ File    Fixture    Preview    Setting    Help    About                                           │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.1. Menu `File` (Dropdown Minimalis)
Hanya memuat 4 aksi inti:
- **Open Project:** `Ctrl+O` (Membuka dialog file explorer / Thunar untuk memilih file `.zlx`)
- **Save Project:** `Ctrl+S` (Menyimpan proyek saat ini)
- **Save As Project:** `Ctrl+Shift+S` (Menyimpan proyek dengan nama/lokasi baru)
- **Exit:** `Alt+F4` (Keluar dari aplikasi)

### 3.2. Menu `Fixture` (Dropdown 2 Menu Inti)
Mengonsolidasikan seluruh fungsi fixture menjadi 2 menu langsung:
- **Fixture Library:** `Ctrl+F` (Membuka jendela pop-up *Fixture Library*)
- **Fixture Editor:** `Ctrl+E` (Membuka jendela pop-up *Fixture Editor*)

### 3.3. Menu `Preview` (Direct Action — Tanpa Dropdown)
- Menu `Preview` bertindak sebagai aksi langsung (*direct QAction on QMenuBar*): sekali klik langsung membuka jendela pop-up **Stage Visualizer**.
- Shortcut `Ctrl+P` tersembunyi (tetap aktif secara global di aplikasi tanpa mengotori tampilan).

### 3.4. Menu `Editor` (Dieliminasi)
- Menu `Editor` di level atas **dihapus** karena fungsinya telah terwakili secara elegan di dalam `Fixture -> Fixture Editor`.

### 3.5. Menu Lainnya
- `Setting` (`Ctrl+Shift+P`), `Help` (`F1`), dan `About` tetap sebagai floating window independen.

---

## 📚 4. Jendela Fixture Library (To-The-Point & Resizable)

- **Title Bar Jendela:** Langsung **`Fixture Library`**.
- **Penghapusan Header Dekoratif:** Tanpa judul besar atau deskripsi panjang.
- **Tata Letak Bersih & Fleksibel (Vertical QSplitter):**
  - **Bagian Atas:** Daftar profil fixture lampu (eksklusif membaca `fixtures/*.zfx`) dengan dukungan penuh aksi **Drag and Drop** langsung ke matriks Tab Address.
  - **Bagian Bawah:** Kolom teks penjelasan detail footprint kanal, tanpa judul kotak pembungkus (*no groupbox frame*). Format tampilan kanal selaras dengan Fixture Editor:
    ```text
    Model       : Alien AL36 (8CH RGB)
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
  - **Pemisah Interaktif (Resizable):** Splitter dapat digeser naik-turun secara fleksibel.
- **Tombol Bawah:**
  - `RELOAD` (Warna hijau solid `#16a34a`, teks tebal putih)
  - `CLOSE` (Warna standar console)

---

## 🛠️ 5. Jendela Fixture Definition Editor (QLC+ Aligned)

- **Title Bar Jendela:** Langsung **`Fixture Editor`** (atau `Fixture Editor [nama_file.zfx]`).
- **Menu Bar `File` (Dropdown Mandiri):**
  - **New Fixture:** `Ctrl+N` (Mereset form ke template awal)
  - **Open Fixture:** `Ctrl+O` (Membuka berkas `.zfx`)
  - **Save Fixture:** `Ctrl+S` (Menyimpan berkas `.zfx`)
  - **Save As Fixture:** `Ctrl+Shift+S` (Menyimpan sebagai `.zfx` baru)
  - **Close:** `Alt+F5` (Menutup editor fixture)

- **Form Header Model, Manufacture, & Channel:**
  - Tanpa banner/groupbox dekoratif.
  - Langsung form field sejajar:
    - **Model:** `LED` (Template default)
    - **Manufacture:** `Generic` (Template default dengan G kapital)
    - **Channel:** `4` (Template default spinbox)

- **Tabel Pemetaan Kanal (Channel Footprint):**
  - Tanpa judul tabel pemetaan.
  - **Tiga Kolom Tabel:**
    1. **Channel:** Format angka 2-digit berpading nol: `01`, `02`, `03`, `04`, dst.
    2. **Label:** Teks custom yang dapat diketik bebas oleh pengguna (*e.g., Red, Green, Master Dimmer, Pan, Tilt, Shutter*).
    3. **Type:** Dropdown combo box memuat tipe-tipe fungsi kanal standar industri (QLC+):
       - `Dimmer`, `Red`, `Green`, `Blue`, `White`, `Amber`, `UV`, `Cyan`, `Magenta`, `Yellow`, `Strobe`, `Shutter`, `Pan`, `Tilt`, `Color Macro`, `Gobo`, `Prism`, `Program`, `Speed`, `Effect`, `Maintenance`, `Empty`.
  - **Dukungan Multi-Fixture:** Mendukung PAR LED, Moving Head, Strobe, Bar LED, dan fixture panggung lainnya.
  - **Integrasi Warna dengan Tab Address:** Seluruh tipe fungsi ini terhubung secara visual (*color-coded & short label*) ke tampilan sel kotak DMX di Tab Address.

- **Tombol Aksi Bawah:**
  - `Save` (Warna hijau solid `#16a34a`, teks tebal putih)
  - `Close` (Warna standar console)

---

## 🎭 6. Jendela Stage Visualizer (2D & 3D Dual-View dengan Full Mouse Control)

- **Title Bar Jendela:** Langsung **`Stage Visualizer`**.
- **Tanpa Header & Tombol Close Bawah:** Area visualisasi panggung maksimal tanpa header teks panjang dan tanpa tombol close di bawah.
- **Default View Ringan (2D First):**
  - Saat dibuka, default aktif pada **`2D Front View`** (Tab index 0) agar ringan dan tidak membebani komputasi saat peluncuran awal.
  - Dua Tab Utama:
    - **`2D Front View`**
    - **`3D Perspective View`**
- **Clean Initial State (Panggung Kosong):**
  - Pada proyek baru / untitled yang belum di-patch (0 fixture), panggung tampil bersih tanpa lampu tiruan/ghost.
  - Menampilkan lantai panggung dan struktur truss netral.
- **Auto-Layout Terpusat (Center Aligned):**
  - Saat fixture di-patch (misal 1 unit Kumastb atau 4 unit Alien AL36 via drag & drop atau auto-patch), posisi lampu **otomatis tertata simetris di tengah panggung (*center aligned*)**, bukan menumpuk di kiri atas.
  - **Rigging & Kabel Adaptif:** Panjang bentangan truss overhead dan kabel power/DMX drop dari pipa truss ke masing-masing fixture otomatis menyesuaikan jumlah lampu yang terpasang.
  - **Label Minimalis:** Hanya menampilkan nama fixture saja (*e.g., "Alien AL36 #1"*), tanpa deretan teks deskripsi atau angka dimmer yang mengotori visual panggung.

### 6.1. Kontrol Mouse 3D Full Fleksibel
- **Klik Kiri (Left Click Drag):** Orbit kamera 3D memutari panggung (*yaw* horizontal & *pitch* vertikal).
- **Klik Tengah (Middle Click):** Netral (*no action*).
- **Scroll Wheel (Wheel Scroll):** Zoom In / Zoom Out dengan batasan jarak aman (*bounded distance 200 s.d. 1400*) agar kamera tidak tembus lantai atau hilang ke antah-berantah.
- **Klik Kanan (Right Click Drag):** Pan / Move posisi kamera (menggeser sudut pandang panggung ke kanan, kiri, atas, dan bawah).

### 6.2. Sidebar Drawer / Menu Hamburger `[ ☰ ]` (Kanan Atas)
Tombol hamburger di pojok kanan atas untuk membuka/menutup panel kontrol samping:
- **Saat Tab `3D Perspective View` Aktif:**
  1. **Reset Camera:** Tombol standby warna abu-abu (`#333844`), saat diklik kamera kembali ke posisi default dan tombol memberikan kilatan hijau sesaat (`#16a34a`).
  2. **Haze FX:** Saklar toggle on/off:
     - Saat **ON**: Tombol berwarna hijau (`#16a34a`).
     - Saat **OFF**: Tombol berwarna abu-abu (`#333844`).
  3. **Posisi Fixture (3 Pivot):**
     - Pivot X (geser horizontal)
     - Pivot Y (ketinggian)
     - Pivot Z (kedalaman maju-mundur)
- **Saat Tab `2D Front View` Aktif:**
  - Hanya menampilkan **Posisi Fixture (2 Pivot: X, Y)**.
  - **Sinkronisasi / Link 2D & 3D:** Nilai Pivot X dan Pivot Y saling terhubung (*linked*) antara 2D dan 3D secara real-time.

---

## 🎨 7. Integrasi Pemetaan Warna Tab Address Multi-Fixture

Pembaruan kamus warna dan label pendek (*short label*) pada sel kotak DMX Tab Address:

| Tipe Kanal | Label Singkat | Warna Latar Kotak | Keterangan / Penggunaan |
| :--- | :---: | :---: | :--- |
| **Dimmer** | `DIM` | Amber Gold (`#d97706`) | Intensitas lampu |
| **Red** | `RED` | Merah (`#dc2626`) | Kanal warna merah |
| **Green** | `GRN` | Hijau (`#16a34a`) | Kanal warna hijau |
| **Blue** | `BLU` | Biru (`#2563eb`) | Kanal warna biru |
| **White** | `WHT` | Putih (`#f8fafc`) | Kanal warna putih murni |
| **Amber** | `AMB` | Amber Warm (`#f59e0b`) | PAR LED RGBA / RGBAW |
| **UV** | `UV` | Deep Violet (`#7c3aed`) | Sinar Blacklight / UV |
| **Cyan** | `CYN` | Neon Cyan (`#06b6d4`) | Color mixing CMY |
| **Magenta** | `MAG` | Vivid Magenta (`#d946ef`) | Color mixing CMY |
| **Yellow** | `YEL` | Electric Yellow (`#eab308`) | Color mixing CMY |
| **Strobe / Shutter** | `STR` / `SHT` | Flash Yellow (`#eab308`) | Strobo / Shutter mekanik |
| **Pan** | `PAN` | Violet (`#8b5cf6`) | Gerakan horizontal moving head |
| **Tilt** | `TLT` | Violet (`#8b5cf6`) | Gerakan vertikal moving head |
| **Color Macro** | `MAC` | Rainbow Pink (`#ec4899`) | Makro warna built-in |
| **Gobo** | `GOB` | Deep Sky Blue (`#0284c7`) | Pola proyeksi roda gobo |
| **Prism** | `PRS` | Indigo (`#6366f1`) | Prisma pembias cahaya |
| **Program** | `PRG` | Ungu (`#9333ea`) | Program internal fixture |
| **Speed** | `SPD` | Slate Grey (`#475569`) | Kecepatan program |
| **Effect** | `FX` | Hot Pink (`#ec4899`) | Efek visual khusus |
| **Maintenance** | `MNT` | Slate Dark (`#4a5264`) | Reset motor / lampu |
| **Empty / Unused** | `EMP` | Dark Grey (`#282c34`) | Kanal kosong |

---

## ⚡ 8. Aturan Transmisi Art-Net & Play-Gated System (Dipertahankan)

- Paket Art-Net UDP 6454 **hanya dikirimkan saat tombol PLAY aktif** (`is_transmitting == True`).
- Status Idle tetap dalam *Preparation Mode* tanpa memancarkan paket ke jaringan.
