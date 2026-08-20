# ZZLIGHT-Luxora — Standalone Desktop Application Rebuild

Rebuild ZZLIGHT-Luxora dari aplikasi Flask+browser menjadi standalone desktop EXE menggunakan PyWebView dengan native window, GUI lengkap, dark mode, collapsible sidebar, dan settings file .ini.

---

## Perubahan Arsitektur Utama

| Aspek | Sebelum (v1) | Sesudah (v2) |
|-------|-------------|-------------|
| **Window** | Flask → `webbrowser.open()` → browser tab | PyWebView → native window (minimize, maximize, close) |
| **File Dialog** | `prompt()` text input | Native file dialog via `webview.windows[0].create_file_dialog()` |
| **Settings** | Hardcoded | File `.ini` di folder yang sama dengan EXE |
| **Theme** | Dark mode | Dark mode only (permanent) |
| **Sidebar** | Fixed sidebar | Collapsible sidebar dengan hamburger icon (☰) |
| **Tab Structure** | 3 tab (Analysis, Scenes, Preview) | Sidebar menu → 6 program tab + 5 panel |
| **EXE** | PyInstaller `--console` | PyInstaller `--windowed` (no console) |

---

## User Review Required

> [!IMPORTANT]
> **Perubahan Breaking:**
> - Flask `webbrowser.open()` dihapus, diganti PyWebView native window
> - File selection sekarang pakai native Windows file dialog (bukan prompt text)
> - Settings disimpan di `config.ini` di folder yang sama dengan EXE
> - Fixture files disimpan di subfolder `fixtures/` di folder yang sama dengan EXE

> [!WARNING]
> **Segmentasi lagu:** Sesuai keputusan di `script_plan.md`, software tetap menggunakan **beat tracking + onset detection** (bukan segmentasi verse/chorus). Tapi di UI tab "Scenes" tetap menampilkan label segment dari SSM heuristic yang sudah ada di `segment_song()`. Apakah ini ok, atau mau dihapus segmentasi SSM-nya?

---

## Open Questions

> [!IMPORTANT]
> 1. **Fixture file format:** Fixture definition pakai format apa? Saya usulkan JSON (mudah di-edit), contoh: `Generic PAR RGBW 8ch.json`. Atau mau XML?
> 2. **Chase logic:** Kamu bilang "masih buntu" untuk chase. Saya usulkan: Chase = kumpulan Scenes yang di-sequence dengan timing. User bisa drag scenes ke chase, atur urutan & fade time. Ok?
> 3. **Multi-lagu mechanism:** Saya usulkan tab Analyze punya dropdown/list di atas untuk switch antar lagu yang sudah dianalisis. Semua tersimpan di memory (dan bisa export/save). Ok?
> 4. **About page identity:** Saya akan pakai data dari skripsi: **Andreas Restuawanta Christwara, NIM 5312422036, Teknik Komputer, UNNES**. Ada info lain yang mau ditambahkan?

---

## Proposed Changes

### Component 1: Backend — App Entry Point

#### [MODIFY] [app.py](file:///c:/Users/andre/OneDrive/Documents/SCRIPT/zzlight-luxora/app.py)

**Perubahan besar:** Ganti Flask runner → PyWebView window launcher.

- Hapus `webbrowser.open()` dan `threading.Timer`
- Tambah `webview.create_window()` dengan title "ZZLIGHT-Luxora", min_size=(1280,720)
- Tambah `webview.start()` 
- Tambah class `Api` yang di-expose ke JavaScript via `window.pywebview.api`
- Semua API endpoint dipindah ke method class `Api`:
  - `Api.select_file()` → native file dialog (.mp3/.wav)
  - `Api.analyze(filepath)` → run audio pipeline, return JSON
  - `Api.save_fixture(data)` → save fixture JSON ke `fixtures/`
  - `Api.load_fixtures()` → list fixture files
  - `Api.connect_artnet(ip, universe)` → connect
  - `Api.disconnect_artnet()` → disconnect
  - `Api.send_dmx(data)` → send single frame
  - `Api.play_chase(frames)` → play chase
  - `Api.stop_chase()` → stop
  - `Api.blackout()` → all zeros
  - `Api.get_status()` → status dict
  - `Api.get_settings()` / `Api.save_settings(data)` → read/write config.ini
  - `Api.export_scenes(data)` → export scenes to file
  - `Api.export_chase(data)` → export chase to file

---

#### [NEW] [config.ini](file:///c:/Users/andre/OneDrive/Documents/SCRIPT/zzlight-luxora/config.ini)

Default settings file:
```ini
[ArtNet]
target_ip = 127.0.0.1
universe = 0
fps = 30

[Fixture]
default_count = 4
channels_per_fixture = 8

[General]
last_audio_dir = 
last_fixture_dir = fixtures
```

---

### Component 2: Backend — Audio & Scene Engine

#### [KEEP] [audio_engine.py](file:///c:/Users/andre/OneDrive/Documents/SCRIPT/zzlight-luxora/audio_engine.py)
Tidak ada perubahan logika. Semua math model tetap sesuai `script_math_model.md`.

#### [KEEP] [scene_generator.py](file:///c:/Users/andre/OneDrive/Documents/SCRIPT/zzlight-luxora/scene_generator.py)
Tidak ada perubahan logika.

#### [KEEP] [artnet_sender.py](file:///c:/Users/andre/OneDrive/Documents/SCRIPT/zzlight-luxora/artnet_sender.py)
Tidak ada perubahan logika.

---

### Component 3: Frontend — HTML

#### [MODIFY] [index.html](file:///c:/Users/andre/OneDrive/Documents/SCRIPT/zzlight-luxora/templates/index.html)

**Rewrite total.** Struktur baru:

```
┌─────────────────────────────────────────────────────────────────┐
│ ZZLIGHT-LUXORA (italic, green gradient)   [▶ Start] Art-Net: ● │
├──┬──────────────────────────────────────────────────────────────┤
│☰ │                                                              │
│──│                                                              │
│P │           MAIN CONTENT AREA                                  │
│r │           (changes based on sidebar selection)               │
│o │                                                              │
│g │  Tab: Address | Analyze | Scenes | Chase | Mixer | Preview   │
│r │       (sub-tabs only for Program menu)                       │
│a │                                                              │
│m │                                                              │
│──│                                                              │
│F │                                                              │
│L │                                                              │
│──│                                                              │
│F │                                                              │
│E │                                                              │
│──│                                                              │
│S │                                                              │
│──│                                                              │
│A │                                                              │
└──┴──────────────────────────────────────────────────────────────┘
```

**Header:**
- Kiri: "ZZLIGHT-LUXORA" — font bold italic, gradient hijau
- Kanan: tombol Start/Stop + status Art-Net (● Connected/Disconnected)
- Status connected = lingkaran hijau + teks hijau
- Status disconnected = lingkaran merah + teks merah

**Sidebar (collapsible):**
- Hamburger icon (☰) untuk buka/tutup (slide animation)
- Menu items dengan icon:
  - 🎛️ Program (active by default)
  - 📋 Fixture List
  - 🔧 Fixture Editor
  - ⚙️ Settings
  - ℹ️ About

**Program → Sub-tabs:**
1. **Address** — Grid 512 kotak (DMX address 1-512), drag & drop fixtures dari Fixture List. Kotak kosong = nomor saja. Kotak terisi = hijau gradient + nomor + channel label (1 – Dimmer, 2 – Red, dst.)
2. **Analyze** — File input (native dialog), tombol Analyze (hijau gradient), progress bar, hasil analisis (features, V-A diagram, color preview, waveform, segments). Multi-lagu support (list sidebar).
3. **Scenes** — Tabel scenes per lagu, multi-lagu tabs, tombol "Export to Chase". Empty state: "Analisa lagu dulu baru bisa pakai tab ini"
4. **Chase** — Hasil chase dari multiple scenes, timeline view, playback controls. Empty state: "Analisa lagu dulu baru bisa pakai tab ini"
5. **Mixer** — 512 fader vertical (seperti QLC+), setiap fader = 1 DMX channel, value 0-255
6. **Preview** — Lingkaran fixtures (PAR LED), warna berubah real-time sesuai DMX output

**Fixture List panel:**
- List fixture files dari folder `fixtures/`
- Bisa drag & drop ke tab Address
- Tampilan seperti file browser

**Fixture Editor panel:**
- Form editor untuk membuat/edit fixture definition
- Field: name, manufacturer, channels[], channel labels
- Tombol Open (native file dialog) dan Save

**Settings panel:**
- Art-Net settings (IP, Universe, FPS)
- Fixture defaults
- Load/Save dari config.ini

**Output panel (di header area atau sub-panel):**
- List output Art-Net targets
- Checkbox enable/disable
- Tombol Start/Stop
- Support 127.0.0.1 (QLC+) dan IP module langsung

**About panel:**
- Nama: ZZLIGHT-Luxora
- Versi: v2.0
- Pembuat: Andreas Restuawanta Christwara
- NIM: 5312422036
- Program Studi: Teknik Komputer
- Universitas: Universitas Negeri Semarang (UNNES)
- Judul Skripsi: "Implementasi Rule-Based Audio Feature Mapping untuk Sistem Lighting Design RGBW Otomatis dengan Protokol Art-Net DMX512"
- Tahun: 2024

---

### Component 4: Frontend — CSS

#### [MODIFY] [style.css](file:///c:/Users/andre/OneDrive/Documents/SCRIPT/zzlight-luxora/static/css/style.css)

**Rewrite total.** Dark mode only, premium design:

- Background: `#0d0d0d` (darker), cards: `#1a1a1a`, borders: `#2a2a2a`
- Font: Roboto (tetap), accent: hijau gradient (#2ecc71 → #27ae60)
- Glassmorphism cards (subtle `backdrop-filter: blur()`)
- Smooth micro-animations (hover, transitions, sidebar slide)
- Collapsible sidebar animation (transform + width transition)
- DMX Address grid styling (512 cells grid layout)
- Fader styling (vertical sliders) untuk Mixer
- Fixture circle glow effects untuk Preview
- Progress bar styling
- Scrollbar dark styling

---

### Component 5: Frontend — JavaScript

#### [MODIFY] [app.js](file:///c:/Users/andre/OneDrive/Documents/SCRIPT/zzlight-luxora/static/js/app.js)

**Rewrite total.** Semua `fetch()` API calls diganti dengan `window.pywebview.api.*()`.

Modules:
- **Sidebar** — toggle, menu selection, slide animation
- **Address Tab** — DMX grid render, drag & drop handling, fixture placement
- **Analyze Tab** — file dialog via pywebview API, analyze call, progress bar, multi-song management, render results (features, V-A, color, waveform, segments)
- **Scenes Tab** — render scene table per song, export to chase
- **Chase Tab** — render chase from scenes, playback controls
- **Mixer Tab** — 512 fader rendering, value change → DMX send
- **Preview Tab** — fixture circles, real-time color update
- **Fixture List** — load from API, drag support
- **Fixture Editor** — form handling, save/load
- **Settings** — form bound to config.ini via API
- **About** — static content rendering
- **Output** — Art-Net target list, connect/disconnect

---

### Component 6: Build System

#### [MODIFY] [build_exe.py](file:///c:/Users/andre/OneDrive/Documents/SCRIPT/zzlight-luxora/build_exe.py)

- Ganti `--console` → `--windowed` (no console window)
- Tambah `--hidden-import=webview`
- Tambah `--add-data=config.ini;.`
- Tambah `--add-data=fixtures;fixtures`
- Tambah icon jika ada

#### [MODIFY] [requirements.txt](file:///c:/Users/andre/OneDrive/Documents/SCRIPT/zzlight-luxora/requirements.txt)

Hapus `flask` dan `flask-socketio`, tambah `pywebview>=5.0` (sudah ada).

```
librosa>=0.10.0
numpy>=1.24.0
scipy>=1.10.0
pywebview>=5.0
stupidArtnet>=1.4.0
soundfile>=0.12.0
pyinstaller>=6.0
```

#### [NEW] [fixtures/](file:///c:/Users/andre/OneDrive/Documents/SCRIPT/zzlight-luxora/fixtures/)

Folder default untuk fixture definitions.

#### [NEW] [fixtures/Generic PAR RGBW 8ch.json](file:///c:/Users/andre/OneDrive/Documents/SCRIPT/zzlight-luxora/fixtures/Generic%20PAR%20RGBW%208ch.json)

```json
{
  "name": "Generic PAR RGBW 8ch",
  "manufacturer": "Generic",
  "channels": 8,
  "channel_map": [
    {"ch": 1, "label": "Dimmer"},
    {"ch": 2, "label": "Red"},
    {"ch": 3, "label": "Green"},
    {"ch": 4, "label": "Blue"},
    {"ch": 5, "label": "White"},
    {"ch": 6, "label": "Program"},
    {"ch": 7, "label": "Speed"},
    {"ch": 8, "label": "—"}
  ]
}
```

---

## File Structure (Final)

```
SCRIPT/zzlight-luxora/
├── app.py                    # PyWebView entry point + API class
├── audio_engine.py           # Audio analysis (unchanged logic)
├── scene_generator.py        # Scene/chase generation (unchanged logic)
├── artnet_sender.py          # Art-Net UDP wrapper (unchanged logic)
├── config.ini                # Default settings
├── requirements.txt          # Python dependencies (no Flask)
├── build_exe.py              # PyInstaller build script
├── fixtures/                 # Fixture definition files
│   └── Generic PAR RGBW 8ch.json
├── templates/
│   └── index.html            # Full GUI (rewritten)
└── static/
    ├── css/
    │   └── style.css         # Dark theme (rewritten)
    └── js/
        └── app.js            # Frontend logic (rewritten)
```

---

## Verification Plan

### Automated Tests
1. Run `python app.py` — verify PyWebView window opens
2. Test file dialog — select .mp3/.wav file
3. Test analyze — verify results appear in UI
4. Test Art-Net connect/disconnect
5. Test all sidebar menu navigation
6. Test DMX address grid drag & drop
7. Test mixer faders

### Manual Verification
1. Visual check dark mode theme
2. Test sidebar collapse/expand animation
3. Test all 6 program tabs
4. Verify fixture list and editor
5. Test multi-song analysis workflow
6. Build EXE with `python build_exe.py` → verify standalone run

### Browser Recording
- Record sidebar navigation flow
- Record analyze workflow
- Record mixer interaction
