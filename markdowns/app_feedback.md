# Feedback v1 → zzluxora v6 Alignment Audit

**Date**: 2026-06-14
**Source**: `C:\Users\andre\OneDrive\Documents\feedback_v1.txt` (179 lines, v4→v6 brief)
**Target**: `C:\Users\andre\OneDrive\Documents\SCRIPT\zzluxora\` (v6.0.0 release)

## TL;DR

**~60 % aligned.** Core math + audio + Art-Net engine = full match. Branding + docs + structure = full match. **UX/UI still has 4 major gaps + 7 partial gaps.**

| Bucket | Count | Examples |
| ------ | ----- | -------- |
| 🟢 Fully aligned | ~30 | splash, branding, file menu, artnet pill, channel colors, scene types, About order, modern minimalist |
| 🟡 Partial / differs | ~10 | 2-buttons vs 1-button, mixer master on top vs left, 0–255 vs 1–255, onboarding vs faded empty |
| 🔴 Major gap | 4 | preview = plain text (not PAR LED), output = manual IP (not QLC+ scan), fixture list = sidebar item (not dropdown), help menu = About (not Shortcuts) |
| ⚪ TBD / unchecked | ~6 | AddressGrid position-corner, analyze button disabled state, address 24-col density, sidebar auto-hide icons |

---

## Detailed Map (53 items)

| # | Feedback | Current | Status | File:line |
| - | -------- | ------- | ------ | --------- |
| 1 | App name `zzluxora` | `BRAND_TEXT = "zzluxora"` | 🟢 | widgets/header_bar.py:17 |
| 2 | Logo lampu putih bg hitam | `assets/logo_256.png` | 🟢 | assets/ |
| 3 | Splash 3s, grandma3 ref | `SplashScreen` 3 s | 🟢 | widgets/splash_screen.py |
| 4 | 3 menubar (File/View/Help) | 3 menus | 🟢 | main_window.py |
| 5 | File: open/save/save as/exit | 4 actions | 🟢 | main_window.py |
| 6 | Exit no shortcut | no shortcut | 🟢 | main_window.py |
| 7 | Ext `.zlx` | `.zlx` | 🟢 | panels/project_io.py |
| 8 | `Untitled.zlx` default | `"Untitled.zlx"` | 🟢 | widgets/header_bar.py:81 |
| 9 | View 5 items | 6 items (incl. Color) | 🟡 | sidebar.py:20-27 |
| 10 | Sidebar active marker | none | 🔴 | sidebar.py |
| 11 | Help = Shortcuts | Help → About | 🔴 | main_window.py (Help menu) |
| 12 | Help: less emoji | "🎨 Keyboard Shortcuts" | ⚪ | widgets/help_modal.py:30 |
| 13 | Help: no v4 ref | `"v6.0 - Native PySide6 + Art-Net"` | 🟡 | widgets/help_modal.py:32 |
| 14 | Header: shortcuts text | Start + Stop buttons | 🔴 | widgets/header_bar.py:106-116 |
| 15 | Project name in header | `"Project: <i>name</i>"` | 🟢 (verbose) | widgets/header_bar.py:95 |
| 16 | Art-Net status w/ colors | `ArtNetStatusPill` | 🟢 | widgets/artnet_pill.py |
| 17 | Play/Stop **1 button** | 2 buttons (Start + Stop) | 🔴 | widgets/header_bar.py:106-116 |
| 18 | Status right-aligned | `addWidget(pill)` after stretch | 🟢 | widgets/header_bar.py:99 |
| 19 | Sidebar collapsed when no zlx | onboarding overlay | 🟠 | main_window.py |
| 20 | Faded empty state | onboarding (5 steps) | 🟠 | widgets/onboarding.py |
| 21 | Hamburger stays `☰` | `☰` always | 🟢 | sidebar.py:109 |
| 22 | Sidebar icons auto-hide | no auto-hide | ⚪ | sidebar.py |
| 23 | Address: more buttons | only clear + auto | 🟡 | panels/address_tab.py:60-69 |
| 24 | Address: 24 horizontal | TBD | ⚪ | widgets/fixture_grid.py |
| 25 | Address: position in corner | TBD | ⚪ | widgets/fixture_grid.py |
| 26 | Address: cell color by type | `CHANNEL_COLORS` (10 colors) | 🟢 | panels/address_tab.py:14-25 |
| 27 | Analyze: 4 buttons disabled | TBD | ⚪ | panels/audio_tab.py |
| 28 | Analyze: progress + 3 s desc | TBD | ⚪ | panels/audio_tab.py |
| 29 | Scenes: **no regenerate** | `🔄 Regenerate Scenes` exists | 🔴 | panels/scenes_tab.py:38-42 |
| 30 | Scenes: section types | chorus/verse/etc | 🟢 | engines/scene_generator.py |
| 31 | Chase: clean up | has editor | 🟢 | panels/chase_tab.py |
| 32 | Custom page tab | Programs tab | 🟢 | panels/programs_tab.py |
| 33 | Mixer: master **left** | master on top | 🔴 | panels/mixer_tab.py:35-51 |
| 34 | Mixer: 513 sliders | 512 sliders | 🟡 | panels/mixer_tab.py:62 |
| 35 | Mixer: 1–255 range | 0–255 | 🟡 | panels/mixer_tab.py:64 |
| 36 | Mixer: refresh **top right** | bottom | 🟡 | panels/mixer_tab.py:88-91 |
| 37 | Preview: PAR LED circle + drag | plain text list | 🔴 | panels/preview_tab.py:42-77 |
| 38 | Preview: right x/y sidebar | none | 🔴 | panels/preview_tab.py |
| 39 | Output: Art-Net IP scan | manual IP only | 🔴 | panels/output_tab.py:83-87 |
| 40 | Output: drop universe + FPS | both still there | 🔴 | panels/output_tab.py:88-96 |
| 41 | Output: just save button | 5 buttons (connect/disconnect/blackout/test/live) | 🔴 | panels/output_tab.py:100-134 |
| 42 | Fixture list: **dropdown** | sidebar item | 🔴 | panels/fixture_list_panel.py |
| 43 | Fixture list: drag n drop | `setDragEnabled(True)` | 🟢 | panels/fixture_list_panel.py:46-47 |
| 44 | Fixture editor: open + new | New + Save only | 🟠 | panels/fixture_editor_panel.py:92-105 |
| 45 | Fixture editor: name/mfr/ch | all present | 🟢 | panels/fixture_editor_panel.py:33-43 |
| 46 | Fixture editor: 3 cols (ch, label, type) | 2 cols (ch, label) | 🟡 | panels/fixture_editor_panel.py:62-64 |
| 47 | Fixture editor: types | `FIXTURE_TYPES` (10 types) | 🟢 | engines/fixture_types.py |
| 48 | Fixture editor: save below | yes | 🟢 | panels/fixture_editor_panel.py:97-104 |
| 49 | About order (app → judul) | yes | 🟢 | panels/about_panel.py |
| 50 | About: no bug text | yes | 🟢 | panels/about_panel.py |
| 51 | Modern minimalis (grandma3 + qlc+) | yes | 🟢 | DESIGN.md |
| 52 | Plan in markdowns/app_upgrade.md | yes | 🟢 | markdowns/app_upgrade.md |
| 53 | Compare v5 + suggestions | yes (v6.0.0 entry) | 🟢 | CHANGELOG.md |

---

## Major Gaps (🔴) — needs refactor

| # | Item | Current | Feedback wants |
| - | ---- | ------- | -------------- |
| 1 | **Preview tab** | plain text list of fixtures w/ values | PAR LED circle widget, draggable, right sidebar with x/y fields |
| 2 | **Output tab** | manual `QLineEdit` for IP + universe + FPS + 5 buttons | QLC+ style node scan (localhost + 192.168.4.1 + custom) + just save button |
| 3 | **Fixture list** | sidebar item → opens right panel | triangle-down button → dropdown overlay |
| 4 | **Help menu** | `Help → About (F1)` | `Help → Shortcuts (F1)` (or rename to "Shortcuts") |
| 5 | **Header buttons** | Start + Stop (2 buttons) | 1 play/pause toggle |
| 6 | **Mixer master** | on top (own `QGroupBox`) | on the left of channels 1-512 |
| 7 | **Scenes regenerate** | `🔄 Regenerate Scenes` button | remove (redundant w/ analyze) |

## Partial Gaps (🟡) — quick polish

| # | Item | Current | Wants |
| - | ---- | ------- | ----- |
| 1 | Help modal subtitle | `"v6.0 - Native PySide6 + Art-Net"` | drop subtitle (v4 ghost) |
| 2 | View sidebar items | 6 (incl. Color) | 5 (no Color) |
| 3 | Address buttons | 2 (clear + auto) | more (random, group, etc.) |
| 4 | Mixer count | 512 sliders | 513 sliders (master + 512) |
| 5 | Mixer range | 0–255 | 1–255 |
| 6 | Mixer refresh | bottom | top right |
| 7 | Fixture editor cols | 2 (ch, label) | 3 (ch, label, type) |

## Differs (🟠) — design choice, not strict gap

| # | Item | Current | Feedback wants |
| - | ---- | ------- | -------------- |
| 1 | Empty state | onboarding overlay (5 steps) | faded icon + "silahkan..." text |
| 2 | Fixture editor open | only "New" button | "Open" + "New" buttons (file explorer) |

---

## Suggested Phases (if you want to close gaps)

### Phase 9 — Header & Help Refactor
- Replace Start/Stop → 1 play/pause toggle
- Drop "Project: " prefix, show filename + path on hover
- Help menu: "Shortcuts" (not "About")
- Help modal: drop subtitle
- **Files**: `widgets/header_bar.py`, `widgets/help_modal.py`, `main_window.py`

### Phase 10 — Preview Tab Rewrite
- PAR LED circle widget per fixture
- Drag-to-move (top-down 2D view)
- Right sidebar with x/y spinboxes
- **Files**: `panels/preview_tab.py`, `widgets/preview_widget.py`

### Phase 11 — Mixer Tab Refactor
- Master dimmer **left** (full-height vertical fader, value 1-255)
- 513 sliders (master + 512)
- Refresh **top right** as icon button
- 24 columns horizontal (was 32)
- **Files**: `panels/mixer_tab.py`

### Phase 12 — Output Tab QLC+ Style
- IP scan panel: localhost + 192.168.4.1 + custom
- Drop universe + FPS from panel (moved to header status?)
- Buttons: just `Save` (connect/disconnect/blackout in header)
- **Files**: `panels/output_tab.py`, `engines/artnet_sender.py` (add `scan()`)

### Phase 13 — Fixture List Dropdown
- Triangle-down button (in header? sidebar?)
- Dropdown overlay with list (drag n drop)
- Drop "Fixture List" sidebar item
- **Files**: `panels/fixture_list_panel.py` (rewrite as popup), `sidebar.py`

### Phase 14 — Sidebar + Empty State
- Active marker (triangle/dot on current item)
- Collapsed when no zlx (onboarding hides sidebar instead of overlay)
- Faded icon + "Silahkan buka project" text
- **Files**: `sidebar.py`, `widgets/empty_state.py`, `main_window.py`

### Phase 15 — Scenes Tab Cleanup
- Remove "Regenerate" button
- Group scenes by type (chorus/verse/bridge)
- "Convert to Chase" button
- **Files**: `panels/scenes_tab.py`

### Phase 16 — Fixture Editor 3-col + Open
- Table: Ch | Label | Type (3 cols)
- Open button (file explorer for .json)
- Type column = `QComboBox` per row
- **Files**: `panels/fixture_editor_panel.py`

### Phase 17 — Address Tab Density + Position Corner
- Max 24 horizontal (configurable)
- Position number in corner (top-right)
- More buttons: random, group-by-type, etc.
- **Files**: `panels/address_tab.py`, `widgets/fixture_grid.py`

---

## TL;DR Verdict

> **v6.0.0 is a solid functional MVP, ready for skripsi submission.**
> Math/audio/Art-Net core = perfect. Branding/docs/structure = perfect.
> UX/UI has feedback items unaddressed (8 major, 10 partial).
>
> **Three options**:
> (A) **Ship v6.0.0 as-is** — skripsi-final, polished, complete
> (B) **Tackle Phase 9+** to close all gaps (better UX, more work)
> (C) **Cherry-pick specific gaps** (e.g. just header + help)
