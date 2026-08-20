# zzluxora v6.0 — Comprehensive Upgrade Plan

> **Lokasi file:** `C:\Users\andre\OneDrive\Documents\SCRIPT\markdowns\app_upgrade.md`
> **Tanggal:** 2026-06-14
> **Versi saat ini:** v5.0.0 (current app di `SCRIPT/zzluxora/`, sesuai `build.py`)
> **Target:** v6.0.0 (skripsi-final, production-grade)
> **Status:** DRAFT v2 — menunggu approval
> **Referensi core analyze:** `script_andreas_v3.docx` (BAB 3) + `script_math_model.md` (10 sections, 219 baris)

---

## 0. Ringkasan Eksekutif

User ingin upgrade dari **v5.0 (current)** ke **v6.0 (skripsi-final)**. Perubahan besar:

1. **CORE ANALYZE re-engineer** — audio engine harus mengikuti rumus eksplisit skripsi (math model) tepat per baris. Ini OTAK skripsi.
2. **Brand identity** — logo lampu putih BG hitam, app name `zzluxora` lowercase, splash 3 detik.
3. **Shell redesign** — header (play/pause single, blackout icon), menu (Exit no-shortcut, view markers), sidebar (default collapsed + empty state, hamburger tetap `☰`).
4. **8 sub-tab program** dirombak: Address, Analyze, Scenes, Chase, **Page (NEW)**, Mixer, Preview, Output.
5. **Fixture List** — drawer ke BAWAH (bukan ke kanan).
6. **Fixture Editor** — MDI-style dengan tabel channel + type system.
7. **About & Settings** — reordered sesuai skripsi identity, cleanup placeholder.
8. **Design system** — modern minimalis, grandma3 + QLC+ referensi, responsif.

> [!IMPORTANT]
> Dokumen ini **planning only**. Belum ada code yang diubah. Setelah approval, eksekusi bertahap 8 fase (§18).
> **CRITICAL:** Core analyze v6 WAJIB menghasilkan output identik dengan test case §3.10 di `script_math_model.md` ("10.000 Reasons": V=0.627, A=0.126, D=34 R=0 G=6 B=4 W=28).

---

## 1. Komparasi v5.0 → v6.0

### 1.1 Ringkasan Perubahan Besar

| Aspek | v5.0 (current) | v6.0 (target) |
|---|---|---|
| **Brand name** | "ZZLIGHT-LUXORA" (caps, hyphen) di banyak file | **"zzluxora"** lowercase fix, no hyphen, no version suffix |
| **Window title** | "ZZLIGHT-LUXORA v5.0" | **"zzluxora"** |
| **App icon** | Default Qt / emoji | **Custom logo** (lampu putih, BG hitam) di taskbar & window |
| **Splash screen** | Tidak ada | **3 detik** dengan icon + tulisan besar, skipable |
| **CORE ANALYZE** | V/A weight + formula **tidak terdokumentasi eksplisit** di code | **Re-engineer sesuai `script_math_model.md`** (w_A=0.40/0.35/0.25, w_V=0.50/0.30/0.20, 4 kuadran, HSV→RGB Foley-van Dam, RGB→RGBW) |
| **Header** | Brand + project + ArtNet pill + Start + Stop | **Brand + project + path + ArtNet pill (color-coded) + Play/Pause (single) + Blackout (icon)** |
| **Menu File** | Open, Save, Save As, Exit (Ctrl+Q) | **Open, Save, Save As, Exit (NO shortcut)** |
| **Menu View** | Program, Fixture List, Fixture Editor, Settings, About | **Sama, + marker (✓) untuk active** |
| **Menu Help** | About (F1) — ada "v4 native artnet" | **Shortcut info (F1)**, no emoji, no "v4 native artnet" |
| **Sidebar default** | Terbuka (200px) | **Tertutup** saat belum load `.zlx` (empty state) |
| **Sidebar toggle** | Hamburger `☰` ↔ `›` (salah) | **Tetap `☰`** saat buka/tutup |
| **Address tab** | 16×32 fixed (32 cols) | **Max 24 cols, scroll H+V, type-based color** |
| **Address cell kosong** | Border only | **Nomor posisi pojok kanan** |
| **Address cell isi** | Channel label (fixed color palette) | **Channel type color-coded** + label + nomor |
| **Analyze tab** | 4 tombol selalu aktif | **3 tombol disabled** sampai song dipilih |
| **Analyze progress** | Spinner | **Progress bar + deskripsi rotating 3 detik** |
| **Analyze core** | Vague, hardcoded weights | **8-step pipeline sesuai math model** + 7-stage progress |
| **Scenes tab** | Ada regenerate | **Hapus regenerate** + structural detection |
| **Chase tab** | Berantakan | **Songlist + control + scene sequence** — full layout baru |
| **Page tab** | Tidak ada | **NEW** — custom page untuk scene/chase buttons |
| **Mixer tab** | 16×32 grid (32 cols), master horizontal | **1×513 horizontal, master kiri, grandma-style, default 0** |
| **Preview tab** | Static list + swatch | **PAR LED circles** + drag + X/Y sidebar |
| **Output tab** | Form lengkap (IP, universe, FPS, connect, disconnect, blackout) | **IP scan list (127/192.168.4.1/scanned/custom) + save only** |
| **Fixture List** | Sidebar panel | **Drawer ke BAWAH**, drag ke Address |
| **Fixture Editor** | Sidebar panel | **MDI-style windows** + tabel channel dengan type |
| **Settings** | Form sederhana | **Redesign** (General/Art-Net/Audio/UI sections) |
| **About** | v5.0.0, urutan acak, ada "about sepertinya bug" | **v6.0.0, urutan: application → desc → author → NIM → prodi → jurusan → fakultas → unik → judul** |
| **Engine modules** | audio, scene, artnet | **Sama, audio di-re-engineer sesuai math model** |
| **Fixture data** | Channel map dengan label | **Channel map + type** (untuk color coding) |

### 1.2 Statistik

| Metrik | v5.0 | v6.0 (est) |
|---|---|---|
| **Panels** | 13 | 14 (+ Page tab) |
| **Sub-tabs (Program)** | 7 | 8 (+ Page) |
| **Audio engine stages** | 1 monolithic | **8 distinct stages** (sesuai math model) |
| **Math model compliance** | Implicit | **Explicit + test-verified** (test case §3.10) |
| **Fixture JSON fields** | name, manufacturer, channels, channel_map (label) | **+ type per channel** |
| **Header widgets** | 5 (brand, project, artnet, start, stop) | 6 (+ blackout icon, + file path) |
| **Mixer sliders** | 513 (16×32 + master) | 513 (1×513 horizontal grandma-style) |
| **Address grid max cols** | 32 fixed | 24 max, scrollable |
| **Sample colors** | Hardcoded per offset | 12 type-keyed colors (dimmer/red/green/blue/white/amber/uv/strobe/rainbow/program/speed/empty) |

### 1.3 Kenapa v6.0 (bukan v5.1)?

- **CORE ANALYZE re-engineer** = major version (skripsi-defining change)
- **New tab (Page)** = feature addition user-facing
- **Brand identity lock** = breaking untuk existing user
- **Splash screen** = significant UX change
- **Color coding system** = new visual paradigm
- **Test verification required** (math model §3.10) = release-blocking criteria

---

## 2. CORE ANALYZE (BAGIAN PALING KRITIS — Otak Skripsi)

> [!CAUTION]
> Ini adalah **fondasi skripsi**. Code audio engine v6 WAJIB mengikuti rumus di `script_math_model.md` (219 baris) tepat per formula. Test case §3.10 ("10.000 Reasons") harus PASS.

### 2.1 Sumber Kebenaran

**File sumber utama:**
- `C:\Users\andre\OneDrive\Documents\SCRIPT\markdowns\script_math_model.md` (10 sections, 219 baris)
- `C:\Users\andre\OneDrive\Documents\SCRIPT\markdowns\script_chapter_03.md` (BAB 3 Metodologi)
- `C:\Users\andre\OneDrive\Documents\SCRIPT\script_projects\script_andreas_v3.docx` (skripsi v3, 62.8 KB)

**Pipeline lengkap (sesuai `script_math_model.md` overview):**
```
Audio File → Ekstraksi Fitur → Normalisasi [0,1] → V-A → HSV → RGB → RGBW → Scene/Chase → DRGBW
```

### 2.2 Arsitektur Engine Baru (8-Stage Pipeline)

**File refactor:** `engines/audio_engine.py` (sekarang monolithic) → `engines/analyze_pipeline.py` (modular, 8 stages).

```
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: Load Audio                                         │
│   librosa.load(path, sr=None, mono=True)                    │
│   y, sr, duration = ...                                     │
│   → output: AudioBuffer                                     │
├─────────────────────────────────────────────────────────────┤
│ STAGE 2: Extract Features (7 fitur)                        │
│   librosa.beat.beat_track(y, sr) → tempo, beats             │
│   librosa.feature.rms(y) → rms_mean, rms_per_frame         │
│   librosa.feature.spectral_centroid(y=y, sr=sr) → sc        │
│   librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13) → mfcc        │
│   librosa.feature.chroma_stft(y=y, sr=sr) → chroma          │
│   librosa.onset.onset_strength(y, sr) → onset               │
│   → output: RawFeatures {bpm, rms, sc, mfcc, chroma, onset} │
├─────────────────────────────────────────────────────────────┤
│ STAGE 3: Compute Chroma Major Ratio                         │
│   major_indices = [0, 2, 4, 5, 7, 9, 11]                   │
│   chroma_mean = np.mean(chroma, axis=1)                     │
│   major_energy = np.sum(chroma_mean[major_indices])         │
│   chroma_major_ratio = major_energy / np.sum(chroma_mean)   │
│   → output: chroma_major_ratio ∈ [0, 1]                    │
├─────────────────────────────────────────────────────────────┤
│ STAGE 4: Normalize Features (Min-Max)                       │
│   x_norm = clip((x - x_min) / (x_max - x_min), 0, 1)        │
│                                                             │
│   Ranges (dari math model §[2]):                            │
│   - BPM: 60-180                                             │
│   - RMS: 0.01-0.50                                          │
│   - SC: 500-5000 Hz                                         │
│   - MFCC1: -300-100                                         │
│   - Onset Rate: 0.5-8.0                                     │
│   - Chroma Major: 0.0-1.0                                   │
│   → output: NormalizedFeatures {bpm, rms, sc, mfcc1,        │
│                                 onset_rate, chroma_major}   │
├─────────────────────────────────────────────────────────────┤
│ STAGE 5: Compute Valence & Arousal (Rule-Based)             │
│   A = 0.40·BPM_norm + 0.35·RMS_norm + 0.25·OnsetRate_norm  │
│   V = 0.50·ChromaMajor_norm + 0.30·SC_norm                  │
│       + 0.20·(1 - |MFCC1_norm - 0.5| × 2)                  │
│   → output: VA {valence ∈ [0,1], arousal ∈ [0,1]}           │
├─────────────────────────────────────────────────────────────┤
│ STAGE 6: Segment Song (SSM-based structural detection)      │
│   - Compute self-similarity matrix (SSM)                    │
│   - Novelty curve (diagonal checkerboard kernel)            │
│   - Peak picking → segment boundaries                        │
│   - Auto-label segments (intro/verse/prechorus/chorus/       │
│     bridge/outro) via heuristics (position + V-A centroid)  │
│   → output: List[Segment] with start, end, label, va        │
├─────────────────────────────────────────────────────────────┤
│ STAGE 7: Map V-A → HSV (Rule-Based)                         │
│   H_base (per kuadran):                                     │
│     Q1 (V>0.5, A>0.5): 30 + (V-0.5)·60  → warm             │
│     Q2 (V≤0.5, A>0.5): 270 + (0.5-V)·120 → purple          │
│     Q3 (V≤0.5, A≤0.5): 200 + (0.5-V)·120 → blue            │
│     Q4 (V>0.5, A≤0.5): 150 + (V-0.5)·100 → cyan/green      │
│   H = H_base + (ChromaPeak - 6) × 5°                        │
│   S = 0.6·A + 0.4·|2V - 1|                                  │
│   V_hsv = max(0.5·RMS_norm + 0.5·A, 0.10)                  │
│   → output: HSV {h ∈ [0,360), s ∈ [0,1], v ∈ [0,1]}        │
├─────────────────────────────────────────────────────────────┤
│ STAGE 8: HSV → RGB → RGBW + DRGBW                           │
│   HSV → RGB (Foley & van Dam):                              │
│     C = V_hsv × S                                           │
│     H' = H / 60°                                            │
│     X = C × (1 - |H' mod 2 - 1|)                            │
│     m = V_hsv - C                                           │
│     (R_1, G_1, B_1) = sector_table[H' mod 6]                │
│     R, G, B = (R_1 + m), (G_1 + m), (B_1 + m)               │
│                                                             │
│   RGB → RGBW:                                               │
│     W = min(R, G, B)                                        │
│     R' = R - W, G' = G - W, B' = B - W                      │
│                                                             │
│   Output 8-bit:                                             │
│     D = round(V_hsv × 255)                                  │
│     R_out = round(R' × 255)                                 │
│     G_out = round(G' × 255)                                 │
│     B_out = round(B' × 255)                                 │
│     W_out = round(W × 255)                                  │
│   → output: DRGBW tuple per scene per fixture               │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Per-Scene Application

Setiap **segment** dari STAGE 6 menghasilkan 1+ scene:
- For each segment, compute mean V-A across segment
- Map ke HSV → RGB → RGBW → DRGBW
- Apply chase rules (math model §[8]):

| Kondisi | Timing |
|---|---|
| BPM > 120 | ~500ms per scene |
| BPM 90-120 | ~700ms per scene |
| BPM < 90 | ~1500ms per scene |
| Onset strength > 0.7 | Instant snap |
| Onset strength < 0.3 | Gradual crossfade |

### 2.4 Test Verification (WAJIB PASS)

**Test case dari `script_math_model.md` §3.10 ("10.000 Reasons"):**

| Fitur | Raw | Norm |
|-------|-----|------|
| BPM | 73 | 0.108 |
| RMS | 0.08 | 0.143 |
| SC | 1800 | 0.289 |
| MFCC1 | -120 | 0.450 |
| Onset | 1.5 | 0.133 |
| Chroma Major | 0.72 | 0.720 |

**Expected output:**
- A = 0.40×0.108 + 0.35×0.143 + 0.25×0.133 = **0.126**
- V = 0.50×0.720 + 0.30×0.289 + 0.20×0.900 = **0.627**
- Q4 (V>0.5, A≤0.5): Damai/tenang
- H = 162.7° (cyan), S = 0.178, V_hsv = 0.135
- D = 34, R = 0, G = 6, B = 4, W = 28

> [!IMPORTANT]
> **Unit test `tests/test_math_model.py` WAJIB pass** sebelum engine di-merge ke main branch. Ini release-blocker.

### 2.5 File Refactor

**Modify:** `engines/audio_engine.py` (existing monolithic)
- Split jadi `engines/analyze_pipeline.py` (8-stage pipeline)
- Add `engines/color_mapping.py` (V-A → HSV → RGBW logic)
- Keep `engines/scene_generator.py` (uses color_mapping output)
- Keep `engines/artnet_sender.py` (no changes)

**New:** `engines/analyze_pipeline.py`
- Class `AnalyzePipeline(stages: List[Stage])`
- Each stage: `process(features: dict) → dict`
- `run(audio_path) → AnalyzeResult` orchestrator
- Emit progress signals (0-100%, stage label) untuk UI consumption

**New:** `engines/color_mapping.py`
- `compute_va(normalized: dict) → (V, A)`
- `va_to_hsv(V, A, chroma_peak=6) → (H, S, V_hsv)`
- `hsv_to_rgbw(H, S, V_hsv) → (D, R, G, B, W)`

**New:** `tests/test_math_model.py`
- Test case "10.000 Reasons" → expect A=0.126, V=0.627, D=34 R=0 G=6 B=4 W=28
- Edge cases: all-zero features, extreme values, chroma = 0, etc.

---

## 3. Brand & Identity (Splash, Logo, Icon)

### 3.1 Logo

| Item | Spec |
|---|---|
| **Visual** | Icon lampu (lightbulb) **putih** di background **hitam** |
| **Format** | SVG (vector) + PNG fallback (256, 128, 64, 32, 16 px) |
| **Color** | Bulb fill `#ffffff`, stroke `#cccccc`, background `#000000` |
| **Style** | Modern, simple, recognizable di 16px taskbar |

**Asset path:** `assets/logo.svg`, `assets/logo_*.png`

**Logo harus visible di:**
- Splash screen (center, ~240×240px)
- Taskbar (16x16 atau 24x24)
- Window title bar (16x16)
- About panel header (~120×120px)
- Header bar (small, ~24×24px)

### 3.2 App Name Standardization

**Fix di semua file** (CRITICAL — search & replace):

| Context | Wrong | Correct |
|---|---|---|
| Window title | "ZZLIGHT-LUXORA v5.0" | **"zzluxora"** |
| Brand header | "ZZLIGHT-LUXORA" | **"zzluxora"** |
| App icon taskbar | Default Qt | Custom logo |
| Splash text | N/A | "zzluxora" (gradient) |
| About app name | "zzluxora" | **"zzluxora"** ✓ |
| Build spec | "zzluxora.spec" | **Sama** ✓ |
| .exe output | "zzluxora.exe" | **Sama** ✓ |
| README/CHANGELOG | Various | Konsisten "zzluxora" |

**Files to grep & fix:**
- `zzluxora/widgets/header_bar.py` → `BRAND_TEXT = "zzluxora"` (lowercase)
- `zzluxora/main.py` → `setApplicationName("zzluxora")`
- `zzluxora/main_window.py` → `setWindowTitle("zzluxora")`
- `zzluxora/panels/about_panel.py` → APP_NAME = "zzluxora"
- `zzluxora/CHANGELOG.md` → update branding
- `zzluxora/README.md` → konsistensi

### 3.3 Splash Screen

**Durasi:** 3 detik (skipable: click/ESC/Space)

**Layout:**
```
┌──────────────────────────────────────────┐
│                                          │
│           [LOGO 240×240 PUTIH]           │
│                                          │
│              z z l u x o r a             │
│         (gradient putih → hijau)         │
│                                          │
│       Audio-Reactive Lighting System     │
│                                          │
│              ▓▓▓▓▓▓▓░░░░░░░              │
│              (progress bar)              │
│                                          │
└──────────────────────────────────────────┘
```

**Spec:**
- Frameless, centered, 600×400
- BG: `#000000`
- Logo: 240×240px center-top
- Text "zzluxora": Inter/Outfit, bold italic, 48pt, gradient
- Subtitle: 14pt, `#707070`
- Progress bar: 60% width, 4px height, gradient hijau
- Animation: subtle pulse pada logo

**Behavior:**
- 3 detik (atau engine ready) → fade out 300ms → MainWindow
- Skipable: click anywhere, ESC, atau Space
- Background thread: initialize engine

**New file:** `widgets/splash_screen.py`

---

## 4. Header Redesign

**Current:** `widgets/header_bar.py` — 2 tombol (Start + Stop), 5 widget total.

### 4.1 Layout v6 (Final)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ [💡logo] z z l u x o r a │ Project: name.zlx │ path/to/file.zlx │ ● Connected │  ▶  ⏸  ⚫ │
└──────────────────────────────────────────────────────────────────────────────┘
   kiri                                center-stretch                      kanan
```

### 4.2 Komponen Detail

#### 4.2.1 Brand Title (kiri)
- Icon lampu putih 24×24px + text "zzluxora"
- Font: Inter/Outfit italic bold 18pt
- Gradient: `#ffffff` → `#cccccc`
- Clickable → goto About panel
- Min width: 160px

#### 4.2.2 Project Info (center)
- Line 1: `Project: <i>nama_project.zlx</i>` (12pt muted)
- Line 2: path absolut file (10pt, `#707070`, auto-truncate tengah)
- Clickable → reveal in File Explorer (Windows: `explorer /select,path`)

#### 4.2.3 ArtNet Pill (kanan)
- States: connected (`#2ecc71`), disconnected (`#e74c3c`), connecting (`#4aa3ff`)
- Text: "Connected" / "Disconnected" / "Connecting..."
- Clickable → goto Output tab
- Hover: border highlight

#### 4.2.4 Play/Pause (single button, **NEW v6**)
- Single toggle button (replace Start+Stop)
- Icon `▶` saat stopped (hijau)
- Icon `⏸` saat playing (hijau active)
- Disabled saat artnet disconnected
- Tooltip: "Play/Pause Chase (Space)"

#### 4.2.5 Blackout (icon button, **NEW v6**)
- Icon `⚫` atau `🌑` 24×24px
- Click → `ArtNetController.blackout()` + state → `disconnected`
- Tooltip: "Blackout (B)"

### 4.3 File Impact

**Modify:** `widgets/header_bar.py`
- Refactor `start_btn` + `stop_btn` → `play_pause_btn` (QPushButton checkable)
- Add `blackout_btn` (icon only)
- Add `project_path_label` (new)
- Add `logo_icon` (new)
- Update `BRAND_TEXT = "zzluxora"`

**Modify:** `main_window.py`
- Update signal handlers: `_on_header_play_pause`, `_on_header_blackout`
- Remove `start_clicked`/`stop_clicked` (replace `play_pause_clicked`)

**Modify:** `styles.py`
- Add QSS: `QPushButton#playPauseBtn`, `QPushButton#blackoutBtn`
- Brand title gradient: white (bukan green)

---

## 5. Menu Bar

### 5.1 File Menu

| Item | Shortcut | Behavior |
|---|---|---|
| Open Project… | `Ctrl+O` | QFileDialog, filter `*.zlx` |
| Save Project | `Ctrl+S` | Save ke `manager.project_filepath`, kalau None → Save As |
| Save Project As… | `Ctrl+Shift+S` | QFileDialog, default `untitled.zlx`, auto-append `.zlx` |
| --- | --- | --- |
| Exit | **(NO SHORTCUT)** | Close window |

> [!IMPORTANT]
> **Hapus `QKeySequence.StandardKey.Quit`** dari `main_window.py:79` (atau line yang saat ini set Exit shortcut).

### 5.2 View Menu

Items + shortcuts (sama dengan sidebar):
- Program (`Ctrl+1`)
- Fixture List (`Ctrl+2`)
- Fixture Editor (`Ctrl+3`)
- Settings (`Ctrl+4`)
- About (`Ctrl+5`)

**Marker untuk active:** `QAction.setChecked(True)` di `_show_panel`, sync dengan sidebar.

### 5.3 Help Menu

| Item | Shortcut | Behavior |
|---|---|---|
| Keyboard Shortcuts | `F1` | Buka help modal |

**Help modal content** (`widgets/help_modal.py`):
- Header: "Keyboard Shortcuts" (no emoji, no "v4 native artnet")
- Sections:

| Action | Shortcut |
|---|---|
| Open Project | Ctrl+O |
| Save Project | Ctrl+S |
| Save Project As | Ctrl+Shift+S |
| Switch to Program | Ctrl+1 |
| Switch to Fixture List | Ctrl+2 |
| Switch to Fixture Editor | Ctrl+3 |
| Switch to Settings | Ctrl+4 |
| Switch to About | Ctrl+5 |
| Play / Pause Chase | Space |
| Blackout | B |
| Emergency Stop | Esc |
| Show Shortcuts | F1 |

- Tombol close: atas (X corner) + bawah (centered "Close" button)
- Table styling: clean, monospace untuk shortcut, no emoji

---

## 6. Sidebar Behavior

### 6.1 Default State

**Sebelum load `.zlx`:**
- Sidebar **TERTUTUP** (56px)
- Hamburger `☰` di header
- Main area: empty state:
  - Icon lampu + "zzluxora" samar (opacity 0.3)
  - Text: "Silahkan buka project untuk memulai"
  - Button "Open Project" (large, centered)

**Setelah load `.zlx`:**
- Sidebar **expanded** (200px) dengan animasi slide
- Empty state hilang

### 6.2 Toggle Behavior

**v5 (wrong):** icon `☰` ↔ `›`

**v6 fix:** icon collapse button **SELALU `☰`** (hamburger 3 garis)
- Tidak berubah saat collapse/expand
- Tooltip: "Toggle sidebar"

### 6.3 Collapsed Mode Icons

Saat sidebar tertutup (56px), tampilkan icon saja (centered, no text):
- Program: 🎛️
- Fixture List: 📋
- Fixture Editor: 🔧
- Settings: ⚙️
- About: ℹ️

**v6 improvement:** SVG icons (bukan emoji) untuk crispness. Emoji fallback OK.

### 6.4 File Impact

**Modify:** `sidebar.py`
- Hapus logic ganti icon `☰` ↔ `›` di `_apply_width:108`
- Set `collapse_btn.setText("☰")` di `_build_ui` (fixed)
- Add `collapsed_icons_only` mode

**New:** `widgets/empty_state.py`

**Modify:** `main_window.py`
- Default `Sidebar(collapsed=True)`
- Add empty state widget di stack (index 0)
- Show empty state kalau `not manager.project_filepath`

---

## 7. Program Panel — Sub Tabs

**Current:** `program_panel.py` — 7 tab

**v6:** 8 tab (tambah Page)

### 7.1 Address Tab

**Current:** 16×32 fixed grid, fixed color palette per offset.

**v6 changes:**

#### 7.1.1 Grid Sizing
- **Max 24 kolom** (sebelumnya 32)
- **Scroll H+V** (auto-fit)
- Cell: 32×32px atau 36×36px
- Empty cells: border tipis + **nomor posisi pojok kanan**
- Filled cells: label tengah, nomor pojok, warna sesuai type

#### 7.1.2 Color Coding per Channel Type

| Type | Color | Label |
|---|---|---|
| `dimmer` | `#f1c40f` (kuning) | "Dim" |
| `red` | `#e74c3c` | "R" |
| `green` | `#2ecc71` | "G" |
| `blue` | `#3498db` | "B" |
| `white` | `#e8e8e8` | "W" |
| `amber` | `#f39c12` | "A" |
| `uv` | `#9b59b6` | "UV" |
| `strobe` | icon ⚡ | "Str" |
| `rainbow` | gradient | "Rbw" |
| `program` | `#7f8c8d` | "Prg" |
| `speed` | `#95a5a6` | "Spd" |
| `empty` | transparent | "—" |

#### 7.1.3 Toolbar
- **Clear All Patches** (existing, improve UI)
- **Auto-Patch Sequential** → popup menu (start addr, skip patched, preview)
- **Auto-Patch by Universe** (NEW) — split ke multiple universes
- **Export Patch** (NEW) — save `.csv`/`.json`
- **Import Patch** (NEW)
- **Validate** (NEW) — cek konflik channel

#### 7.1.4 Keterangan Panel (kanan, lebih gede)
- Total fixtures patched
- Total channels used
- Conflicts (jika ada)
- Universe utilization (X/512)

**Modify:** `panels/address_tab.py`
- Refactor grid → responsive (max 24 cols)
- New `CellWidget` dengan type-based color

**Modify:** `widgets/address_grid.py`
- QScrollArea
- Dynamic column count (max 24)

---

### 7.2 Analyze Tab (CORE — Wired to v6 Pipeline)

**Current:** 4 tombol selalu aktif, spinner, vague processing.

**v6 changes:**

#### 7.2.1 Tombol Disabled States
- **Load Audio** → always enabled
- **Analyze** → enabled HANYA kalau song dipilih
- **Remove Song** → enabled HANYA kalau song dipilih
- **Export to Scene** → enabled HANYA kalau ada hasil analyze
- Visual: opacity 0.4, no hover, no click

#### 7.2.2 Song Display (kiri)
- Filename, Duration, Sample rate, BPM (jika analyzed), Status ("Not analyzed" / "Analyzed ✓")
- Click song → highlight + load detail

#### 7.2.3 Audio Formats
- 4 ekstensi: `.wav`, `.mp3`, `.flac`, `.ogg`

#### 7.2.4 Progress Bar + Deskripsi Rotating (3 detik)

| Stage | % | Text |
|---|---|---|
| 1 | 0-15% | "Loading audio waveform dengan librosa..." |
| 2 | 15-30% | "Extracting spectral features (MFCC, centroid, bandwidth)..." |
| 3 | 30-45% | "Detecting tempo and beat frames via librosa.beat..." |
| 4 | 45-55% | "Computing onset strength and chroma features..." |
| 5 | 55-70% | "Segmenting song via self-similarity matrix (SSM)..." |
| 6 | 70-85% | "Mapping Valence-Arousal using rule-based model..." |
| 7 | 85-95% | "Converting HSV → RGB → RGBW color space..." |
| 8 | 95-100% | "Generating DMX scenes and saving to library..." |

**Timer:** QTimer 3000ms untuk rotate text saat analyzing.

#### 7.2.5 Wire to v6 Pipeline
- Connect button `Analyze` → `AnalyzePipeline.run(audio_path)`
- Pipeline emits progress signals → update QProgressBar + rotating label
- On complete → populate scene library (Scenes tab) dengan structural detection

#### 7.2.6 Keterangan Panel (kanan, lebih gede)
- Total songs analyzed
- Total duration
- Cache size
- Avg V-A quadrant distribution

**Modify:** `panels/audio_tab.py` → rename ke `panels/analyze_tab.py` (sesuai tab name)
- Add progress signals listener
- Wire ke `AnalyzePipeline`

---

### 7.3 Scenes Tab

**Current:** Scene list, regenerate, export to chase.

**v6 redesign:**

#### 7.3.1 Layout
```
┌──────────────┬────────────────────────────────────┐
│              │  Structural Detection              │
│  Song List   │  ┌─────────┬──────┬─────┬────────┐ │
│              │  │ Time    │ Type │ BPM │ Color  │ │
│  song1.wav ✓ │  │ 0:00    │Intro │ 120 │ 🟡     │ │
│  song2.wav   │  │ 0:32    │Verse │ 120 │ 🔵     │ │
│  song3.wav   │  │ 1:15    │Cho.  │ 140 │ 🔴     │ │
│              │  │ ...     │      │     │        │ │
│              │  └─────────┴──────┴─────┴────────┘ │
│              │                                    │
│              │  [Group into Chase] [Export]       │
└──────────────┴────────────────────────────────────┘
```

#### 7.3.2 Hapus Regenerate
Analyze sudah generate scenes. (User feedback)

#### 7.3.3 Group into Chase
Select multiple scenes → group jadi chase → add ke Chase tab.

**Modify:** `panels/scenes_tab.py`
- Remove regenerate logic
- Add structural detection table
- Add group-to-chase button

---

### 7.4 Chase Tab

**Current:** Berantakan, timeline + play/stop.

**v6 redesign:**

#### 7.4.1 Layout
```
┌──────────────┬────────────────────────────────────┐
│              │  Chase Control                     │
│  Chase List  │  ▶ Play   ⏸ Pause   ⏹ Stop        │
│              │                                    │
│  Chase 1 ✓   │  Fade In:  [====●====] 0.5s       │
│  Chase 2     │  Fade Out: [====●====] 0.5s       │
│  Chase 3     │  Speed:    [==●======] 1.0x        │
│              │  Loop:     [✓]                      │
│  + New Chase │                                    │
│              │  Scene Sequence                    │
│              │  1. Intro  🟡 0:00-0:32             │
│              │  2. Verse  🔵 0:32-1:15             │
│              │  3. Chorus 🔴 1:15-2:00             │
│              │                                    │
│              │  [↑ Move] [↓ Move] [🗑 Remove]     │
└──────────────┴────────────────────────────────────┘
```

**Modify:** `panels/chase_tab.py`
- Refactor ke 2-column (list + control)
- Add fade in/out sliders
- Add speed multiplier
- Add scene sequence table
- Keep timeline paintEvent (existing)

---

### 7.5 Page Tab (NEW)

**Tujuan:** Custom page builder untuk scene + chase buttons (live operation).

**Layout:**
```
┌─────────────────────────────────────────────────┐
│  Page Builder                                   │
│  + Add Scene Button                             │
│  + Add Chase Button                             │
│  + Add Blackout Button                          │
│  Grid: 4x4 (configurable 1-8 cols)              │
│  ┌────┬────┬────┬────┐                          │
│  │ S1 │ S2 │ S3 │ C1 │                          │
│  │ Ch │ V1 │ Br │ Ch │                          │
│  ├────┼────┼────┼────┤                          │
│  │ C2 │ BO │    │    │                          │
│  │ Ch │ ⬤ │    │    │                          │
│  └────┴────┴────┴────┘                          │
│  [Save Page] [Load Page] [Clear]               │
└─────────────────────────────────────────────────┘
```

**Features:**
- Add button → pilih dari scene/chase library
- Drag button untuk reorder
- Click button → activate (scenes: apply color, chases: play)
- Save embedded ke `.zlx`
- Multiple pages (Page 1, Page 2, ...)

**New file:** `panels/page_tab.py`

---

### 7.6 Mixer Tab

**Current:** 16×32 grid, master horizontal.

**v6 redesign:**

#### 7.6.1 Layout
- **Master dimmer PALING KIRI** (vertical, bukan horizontal)
- 512 channel sliders **sebelah kanan master**
- **1 baris × 513 kolom** (full horizontal scroll)
- Vertical scroll disabled (1 row tinggi)

#### 7.6.2 Slider Style (Referensi Grandma)
```
┌───┐
│   │  ← slider vertikal (0-255)
│ ▓ │
│   │
│   │
│128│  ← tombol kotak value (clickable, editable)
└───┘
```

- Slider: vertical, 20px wide, 200px tall
- Tombol value: 30×24px kotak, monospace, di bawah slider
- Click tombol → inline edit (QLineEdit)

#### 7.6.3 Value Range
- Master: 0-255
- Channel 1-512: 0-255
- **Default 0** (user feedback)

#### 7.6.4 Refresh Button
- Kanan atas (bukan bawah)
- Tooltip: "Refresh from Art-Net"

**Modify:** `panels/mixer_tab.py`
- 1×513 horizontal layout
- Default 0
- Master kiri
- Refresh kanan atas
- New `ChannelFader` widget

---

### 7.7 Preview Tab

**Current:** Static list + swatch.

**v6 redesign:**

#### 7.7.1 Visual
- **PAR LED fixtures sebagai LINGKARAN** (bukan kotak)
- Glow effect dengan current color
- 2D top-down stage view
- Size: 60-80px diameter

#### 7.7.2 Interaction
- Drag fixture untuk pindah posisi
- Click untuk select (border hijau tebal)
- Multi-select dengan Ctrl+Click

#### 7.7.3 Sidebar Kanan (NEW)
Untuk selected fixture:
- Position X (0-100%)
- Position Y (0-100%)
- Intensity (0-255)
- Color override
- Channel readout

**Modify:** `panels/preview_tab.py`
- Custom `StageView` widget
- `FixtureCircle` (draggable)
- `PropertiesPanel`

---

### 7.8 Output Tab

**Current:** Form lengkap (IP, universe, FPS, connect/disconnect/blackout).

**v6 redesign:**

#### 7.8.1 Layout
```
┌────────────────────────────────────────────┐
│  Art-Net Output Configuration              │
│                                            │
│  Detected/Available Nodes:                 │
│  ┌──────────────────────────────────────┐  │
│  │ ☑ 127.0.0.1 (Localhost - QLC+)      │  │
│  │ ☑ 192.168.4.1 (AP Mode - ESP32)     │  │
│  │ ☐ 192.168.1.100 (scanned)           │  │
│  │ ☐ 192.168.1.105 (scanned)           │  │
│  │ + Custom IP: [____________] [Add]    │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  [🔄 Scan Network]    [💾 Save]             │
└────────────────────────────────────────────┘
```

#### 7.8.2 IP Sources
- 127.0.0.1 (Localhost - QLC+) — always present
- 192.168.4.1 (AP mode - ESP32) — always present
- Scanned (auto-detect via ArtPoll)
- Custom (manual add)

#### 7.8.3 Remove Universe & FPS
User feedback: "universe dan fps gaada"
- FPS hardcoded 30
- Universe hardcoded 0 (auto-allocate future)

#### 7.8.4 Tombol
- Save only (simpan IP list)
- Scan Network
- Connect/Disconnect/Blackout **dihapus** (ada di header)

**Modify:** `panels/output_tab.py`
- Hapus universe_spin, fps_spin
- Hapus connect_btn, disconnect_btn, blackout_btn
- Add IP list widget (QListWidget + checkbox)
- Add custom IP input
- Add scan button

---

## 8. Fixture List Redesign (Drawer ke BAWAH)

**Current:** Sidebar list (terpisah panel).

**v6:** Drawer/panel yang muncul di BAWAH header, bukan di kanan.

### 8.1 Behavior
- Klik "Fixture List" di sidebar → drawer slide-down (250ms)
- Drawer berisi:
  - List fixture files dari `fixtures/`
  - Search bar
  - Drag handle per item
- Drag n drop ke Address tab cells
- Close (X) di kanan drawer header

**Modify:** `panels/fixture_list_panel.py`
- Refactor ke `FixtureListDrawer` (QFrame + slide animation)
- Add drag support (MIME, target = AddressGrid)
- Add search/filter

**Modify:** `main_window.py`
- Wire drawer show/hide via sidebar click atau Ctrl+F2
- Wire drag-drop ke AddressGrid

---

## 9. Fixture Editor Redesign (MDI-Style)

**Current:** Sidebar panel (single edit session).

**v6:** MDI-style windows di dalam panel.

### 9.1 Layout
```
┌─────────────────────────────────────────────────┐
│  Fixture Editor                          [+ New]│
│  ┌─────────────────────────────────────────┐    │
│  │ [Window 1: PAR RGBW 8ch]      [_][□][X] │    │
│  │ Name: [Generic PAR RGBW 8ch]            │    │
│  │ Manufacturer: [Generic]                  │    │
│  │ Channels: [< 8 >]                        │    │
│  │ Channel Table:                           │    │
│  │ ┌────┬───────┬──────┐                    │    │
│  │ │ Ch │ Label │ Type │                    │    │
│  │ │ 1  │ Dim   │Dimmer│                    │    │
│  │ │ 2  │ Red   │Red   │                    │    │
│  │ │ ...│       │      │                    │    │
│  │ └────┴───────┴──────┘                    │    │
│  │ [Save] [Save As] [Cancel]                │    │
│  └─────────────────────────────────────────┘    │
│  [+ New] [Open...] [Save All]                  │
└─────────────────────────────────────────────────┘
```

### 9.2 MDI Window Specs
- Container: QMdiArea atau custom QFrame
- Window: draggable (mouse drag on title bar)
- Bounds: tidak keluar container (clamp)
- Stack: newest on top
- Min/Max/Close: di title bar kanan
- Max 5 simultaneous

### 9.3 Channel Table (NEW)
- QTableWidget rows = jumlah channels
- Kolom: Ch (read-only), Label (editable), Type (combobox)
- Type options: Empty, Dimmer, Red, Green, Blue, White, Amber, UV, RGB, Rainbow, Strobe, Program, Speed, Macro

**Modify:** `panels/fixture_editor_panel.py`
- Refactor ke MDI
- New `FixtureEditorWindow` (movable, resizable)
- New `ChannelTable` (QTableWidget)
- Add type combobox

**Modify:** `fixture_manager.py`
- Update `save_fixture()` validation untuk type field
- Default `Empty` untuk backward compat

---

## 10. Settings Redesign

**Current:** 1.4 KB (sangat minimal).

**v6:** Redesign sesuai design system.

### 10.1 Layout
```
┌─────────────────────────────────────────────┐
│  Settings                                   │
│                                             │
│  General                                    │
│  ┌─────────────────────────────────────┐    │
│  │ Theme: [Dark ▼] (locked)            │    │
│  │ Default Sample Rate: [22050 ▼]      │    │
│  │ Default FPS: [30 ▼]                 │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  Art-Net                                    │
│  ┌─────────────────────────────────────┐    │
│  │ Default Target IP: [127.0.0.1]      │    │
│  │ Default Universe: [0]               │    │
│  │ Default FPS: [30]                   │    │
│  │ Auto-reconnect: [✓]                 │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  Audio                                      │
│  ┌─────────────────────────────────────┐    │
│  │ Last Audio Dir: [____________] [📂] │    │
│  │ Cache Analyzed Songs: [✓]           │    │
│  │ Cache Size: 12.3 MB (clear)         │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  UI                                         │
│  ┌─────────────────────────────────────┐    │
│  │ Sidebar Default: [Expanded ▼]       │    │
│  │ Animation Speed: [Normal ▼]         │    │
│  │ Confirm Before Exit: [✓]            │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  [Save] [Reset to Default]                  │
└─────────────────────────────────────────────┘
```

**Modify:** `panels/settings_panel.py`
- QGroupBox sections
- Wire ke `config.py`
- Add Save/Reset buttons

---

## 11. About Redesign

**Current:** Urutan acak, ada "about sepertinya bug".

**v6:** Urutan sesuai user feedback.

### 11.1 Layout
```
┌─────────────────────────────────────────────┐
│  ┌─────────────────────────────────────┐    │
│  │         [LOGO 120×120]              │    │
│  │           zzluxora                  │    │
│  │        v6.0.0                       │    │
│  │  Audio-Reactive Lighting System     │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  Application      : zzluxora                │
│  Description      : Audio-Reactive Lighting │
│                     Design System           │
│  Author           : Andreas Restuawanta C.  │
│  NIM              : 5312422036              │
│  Program Studi    : Teknik Komputer         │
│  Jurusan          : Teknik Elektro          │
│  Fakultas         : Fakultas Teknik         │
│  Universitas      : UNNES                   │
│                                             │
│  ─────────────────────────────────────      │
│                                             │
│  JUDUL SKRIPSI                              │
│  "Implementasi Rule-Based Audio Feature     │
│  Mapping untuk Sistem Lighting Design       │
│  RGBW Otomatis dengan Protokol              │
│  Art-Net DMX512"                            │
│                                             │
│  ─────────────────────────────────────      │
│                                             │
│  © 2024 Andreas Restuawanta Christwara      │
│     Built with PySide6 · Qt 6.11.1          │
└─────────────────────────────────────────────┘
```

### 11.2 Remove
- Hapus placeholder text (yang user kira bug)
- Hapus "v4 native artnet" (kalau ada di about)

**Modify:** `panels/about_panel.py`
- Reorder fields sesuai §11.1
- Update APP_VERSION ke "6.0.0"
- Update logo ke custom
- Cleanup PANEL_NAME/PANEL_DESC (no emoji, lowercase)

---

## 12. UX Polish & Responsive

### 12.1 Responsive
- Window resize → panels auto-adjust
- Sidebar collapse threshold (< 1024px)
- Mixer 513 sliders handle 1920px+
- Splash center di primary monitor

### 12.2 Animation
- Sidebar collapse: 200ms ease-out
- Drawer slide: 250ms ease-in-out
- Button hover: 150ms
- Toast: 300ms slide-up + 3s auto-dismiss
- Page transitions: 200ms fade

### 12.3 Accessibility
- Tab order + focus rings
- Tooltip untuk icon-only buttons
- High contrast (min 4.5:1)
- QAccessibleObjectName

### 12.4 Performance
- Mixer: virtualized rendering
- Address grid: virtualization
- Preview: 200ms poll

---

## 13. Design System Update

### 13.1 Color Palette

| Token | Hex | Use |
|---|---|---|
| `--bg-1` | `#0d0d0d` | Root BG |
| `--bg-2` | `#141414` | Panels, header |
| `--bg-3` | `#1a1a1a` | Cards, inputs |
| `--bg-4` | `#1f1f1f` | Hover |
| `--border` | `#2a2a2a` | Dividers, input borders |
| `--text-1` | `#e8e8e8` | Primary |
| `--text-2` | `#b0b0b0` | Secondary |
| `--text-3` | `#707070` | Muted |
| `--accent` | `#2ecc71` | Primary action (hijau grandma) |
| `--accent-hover` | `#27ae60` | Accent hover |
| `--danger` | `#e74c3c` | Errors, disconnect, blackout |
| `--info` | `#4aa3ff` | Connecting, info |
| `--warning` | `#f39c12` | Warnings |

### 13.2 Typography
- Primary: Inter (Google Fonts atau local)
- Monospace: Consolas / Cascadia Code
- Sizes: 10 / 11 / 12 / 14 / 16 / 18 / 24 / 32 / 48

### 13.3 Spacing
- Base: 4px
- Scale: 4 / 8 / 12 / 16 / 20 / 24 / 32

### 13.4 Border Radius
- Small: 4px
- Medium: 8px
- Large: 12px

**Modify:** `styles.py`
- Design tokens
- QSS untuk widget baru (splash, MDI, mixer fader)

---

## 14. File Format (`.zlx`)

**Backward compatible** dengan v3.0:
- Tetap `.zlx` JSON
- New optional field: `fixture_types` (per channel type)
- New optional field: `pages` (Page tab buttons)

**Default name:** `untitled.zlx`

**Save dialog filter:** `zzluxora Project (*.zlx)`

---

## 15. Open Questions

> [!IMPORTANT]
> Mohon dijawab sebelum eksekusi.

### Q1: Logo Asset
**Q:** Logo SVG/PNG, atau AI generate?
- **A (Recommended):** AI generate (sesuai spec: lampu putih BG hitam, simple)
- **B:** User provide file nanti

### Q2: CORE ANALYZE — Backward Compatibility
**Q:** v5 audio engine sudah ada (working). v6 re-engineer dengan math model. Apakah output **harus identik** dengan v5, atau boleh beda?
- **A (Recommended):** Output boleh beda (v6 = skripsi-defined). User re-analyze songs di v6 untuk dapat DRGBW sesuai math model.
- **B:** Output harus identik (porting math model formulas ke v5 code without semantic change)

> [!CAUTION]
> Kalau v5 implementation ternyata sudah match math model (case B), tidak perlu ubah logic — hanya dokumentasi. Kalau beda, re-engineer penuh.

### Q3: Channel Type Schema Migration
**Q:** Existing fixtures (`fixtures/*.json`) belum ada `type` field. Auto-detect dari label atau hardcode default?
- **A (Recommended):** Auto-detect dari label (e.g., "Red" → "red") + user override di editor
- **B:** Hardcode default `empty`, user edit manual

### Q4: Mixer Refresh Behavior
**Q:** Refresh button → reset semua slider ke 0, atau sync dengan Art-Net state?
- **A (Recommended):** Reset ke 0 (sesuai user "0 semua")
- **B:** Sync dengan current Art-Net (existing)

### Q5: Page Tab — Save Format
**Q:** Page config save di `.zlx` atau separate file?
- **A (Recommended):** Embedded di `.zlx`
- **B:** Separate `.zpg`

### Q6: "About Bug" yang Dihapus
**Q:** User bilang "dibawah ada tulisan about sepertinya bug, hapus aja" — yang dimaksud apa?
- **A (Recommended):** `PANEL_DESC = "Application info..."` placeholder text di `about_panel.py:17`
- **B:** Section "About" di menu Help
- **C:** Lainnya

### Q7: Splash Skip Mechanism
**Q:** Splash 3 detik fixed, atau skipable?
- **A (Recommended):** Skipable (click/ESC/Space)
- **B:** Fixed 3 detik, no skip

### Q8: Multi-Fixture Patterns
**Q:** 4 pattern (All On / Running / Gradient / Center-Out) dari math model §[8] — diimplementasi di mana?
- **A (Recommended):** Di Chase tab, configurable per chase
- **B:** Auto-pick berdasarkan V-A quadrant (Q1=All On, Q2=Running, Q3=Gradient, Q4=Center-Out)
- **C:** User pilih manual per scene

### Q9: 25 Responden Data
**Q:** Apakah v6 perlu support import data kuesioner (SUS, kesesuaian) untuk analisis skripsi?
- **A:** Skip dulu (di luar scope v6)
- **B:** Add "Kuesioner" tab simple (import CSV, show stats)

### Q10: Black-box Testing Module
**Q:** v6 core analyze mau di-test otomatis (BAB 3 §3.7.1 sebut black-box testing) — built-in test runner atau separate pytest?
- **A (Recommended):** Separate pytest di `tests/` folder (v6.1)
- **B:** Built-in test dialog di About (developer mode)

---

## 16. File Impact Summary

### 16.1 New Files

| File | Purpose |
|---|---|
| `assets/logo.svg` | Logo vector (lampu putih BG hitam) |
| `assets/logo_*.png` | Logo raster (multi-size) |
| `widgets/splash_screen.py` | Splash 3 detik |
| `widgets/empty_state.py` | Empty state component |
| `panels/page_tab.py` | Page tab (NEW) |
| `engines/analyze_pipeline.py` | 8-stage audio analyze pipeline |
| `engines/color_mapping.py` | V-A → HSV → RGBW math |
| `tests/test_math_model.py` | Math model verification tests |
| `scripts/migrate_fixture_types.py` | Migration script untuk type field |
| `fixtures/_defaults.json` | Default fixtures dengan type field |

### 16.2 Modified Files

| File | Change |
|---|---|
| `main.py` | Add splash init |
| `main_window.py` | Empty state, default sidebar, play/pause single, remove Exit shortcut, view marker |
| `sidebar.py` | Fixed hamburger icon, collapsed icon-only mode |
| `widgets/header_bar.py` | Logo icon, file path, play/pause single, blackout icon, lowercase brand |
| `widgets/help_modal.py` | Cleaned shortcut table, no emoji, no "v4 native artnet" |
| `styles.py` | Design tokens, new widget styles |
| `panels/program_panel.py` | Add Page tab |
| `panels/address_tab.py` | Max 24 cols, type-based color, extended toolbar |
| `panels/audio_tab.py` → `analyze_tab.py` | Disabled states, rotating descriptions, wire to AnalyzePipeline |
| `panels/scenes_tab.py` | Remove regenerate, structural detection, group to chase |
| `panels/chase_tab.py` | Full layout redesign |
| `panels/mixer_tab.py` | 1×513 horizontal, grandma-style, default 0 |
| `panels/preview_tab.py` | PAR LED circles, drag, X/Y sidebar |
| `panels/output_tab.py` | IP scan list, save only, remove universe/fps |
| `panels/fixture_list_panel.py` | Drawer-style, drag to address |
| `panels/fixture_editor_panel.py` | MDI-style, channel table with type |
| `panels/settings_panel.py` | Full redesign |
| `panels/about_panel.py` | Reorder, v6.0.0, no "bug" text |
| `engines/audio_engine.py` | Replaced by analyze_pipeline (or refactor in place) |
| `fixture_manager.py` | Type field support, validation |
| `config.py` | New keys (recent_files, autosave) |
| `build.py` | Add logo asset, splash assets |
| `zzluxora.spec` | Add logo icon |

---

## 17. Verification Plan

### 17.1 Automated Tests (NEW v6)

```python
# tests/test_math_model.py — RELEASE BLOCKER
def test_math_model_10k_reasons():
    """Test case dari script_math_model.md §3.10"""
    features = {
        "bpm": 73, "rms": 0.08, "sc": 1800,
        "mfcc1": -120, "onset": 1.5, "chroma_major": 0.72
    }
    result = analyze_pipeline.run_with_features(features)
    assert abs(result.arousal - 0.126) < 0.01
    assert abs(result.valence - 0.627) < 0.01
    assert result.quadrant == "Q4"  # Damai
    assert result.drgbw == (34, 0, 6, 4, 28)
```

### 17.2 Manual Verification Checklist

#### Phase 1: Foundation
- [ ] App icon visible di taskbar (logo custom)
- [ ] Window title = "zzluxora" (lowercase, no version)
- [ ] Splash 3 detik muncul, show logo + "zzluxora"
- [ ] Brand di header = "zzluxora" lowercase
- [ ] `test_math_model.py` PASS

#### Phase 2: Header & Menu
- [ ] Header: brand kiri, project center, pill+play+blackout kanan
- [ ] ArtNet pill: green/red/blue proper case
- [ ] Play/Pause single button toggle
- [ ] Blackout icon works
- [ ] File menu: Exit NO shortcut
- [ ] View menu: ✓ marker untuk active
- [ ] Help menu: no "v4 native artnet"

#### Phase 3: Sidebar
- [ ] Default collapsed + empty state
- [ ] Empty state: icon + "zzluxora" samar + "Open Project"
- [ ] Toggle: icon tetap ☰
- [ ] Collapsed: icons only

#### Phase 4: Help & About
- [ ] Help table clean, no emoji
- [ ] About: application → desc → author → NIM → prodi → ...
- [ ] About: v6.0.0, no "bug" text

#### Phase 5: Address + Analyze
- [ ] Address: max 24 cols, scroll, type color
- [ ] Address: cell empty show nomor pojok
- [ ] Analyze: tombol disabled rules correct
- [ ] Analyze: progress bar + 8-stage rotating descriptions
- [ ] Analyze output matches math model test

#### Phase 6: Remaining Tabs
- [ ] Scenes: no regenerate, structural detection
- [ ] Chase: songlist + control
- [ ] Page: NEW tab, buttons
- [ ] Mixer: 1×513, master left, grandma, default 0
- [ ] Preview: PAR circles, drag, X/Y
- [ ] Output: IP list (127/192.168.4.1/scanned/custom), save only

#### Phase 7: Fixture List + Editor
- [ ] Fixture list: drawer ke BAWAH
- [ ] Drag fixture to Address works
- [ ] Fixture editor: MDI, multiple windows
- [ ] Channel table: ch, label, type dropdown
- [ ] Type options correct

#### Phase 8: Settings + Build
- [ ] Settings: full redesign
- [ ] Build .exe works
- [ ] .exe icon visible
- [ ] Splash bundled

### 17.3 Performance
- [ ] Mixer 513 sliders: 60fps scroll
- [ ] Address 512 cells: 60fps
- [ ] App startup: < 5s
- [ ] Audio analyze 3min song: < 5s
- [ ] Memory idle: < 250 MB

---

## 18. Implementation Order (8 Phases)

> [!TIP]
> Eksekusi bertahap untuk manageable review per fase.

### Phase 1: Foundation (Brand + Splash + **Core Analyze**)
- Generate logo assets
- Create splash screen widget
- **Re-engineer `engines/audio_engine.py` → `analyze_pipeline.py` (8 stages)**
- **Add `engines/color_mapping.py` (V-A → HSV → RGBW)**
- **Write `tests/test_math_model.py` — MUST PASS**
- Update `styles.py` design tokens
- Update window title + brand text
- Add custom app icon

**Review:** Splash, branding, app icon, math model test PASS

### Phase 2: Header Redesign
- Refactor HeaderBar (logo, project path, play/pause single, blackout)
- Update artnet_pill text
- Remove Exit shortcut
- Add view menu markers

**Review:** Header layout, menu markers

### Phase 3: Sidebar + Empty State
- Fix hamburger icon (tetap ☰)
- Add empty state widget
- Default collapsed when no project
- Collapsed icon-only mode

**Review:** Sidebar behavior, empty state

### Phase 4: Help Modal + About Panel
- Clean help modal (no emoji, no "v4 native artnet")
- Reorder About fields
- Remove "bug" text
- Add logo to About

**Review:** Help table, About layout

### Phase 5: Program Tabs — Part 1 (Address + Analyze wiring)
- Address: max 24 cols, type-based color, extended toolbar
- Address: cell numbering
- Analyze: disabled states, rotating descriptions
- Wire Analyze button ke AnalyzePipeline
- Fixture JSON: add `type` field + migration script

**Review:** Address grid color, Analyze UX, pipeline integration

### Phase 6: Program Tabs — Part 2 (Scenes, Chase, Page, Mixer, Preview, Output)
- Scenes: remove regenerate, structural detection
- Chase: full redesign
- Page: NEW tab
- Mixer: 1×513 horizontal, grandma-style
- Preview: PAR LED circles, X/Y sidebar
- Output: IP scan, save only

**Review:** All remaining tabs

### Phase 7: Fixture List (Drawer) + Fixture Editor (MDI)
- Fixture list: drawer-style, drag to address
- Fixture editor: MDI windows, channel table with type

**Review:** Drawer behavior, MDI windows

### Phase 8: Settings Redesign + Final Polish + Build
- Settings: full redesign
- Responsive testing
- Performance check
- Build .exe with new assets

**Review:** Final app, distribution

---

## 19. Migration & Backward Compatibility

### 19.1 Project Files (`.zlx`)
- **v5.0 → v6.0:** Backward compatible
- Existing `.zlx` files load tanpa migration
- New optional fields: `fixture_types`, `pages`

### 19.2 Fixture JSON Files
- **v1.0 → v2.0 (v6.0):** Add `type` field per channel
- Default ke `empty` kalau tidak ada
- Migration script: `scripts/migrate_fixture_types.py`
- Auto-detect dari label (e.g., "Red" → "red")

### 19.3 Config (`config.ini`)
- **v5.0 → v6.0:** New keys ditambahkan dengan defaults
- Backward compatible (old keys tetap dibaca)

### 19.4 No Breaking Changes
- Engine modules: **REFACTOR (audio_pipeline), no breaking API change untuk callers**
- `.zlx` schema: **additive only**
- Settings: **new keys optional**

---

## 20. Risk & Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Math model formula salah interpretasi | **HIGH** | **Unit test `tests/test_math_model.py` WAJIB PASS** (release blocker) |
| Logo AI tidak match vision | Medium | Generate variants, user pilih |
| MDI window lost outside container | Low | Clamp position ke bounds |
| 513 sliders performance | Medium | Virtualized rendering, monitor FPS |
| Drag-drop ke scrollable address grid | Medium | Test thoroughly, fallback click-to-patch |
| Type detection misleading | Low | Migration script + user override |
| Splash 3 detik terasa lama | Low | Skipable |
| Multiple editor windows confusing | Low | Limit 5 |

---

## 21. Success Criteria

v6.0.0 dianggap **siap release** kalau:

1. ✅ `tests/test_math_model.py` PASS (test "10.000 Reasons")
2. ✅ Semua checklist §17.2 passed
3. ✅ App icon visible di taskbar (logo custom)
4. ✅ Window title = "zzluxora" (lowercase, no version)
5. ✅ Splash 3 detik functional
6. ✅ Semua 8 program tabs sesuai spec
7. ✅ Mixer 513 sliders horizontal grandma-style
8. ✅ Fixture editor MDI dengan type system
9. ✅ About panel reordered sesuai skripsi identity
10. ✅ Build .exe sukses dengan semua assets
11. ✅ Performance: startup < 5s, mixer 60fps

---

## 22. Referensi Skripsi (Untuk Dokumentasi)

> [!NOTE]
> Setiap code v6 yang mengimplementasikan core analyze harus reference ke math model section.

| Implementasi | Referensi |
|---|---|
| `compute_va()` | `script_math_model.md §[3]` |
| `va_to_hsv()` | `script_math_model.md §[4]` |
| `hsv_to_rgb()` | `script_math_model.md §[5]` (Foley & van Dam) |
| `rgb_to_rgbw()` | `script_math_model.md §[6]` |
| Normalization ranges | `script_math_model.md §[2]` |
| Chase timing rules | `script_math_model.md §[8]` |
| Multi-fixture patterns | `script_math_model.md §[8] Pola Multi-Fixture` |
| Test case | `script_math_model.md §[9]` ("10.000 Reasons") |

---

## 23. Next Steps (Setelah Approval)

1. **User review** dokumen ini
2. **User jawab Open Questions (§15)** — terutama Q2 (backward compat analyze)
3. **AI eksekusi** Phase 1: Foundation (brand + splash + **core analyze**)
4. **User verify** Phase 1 (logo, splash, math model test PASS)
5. **AI eksekusi** Phase 2-8 (header, sidebar, help, tabs, fixtures, settings, build)
6. **Final build** + verification

---

**Status:** DRAFT v2 — menunggu approval
**Author:** Antigravity AI + Andre (UNNES)
**Last updated:** 2026-06-14
