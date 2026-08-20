# zzluxora — Product Requirements Document (PRD)

> **File:** `C:\ANDREAS\SCRIPT\markdowns\app_prd.md`
> **Tanggal:** 2026-06-22
> **Versi target:** v7.0.0 (skripsi-final + Windows installer)
> **Sumber requirement:** `notes/feedback_v1.txt` (179 baris, brief v4→v6)
> **Dokumen pendukung:** `markdowns/app_upgrade.md` (rencana teknis), `markdowns/app_feedback.md` (audit alignment), `markdowns/app_verify.md` (hasil verifikasi)
> **Status:** IMPLEMENTED di `zzluxora2/` (v7.0.0). Disesuaikan ke feedback literal (mixer 0–255 default 0, fixture editor MDI, auto-patch popup, help close atas+bawah, analyze teks gede, fixtures dropdown trigger) + emoji chrome dibersihkan (DESIGN.md §5.3) + Windows installer. Tanda ✅ = sudah terpasang & terverifikasi.

---

## 1. Ringkasan Produk

**zzluxora** = aplikasi desktop audio-reactive lighting design. Analisa lagu → generate scene/chase DMX otomatis → kirim via Art-Net ke fixture (PAR LED). Otak: rule-based audio feature mapping (Valence-Arousal → HSV → RGBW), inti skripsi.

**Platform:** Windows desktop (PySide6 / Qt). Output `.exe`.
**Brand:** nama fix `zzluxora` (lowercase, no hyphen, no versi). Logo lampu putih BG hitam.
**Referensi UX:** grandMA3 + QLC+. Konsep modern minimalis, cocok production.

---

## 2. Tujuan & Non-Tujuan

### 2.1 Tujuan
- T1. Engine analyze sesuai rumus skripsi (`script_math_model.md`), test-verified.
- T2. UI/UX rapi, responsif (terutama buka-tutup sidebar & fixture list).
- T3. Brand konsisten + splash + ikon custom di taskbar/window.
- T4. 8 sub-tab program lengkap & koheren (saling koordinasi, kroscek).
- T5. Build `.exe` distributable dengan semua aset.

### 2.2 Non-Tujuan (v6)
- Import data kuesioner / SUS (di luar scope, kandidat v6.1).
- Multi-platform (macOS/Linux).
- Fixture selain PAR LED (visual hanya lingkaran).

---

## 3. Pengguna

| Persona | Kebutuhan |
|---|---|
| Andre (operator + author skripsi) | Analisa lagu, generate lighting, demo production, dokumentasi skripsi |
| Operator lighting | Live trigger scene/chase, blackout cepat, mixer manual |
| Penguji skripsi | Lihat About (identitas), hasil analyze konsisten dengan rumus |

---

## 4. Functional Requirements

> Prioritas: **P0** = wajib (release blocker), **P1** = penting, **P2** = nice-to-have.

### 4.1 Brand, Logo, Splash

| ID | Requirement | Prioritas |
|---|---|---|
| BR-1 | Nama app fix `zzluxora` (lowercase) di window title, header, About, build | P0 |
| BR-2 | Logo: ikon lampu putih, background hitam, SVG + PNG multi-size (16–256px) | P0 |
| BR-3 | Ikon taskbar + window = logo zzluxora | P0 |
| BR-4 | Splash screen 3 detik saat open: logo besar + tulisan, referensi gaya grandMA | P0 |
| BR-5 | Hapus tulisan "ZZLIGHT-LUXORA" / "zzlight luxora" dimanapun muncul | P0 |

### 4.2 Menu Bar (pojok kiri atas, 3 menu)

| ID | Requirement | Prioritas |
|---|---|---|
| MN-1 | **File**: Open Project, Save Project, Save As Project, Exit | P0 |
| MN-2 | Open/Save/Save As → popup file explorer; ekstensi `zzluxora .zlx` | P0 |
| MN-3 | Save & Save As default nama `untitled.zlx`, auto-append `.zlx` | P0 |
| MN-4 | Exit **tanpa shortcut**; Open/Save/Save As shortcut tetap | P0 |
| MN-5 | **View**: Program, Fixture List, Fixture Editor, Settings, About + marker (titik/segitiga) untuk sidebar aktif | P0 |
| MN-6 | **Help**: ubah dari "About" → **Shortcuts** (F1) | P0 |
| MN-7 | Help modal: header langsung "Shortcuts", lalu daftar keyboard shortcut di bawah; kurangi emoji; hapus tulisan "v4 native artnet" | P0 |
| MN-8 | Help tabel shortcut disesuaikan dengan fitur lain (kroscek), **tombol close di atas (X pojok) + bawah (tengah)** | P1 ✅ |

### 4.3 Header (atas)

| ID | Requirement | Prioritas |
|---|---|---|
| HD-1 | Kiri: ikon + `zzluxora`. Tulisan File/View/Help rata kiri | P0 |
| HD-2 | Nama project + path file project di header (samping ikon+zzluxora) | P1 |
| HD-3 | Kanan (rata kanan, sejajar): status Art-Net + tombol play/pause + ikon blackout | P0 |
| HD-4 | Status Art-Net: "connected" hijau / "disconnected" merah | P0 |
| HD-5 | **Satu tombol** play/pause (bukan 2 tombol Start+Stop terpisah) | P0 |
| HD-6 | Ikon blackout (lingkaran hitam) kanan: semua slider mixer → 0 (master + ch 1–512) | P0 |

### 4.4 Sidebar

| ID | Requirement | Prioritas |
|---|---|---|
| SB-1 | Ikon hamburger `☰` untuk toggle; **tetap `☰`** saat buka/tutup (tidak berubah) | P0 |
| SB-2 | Sebelum load `.zlx`: sidebar **tertutup**, tidak buka tab apapun | P0 |
| SB-3 | Empty state: tulisan "silahkan buka project…" + ikon `+ zzluxora` samar | P0 |
| SB-4 | Setelah load project, buka sidebar untuk run program | P0 |
| SB-5 | Isi: Program, Fixture List, Fixture Editor, Settings, About | P0 |
| SB-6 | Saat collapsed: tampil ikon masing-masing item (disesuaikan) | P1 |

### 4.5 Program — Sub-tab Address

| ID | Requirement | Prioritas |
|---|---|---|
| AD-1 | Judul + deskripsi tab | P0 |
| AD-2 | Tombol: Clear All Patch (popup konfirmasi), **Auto-Patch Sequential (popup menu sendiri: start address, gap, clear-first)**, + tombol tambahan (Random, Group by Type) | P0 ✅ |
| AD-3 | Keterangan panel kanan (Patch Info: fixtures/channels/free), ukuran teks **lebih besar** | P1 ✅ |
| AD-4 | Grid kotak: maks **24 kolom** ke samping, ke bawah scrollable | P0 |
| AD-5 | Cell kosong: nomor posisi di pojok kanan | P0 |
| AD-6 | Cell terisi: label channel di tengah + nomor di pojok; warna kotak sesuai **type channel** (dimmer=ikon lampu, red=merah, strobe=ikon, dst) koordinasi dengan fixture & editor | P0 |

### 4.6 Program — Sub-tab Analyze (CORE SKRIPSI)

| ID | Requirement | Prioritas |
|---|---|---|
| AN-1 | Judul + deskripsi + keterangan seberang (teks **lebih besar**, font 15px) | P0 ✅ |
| AN-2 | Tombol: Load Audio (4 ekstensi: wav/mp3/flac/ogg), Analyze, Remove Song, Export to Scene | P0 |
| AN-3 | Analyze/Remove/Export **disabled** sampai song dipilih; Export aktif hanya kalau sudah ada hasil analyze | P0 |
| AN-4 | Song terpilih tampil di kotak kiri | P0 |
| AN-5 | Progress bar + deskripsi yang **berubah tiap 3 detik** (penjelasan ilmiah tiap tahap analyze) | P0 |
| AN-6 | Analyze boleh dijalankan ulang kalau hasil kurang puas | P1 |
| AN-7 | Core engine: ikuti rumus `script_math_model.md` (ambil dari skripsi v3) — V/A → HSV → RGB → RGBW; test case "10.000 Reasons" PASS | P0 |
| AN-8 | UI/UX & perhitungan detail core: diserahkan ke tim, atur sebaik mungkin | P1 |

### 4.7 Program — Sub-tab Scenes

| ID | Requirement | Prioritas |
|---|---|---|
| SC-1 | Judul + deskripsi | P0 |
| SC-2 | **Hapus** tombol Regenerate Scene (redundan, sudah ada Analyze) | P0 |
| SC-3 | Kotak kiri = songlist | P0 |
| SC-4 | Panel kanan: deteksi struktur lagu (intro/verse/prechorus/chorus/bridge/outro) — desain diserahkan ke tim | P1 |
| SC-5 | Bisa grouping kumpulan scene → jadikan chase | P1 |

### 4.8 Program — Sub-tab Chase

| ID | Requirement | Prioritas |
|---|---|---|
| CH-1 | Judul + deskripsi (rapikan, sekarang berantakan) | P0 |
| CH-2 | Kotak songlist + panel control chase di samping | P0 |
| CH-3 | Control: kumpulan scene, fade, dll — desain diserahkan ke tim | P1 |

### 4.9 Program — Sub-tab Page (BARU)

| ID | Requirement | Prioritas |
|---|---|---|
| PG-1 | Custom page untuk tombol-tombol scene & chase yang sudah dibuat | P1 |
| PG-2 | Layout & detail diserahkan ke tim | P2 |

### 4.10 Program — Sub-tab Mixer

| ID | Requirement | Prioritas |
|---|---|---|
| MX-1 | Judul + deskripsi | P0 |
| MX-2 | Paling kiri slider master dimmer, lalu slider channel 1–512 di kanan | P0 |
| MX-3 | Layout full kiri→kanan, total **513 slider**, scroll ke samping | P0 |
| MX-4 | Bentuk slider referensi grandMA: slider + tombol kotak value | P0 |
| MX-5 | Value range **0–255** per channel & master, default 0 (DESIGN.md §3.3 DMX 000–255; feedback baris 26 blackout = semua slider 0) | P0 ✅ |
| MX-6 | Tombol refresh di **kanan atas** | P1 |

### 4.11 Program — Sub-tab Preview

| ID | Requirement | Prioritas |
|---|---|---|
| PV-1 | Judul + deskripsi | P0 |
| PV-2 | Fixture = **lingkaran** (PAR LED), tampak depan | P0 |
| PV-3 | Fixture bisa di-select & digeser | P0 |
| PV-4 | Sidebar kanan: atur posisi X & Y fixture terpilih | P0 |
| PV-5 | Tampilan detail diserahkan ke tim | P1 |

### 4.12 Program — Sub-tab Output

| ID | Requirement | Prioritas |
|---|---|---|
| OUT-1 | Judul + deskripsi | P0 |
| OUT-2 | Scan Art-Net gaya QLC+: daftar IP — wajib localhost `127.0.0.1`, AP mode `192.168.4.1` (modul), IP scanned, + custom | P0 |
| OUT-3 | **Hapus** universe & FPS dari panel | P0 |
| OUT-4 | Tombol **Save saja** (connect/disconnect/blackout sudah di header) | P0 |

### 4.13 Fixture List

| ID | Requirement | Prioritas |
|---|---|---|
| FL-1 | Buka ke **bawah** (dropdown) via tombol `Fixtures ▾` di header (bukan ke kanan) | P0 ✅ |
| FL-2 | Isi: list fixture dari folder `fixtures/` | P0 |
| FL-3 | Drag-n-drop fixture ke tab Address | P0 |

### 4.14 Fixture Editor

| ID | Requirement | Prioritas |
|---|---|---|
| FE-1 | Judul + deskripsi; kotak besar dengan tombol **Open** & **New** | P0 |
| FE-2 | Open → popup file explorer (ekstensi `.json`); New → program baru buat fixture | P0 |
| FE-3 | Editor jadi window dalam kotak (QMdiArea): tidak keluar kotak, bisa digeser, tumpuk, min/max/close per window | P0 ✅ |
| FE-4 | Field: nama, manufacture, channel (dengan `< >`) | P0 |
| FE-5 | Tabel channel mengikuti jumlah channel; kolom: Channel, Label, Type | P0 |
| FE-6 | Type: dimmer, rgb, rainbow/warna pelangi, strobe, empty, dll | P0 |
| FE-7 | Tombol Save di bawah; header + tombol close | P0 |

### 4.15 Settings

| ID | Requirement | Prioritas |
|---|---|---|
| ST-1 | Redesign disesuaikan design system (diserahkan ke tim) | P1 |

### 4.16 About

| ID | Requirement | Prioritas |
|---|---|---|
| AB-1 | Judul + deskripsi (sudah oke) | P0 |
| AB-2 | Urutan detail: **Application → Description → Author → NIM → Prodi → Jurusan → Fakultas → Universitas → Judul** | P0 |
| AB-3 | **Hapus** tulisan "about" di bawah (placeholder/bug) | P0 |

---

## 5. Non-Functional Requirements

| ID | Requirement | Prioritas |
|---|---|---|
| NF-1 | Tampilan modern minimalis, nyawa grandMA3 + QLC+, cocok production; **ikut design contract `zzluxora2/DESIGN.md`** (warna, tipografi, spacing, no-emoji-in-chrome) | P0 |
| NF-2 | Responsif — terutama saat buka/tutup sidebar & fixture list | P0 |
| NF-3 | Warna, ukuran teks, spacing konsisten (design system) | P0 |
| NF-4 | Core analyze test-verified (`tests/test_math_model.py` PASS) sebelum release | P0 |
| NF-5 | Startup < 5s; mixer 513 slider scroll 60fps | P1 |
| NF-6 | Backward compatible: `.zlx` & fixture JSON lama tetap load | P1 |

---

## 6. Acceptance Criteria (release blocker)

1. Window title & taskbar ikon = `zzluxora` + logo lampu putih BG hitam.
2. Splash 3 detik tampil saat open.
3. Menu File/View/Help sesuai 4.2; Exit tanpa shortcut; Help = Shortcuts.
4. Header: status Art-Net warna + 1 tombol play/pause + ikon blackout.
5. Sidebar tertutup + empty state sebelum load project; hamburger tetap `☰`.
6. 8 sub-tab program lengkap (Address, Analyze, Scenes, Chase, Page, Mixer, Preview, Output) sesuai §4.5–4.12.
7. Mixer 513 slider, master kiri, range 0–255 default 0, scroll samping.
8. Fixture List dropdown ke bawah + drag ke Address.
9. Fixture Editor MDI dengan tabel Channel/Label/Type + Open & New.
10. About urutan benar + tanpa teks bug.
11. `test_math_model.py` PASS (test case "10.000 Reasons": V=0.627, A=0.126, D=34 R=0 G=6 B=4 W=28).
12. Build `.exe` sukses dengan semua aset.

---

## 7. Komparasi v5 → v6 (ringkas)

| Aspek | v5 (sekarang) | v6 (target) |
|---|---|---|
| Brand | "ZZLIGHT-LUXORA v5.0" | `zzluxora` |
| Splash | tidak ada | 3 detik |
| Header tombol | Start + Stop (2) | 1 play/pause + blackout ikon |
| Help menu | About | Shortcuts |
| Sidebar default | terbuka | tertutup + empty state |
| Mixer | 512 slider, master atas | 513 slider, master kiri, range 0–255 default 0 |
| Preview | list teks | lingkaran PAR LED + drag + X/Y |
| Output | IP manual + universe + FPS + 5 tombol | scan IP QLC+ + Save saja |
| Fixture List | item sidebar (kanan) | dropdown ke bawah |
| Fixture Editor | New + Save, panel tunggal, 2 kolom | MDI (window draggable), Open+New, 3 kolom (ch/label/type) |
| Page tab | tidak ada | baru |
| Core analyze | implicit | eksplisit per rumus + test |

---

## 7b. Revisi penyesuaian ke feedback literal (2026-06-22)

Setelah build awal mengikuti tafsir PRD, lima poin disetel ulang agar persis dengan `feedback_v1.txt`:

| Poin | Baris feedback | Perubahan |
|---|---|---|
| Mixer range | 26 + DESIGN.md §3.3 | **0–255 default 0** (blackout = semua slider 0; DMX standar 000–255). Catatan: feedback baris 110 sempat tulis "1–255", tapi baris 26 minta blackout 0 dan DESIGN.md pakai 000–255 → 0–255 dipilih. |
| Fixture editor | 142 | panel tunggal → **QMdiArea** (window draggable, clamp, tumpuk) |
| Auto-patch | 54 | langsung patch → **popup dialog** (start address, gap, clear-first) |
| Help close | 23 | hanya bawah → **X pojok atas + tombol bawah (tengah)** |
| Analyze keterangan | 64 | font kecil → **15px** |
| Fixtures dropdown | 132–133 | tombol pemicu hilang (bug) → **tambah `Fixtures ▾` di header** → buka dropdown ke bawah |
| Emoji chrome | DESIGN.md §5.3 | header (Connect/Blackout/Disconnect), mixer refresh, toast → **glyph geometric** (no emoji pictographic) |
| Sidebar icon | DESIGN.md §5.3/§5.4 | emoji 🎛️📋🔧⚙️ℹ️ → **glyph geometric** (▦ ▤ ⚙ ⓘ); key disinkron ke item sidebar; placeholder ⏳ dibuang |

## 7c. Distribusi — Windows Installer & v7 (feedback baris 181–190)

Bump versi **v6 → v7.0.0**. Tambah installer Windows.

| ID | Requirement | Prioritas |
|---|---|---|
| INST-1 | Installer `.exe` wizard (Inno Setup), masuk Add/Remove Programs | P0 ✅ |
| INST-2 | Instal ke Program Files / Program Files (x86) otomatis (`{autopf}`) | P0 ✅ |
| INST-3 | Data user di `%APPDATA%\zzluxora\` (Roaming): config, fixtures, chases, programs, pages, presets | P0 ✅ |
| INST-4 | **Clean install**: folder app dihapus dulu sebelum copy (`[InstallDelete]`) — fresh, anti-tumpuk | P0 ✅ |
| INST-5 | Saat instal, opsi checkbox hapus data AppData lama (clean install penuh) atau keep | P0 ✅ |
| INST-6 | **Uninstall**: folder app bersih + prompt keep/hapus settings & data AppData | P0 ✅ |
| INST-7 | Icon `.ico` di setup + exe + shortcut (Start Menu + opsional desktop) | P1 ✅ |

**Blocker arsitektur yang dibereskan:** `config.ini` (`config.py`) & `fixtures/` (`fixture_manager.py`) dulu disimpan di sebelah `.exe` → gagal di Program Files (read-only). Dipindah ke `%APPDATA%\zzluxora` saat frozen (dev mode tetap di project root). Konsisten dengan chases/programs/pages/presets yang sudah pakai `%APPDATA%`.

**File:** `installer/zzluxora.iss` (Inno Setup), `installer/BUILD_INSTALLER.md` (langkah build), `tools/make_ico.py` (PNG→ICO), `build.py` (`--icon`). Build chain: `make_ico.py` → `build.py` (PyInstaller onedir) → `ISCC.exe zzluxora.iss` → `installer/Output/zzluxora-setup-v7.0.0.exe`.

## 8. Saran & Koreksi (dari AI)

- **Core analyze**: kunci sumber kebenaran ke `script_math_model.md`; tulis unit test dulu (TDD) supaya hasil tidak melenceng dari skripsi. Ini release blocker — jangan ship tanpa test PASS.
- **Type channel** jadi tulang punggung warna di Address + Preview + Editor — definisikan enum type sekali, pakai di semua tab (single source of truth), hindari hardcode warna per tab.
- **Output universe/FPS**: dihapus dari UI tapi tetap perlu di engine — hardcode default (universe 0, FPS 30) agar tidak hilang fungsinya.
- **Page tab, Chase control, Scenes structural, Preview, Settings**: spec sengaja terbuka ("atur aja") — saya usulkan desain konkret di `app_upgrade.md`, butuh approval terpisah sebelum eksekusi.
- **Responsif**: pakai animasi slide untuk sidebar & fixture-list drawer; uji di lebar window kecil (<1024px) dan besar (1920px+) untuk mixer 513 slider.

---

## 9. Open Questions (jawab sebelum eksekusi)

1. **Backward-compat analyze**: output v6 boleh beda dari v5 (re-engineer penuh sesuai math model) atau harus identik?
2. **Type channel fixture lama**: auto-detect dari label, atau default `empty` lalu user edit?
3. **Page tab save**: embedded di `.zlx` atau file terpisah?
4. **Mixer refresh**: reset semua ke 0, atau sync dengan state Art-Net?
5. **Logo**: AI generate sesuai spec, atau user sediakan file?

---

**Status:** IMPLEMENTED v7.0.0 di `zzluxora2/` — feedback literal + DESIGN.md + Windows installer. Verifikasi di `markdowns/app_verify.md`. Detail teknis di `markdowns/app_upgrade.md`, build installer di `zzluxora2/installer/BUILD_INSTALLER.md`.
