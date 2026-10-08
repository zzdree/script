# Protokol Pengujian Sistem dan Pengambilan Data

> **Status:** rancangan protokol untuk ditinjau dan disetujui dosen pembimbing sebelum pengambilan data. Dokumen ini tidak memuat hasil pengujian. Semua kolom hasil aktual dan status uji sengaja dikosongkan.

## 1. Tujuan, batas pengujian, dan status bukti

Protokol ini merinci pengujian teknis, fungsional, reliabilitas instrumen, rekrutmen, dan persiapan lapangan untuk melengkapi metode pada [Bab 3](script_chapter_03.md) serta lembar hasil pada [Bab 4](script_chapter_04.md). Acuan khususnya adalah Bab 3 §3.3 (subjek), §3.5 (hipotesis), §3.7.1 (pengujian teknis), §3.8 (keabsahan dan reliabilitas), §3.9.1 (analisis teknis), dan Bab 4 §4.2–§4.3. Kuesioner yang dirujuk ialah [script_questionnaires.md](script_questionnaires.md).

### 1.1 Fakta yang tercatat dalam berkas proyek

| Fakta terdokumentasi (belum sama dengan hasil uji lapangan) | Sumber |
|---|---|
| Bab 3 menetapkan H₃: *end-to-end latency* < 100 ms. Bab 3 §3.4.2 mendefinisikan variabel dari transmisi paket sampai respons lampu; §3.7.1 menyebut pencatatan waktu transmisi dan *end-to-end*; §3.9.1.c meminta statistik deskriptif. | `markdowns/script_chapter_03.md` |
| Bab 3 merencanakan 25 responden dari jemaat/*Youth* GIA Deliksari, usia 17–45 tahun, dengan kesukarelaan dan kesediaan mempelajari/mengoperasikan sistem. Dokumen yang sama mengusulkan α Cronbach ≥ 0,6. | `markdowns/script_chapter_03.md` §3.3 dan §3.8 |
| Kuesioner yang tersedia memuat 10 butir SUS dan 6 butir kesesuaian pencahayaan per lagu, skala 1–5. | `markdowns/script_questionnaires.md` |
| Pengirim aplikasi dirancang mengirim ArtDmx melalui UDP port 6454, Universe 0; uji SITL terdokumentasi memakai loopback `127.0.0.1`. | `zzluxora_v10/CLAUDE.md`; `zzluxora_v10/markdowns/TEST_PLAN.md`; `zzluxora_v10/core/artnet_sender.py` |
| Showfile GIA berisi empat patch Alien AL36 8 kanal pada alamat awal DMX 1, 17, 33, dan 49. Berkas saat ini menyimpan `target_ip` `127.0.0.1` dan `universe` 0. | `zzluxora_v10/showfiles/gia_deliksari_alien_4x.zlx` |
| Profil `Alien-AL36.zfx` mendefinisikan 8 kanal (Dimmer, R, G, B, Empty, Program, Speed, Empty); tidak mendefinisikan kanal putih khusus. | `zzluxora_v10/fixtures/Alien-AL36.zfx` |
| Firmware yang tersedia menyebut ESP32 DevKit V1, MAX485, dan LCD 16×2 I2C; DMX memakai GPIO TX 17, RX 16, DE/RE 4 dan Serial2 250.000 bps, 8N2. Firmware memperbarui penanda waktu Art-Net terakhir, tetapi kode yang ditinjau tidak menyediakan penghitung penerimaan/kehilangan berbasis nomor urut. | `artnet_projects/artnet_dmx_final.ino`; `markdowns/artnet_dmx_review.md` |
| ROADMAP v10 menempatkan uji lapangan ESP32 dan PAR LED di Fase 6 sebagai pekerjaan yang belum dicentang; dokumen konteks proyek menyatakan perangkat keras sedang dipinjam dan pengujian aktif beralih ke SITL. Ini status yang tertulis dan perlu dikonfirmasi sebelum jadwal uji. | `zzluxora_v10/markdowns/ROADMAP.md` §Fase 6; `CLAUDE.md` §5 |
| Sepuluh berkas audio tersedia di `zzluxora_v10/data/audio/`; nama-namanya dicantumkan pada §5. | Daftar berkas `zzluxora_v10/data/audio/` |

**Pemisahan bukti:** fakta pada tabel di atas berasal dari spesifikasi, kode, dan rencana yang diperiksa. Fakta tersebut bukan bukti bahwa paket telah diterima, DMX telah keluar, lampu telah menyala, latensi telah memenuhi H₃, atau data responden telah terkumpul. Seluruh hasil empiris harus diisi setelah observasi dan disimpan bersama catatan alat, kondisi, dan waktu pengujian.

### 1.2 Keputusan yang wajib dikunci sebelum pengujian

1. Tetapkan arti operasional H₃ dan statistik utama yang dibandingkan dengan 100 ms; lihat §2.1.
2. Pastikan alat/metode penanda waktu yang tersedia dapat mengukur titik awal dan titik akhir pada basis waktu yang sama. Jangan mengurangkan jam laptop, ESP32, kamera, atau osiloskop yang belum disinkronkan.
3. Tentukan cara instrumentasi/pencatatan penerimaan Art-Net pada ESP32. Keberhasilan `sendto()` atau paket yang terlihat pada sisi pemancar tidak membuktikan paket diterima firmware maupun menghasilkan cahaya pada fixture.
4. Minta persetujuan pembimbing atas ukuran dan status peserta pilot, populasi utama (jemaat, operator lighting, atau kelompok terpisah), pemilihan lagu, dan persyaratan etik bagi peserta usia 17 tahun.
5. Verifikasi empat fixture, mode kanal yang benar, terminasi DMX, akses jaringan, serta ketersediaan perangkat keras secara langsung sebelum menetapkan jadwal lapangan.

## 2. Protokol latensi dan kehilangan paket Art-Net

### 2.1 Definisi pengukuran dan titik ukur

Alur yang hendak diamati ialah: **aksi/uji pemicu di aplikasi → pengiriman ArtDmx → penerimaan paket yang valid di ESP32 → keluaran serial DMX512 → respons optik fixture**. Catat titik-titik berikut secara terpisah agar istilah *latency* tidak menyamarkan batas yang berbeda.

| Simbol | Titik ukur | Instrumen/catatan yang diusulkan |
|---|---|---|
| `t_app` | Aksi yang mengubah output (misalnya perintah uji GO+ yang menghasilkan perubahan DMX terkontrol) | Log aplikasi dengan jam monotonik; untuk pengukuran optik, aksi juga harus menjadi penanda yang terlihat/terekam pada alat pencatat bersama. |
| `t_tx` | Tepat sebelum `sendto()` mengirim datagram ArtDmx | Log pengirim: waktu monotonik, nomor urut Art-Net, Universe, alamat tujuan, dan hasil pemanggilan kirim. Timestamp ini hanya berbasis jam laptop. |
| `t_rx` | Firmware menerima dan memvalidasi ArtDmx pada port 6454 dan Universe yang diuji | Instrumentasi/pencatatan diagnostik penerima yang menyimpan waktu lokal dan nomor urut. Firmware saat ini tidak memberi penghitung kehilangan yang memadai; jangan menganggap titik ini telah tersedia. |
| `t_dmx` | Transisi/frame DMX pada keluaran MAX485/XLR | *Logic analyzer* atau osiloskop pada jalur DMX, bila tersedia; pisahkan keterlambatan pembaruan DMX dari keterlambatan jaringan. |
| `t_light` | Perubahan cahaya pertama yang terukur pada fixture | Fotodioda/sensor optik dan pencatat waktu, atau kamera berkecepatan tinggi untuk ukuran proksi yang didefinisikan dengan jelas. Tentukan ambang deteksi dari kondisi gelap/noise sebelum uji dan dokumentasikan. |

Ukuran yang dapat dilaporkan: `t_rx − t_tx` (satu arah jaringan), `t_dmx − t_rx` (penerima ke DMX), `t_light − t_rx` (penerima ke cahaya), serta `t_light − t_tx` (kirim aplikasi sampai cahaya). Hanya hitung selisih bila kedua timestamp benar-benar berada pada basis waktu yang sama atau koreksi sinkronisasinya telah diukur dan ketidakpastiannya dicatat.

**Metode yang diusulkan untuk H₃:** ukur `t_tx → t_light` dengan akuisisi waktu bersama. Salah satu rancangan ialah penanda listrik saat *test harness* mengirim cue yang diketahui dan sinyal fotodioda pada kanal-kanal pencatat osiloskop/DAQ yang sama; penanda saat paket diterima ESP32 atau aktivitas DMX dapat direkam sebagai kanal diagnostik tambahan. Penundaan penanda terhadap `sendto()` harus dikalibrasi/dibatasi. Keberadaan penanda listrik dan alat tersebut belum terverifikasi; bila tidak tersedia, jangan menyebut angka proksi sebagai pengukuran paket-ke-cahaya yang presisi.

**Alternatif proksi operasional:** rekam satu klip kamera berkecepatan tinggi yang memperlihatkan pemicu antarmuka/operator dan fixture sekaligus. Hitung selisih frame dari aksi visual yang didefinisikan sebelumnya sampai cahaya terdeteksi; `latency_ms = jumlah_frame_selisih / fps_kamera × 1000`. Cara ini memakai satu basis waktu dan berguna untuk *aksi UI-ke-cahaya*, tetapi bukan timestamp paket `sendto()` yang persis. Laporkan sebagai ukuran terpisah/proksi, berikut laju frame dan resolusinya; minta persetujuan pembimbing sebelum menggunakannya untuk H₃.

`time.monotonic_ns()` pada laptop dan `micros()`/`millis()` pada ESP32 adalah jam lokal yang berbeda. Sinkronkan keduanya melalui metode yang dapat diverifikasi bila akan menghitung latensi satu arah, lalu catat metode, offset, dan ketidakpastian sebelum/sesudah sesi. SoftAP ESP32 tanpa akses ke sumber waktu bersama tidak otomatis menyediakan sinkronisasi. Jika sinkronisasi atau galatnya tidak dapat dibuktikan, biarkan selisih lintas-jam kosong/`NA`; laporkan hitungan paket dan ukuran dalam-jam yang tetap valid. Jangan memakai timestamp kalender LCD/komputer sebagai pengganti jam presisi.

**Keputusan H₃ yang menunggu persetujuan:** hipotesis menetapkan ambang ketat `<100 ms`, tetapi protokol Bab 3 belum memilih apakah kriteria berlaku untuk rerata, median, persentil ke-95, atau setiap percobaan. Saran awal: laporkan n, rerata, simpangan baku, median, persentil ke-95, minimum, dan maksimum; tetapkan satu statistik utama serta aturan interval kepercayaan sebelum data dilihat. Terapkan `<100 ms` pada statistik utama yang disetujui, bukan memilih statistik setelah melihat hasil. Jangan gabungkan ukuran UI→cahaya, TX→RX, dan RX→cahaya menjadi satu nilai tanpa dasar sinkronisasi dan definisi yang disetujui.

### 2.2 Packet loss: observabilitas, penghitungan, dan batas klaim

Untuk setiap jendela uji, catat jumlah ArtDmx unik yang dikirim (`N_tx`) serta jumlah yang diterima dan lolos validasi firmware (`N_rx_valid`). Jika penghitung dan pencocokan nomor urut telah disediakan dan diuji, hitung:

`packet loss (%) = (N_tx − N_rx_valid) / N_tx × 100`

Perlakukan duplikat, nomor urut di luar urutan, reset sesi, dan *wraparound* nomor urut secara eksplisit; nomor urut Art-Net satu byte berulang sehingga nomor urut saja tidak cukup untuk mengidentifikasi paket secara global sepanjang sesi. Gunakan identitas jendela/sesi, penghitung lokal, dan pencocokan urutan yang sadar-*wrap*. Validasi bahwa pengirim benar-benar mengirim nomor urut yang dapat dipakai untuk diagnostik.

**Kondisi implementasi saat ini:** firmware yang ditinjau membaca ArtDmx dan memperbarui waktu paket terakhir, tetapi tidak menghitung atau menampilkan total paket valid, nomor urut yang hilang, duplikat, atau paket yang ditolak. Pengirim `sendto()` sukses hanya menunjukkan operasi penyerahan datagram di sisi lokal; *packet capture* pemancar hanya membuktikan paket tampak pada titik tangkap itu. Keduanya tidak membuktikan penerimaan aplikasi ESP32. Maka, untuk angka kehilangan pada penerima diperlukan pencatatan diagnostik penerima/penghitung yang disetujui dan diverifikasi, atau metode instrumentasi setara. *Sniffer* Wi-Fi di udara dapat melengkapi, tetapi bukan pengganti penghitung paket yang diterima firmware.

Paket yang diterima ESP32 pun bukan bukti bahwa fixture menafsirkan DMX dengan benar atau menghasilkan cahaya. Periksa terpisah keluaran DMX fisik dan respons masing-masing lampu (uji black-box FB-24 dan checklist §7). Saat bukti penerimaan firmware tidak tersedia, laporkan metrik itu sebagai **tidak terukur**, bukan `0% loss` dan bukan sebagai bukti output optik.

Saat ini Bab 3 tidak menetapkan ambang penerimaan *packet loss*. Jangan mengarang batas lulus. Sajikan `N_tx`, `N_rx_valid`, jumlah gap/duplikat/invalid bila dapat diamati, durasi, laju kirim, kondisi jaringan, serta persentase terukur; minta pembimbing menetapkan kriteria sebelum pengambilan data bila diperlukan.

### 2.3 Kondisi dan pengulangan (usulan, perlu dikonfirmasi)

1. Pisahkan hasil **SITL loopback** `127.0.0.1:6454` dari hasil **ESP32/fixture**. Loopback memvalidasi jalur perangkat lunak–penerima virtual, bukan Wi-Fi atau lampu fisik.
2. Sebagai rancangan awal, ukur setiap kondisi jaringan yang benar-benar akan dipakai (SoftAP ESP32 dan/atau AP gereja yang diizinkan) dalam **3 sesi independen × 5 menit** untuk hitungan paket. Catat jumlah paket pada setiap sesi, bukan hanya rerata gabungan. Jumlah sesi dan durasi ini adalah usulan, bukan fakta atau hasil.
3. Untuk respons optik, sebagai rancangan awal lakukan **30 transisi terkontrol per kondisi** (contoh: blackout ke warna/level yang jelas, lalu transisi berbeda dengan nilai awal dan akhir yang dicatat). Pastikan fixture stabil sebelum pemicu berikutnya. Acak/selang-seling urutan warna bila praktis agar hasil tidak hanya menggambarkan satu transisi. Konfirmasikan jumlah ulangan dengan pembimbing.
4. Rekam konfigurasi dan kondisi: ID sesi, laptop/aplikasi, firmware, mode jaringan, tujuan/IP, Universe, laju transmisi yang diminta, kanal Wi-Fi, RSSI bila tersedia, jarak/posisi, status AP/client isolation, jumlah klien, fixture, cuaca/pencahayaan sekitar jika relevan, alat ukur, operator, serta gangguan dan penyimpangan prosedur.
5. Sebelum tiap sesi, cocokkan nomor urut serta penghitung TX/RX dengan pengiriman singkat terkendali; uji nilai cue yang dapat dibedakan dan tentukan ambang sensor dari baseline. Simpan log mentah, tangkapan jaringan (jika digunakan), log diagnostik firmware, video/rekaman alat, dan CSV dengan ID sesi yang sama. Jangan menghapus percobaan gagal; beri kode alasan dan putuskan perlakuannya sebelum analisis.

### 2.4 Templat CSV pengukuran

Satu baris mewakili satu paket/transisi terpilih dalam suatu sesi; `run_*` berulang pada baris sesi yang sama dan dipakai untuk rekapitulasi jendela. Gabungkan log pengirim dan penerima berdasarkan sesi serta urutan/nomor urut dengan menangani *wraparound*. Timestamp penerima atau sensor boleh kosong jika alat belum mencatatnya. `NA` berarti tidak terukur/tidak berlaku, bukan nol. Jangan mengisi timestamp lintas-jam atau latensi turunannya sebelum sinkronisasinya tervalidasi.

```csv
run_id,trial_id,scenario,transport_mode,showfile,fixture_profile,track_file,stimulus_id,fixture_id,universe,destination_ip,wifi_mode,ap_isolation,wifi_channel,rssi_dbm,tx_index,artnet_sequence,tx_host_monotonic_ns,rx_esp32_us,rx_valid,rx_marker_daq_ns,dmx_marker_daq_ns,light_onset_daq_ns,ui_trigger_video_frame,light_video_frame,camera_fps,light_threshold_method,clock_sync_method,host_esp32_offset_ms,clock_uncertainty_ms,tx_to_rx_ms,rx_to_dmx_ms,rx_to_light_ms,tx_to_light_ms,ui_to_light_ms,run_tx_count,run_rx_unique_count,run_loss_count,run_loss_rate_pct,operator_code,notes
```

`rx_marker_daq_ns`/`dmx_marker_daq_ns` hanya terisi bila marker yang sesuai benar-benar diukur pada pencatat waktu yang sama dengan fotodioda; `ui_to_light_ms` dihitung dari frame kamera pada klip yang sama; `tx_to_light_ms` hanya terisi bila titik TX dan cahaya direkam/sinkron pada basis waktu bersama. Laporkan cara konversi tiap kolom turunan dan pembulatan pada catatan analisis. Header di atas adalah skema usulan dan boleh disesuaikan sebelum uji, tetapi jangan mengubah nama/definisi kolom di tengah pengambilan data tanpa mencatat versi.

## 3. Matriks pengujian fungsional black-box

Laksanakan pada versi aplikasi/firmware yang dicatat; gunakan `zzluxora_v10/markdowns/TEST_PLAN.md` sebagai rujukan tambahan. Setiap uji mencatat langkah aktual, bukti (tangkapan layar/log/video/paket), status, tanggal, versi, dan ID penguji. `Pass` hanya jika seluruh hasil yang diharapkan terpenuhi; `Fail` jika tidak; `N/A` hanya bila alasan dan persetujuannya dicatat. Kolom aktual dan status sengaja kosong.

| ID | Fitur/skenario | Langkah ringkas | Kriteria penerimaan (*expected*) | Hasil aktual | Status (Pass/Fail/N/A) |
|---|---|---|---|---|---|
| FB-01 | Peluncuran aplikasi | Jalankan ZZLUXORA v10 dari kondisi tertutup. | Jendela utama terbuka dan tab/workspace tersedia; tidak ada crash yang menghentikan sesi. | | |
| FB-02 | Muat profil `.zfx` valid | Buka `fixtures/Alien-AL36.zfx` melalui Fixture List/Editor. | Profil Alien AL36 terbaca sebagai 8 kanal dengan label/tipe sesuai definisi berkas. | | |
| FB-03 | Profil `.zfx` tidak valid | Coba muat salinan uji yang sengaja rusak/JSON tidak valid; jangan menimpa profil asli. | Aplikasi menolak atau memberi kesalahan yang dapat dipahami; sesi tetap berjalan dan patch lama tidak berubah tanpa konfirmasi. | | |
| FB-04 | Patch satu fixture | Tambahkan satu Alien AL36 di alamat awal yang tersedia. | Fixture muncul pada alamat yang dipilih; kanal menempati rentang 8 kanal dan tidak mengubah fixture lain. | | |
| FB-05 | Patch cepat GIA 4× | Jalankan preset `[PATCH 4x ALIEN (GIA)]`/muat patch pada showfile GIA. | Empat fixture mulai di DMX 1/17/33/49, masing-masing 8 kanal, tanpa tumpang tindih. | | |
| FB-06 | Undo/redo patch | Ubah satu patch, lakukan Undo lalu Redo. | State kembali tepat ke sebelum/sesudah perubahan; alamat dan jumlah fixture cocok. | | |
| FB-07 | Muat audio valid | Pilih satu berkas WAV yang tercantum pada §5. | Nama/berkas audio tampil sebagai input; aplikasi tidak melaporkan berkas tidak terbaca. | | |
| FB-08 | Audio tidak didukung/rusak | Coba berkas uji rusak atau format yang tidak didukung; pertahankan berkas benchmark. | Aplikasi memberi umpan balik kegagalan dan tidak crash atau mengganti input valid secara diam-diam. | | |
| FB-09 | Analisis audio | Tekan Analyze untuk input valid. | Analisis selesai, progres berakhir, GUI tetap merespons, dan hasil dapat dibuka. | | |
| FB-10 | Validitas tampilan hasil | Periksa metrik, mood/koordinat, dan keluaran warna setelah analisis. | Nilai yang ditampilkan ada, berhingga, dan berada pada rentang yang didefinisikan aplikasi; tidak ada bidang hasil kosong akibat kegagalan diam-diam. Catat nilainya, jangan menilai kesesuaian estetis pada uji teknis ini. | | |
| FB-11 | Analisis ulang deterministik | Analisis ulang berkas dan setelan yang sama. | Hasil deterministik yang seharusnya tetap sama dapat dibandingkan; setiap perbedaan dicatat untuk ditelusuri, bukan diabaikan. | | |
| FB-12 | Ekspor ke Perform | Pilih hasil analisis lalu gunakan `EXPORT TO PERFORM`/buat executor. | Lagu/segmen yang dipilih tersedia di playlist Perform dan cue yang dihasilkan dapat dilihat. | | |
| FB-13 | Muat showfile `.zlx` GIA | Buka `showfiles/gia_deliksari_alien_4x.zlx`. | Project terbuka tanpa kehilangan state; empat fixture dan cue yang tersimpan terlihat. Verifikasi target IP secara terpisah karena berkas saat ini menyimpan `127.0.0.1`. | | |
| FB-14 | Simpan dan muat ulang `.zlx` | Simpan proyek uji ke nama baru, tutup, lalu buka kembali berkas tersebut. | Patch, playlist/cue, nilai fader, Universe, dan state yang memang diserialisasi identik dengan kondisi sebelum tutup. Jangan mengganti showfile asli. | | |
| FB-15 | Perform GO+ | Dengan minimal dua cue berbeda, tekan `[GO+]`. | Cue aktif berpindah sesuai urutan; nilai output mengikuti cue aktif dan antarmuka menunjukkan state yang sama. | | |
| FB-16 | Perform PREV | Setelah maju satu cue, tekan `[PREV]`. | Cue kembali ke cue sebelumnya sesuai urutan yang tampil. | | |
| FB-17 | Crossfade | Atur waktu fade yang tercatat, jalankan GO+ dan observasi beberapa titik selama transisi. | Nilai bergerak dari nilai awal menuju tujuan secara bertahap, mencapai tujuan dalam waktu yang disetel, dan tidak melompat/berkedip di luar toleransi yang telah ditetapkan. Catat waktu dan nilai aktual. | | |
| FB-18 | Page/executor | Buat/gunakan executor dari cue yang tersedia dan aktifkan tombol Page. | Tombol yang dipilih memanggil cue/output yang sesuai; tombol lain tidak terpicu tanpa aksi. | | |
| FB-19 | Mixer kanal DMX | Ubah fader kanal yang telah di-patch dan amati keluaran/monitor. | Hanya kanal yang dipilih berubah sesuai skala fader; kanal fixture yang tidak terkait tidak berubah. | | |
| FB-20 | Grand Master dan reset | Ubah Grand Master, lalu jalankan reset fader yang relevan. | Skala master memengaruhi output sesuai spesifikasi; reset membawa nilai ke kondisi yang ditetapkan dan tercatat. | | |
| FB-21 | Play-gated dan Stop | Amati jaringan/monitor saat Play mati, aktifkan Play lalu Stop. | Tidak ada streaming saat state berhenti sesuai spesifikasi; paket mulai saat Play dan berhenti saat Stop. Gerakan UI saja bukan bukti paket. | | |
| FB-22 | Blackout | Aktifkan Blackout saat output aktif. | Seluruh kanal DMX yang dikendalikan turun ke 0 pada monitor/penerima dan lampu padam. Catat terpisah bukti aplikasi, DMX, dan optik. | | |
| FB-23 | Loopback QLC+ | Hubungkan ke QLC+ SITL `127.0.0.1:6454`, Universe pemetaan sesuai TEST_PLAN, lalu kirim cue. | QLC+ menerima perubahan kanal yang cocok dengan nilai uji; bukti ini hanya untuk SITL, bukan ESP32/lampu. | | |
| FB-24 | ESP32 dan empat fixture | Pada instalasi lapangan yang aman, kirim cue warna/dimmer yang diketahui dan inspeksi masing-masing fixture. | Penerimaan ESP32, frame DMX, dan respons optik setiap fixture diverifikasi terpisah; alamat/kanal sesuai patch dan tidak ada fixture yang hanya diasumsikan menyala karena aplikasi menunjukkan output. | | |

Rekap pass rate mengikuti Bab 3 §3.9.1.b: `jumlah test case Pass / jumlah test case yang dieksekusi × 100%`. Laporkan jumlah `N/A` dan alasannya terpisah serta tetapkan penyebut sebelum menyimpulkan persentase. Jangan mengisi hasil aktual/status dari ekspektasi di tabel.

## 4. Pilot kuesioner dan reliabilitas Cronbach

Pilot dilakukan **sebelum** pengumpulan data utama 25 responden agar masalah instruksi, pemahaman butir, prosedur demonstrasi, dan reliabilitas diketahui lebih awal. Pilot bukan tempat membuat atau mengasumsikan skor; seluruh nilai harus berasal dari formulir yang benar-benar diisi.

**Usulan keputusan desain untuk persetujuan pembimbing:** rekrut **10–15 orang pilot** yang menyerupai populasi yang akhirnya dipilih. Rentang ini hanya usulan operasional, bukan ketentuan metodologis yang sudah disahkan dan bukan jaminan estimasi α stabil pada sampel kecil. Disarankan pilot terpisah dan tidak dihitung ke dalam 25 responden utama, khususnya bila butir/prosedur direvisi. Pembimbing harus menyetujui jumlah, kesesuaian peserta, dan apakah ada keadaan khusus yang membolehkan data pilot dipakai kembali.

Prosedur pilot:

1. Kunci versi sementara kuesioner, instruksi lisan/tertulis, urutan demo lagu/cue, durasi, skala respons, kode responden anonim, dan definisi kelompok peserta. Minta tinjauan validitas isi sebagaimana Bab 3 §3.8.
2. Jalankan sesi dengan kondisi yang sama antarpeserta: jelaskan hak partisipasi, demonstrasikan sistem dengan naskah instruksi yang seragam, beri kesempatan menjawab sendiri, dan catat pertanyaan/kebingungan tanpa mengarahkan jawaban. Beri instrumen kesesuaian hanya setelah lagu dan pencahayaan yang dinilai benar-benar diamati. SUS diberikan kepada orang yang benar-benar menggunakan aplikasi sesuai tujuan instrumen; penonton yang hanya melihat lampu tidak boleh diminta menilai pengalaman pengoperasian aplikasi.
3. Periksa kelengkapan data, pola respons, waktu pengisian, butir yang disalahpahami, efek plafon/lantai, dan korelasi butir-total terkoreksi. Hitung α **secara terpisah** untuk SUS dan skala kesesuaian; jangan mencampur konstruk berbeda. Untuk butir SUS negatif, balik kode respons (skala 1–5 menjadi `6 − respons`) sebelum analisis konsistensi internal. Jika setiap lagu memiliki enam penilaian, tetapkan sebelumnya apakah analisis α dilakukan per lagu atau untuk respons yang digabung dengan mempertimbangkan struktur berulang; jangan memperlakukan penilaian lagu berulang dari orang yang sama sebagai responden independen.
4. Bandingkan α dengan kriteria Bab 3 §3.8 (α ≥ 0,6) sebagai kriteria rancangan penelitian ini. Laporkan jumlah peserta dan butir, penanganan data hilang, α, korelasi butir-total terkoreksi, serta α jika butir dihapus. Ukuran pilot kecil membuat estimasi awal tidak presisi; laporkan sebagai evaluasi awal, bukan bukti reliabilitas universal.
5. Bila α < 0,6 atau ada butir bermasalah, telusuri redaksi ganda/ambigu, kesesuaian konstruk, urutan, skala, dan prosedur. Revisi hanya dengan alasan substantif dan tinjauan pembimbing/ahli; jangan menghapus butir semata-mata untuk menaikkan α. Bila perubahan substantif dilakukan, jalankan pilot ulang pada versi terkunci yang baru bila disetujui. Simpan versi instrumen dan jejak perubahan; jangan mengganti butir di tengah pengumpulan data utama.
6. Setelah versi final disetujui, pisahkan data pilot dari dataset utama atau tandai secara eksplisit sesuai keputusan etik/pembimbing. Analisis instrumen final pada data utama juga dilaporkan sesuai rencana, dengan keterbatasan ukuran sampel dinyatakan.

**Lembar keputusan pilot sebelum pelaksanaan:** ukuran pilot disetujui: ________; tanggal/persetujuan: ________; pilot dihitung sebagai bagian dari 25 responden: ya/tidak (lingkari setelah disetujui); populasi/role peserta pilot: ________; versi instrumen: ________.

## 5. Rekrutmen responden dan pemilihan lagu

### 5.1 Rekrutmen 25 responden

Bab 3 §3.3 dan lembar *informed consent* saat ini berfokus pada jemaat/*Youth* GIA Deliksari, usia 17–45 tahun, partisipasi sukarela, serta kesediaan mempelajari/mengoperasikan sistem. Sebelum mengundang peserta, putuskan apakah populasi sasaran adalah (A) jemaat sebagai penilai kesesuaian pencahayaan, (B) operator lighting sebagai pengguna/usability, atau (C) dua kelompok yang dianalisis terpisah. Jangan menyamakan jemaat penonton dengan operator hanya karena keduanya berada di gereja.

Kuesioner SUS menilai pengalaman memakai aplikasi; responden SUS harus benar-benar mengoperasikan aplikasi dengan skenario dan pengarahan yang konsisten. Skala kesesuaian pencahayaan dapat dijawab oleh orang yang menyaksikan lagu serta cahaya yang bersangkutan. Bila sampel 25 mencakup kedua peran, tetapkan kriteria, kuota, dan analisis per kelompok lebih dahulu; jangan menggabungkan skor SUS dari bukan-pengguna atau menggabungkan strata tanpa alasan. Keputusan populasi/kuota menunggu pembimbing.

Kriteria awal yang diturunkan dari Bab 3, untuk disahkan sebelum rekrutmen:

- Jemaat aktif GIA Deliksari bila kelompok jemaat dipilih; identifikasi role sebagai jemaat/*Youth*/operator secara terpisah.
- Usia sesuai protokol etik yang disetujui. Bab 3 menulis 17–45 tahun; **usulan kehati-hatian** adalah merekrut usia ≥18 tahun kecuali pelibatan peserta usia 17 telah memperoleh izin etik dan persetujuan orang tua/wali sesuai ketentuan institusi.
- Bersedia berpartisipasi secara sukarela dan menandatangani lembar persetujuan setelah menerima penjelasan; penolakan/pengunduran diri tidak berdampak pada layanan atau keanggotaan gereja.
- Untuk penilaian SUS: bersedia mengikuti tugas pengoperasian yang sama, dengan tingkat pengalaman lighting dicatat; untuk penilaian visual: bersedia menyaksikan sesi lagu/cahaya.
- Rekrut purposif tanpa tekanan dari pemimpin/pengurus; cegah nama/identitas masuk ke dataset analisis, gunakan kode peserta.

Gunakan surat izin lokasi dan formulir sesuai kebijakan UNNES/pengurus gereja. Lembar persetujuan di berkas saat ini menyebut jemaat/Youth dan usia 17–45; sesuaikan hanya setelah persetujuan pembimbing/etik, termasuk perlindungan peserta di bawah umur. Jangan mengisi nama, tanda tangan, usia, atau data responden contoh pada protokol ini.

### 5.2 Berkas audio yang tersedia dan prosedur pemilihan

Daftar nama aktual di `zzluxora_v10/data/audio/`:

1. `Franky_Sihombing_-_Kuberikan_Hatiku.wav`
2. `GMS_Live_-_Kemenangan_Terjadi_Di_Sini.wav`
3. `GMS_Live_-_Nyalakan_ApiMu.wav`
4. `JPCC_Worship_-_Sampai_Akhir_Hidupku.wav`
5. `JPCC_Worship_-_Tuhan_Raja_Maha_Besar.wav`
6. `NDC_Worship_-_Bapa_Yang_Kekal.wav`
7. `NDC_Worship_-_Waktu_Tuhan.wav`
8. `Symphony_Worship_-_Dengan_SayapMu.wav`
9. `Symphony_Worship_-_Kubahagia.wav`
10. `Symphony_Worship_-_Kumenang.wav`

Nama penyanyi/lagu di atas adalah nama berkas yang tersedia, bukan klasifikasi mood atau bukti karakter musiknya. Dengarkan dan lakukan analisis awal seluruh kandidat; catat durasi/format, BPM dan/atau segmen yang benar-benar terukur, bagian yang dipakai, serta alasan inklusi. Pilih **3–5 lagu** sesuai rancangan kuesioner yang ada, dengan variasi karakter yang diverifikasi dari materi aktual dan relevan dengan ibadah. Jangan menyebut lagu “Praise”, “Worship”, cepat/lambat, atau mewakili mood tertentu hanya berdasarkan nama berkas. Minta persetujuan pembimbing atas jumlah dan judul final; gunakan nama berkas yang sama pada form, log, dan hasil.

| Kandidat berkas (nama persis) | Durasi/segmen yang dipakai (isi setelah verifikasi) | Hasil analisis awal yang relevan | Keputusan inklusi dan alasan |
|---|---|---|---|
| `Franky_Sihombing_-_Kuberikan_Hatiku.wav` | | | |
| `GMS_Live_-_Kemenangan_Terjadi_Di_Sini.wav` | | | |
| `GMS_Live_-_Nyalakan_ApiMu.wav` | | | |
| `JPCC_Worship_-_Sampai_Akhir_Hidupku.wav` | | | |
| `JPCC_Worship_-_Tuhan_Raja_Maha_Besar.wav` | | | |
| `NDC_Worship_-_Bapa_Yang_Kekal.wav` | | | |
| `NDC_Worship_-_Waktu_Tuhan.wav` | | | |
| `Symphony_Worship_-_Dengan_SayapMu.wav` | | | |
| `Symphony_Worship_-_Kubahagia.wav` | | | |
| `Symphony_Worship_-_Kumenang.wav` | | | |

## 6. Persiapan dan pelaksanaan lapangan di GIA Deliksari

Checklist ini adalah prosedur usulan, bukan konfirmasi bahwa seluruh perangkat/perlengkapan telah tersedia atau lolos uji. Isi kondisi dan hasil aktual saat *site survey* dan sesi lapangan.

| Item | Pemeriksaan/prosedur sebelum menyalakan sistem | Kondisi/hasil aktual | Status / bukti |
|---|---|---|---|
| Izin dan keselamatan | Izin tertulis pengurus; waktu/lokasi; kabel aman dari jalur jemaat; area lampu/strobe dan tingkat kecerahan dinilai; petugas bertanggung jawab dan prosedur penghentian jelas. | | |
| Laptop dan aplikasi | Laptop, catu daya/adaptor, aplikasi dan versinya, driver/jaringan, file audio lokal, ruang penyimpanan log, jam sistem; matikan notifikasi/pembaruan yang mengganggu dan cegah sleep selama sesi. | | |
| Firmware/node | ESP32 DevKit V1 dengan firmware yang versinya/hashes dicatat; catu daya stabil; indikator LCD 16×2 menampilkan status yang dapat dibaca; uji reboot dan status Wi-Fi sebelum disambungkan ke lampu. | | |
| MAX485 dan konektor | Periksa modul MAX485, sambungan ESP32 (TX GPIO 17, RX GPIO 16, DE/RE GPIO 4 sesuai firmware), polaritas/jalur diferensial, catu dan ground; cocokkan pin XLR aktual dengan dokumentasi perangkat. Jangan mengasumsikan label A/B selalu konsisten antarperangkat. | | |
| Empat fixture | Identifikasi fisik keempat unit Alien AL36, mode operasi dan jumlah kanal melalui menu/manual pada masing-masing unit; cocokkan mode itu dengan `Alien-AL36.zfx`. Profil yang tersedia adalah 8CH RGB dengan kanal 5 dan 8 kosong, bukan profil dengan kanal putih khusus; pastikan klaim RGB/RGBW sesuai mode fisik sebenarnya. | | |
| Kabel DMX/XLR | Gunakan kabel DMX/XLR 3-pin yang layak; sambungkan daisy-chain dari node ke fixture 1–4 dengan polaritas benar; catat urutan unit dan panjang kabel. | | |
| Terminasi DMX 120 Ω | Verifikasi ada satu terminator nominal 120 Ω pada ujung fisik rantai DMX (fixture terakhir) sesuai topologi; pastikan tidak ada terminasi ganda bila fixture terakhir telah memiliki terminator internal/saklar. Keberadaan dan cara pasang perangkat terminasi belum diverifikasi di lokasi. | | |
| Patch dan Universe | Buka `gia_deliksari_alien_4x.zlx`; verifikasi empat fixture masing-masing 8 kanal pada alamat awal 1/17/33/49 dan Universe 0. Periksa urutan fisik lampu terhadap nomor fixture di aplikasi sebelum memainkan cue. | | |
| Tujuan showfile | Berkas GIA saat ini menyimpan `target_ip` `127.0.0.1`. Setelah membuka showfile, ubah/pilih tujuan Art-Net untuk node aktual (contoh SoftAP `192.168.4.1`) dan port 6454; verifikasi alamat/Universe di UI dan penerima sebelum GO+. Jangan berasumsi nilai loopback akan mengarah ke ESP32. | | |
| Wi-Fi / SoftAP | Catat SSID aktual, mode (SoftAP langsung atau AP gereja), alamat laptop dan node, kanal, jarak/RSSI bila tersedia, jumlah klien, serta gangguan radio. Jangan tulis kata sandi Wi-Fi di CSV/laporan; simpan hanya pada catatan akses terbatas bila diperlukan. | | |
| AP isolation dan broadcast | Pastikan laptop dan node berada pada jaringan yang dapat saling berkomunikasi; periksa client/AP isolation, firewall laptop, subnet, rute, dan aturan broadcast/multicast UDP 6454. Uji penerimaan dengan counter/diagnostik penerima. Jika isolasi AP tidak dapat dimatikan, catat kondisi dan uji unicast/direct SoftAP yang disetujui; jangan menafsirkan tidak adanya broadcast sebagai bukti kerusakan lampu. | | |
| Uji kanal optik | Pada kondisi aman dan tanpa responden, kirim nilai uji rendah/terkendali untuk dimmer dan R/G/B ke setiap fixture satu per satu; catat fixture, alamat, nilai target, tampilan node/DMX, serta observasi cahaya. Verifikasi blackout dan pemulihan. Hindari strobe untuk sesi responden kecuali risiko, kebutuhan, dan persetujuannya sudah dinilai. | | |
| Data dan pencatatan | Siapkan salinan showfile uji (jangan menimpa asli), versi firmware/aplikasi, alat ukur, CSV kosong, pencatat kejadian dan backup lokal; samakan `run_id` pada semua log. | | |
| Responden dan dokumen | Formulir persetujuan versi final, izin lokasi, kuesioner versi final, daftar kode anonim, instruksi sesi, alat tulis, tempat pengisian yang nyaman, prosedur pengembalian/penyimpanan formulir terkunci. Pisahkan lembar nama/tanda tangan dari data jawaban. | | |
| Penutupan sesi | Hentikan output/Blackout, verifikasi DMX aman, matikan node/lampu sesuai prosedur, kumpulkan formulir, salin dan periksa kelengkapan log tanpa membuka identitas, catat penyimpangan/insiden, dan pulihkan pengaturan jaringan/lokasi. | | |

### 6.1 Urutan sesi lapangan yang disarankan

1. Lakukan *site survey* tanpa responden; pastikan izin, pasokan listrik, kabel, posisi fixture, keamanan, jalur kabel, Wi-Fi, pencatatan, dan terminasi. Konfirmasi dulu perangkat fisik tidak lagi dipinjam.
2. Catat versi perangkat lunak/firmware serta kondisi awal. Boot node, periksa LCD/status dan Wi-Fi; sambungkan laptop ke mode jaringan yang disetujui. Catat IP/rute dan status isolasi/broadcast.
3. Buka showfile GIA, verifikasi patch 1/17/33/49, tipe kanal, Universe 0, dan ubah target dari loopback ke alamat ESP32 yang benar. Lakukan uji penerimaan paket dan keluaran DMX diagnostik sebelum menilai lampu.
4. Jalankan uji black-box dan ukur latency/packet loss tanpa responden terlebih dahulu. Validasi sensor optik/threshold atau kamera, pencatatan clock, sinkronisasi, nomor urut, dan backup berkas. Jika instrumentasi tidak memadai, tandai metrik yang tidak dapat diukur dan hentikan klaim terkait.
5. Setelah formulir, populasi, daftar lagu, alur demonstrasi, dan persetujuan final, minta persetujuan sukarela sebelum sesi. Jalankan instruksi yang sama untuk semua peserta; catat kode anonim, role yang disetujui, dan lagu/segmen yang benar-benar disaksikan.
6. Berikan kuesioner yang sesuai dengan peran dan paparan aktual; jangan minta responden menebak pengalaman operator atau menilai lagu yang tidak disaksikan. Periksa halaman kosong sebelum peserta meninggalkan sesi tanpa mengarahkan jawaban.
7. Tutup dengan blackout, matikan sistem aman, amankan formulir dan berkas, serta dokumentasikan gangguan, kondisi jaringan, percobaan terulang, dan alasan eksklusi.

## 7. Lembar catatan keputusan dan hasil aktual

### 7.1 Keputusan yang belum disahkan

| Keputusan | Pilihan/protokol yang akan dipakai | Persetujuan pembimbing / tanggal |
|---|---|---|
| Definisi utama H₃: TX→cahaya, UI→cahaya, atau ukuran lain; statistik utama untuk ambang 100 ms | | |
| Alat/marker dan sinkronisasi jam; batas ketidakpastian yang dapat diterima | | |
| Cara penghitung penerimaan/kehilangan paket pada firmware; ambang packet loss bila akan dipakai | | |
| Jumlah ulangan dan kondisi jaringan; perlakuan paket hilang/percobaan gagal | | |
| Populasi 25 orang, peran jemaat vs operator, strata/kuota, persyaratan peserta usia 17 tahun | | |
| Pilot: jumlah, pemisahan dari 25 responden, aturan uji ulang instrumen | | |
| Lagu final 3–5 berkas, bagian lagu, dan dasar klasifikasi/variasi | | |
| Ketersediaan perangkat, mode kanal Alien AL36, terminator 120 Ω, SSID/rute/isolation/broadcast | | |
| Penyesuaian target IP showfile dari `127.0.0.1` ke node lapangan | | |

### 7.2 Ringkasan pengujian (diisi setelah pelaksanaan)

| Sesi/tanggal | Versi aplikasi/firmware | Lokasi dan kondisi jaringan | Ulangan valid/tidak valid | Bukti/log yang tersimpan | Hasil aktual dan penyimpangan |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

**Larangan pengisian sebelum data terkumpul:** jangan mengisi placeholder dengan angka perkiraan, hasil simulasi sebagai hasil lapangan, status Pass berdasarkan spesifikasi, ataupun skor Cronbach/latency/packet loss yang belum dihitung dari data mentah. Kaitkan setiap kesimpulan Bab 4 dengan berkas sumber dan prosedur yang benar-benar dijalankan.
