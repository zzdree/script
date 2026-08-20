# Verifikasi Build — zzluxora v8.0.0

**Tanggal:** 2026-06-22
**Path:** `C:\ANDREAS\SCRIPT\zzluxora`
**Backup v7:** `C:\ANDREAS\SCRIPT\zzluxora_v7_backup\`
**Status:** ⏳ MENUNGGU VERIFIKASI ANTIGRAVITY

---

## 1. Math Model Test (RELEASE BLOCKER)

| Test | Expected | Status |
|---|---|---|
| test_10k_reasons_normalization | BPM_n=0.108, RMS_n=0.143, SC_n=0.289, MFCC1_n=0.450, Onset_n=0.133, Chroma_n=0.720 | ⬜ |
| test_10k_reasons_va | V=0.627, A=0.126, Q4 Damai | ⬜ |
| test_10k_reasons_hsv | H=162.7°, S=0.178, V_hsv=0.135 | ⬜ |
| test_10k_reasons_drgbw | D=34, R=0, G=6, B=4, W=28 | ⬜ |
| test_10k_reasons_chase_timing | 1500ms (BPM 73 < 90) | ⬜ |
| test_10k_reasons_full | End-to-end PASS | ⬜ |
| test_quadrant_q1_praise | H≈48° | ⬜ |
| test_quadrant_q2_intens | H≈294° | ⬜ |
| test_quadrant_q3_kontemplatif | H≈224° | ⬜ |
| test_quadrant_q4_damai | H≈170° | ⬜ |
| test_hsv_red_pure | RGB(1,0,0) | ⬜ |
| test_hsv_white | RGB(1,1,1) | ⬜ |
| test_hsv_black | RGB(0,0,0) | ⬜ |
| test_rgbw_pure_red | R'=1, W=0 | ⬜ |
| test_rgbw_white_extraction | W=0.5 | ⬜ |
| test_rgbw_mixed | R'=0.5, G'=0.1, W=0.2 | ⬜ |
| test_chase_timing_brackets | 500/700/1500ms | ⬜ |
| test_pattern_selection | all_on/running/gradient/center_out | ⬜ |
| **TOTAL** | **19/19** | ⬜ |

**Perintah:**
```powershell
cd C:\ANDREAS\SCRIPT\zzluxora
C:\ANDREAS\SCRIPT\.venv\Scripts\python.exe tests\test_math_model.py
```

---

## 2. Accent Migration (green → yellow)

| File | Yang diubah | Status |
|---|---|---|
| styles.py | QSS accent tokens (hover, pressed, selected, tab, sidebar, progress) | ⬜ |
| main.py | Version 8.0.0, splash accent yellow | ⬜ |
| splash_screen.py | Progress bar gradient #FFD700/#E6C200 | ⬜ |
| main_window.py | Statusbar color #FFD700, version "v8.0" | ⬜ |
| sidebar.py | Active triangle marker #FFD700 | ⬜ |
| scenes_tab.py | List selected, song header, controls box, apply button, group header | ⬜ |
| audio_tab.py | Analyze button bg/border/hover | ⬜ |
| chase_tab.py | Save button, play button | ⬜ |
| color_mixer_tab.py | Active label, set-active button, tab selected, sync label | ⬜ |
| output_tab.py | Selected item, custom edit color, target label | ⬜ |
| fixture_list_panel.py | Dropdown border, item hover color | ⬜ |
| page_tab.py | Button hover border | ⬜ |
| widgets/__init__.py | Background accent | ⬜ |
| mixer_tab.py | Master value + channel hover | ⬜ |

**Status green TETAP #2ecc71** (benar):
| File | Alasan |
|---|---|
| toast.py | Toast success/info border (status) |
| preview_tab.py:111 | Connected status indicator |
| rms_chart.py | Chart data visualization |
| va_diagram.py | Diagram data visualization |
| address_tab.py:20 | Grid data color key |
| chase_tab.py:57 | Timeline bar fallback color |
| artnet_pill.py | Connected/disconnected dot |
| output_tab.py:298 | Connected status text |

**Verifikasi:**
```powershell
cd C:\ANDREAS\SCRIPT\zzluxora
grep -r "#2ecc71" panels/ widgets/ styles.py sidebar.py main_window.py | grep -v __pycache__
```
Expected: sisa #2ecc71 hanya di status/data locations (toast, preview connected, charts, artnet pill).

---

## 3. Mixer grandMA3 Style

| Item | v7 | v8 | Status |
|---|---|---|---|
| Master default | 255 | 0 (blackout) | ⬜ |
| Master value button text | "255" | "0" | ⬜ |
| Fader strip width | 28px | 48px | ⬜ |
| Fader min height | 60px | 140px | ⬜ |
| Label position | bottom | top (label→fader→value) | ⬜ |

---

## 4. Visual QA Checklist

| # | Checkpoint | Status |
|---|---|---|
| 1 | Splash screen 3 detik, logo besar, progress bar yellow | ⬜ |
| 2 | Header: brand + project path + Art-Net pill + Play/Pause + Blackout | ⬜ |
| 3 | Sidebar: hamburger toggle, 5 items, yellow active marker | ⬜ |
| 4 | Tab system: 8 tabs, yellow selected indicator | ⬜ |
| 5 | Mixer: 513 faders, label top, 48px strip, master default 0 | ⬜ |
| 6 | Preview: 2D canvas, drag fixtures, X/Y sidebar | ⬜ |
| 7 | Output: scan panel, localhost+ESP32+custom, yellow selected | ⬜ |
| 8 | About: urutan Application → Judul Skripsi (9 fields) | ⬜ |
| 9 | No emoji in chrome UI (geometric glyphs only) | ⬜ |
| 10 | Window title = "zzluxora", icon = lampu putih | ⬜ |

**Perintah:**
```powershell
cd C:\ANDREAS\SCRIPT\zzluxora
C:\ANDREAS\SCRIPT\.venv\Scripts\python.exe main.py
```

---

## 5. Build .exe

| Step | Perintah | Status |
|---|---|---|
| Generate ICO | `python tools/make_ico.py` | ⬜ |
| Build dist | `python build.py` | ⬜ |
| Check output | `ls ../results/zzluxora-v8/` | ⬜ |
| Check exe size | `wc -c ../results/zzluxora-v8/zzluxora.exe` | ⬜ |

---

## 6. Build Installer

| Step | Perintah | Status |
|---|---|---|
| Compile ISCC | `ISCC.exe installer\zzluxora.iss` | ⬜ |
| Check output | `ls installer/Output/zzluxora-setup-v8.0.0.exe` | ⬜ |
| Check size | `wc -c installer/Output/zzluxora-setup-v8.0.0.exe` | ⬜ |

---

## 7. Smoke Test

| # | Test | Expected | Status |
|---|---|---|---|
| 1 | Silent install | `C:\Program Files\zzluxora\zzluxora.exe` ADA | ⬜ |
| 2 | Registry key | Terdaftar | ⬜ |
| 3 | Launch app | Splash muncul, config.ini tercipta di %APPDATA% | ⬜ |
| 4 | Uninstall silent | Program Files bersih, registry bersih | ⬜ |
| 5 | AppData prompt | "Keep settings?" muncul saat uninstall | ⬜ |

---

## 8. Dual-source Cleanup (opsional)

| Issue | File | Fix | Status |
|---|---|---|---|
| Legacy duplicate functions | audio_engine.py | Hapus va_to_hsv, hsv_to_rgb, rgb_to_rgbw, full_pipeline | ⬜ |
| Wrong import | scene_generator.py:7 | Ganti `from .audio_engine import full_pipeline` → `from engines.color_mapping import ...` | ⬜ |

---

## Ringkasan

| Fase | Status |
|---|---|
| 1. Branding & Splash | ⬜ |
| 2. Header & Menu | ⬜ |
| 3. Sidebar | ⬜ |
| 4. Design Tokens | ⬜ |
| 5. Tab System | ⬜ |
| 6. Core Analyze (19/19) | ⬜ |
| 7. Scenes/Chase/Page | ⬜ |
| 8. Mixer grandMA3 | ⬜ |
| 9. Preview/Output | ⬜ |
| 10. Installer | ⬜ |

**Kesimpulan:** ⏳ MENUNGGU VERIFIKASI
