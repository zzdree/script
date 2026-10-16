# 🎛️ Feedback ZZLUXORA — v5 (Console Neutrality, Fixture Register & One Song List)

- **Sumber:** User Review & Feedback v5
- **Tanggal:** 16 Oktober 2026
- **Menggantikan:** `feedback_v4.md` (6 Okt 2026) untuk bagian yang bertentangan; bagian lain v4 tetap berlaku
- **Referensi:** QLC+ v4.14.4 & v5.3.0 source (`qmlui/qml/fixturesfunctions/`), grandMA3 onPC

> **Catatan:** beberapa butir di bawah **membatalkan** ketentuan v4 secara sengaja. Butir yang membatalkan ditandai **SUPERSEDES v4 §n** agar tidak ada dua dokumen yang saling bertentangan saat dibaca ulang.

---

## 1. Netralitas Warna: Warna Hanya untuk Makna

**Permintaan:** *"untuk tombol address, analyze, dll, sampai mixer, aku kurang suka karena ada warnanya. kalau bisa seperti app profesional yg lain, netral gitu, ga kebanyakan warna."*

**Hasil pengukuran sebelum diubah** (teknik: crop area + hitung warna piksel, bukan penilaian mata):

| Elemen | Warna terukur | Kesimpulan |
|---|---|---|
| Teks tab aktif | `RGB(255,255,255)` saturasi 0,00 | sudah netral |
| Teks tab lain | `RGB(203,213,225)` = `TEXT_SECONDARY`, saturasi 0,10 | sudah netral |
| Kolom Grand Master | outline `#f59e0b` 2px | **pelanggaran** |
| Heading "GRAND MASTER" | `#f59e0b` | **pelanggaran** |
| Penanda seleksi | `border-left: 3px` / `border-bottom: 3px` beraksen | **pelanggaran** |

**Temuan penting:** kesan "banyak warna" **bukan** dari teks tab, melainkan dari **aksen** di tempat yang melanggar doktrin proyek sendiri (*"Elemen berwarna harus BLOK PENUH, bukan outline"*).

**Keputusan:**
1. Kolom Grand Master: outline amber **dihapus**, menjadi `1px` netral. Amber tinggal di **batang rail** dan **nilai master** — satu-satunya fader yang mengalikan seluruh kanal.
2. Header fader: tidak lagi amber/cyan. Header adalah **label**, bukan **status**.
3. Penanda seleksi: **blok penuh**, bukan garis tepi. Tab aktif memakai latar penuh; item daftar terpilih memakai latar penuh.

**Tetap berwarna (membawa makna, bukan hiasan):**
- Pemetaan warna kanal DMX: `DIM`, `RED`, `GRN`, `BLU`, `WHT`, `STR`
- Tipografi kuadran Russell di tab Result
- Bracket pembatas fixture di grid Address

---

## 2. Hapus Judul dan Deskripsi Ganda per Tab

**Permintaan:** *"tampilan isi menu bar address, analyze, dll, sampai mixer kan ada judul dan deskripsi tuh, hapus aja, kelihatan ai slop banget."*

**Contoh yang dihapus:**
```text
DMX ADDRESS PATCH SHEET                                    ← mengulang nama tab
256 DMX Channel Matrix (Max 24 Columns) | Drag & drop...   ← menerangkan yang sudah jelas
```

**Keputusan:** judul dan deskripsi dihapus dari **keenam** tab, termasuk `QVBoxLayout` pembungkusnya agar tidak menyisakan celah kosong. Nama tabbar sudah menyebutkan tabnya. Pola *judul lalu subjudul* berasal dari halaman pemasaran; QLC+ dan grandMA tidak memakainya.

---

## 3. Tab Address: Panel Fixture, Grid 512, dan Anti-Tumpang-Tindih

### 3.1 Grid 512 Kanal — **SUPERSEDES v4 §10 (256 kanal)**

**Permintaan:** *"kotak sampai 512 ya, karena 1 universe bisa muat sampai 512 channel."*

**Keputusan:** grid naik dari 256 ke **512** kanal (satu universe DMX512 penuh), 24 kolom per baris (22 baris), dapat di-scroll vertikal. Batas validasi patch dan pencarian fixture ikut naik ke 512; sebelumnya paruh atas universe tidak dapat dipakai sama sekali.

### 3.2 Panel Fixture di Kolom Kiri

**Permintaan:** *"kalau bisa ada kotak yg isinya list fixture gitu, yg di drag and drop... nanti ada tombol plus dan minus, atau add dan remove... nama fixture auto urut, pakai [1] gini, atau bisa juga alamat fixture auto detect."*

**Bentuk terpilih: daftar fixture PROYEK** (bukan katalog `.zfx`), lebar 210px:

```text
┌─ FIXTURES ──────────┐
│ [+] [−]             │
│ [1] Alien-AL36 #1   │
│     DMX 1-8         │
│ [2] Alien-AL36 #2   │
│     DMX 17-24       │
└─────────────────────┘
```

- **Nomor urut `[n]`** dihitung dari urutan alamat (auto-urut)
- **Alamat `DMX a-b`** diturunkan dari grid, sehingga panel tidak dapat melenceng dari patch sebenarnya
- `+` memanggil pemilihan preset; `−` menghapus fixture terpilih setelah **satu** konfirmasi yang mencakup seluruh pilihan
- Mengikuti struktur `FixtureBrowserDelegate.qml` QLC+: satu baris per fixture, tinggi tetap, pemisah 1px, tanpa dekorasi

### 3.3 Rombongan Fixture Dapat Dikelola

**Permintaan:** *"rombongan blok fixture harusnya bisa di select, bisa dipindah, bisa dihapus."*

- **Select banyak:** `QListWidget` mode `ExtendedSelection`; kanal fixture terpilih disorot di grid dengan **bingkai putih** sehingga warna kanal tetap terbaca
- **Pindah:** drag dari panel ke grid. Payload membawa seluruh daftar kanal dan `move_source_channels`
- **Hapus:** tombol `−`, satu konfirmasi untuk seluruh pilihan

### 3.4 Anti-Tumpang-Tindih — Mengikuti Pola QLC+

**Permintaan:** *"kalau pindah fixture ke blok lain, usahakan gabisa saling tumpang tindih ya."*

**Referensi QLC+** (`FixtureBrowserDelegate.qml:141` + `FixtureBrowser.qml:287`):
```javascript
if (FxDragJS.endDrag(mouse) === false)
    fxDraggableItem.overlappingEvent()
// ditangani oleh: onOverlappingEvent: errorPopup.open()
```

QLC+ **menolak** drop yang bertabrakan lalu **memberi tahu operator**, bukan mencegah diam-diam.

**Keputusan:** drop yang bertabrakan **ditolak** dengan pesan yang menyebut kanal mana yang sudah terisi. Dua aturan penting:
1. Kanal milik fixture yang **sedang dipindahkan** tidak dihitung sebagai penghalang — fixture tidak memblokir tujuannya sendiri
2. Kanal asal **dilepas hanya setelah** posisi baru dipastikan bebas. Tanpa ini, drop yang ditolak akan **menghapus fixture**

---

## 4. Bilah Tombol Address Disederhanakan

**Permintaan:** *"bagian tombol undo dan redo hapus aja... terus kalau bisa hanya 2 tombol: patch, nanti muncul pop up... terus samping kanan ada clear, untuk clear patch, jangan lupa ada pop up konfirmasi."*

**SUPERSEDES v4 §10 (yang mencantumkan `UNDO`, `REDO`, `PATCH 4x ALIEN (GIA)`, `PATCH 1x KUMA (BENCH)`):**

| Sebelum | Sesudah |
|---|---|
| `UNDO (Ctrl+Z)` | **dihapus** — `Ctrl+Z` sudah global |
| `REDO (Ctrl+Y)` | **dihapus** — `Ctrl+Y` sudah global |
| `PATCH 4x ALIEN (GIA)` | digabung |
| `PATCH 1x KUMA (BENCH)` | digabung |
| `CLEAR PATCH` | tetap, dengan konfirmasi |

**Sesudah:** dua tombol — `PATCH...` (membuka dialog pemilihan preset, harus pilih salah satu) dan `CLEAR PATCH`.

---

## 5. Satu Daftar Lagu untuk Analyze, Result, dan Perform

**Permintaan:** *"isi menu analyze, result, dan perform harusnya kasih song list di sisi kiri, dan itu sinkron kalau di select, bisa? kalau diubah urutan ya sinkron juga... trs ada tombol add dan remove seperti fixture list."*

**Masalah:** Analyze punya `Session Audio Playlist` dan Perform punya `Live Show Playlist` — **dua daftar terpisah**. Bahan yang sama harus dimasukkan dua kali, dan urutannya mudah berbeda.

**Keputusan:** `core/song_library.py` menjadi **sumber tunggal**. Satu perubahan (tambah, hapus, pilih, ubah urutan) terlihat di ketiga tab.

**Dua jalur masuk yang didukung:**
- **Sebagai berkas** — dimuat dari disk, belum dianalisis
- **Sebagai hasil analisis tanpa berkas** — Perform menjadwalkan cue dari **analisis**, bukan dari audionya, sehingga lagu yang dianalisis di mesin lain tetap dapat dipakai

**Aturan kejujuran tampilan:** lagu yang belum dianalisis ditampilkan `not analysed`, **tidak** mengarang angka BPM atau kuadran. Prinsip yang sama dengan perbaikan FASE 8 pada audio diam.

---

## 6. Standar Nama Fixture Resmi Ditegakkan — **MEMPERKUAT v4 §2**

**Ditemukan saat mengerjakan panel fixture:** v4 §2 mewajibkan `Alien-AL36` dan `Kumastb-STL47` tanpa keterangan teks, tetapi **tiga tempat melanggarnya**:

| Berkas | Nama lama (melanggar) | Nama baru |
|---|---|---|
| `ui/panels/address_tab.py` (quick-patch) | `Alien AL36 #1 (8CH)` | `Alien-AL36 #1` |
| `ui/panels/address_tab.py` (quick-patch) | `Kumastb STL47 (8CH RGBW)` | `Kumastb-STL47` |
| `showfiles/gia_deliksari_alien_4x.zlx` | `Alien AL36 #1..4 (8CH)` | `Alien-AL36 #1..4` |
| `showfiles/bench_kumastb_stl47.zlx` | `Kumastb STL47 (8CH RGBW)` | `Kumastb-STL47` |

**Pelanggaran ini terlewat** dari pengawas anti-slop dan seluruh suite test karena tidak ada yang menguji **kepatuhan nama terhadap standar**. Kini ada `TestFixtureNameStandard` yang menjaganya.

**Nomor unit** tetap ada sebagai `#n` agar empat unit fisik dapat dibedakan, tanpa `(8CH)`.

**Batas yang diakui:** fixture **generik** (mis. `PAR LED Front Left (8CH)` pada `demo_church_worship.zlx`) **tidak** diatur v4 §2 karena tidak memiliki profil `.zfx` resmi. Test penamaan sengaja melewatkannya.

---

## 7. Yang BELUM Dikerjakan dari v5

| Butir | Status |
|---|---|
| Drag dari panel fixture ke grid | **selesai** (payload + rilis-kanal-asal) |
| Panel song list **visual** di tab Result | **belum** — data sudah sinkron, tampilan belum dipasang |
| Tampilan BPM/kuadran di song list ketiga tab | **sebagian** — ringkasan sudah tampil, detail belum |

---

## 8. Jebakan Teknis yang Ditemukan (untuk agen berikutnya)

1. **`__len__` membuat objek falsy.** `SongLibrary` mendefinisikan `__len__`, sehingga instance kosong bernilai `False`. Pola `song_library or SongLibrary()` **membuang** library yang diberikan pemanggil dan membuat yang baru, sehingga tiga tab tidak sinkron. **Selalu pakai `is None`** untuk parameter default bertipe itu.
2. **Qt6 memindahkan enum ke dalam kelas enum.** `QListWidget.ExtendedSelection` tidak ada; yang benar `QListWidget.SelectionMode.ExtendedSelection`. `Qt.UserRole` dan `Qt.AlignCenter` **masih** ada di namespace `Qt`.
3. **Memblokir sinyal saat repaint menghilangkan efek samping.** `_refresh_playlist_view` memblokir sinyal list, sehingga `_on_song_selected` tidak jalan dan tabel cue tetap kosong. Efek samping harus dipanggil eksplisit setelah repaint.
4. **Ukur sebelum menebak.** Kesan "tab berwarna-warni" **terbukti salah** setelah sampel piksel. Empat kali dalam sesi ini kesimpulan dari kesan visual keliru; sampel piksel selalu benar.
