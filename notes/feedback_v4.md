# 🎛️ Feedback ZZLUXORA — v4 (Precision Console Polish & To-The-Point UX)

- **Sumber:** User Review & Feedback v4 (Penyempurnaan Presisi UI/UX, Anti-Overengineering & To-the-Point)
- **Referensi:** grandMA2 & grandMA3 onPC Console, QLC+ v4 & v5 Fixture Definition Editor
- **Dokumentasi:** Terstruktur, Rapi, Standar Rekayasa Perangkat Lunak Senior (Lead Architect)
- **Tanggal:** 6 Oktober 2026

---

## 📌 1. Window Title Bar Presisi

- **Nama Aplikasi:** `ZZLUXORA`
- **Status Saat Baru Dibuka (Cold Launch / Proyek Baru):**
  - Judul window: `ZZLUXORA [Untitled.zlx]`
- **Status Setelah Memuat atau Menyimpan Showfile:**
  - Menampilkan alamat berkas lengkap (*full file path*): `ZZLUXORA [alamat file]`
  - Contoh: `ZZLUXORA [/home/zzdree/ANDREAS/zzluxora_v10/showfiles/demo_church_worship.zlx]`

---

## 🧭 2. Main Menu Bar Bersih (Clean QMenuBar)

Menu bar dirampingkan, tidak bertele-tele (*to-the-point*), dan bebas dari *over-engineering*:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ File    Fixture    Preview    Setting    Help    About                                           │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.1. Menu `File` (Dropdown Minimalis)
Hanya memuat 4 aksi inti:
- **Open Project:** `Ctrl+O` (Membuka dialog file explorer / Thunar untuk memilih file `.zlx`)
- **Save Project:** `Ctrl+S` (Menyimpan proyek saat ini)
- **Save As Project:** `Ctrl+Shift+S` (Menyimpan proyek dengan nama/lokasi baru)
- **Exit:** `Alt+F4` (Keluar dari aplikasi)

### 2.2. Menu `Fixture` (Dropdown 2 Menu Inti)
Mengonsolidasikan seluruh fungsi fixture menjadi 2 menu langsung:
- **Fixture Library:** `Ctrl+F` (Membuka jendela pop-up *Fixture Library*)
- **Fixture Editor:** `Ctrl+E` (Membuka jendela pop-up *Fixture Editor*)

### 2.3. Menu `Editor` (Dieliminasi)
- Menu `Editor` di level atas **dihapus** karena fungsinya telah terwakili secara elegan di dalam `Fixture -> Fixture Editor`.

### 2.4. Menu Lainnya
- `Preview` (`Ctrl+P`), `Setting` (`Ctrl+Shift+P`), `Help` (`F1`), dan `About` tetap sebagai floating window independen.

---

## 📚 3. Jendela Fixture Library (To-The-Point & Resizable)

- **Title Bar Jendela:** Langsung `Fixture Library` (tanpa embel-embel teks panjang).
- **Penghapusan Header Dekoratif:** Tidak ada judul besar atau deskripsi panjang seperti *"PERPUSTAKAAN FIXTURE..."*.
- **Tata Letak Bersih & Fleksibel (Vertical QSplitter):**
  - **Bagian Atas:** Daftar profil fixture lampu (`.zfx` / `.json`) dengan dukungan penuh aksi **Drag and Drop** langsung ke matriks Tab Address.
  - **Bagian Bawah:** Kolom teks penjelasan detail footprint kanal, tanpa judul kotak pembungkus (*no groupbox frame/title*).
  - **Pemisah Interaktif (Resizable):** Splitter dapat digeser naik-turun secara fleksibel untuk memudahkan penyesuaian luas tampilan detail channel.
- **Tombol Bawah:**
  - `RELOAD` (Memuat ulang berkas dari folder `fixtures/`)
  - `CLOSE` (Menutup jendela)

---

## 🛠️ 4. Jendela Fixture Definition Editor (QLC+ Aligned)

- **Title Bar Jendela:** Langsung `Fixture Editor` (atau `Fixture Editor [nama_file.zfx]`).
- **Menu Bar `File` (Dropdown Mandiri):**
  - **New Fixture:** `Ctrl+N` (Mereset form ke template awal)
  - **Open Fixture:** `Ctrl+O` (Dialog file explorer untuk membuka file `.zfx` / `.json`)
  - **Save Fixture:** `Ctrl+S` (Menyimpan file profil)
  - **Save As Fixture:** `Ctrl+Shift+S` (Menyimpan dengan nama baru)
  - **Close:** `Alt+F5` (Menutup editor fixture)

- **Form Header Model & Manufaktur:**
  - Hapus banner/groupbox dekoratif (*"Spesifikasi Model & Pabrikan..."*).
  - Langsung form field sejajar:
    - **Model:** Input teks
    - **Manufacturer:** Input teks
    - **Channel:** Spinbox angka
  - **Template Default Baru:**
    - `Model` = **LED**
    - `Manufacturer` = **generic**
    - `Channel` = **4**

- **Tabel Pemetaan Kanal (Channel Footprint):**
  - Hapus judul tabel pemetaan (*"Tabel Pemetaan Kanal DMX..."*).
  - **Tiga Kolom Tabel:**
    1. **Channel:** Format angka 2-digit berpading nol: `01`, `02`, `03`, `04`, dst.
    2. **Label:** Teks custom yang dapat diketik bebas oleh pengguna (*e.g., Red, Green, Master Dimmer, Pan, Tilt, Shutter*).
    3. **Type:** Dropdown combo box memuat tipe-tipe fungsi kanal standar industri (QLC+):
       - `Dimmer`, `Red`, `Green`, `Blue`, `White`, `Amber`, `UV`, `Cyan`, `Magenta`, `Yellow`, `Strobe`, `Pan`, `Tilt`, `Shutter`, `Color Macro`, `Gobo`, `Prism`, `Speed`, `Program`, `Effect`, `Maintenance`, `Empty`.
  - **Dukungan Multi-Fixture:** Tidak hanya terbatas pada lampu PAR LED, namun mencakup Moving Head, Bar LED, Strobe light, dan fixture panggung lainnya.
  - **Integrasi Warna dengan Tab Address:** Seluruh tipe fungsi ini terhubung secara visual (*color-coded & short label*) ke tampilan sel kotak DMX di Tab Address.

- **Tombol Aksi Bawah:**
  - Hanya 2 tombol *to-the-point*:
    - `Save` (Menyimpan profil fixture `.zfx`)
    - `Close` (Menutup jendela editor)

---

## 🎨 5. Integrasi Pemetaan Warna Tab Address Multi-Fixture

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

## ⚡ 6. Aturan Transmisi Art-Net & Play-Gated System (Dipertahankan)

- Paket Art-Net UDP 6454 **hanya dikirimkan saat tombol PLAY aktif** (`is_transmitting == True`).
- Status Idle tetap dalam *Preparation Mode* tanpa memancarkan paket ke jaringan.
