# BAB 1 PENDAHULUAN

## 1.1 Latar Belakang

Pencahayaan (*lighting design*) merupakan salah satu elemen krusial dalam penyelenggaraan ibadah di gereja modern. Lebih dari sekadar penerangan, pencahayaan berfungsi sebagai sarana untuk membangun atmosfer yang mendukung kekhusyukan jemaat selama beribadah [10]. Perpaduan antara pencahayaan yang tepat dengan musik pujian (*praise*) dan penyembahan (*worship*) mampu menciptakan pengalaman ibadah yang lebih mendalam dan bermakna. Dalam konteks ini, pencahayaan bukan hanya aspek teknis semata, melainkan merupakan bagian dari pelayanan rohani yang menunjang kegiatan ibadah secara holistik.

Pada gereja-gereja besar, pengelolaan pencahayaan umumnya ditangani oleh tim teknis profesional dengan peralatan *lighting console* berfitur otomasi lengkap. Namun, pada gereja-gereja kecil dan menengah dengan sumber daya terbatas, pengelolaan pencahayaan sering kali dilakukan secara manual oleh satu atau dua operator yang merangkap pelayanan lain [13]. Proses pembuatan *scene* pencahayaan yang sesuai dengan karakter setiap lagu rohani membutuhkan waktu, keterampilan teknis, dan pemahaman estetika yang tidak mudah diperoleh. Operator harus menyusun *scene* satu per satu secara manual, menyesuaikan nilai RGBW (*Red, Green, Blue, White*) pada setiap kanal, dan mengoperasikannya secara *live* selama ibadah berlangsung. Tantangan ini semakin besar ketika daftar lagu berubah mendadak atau ketika operator yang bertugas berganti, karena tidak ada sistem yang terstandarisasi dan mudah dioperasikan oleh pengguna awam.

Beberapa penelitian menunjukkan adanya korelasi antara karakteristik audio suatu lagu — seperti tempo, frekuensi dominan, energi, dan dinamika — dengan persepsi warna pada pendengar [7][8]. Penelitian Palmer *et al.* (2013) membuktikan bahwa asosiasi warna terhadap musik dimediasi oleh emosi secara lintas-budaya, di mana musik bertempo cepat dan bermodus mayor diasosiasikan dengan warna-warna cerah, tersaturasi, dan hangat, sedangkan musik bertempo lambat dan bermodus minor diasosiasikan dengan warna-warna gelap, desaturasi, dan dingin [24]. Lindborg (2021) memperkuat temuan ini dengan menunjukkan bahwa asosiasi warna terhadap musik dimediasi oleh emosi, sehingga fitur-fitur audio tertentu cenderung diasosiasikan dengan warna-warna spesifik secara sistematis [10]. Model *Circumplex of Affect* yang dikemukakan oleh Russell (1980) menyediakan kerangka dua dimensi — *valence* (valensi emosi) dan *arousal* (tingkat intensitas) — yang dapat digunakan sebagai basis pemetaan fitur audio ke ruang warna [23]. Temuan-temuan ini memberikan landasan ilmiah bahwa pemetaan fitur audio ke parameter pencahayaan dapat dilakukan secara *rule-based* dengan dasar referensi yang kuat.

Dari sisi teknologi, protokol *Art-Net* merupakan standar komunikasi yang banyak digunakan dalam industri *entertainment lighting* untuk mentransmisikan data DMX512 melalui jaringan *Ethernet*/IP [16]. Standar DMX512 sendiri telah menjadi fondasi komunikasi pengendalian pencahayaan panggung sejak ditetapkan oleh ANSI/ESTA [17]. Dengan hadirnya perangkat lunak *open-source* seperti QLC+ serta mikrokontroler berbasis WiFi seperti ESP32, implementasi sistem pencahayaan berbasis *Art-Net* menjadi lebih terjangkau dan dapat diakses oleh gereja-gereja dengan anggaran terbatas [14][22]. Kombinasi teknologi ini memungkinkan pengembangan sistem yang mampu menerima data *Art-Net* melalui jaringan nirkabel dan mengendalikan lampu PAR LED RGBW secara langsung melalui konverter RS-485 (MAX485).

Meskipun teknologi pendukung telah tersedia, saat ini belum banyak penelitian maupun aplikasi yang secara khusus mengintegrasikan analisis fitur audio lagu rohani dengan sistem otomasi pencahayaan berbasis *Art-Net*. Solusi komersial yang ada di pasaran — seperti *SoundSwitch*, *Lightjams*, atau *Madrix* — umumnya bersifat generik, tidak mempertimbangkan karakteristik khusus musik rohani (seperti perbedaan dinamika *praise* dan *worship*), serta memiliki biaya lisensi yang relatif tinggi untuk skala gereja kecil. Selain itu, pendekatan yang ada sering kali menggunakan *machine learning* yang kompleks dan sulit diimplementasikan pada perangkat keras terbatas [1][3]. Oleh karena itu, dibutuhkan pendekatan *rule-based* yang lebih sederhana, transparan, dan mudah diuji secara ilmiah untuk memetakan fitur audio ke parameter pencahayaan RGBW.

Berdasarkan permasalahan tersebut, penelitian ini mengusulkan perancangan dan implementasi sebuah sistem *audio-reactive lighting design* bernama **ZZLUXORA** yang menerima *input* berupa *file* audio lagu rohani (.mp3/.wav), melakukan diskritisasi dan transformasi sinyal melalui *Short-Time Fourier Transform* (STFT) berbasis algoritma *Fast Fourier Transform* (FFT) dengan fungsi *Hann window*, mengekstraksi fitur-fitur akustik spektral menggunakan teknik *Digital Signal Processing* (DSP), memetakan fitur-fitur tersebut ke parameter pencahayaan RGBW melalui model matematis afektif dua dimensi *Valence-Arousal* (Russell) dan transformasi ruang warna HSV, serta menghasilkan *scene* dan *chase* pencahayaan secara otomatis. Data pencahayaan tersebut kemudian dikemas dalam paket biner *ArtDmx* dan ditransmisikan melalui protokol jaringan *Art-Net* 4 (UDP Port 6454) ke perangkat lunak QLC+ maupun langsung ke modul penerima nirkabel berbasis mikrokontroler ESP32 DevKit V1 dan *transceiver* RS-485 (MAX485) untuk mengendalikan lampu panggung PAR LED RGBW secara *real-time*. Sistem ini dirancang khusus untuk penggunaan di lingkungan ibadah gereja dengan mengedepankan presisi saintifik sekaligus kemudahan pengoperasian bagi pengguna awam.

## 1.2 Batasan Masalah

Agar penelitian ini dapat berjalan secara terarah dan hasil yang diperoleh sesuai dengan tujuan yang ditetapkan, maka perlu adanya batasan-batasan masalah sebagai berikut:

1. Sumber *input* berupa *file* audio dalam format .mp3 atau .wav, khusus lagu rohani (*praise* dan *worship*) yang diunduh dari YouTube.
2. Analisis audio menggunakan pendekatan *rule-based audio feature mapping*, bukan *machine learning* atau *deep learning* yang memerlukan proses *training* model.
3. Fitur audio yang diekstraksi meliputi tempo/BPM, *RMS energy*, *spectral centroid*, MFCC, *chroma features*, *onset detection*, dan *beat tracking* menggunakan *library* librosa.
4. Deteksi perubahan dinamika lagu menggunakan *beat tracking* dan *onset detection* untuk menentukan titik pergantian *scene* pencahayaan.
5. Pemetaan warna menggunakan model matematis berbasis HSV (*Hue, Saturation, Value*) yang kemudian dikonversi ke RGBW (*Red, Green, Blue, White*) dengan ekstraksi kanal *white*.
6. *Output* berupa data DRGBW (*Dimmer, Red, Green, Blue, White*) dengan rentang nilai 0–255 per kanal untuk setiap *scene* dan *chase*.
7. Transmisi data pencahayaan menggunakan protokol *Art-Net* melalui *virtual adapter* (ke QLC+) atau langsung melalui WiFi/*hotspot* (ke modul ESP32).
8. Perangkat keras modul *ARTNET-DMX* terdiri dari mikrokontroler ESP32 DevKit V1, modul MAX485/RS-485, LCD 16×2 I2C, konektor XLR *male/female*, dan catu daya 5V.
9. *Fixture* yang digunakan untuk pengujian adalah 4 unit lampu PAR LED RGBW dengan konfigurasi 8 kanal: ch1-*dimmer*, ch2-*red*, ch3-*green*, ch4-*blue*, ch5-*empty*, ch6-*program*, ch7-*speed*, ch8-*empty*. Namun, perangkat lunak mendukung konfigurasi *fixture* yang dapat disesuaikan secara manual untuk jumlah lampu yang lebih banyak.
10. Pengujian lapangan dilakukan di Gereja GIA Deliksari, Semarang.
11. Responden pengujian berjumlah 25 orang yang terdiri dari anggota *Youth* dan jemaat Gereja GIA Deliksari.

## 1.3 Rumusan Masalah

Berdasarkan latar belakang dan batasan masalah yang telah diuraikan, maka rumusan masalah dalam penelitian ini adalah sebagai berikut:

1. Bagaimana merancang dan membangun sistem *audio-reactive lighting design* yang mampu mentransformasikan sinyal audio lagu rohani ke domain frekuensi menggunakan *Short-Time Fourier Transform* (STFT) berbasis algoritma *Fast Fourier Transform* (FFT) dan mengekstraksi fitur spektral untuk dipetakan ke parameter pencahayaan RGBW secara otomatis melalui model matematis HSV-RGBW?
2. Bagaimana mengintegrasikan *output* pencahayaan dari aplikasi ZZLUXORA ke perangkat lampu PAR LED RGBW melalui protokol *Art-Net* DMX512 menggunakan modul mikrokontroler ESP32 dan jaringan nirkabel secara *real-time*?
3. Bagaimana kinerja sistem yang dibangun ditinjau dari aspek teknis (*end-to-end latency*, *packet loss rate*, fungsionalitas *black-box testing*), kesesuaian pencahayaan berdasarkan persepsi pengguna, dan *usability* sistem?

## 1.4 Tujuan Penelitian

Berdasarkan rumusan masalah di atas, tujuan dari penelitian ini adalah sebagai berikut:

1. Merancang dan mengimplementasikan aplikasi ZZLUXORA yang mampu memproses sinyal audio melalui STFT berbasis FFT, mengekstraksi fitur akustik spektral (RMS, *spectral centroid*, *chroma*, MFCC), dan menghasilkan *scene* serta *chase* pencahayaan RGBW secara otomatis menggunakan pemetaan matematis berbasis model emosi *Valence-Arousal* dan ruang warna HSV.
2. Mengintegrasikan aplikasi dengan protokol *Art-Net* 4 DMX512 untuk pengendalian lampu panggung PAR LED RGBW melalui modul *hardware* ESP32 dan jaringan nirkabel.
3. Menguji dan mengevaluasi kinerja sistem berdasarkan parameter teknis (*end-to-end latency*, *packet loss rate*, *black-box testing*), kesesuaian pencahayaan berdasarkan persepsi pengguna, dan *usability* sistem menggunakan *System Usability Scale* (SUS).

## 1.5 Manfaat Penelitian

Penelitian ini diharapkan dapat memberikan manfaat baik secara teoretis maupun praktis, sebagai berikut:

### 1.5.1 Manfaat Teoretis

1. Memberikan kontribusi keilmuan di bidang teknik komputer, khususnya pada kajian *Digital Signal Processing* (DSP) dan *Music Information Retrieval* (MIR) yang diaplikasikan pada sistem pengendalian pencahayaan.
2. Menyediakan model pemetaan matematis (*rule-based*) dari fitur audio ke ruang warna HSV-RGBW yang dapat dijadikan referensi untuk penelitian serupa di masa depan.
3. Memperkaya literatur mengenai integrasi protokol *Art-Net* DMX512 dengan mikrokontroler ESP32 untuk pengendalian lampu PAR LED RGBW secara nirkabel.

### 1.5.2 Manfaat Praktis

1. **Bagi Gereja:** Menyediakan sistem pencahayaan otomatis yang mudah dioperasikan oleh pengguna awam, sehingga gereja-gereja kecil dapat memiliki pencahayaan ibadah yang sesuai dengan karakteristik lagu rohani tanpa memerlukan operator profesional.
2. **Bagi *Lighting Designer*:** Menjadi alat bantu untuk mempercepat proses pembuatan *scene* dan *chase* pencahayaan, terutama untuk lagu *praise* yang membutuhkan pergantian *chase* secara cepat dan lagu *worship* dengan *fade* yang halus.
3. **Bagi Pengembang:** Menyediakan arsitektur sistem *open* yang dapat dikembangkan lebih lanjut, baik dari sisi algoritma pemetaan fitur audio maupun dukungan protokol pencahayaan lainnya.

## 1.6 Kebaruan Penelitian

Berdasarkan kajian literatur yang telah dilakukan, kebaruan (*novelty*) dari penelitian ini dibandingkan dengan penelitian-penelitian sebelumnya terletak pada beberapa aspek berikut:

1. **Pendekatan *Rule-Based* yang Transparan:** Berbeda dengan penelitian terdahulu yang banyak menggunakan *machine learning* atau *deep learning* untuk klasifikasi emosi musik [1][7][8], penelitian ini menggunakan pendekatan *rule-based audio feature mapping* yang lebih transparan, mudah diuji, dan mudah diimplementasikan pada perangkat keras terbatas. Setiap aturan pemetaan didokumentasikan secara eksplisit dalam tabel mapping yang dapat diverifikasi.
2. **Pemetaan Matematis HSV-RGBW Berbasis Fitur Audio:** Penelitian ini merancang model pemetaan matematis yang menghubungkan fitur audio melalui perhitungan *Valence* dan *Arousal* ke ruang warna HSV, kemudian mengonversinya ke RGBW dengan ekstraksi kanal *white*. Dasar pemetaan merujuk pada penelitian Palmer *et al.* (2013) [24] dan Lindborg (2021) [10] mengenai korelasi musik-warna yang dimediasi oleh emosi.
3. **Konteks Spesifik Lagu Rohani:** Sebagian besar penelitian *audio-reactive lighting* berfokus pada musik generik atau *Electronic Dance Music* (EDM). Penelitian ini secara khusus menargetkan lagu rohani (*praise* dan *worship*) yang memiliki karakteristik dinamika yang berbeda.
4. **Integrasi *End-to-End* dari Analisis Audio hingga Lampu Fisik:** Sistem yang dibangun mencakup seluruh *pipeline* dari *input* audio hingga pengendalian lampu PAR LED RGBW fisik melalui protokol *Art-Net* DMX512, termasuk modul *hardware* ESP32 yang dikembangkan secara mandiri.
5. **Desain untuk Pengguna Awam:** Sistem dirancang dengan antarmuka yang mudah digunakan (*easy-to-use*) sehingga dapat dioperasikan oleh jemaat gereja tanpa latar belakang teknis, menjamin keberlanjutan penggunaan bahkan setelah peneliti tidak lagi berada di lokasi.
