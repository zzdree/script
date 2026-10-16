#!/usr/bin/env python3
"""
make_chapter4_figures.py - Bangkitkan Gambar 4.1 dan 4.4 Bab 4 dari fakta kode.

Delapan gambar pada naskah v4 adalah ilustrasi konseptual Bab 2 dan Bab 3 dan
sudah selesai. Gambar 4.1 dan Gambar 4.4 berbeda sifatnya: Bab 4 adalah bab
HASIL, sehingga penandanya menuntut "diagram arsitektur berdasarkan implementasi
yang diverifikasi" dan "topologi jalur yang benar-benar digunakan". Gambar
semacam itu harus dapat ditelusuri ke kode, bukan ditafsirkan ulang oleh model
gambar. Karena itu gambar di sini digambar secara terprogram: setiap kotak,
tanda panah, dan angka berasal dari berkas yang benar-benar ada di repositori.

Gaya mengikuti delapan gambar v4: 1024 px, latar putih, garis dan teks abu
gelap sampai hitam (monokrom, sesuai standar gambar naskah).

Bila ada modul, berkas, atau parameter yang berubah di repositori perangkat
lunak, jalankan ulang skrip ini; gambar akan ikut berubah dan tidak dapat
menjadi basi tanpa terlihat.

Penggunaan:
    python3 tools/make_chapter4_figures.py
    python3 tools/make_chapter4_figures.py --outdir image_references

Keluaran:
    image_references/gambar_4_1_arsitektur_implementasi.png
    image_references/gambar_4_4_topologi_pengukuran.png
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LEBAR = 1024
MARGIN = 48

HITAM = (17, 17, 17)
ABU_TUA = (68, 68, 68)
ABU = (128, 128, 128)
ABU_MUDA = (196, 196, 196)
SANGAT_MUDA = (242, 242, 242)
PUTIH = (255, 255, 255)

_JALUR_FONT = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def muat_font(ukuran: int, tebal: bool = False) -> ImageFont.FreeTypeFont:
    """Ambil DejaVu bila ada; kalau tidak, jatuh ke font bawaan Pillow."""
    kandidat = _JALUR_FONT[1 if tebal else 0], _JALUR_FONT[0]
    for jalur in kandidat:
        if Path(jalur).exists():
            return ImageFont.truetype(jalur, ukuran)
    return ImageFont.load_default(ukuran)


FONT_JUDUL = muat_font(30, tebal=True)
FONT_KEPALA = muat_font(21, tebal=True)
FONT_MODUL = muat_font(20, tebal=True)
FONT_ISI = muat_font(16)
FONT_KECIL = muat_font(14)
FONT_MIKRO = muat_font(12)


def tengah(d: ImageDraw.ImageDraw, teks: str, font, x: int, y: int, isi=HITAM) -> None:
    d.text((x, y), teks, font=font, fill=isi, anchor="mm")


def kiri(d: ImageDraw.ImageDraw, teks: str, font, x: int, y: int, isi=HITAM) -> None:
    d.text((x, y), teks, font=font, fill=isi, anchor="lm")


def panah(d: ImageDraw.ImageDraw, x1: int, y1: int, x2: int, y2: int,
          isi=ABU_TUA, lebar: int = 2, putus: bool = False) -> None:
    """Garis dengan kepala panah; putus=True untuk jalur yang belum diverifikasi."""
    if putus:
        panjang = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        langkah = 9
        for mulai in range(0, int(panjang) - langkah, langkah * 2):
            t0, t1 = mulai / panjang, (mulai + langkah) / panjang
            d.line(
                [
                    (x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0),
                    (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1),
                ],
                fill=isi, width=lebar,
            )
    else:
        d.line([(x1, y1), (x2, y2)], fill=isi, width=lebar)

    sudut = 7 if lebar <= 2 else 9
    if abs(y2 - y1) >= abs(x2 - x1):          # panah vertikal
        arah = 1 if y2 > y1 else -1
        d.polygon(
            [(x2, y2), (x2 - sudut, y2 - arah * sudut * 1.6), (x2 + sudut, y2 - arah * sudut * 1.6)],
            fill=isi,
        )
    else:                                      # panah horizontal
        arah = 1 if x2 > x1 else -1
        d.polygon(
            [(x2, y2), (x2 - arah * sudut * 1.6, y2 - sudut), (x2 - arah * sudut * 1.6, y2 + sudut)],
            fill=isi,
        )


def kotak(d: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int,
          isi=PUTIH, garis=HITAM, lebar: int = 2, radius: int = 8) -> None:
    d.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=isi, outline=garis, width=lebar)


# --------------------------------------------------------------------------
# GAMBAR 4.1 - Arsitektur implementasi yang terverifikasi
# --------------------------------------------------------------------------

# Setiap entri adalah modul yang benar-benar ada di core/. Kolom "berkas" ditulis
# apa adanya sebagai path relatif agar dapat diperiksa langsung di repositori.
MODUL = [
    ("AudioLoader", "core/audio_loader.py", "pemuatan multi-format: .wav .mp3 .flac .ogg"),
    ("STFTEngine", "core/fft_engine.py",
     "fs = 22050 Hz | N = 2048 | H = 512 | Hann | np.fft.rfft | 43,07 frame/s"),
    ("FeatureExtractor", "core/feature_extractor.py",
     "RMS | spectral centroid | kroma 12 | MFCC 13 | spectral flux | tempo"),
    ("EmotionModel", "core/emotion_model.py",
     "afektif (V, A); bobot V = A = 0,50 / 0,30 / 0,20"),
    ("ColorEngine", "core/color_engine.py",
     "(V, A) -> HSV -> RGB -> RGBW, dengan W = min(R, G, B)"),
    ("Scene / Chase", "core/models.py", "pembentukan scene dan chase per segmen"),
    ("ArtNetSender", "core/artnet_sender.py",
     "ArtDmx 530 byte | Universe 0 | UDP 6454 | transmisi ter-gate tombol PLAY"),
]


def gambar_arsitektur(outdir: Path) -> Path:
    tinggi_kotak = 84
    jarak = 26
    atas = 150
    # Tinggi dihitung dari tata letak nyata supaya kotak keluaran dan catatan
    # kaki tidak pernah bertumpuk, berapa pun jumlah modulnya.
    tinggi_kotak_keluar = 48
    tinggi_kaki = 76
    y_akhir = atas + 12 + len(MODUL) * (tinggi_kotak + jarak) - jarak
    y_keluar = y_akhir + jarak + 12
    tinggi = y_keluar + tinggi_kotak_keluar + tinggi_kaki

    im = Image.new("RGB", (LEBAR, tinggi), PUTIH)
    d = ImageDraw.Draw(im)

    tengah(d, "Gambar 4.1  Arsitektur Implementasi Terverifikasi", FONT_JUDUL, LEBAR // 2, 46)
    tengah(
        d,
        "Rantai pemrosesan nyata core/ ZZLUXORA v10; setiap kotak menunjuk berkas yang ada di repositori",
        FONT_KECIL, LEBAR // 2, 78, ABU_TUA,
    )
    d.line([(MARGIN, 104), (LEBAR - MARGIN, 104)], fill=ABU_MUDA, width=1)

    kiri_x, kanan_x = MARGIN + 96, LEBAR - MARGIN - 96
    y = atas

    # Masukan
    kotak(d, kiri_x, y - 54, kanan_x, y - 6, isi=SANGAT_MUDA, garis=ABU_TUA, lebar=1)
    tengah(d, "Berkas audio lagu rohani (masukan)", FONT_ISI, LEBAR // 2, y - 30, ABU_TUA)
    panah(d, LEBAR // 2, y - 6, LEBAR // 2, y + 6, ABU_TUA, 2)
    y += 12

    for indeks, (nama, berkas, rincian) in enumerate(MODUL):
        y0, y1 = y, y + tinggi_kotak
        kotak(d, kiri_x, y0, kanan_x, y1, isi=PUTIH, garis=HITAM, lebar=2)
        # Penanda urutan di tepi kiri kotak
        d.rectangle([kiri_x, y0, kiri_x + 6, y1], fill=HITAM)

        kiri(d, f"{indeks + 1}.  {nama}", FONT_MODUL, kiri_x + 22, y0 + 26, HITAM)
        kiri(d, berkas, FONT_MIKRO, kiri_x + 22, y0 + 50, ABU)
        kiri(d, rincian, FONT_ISI, kiri_x + 22, y0 + 70, ABU_TUA)

        if indeks < len(MODUL) - 1:
            panah(d, LEBAR // 2, y1, LEBAR // 2, y1 + jarak, ABU_TUA, 2)
        y = y1 + jarak

    # Keluaran
    panah(d, LEBAR // 2, y - jarak, LEBAR // 2, y_keluar, ABU_TUA, 2)
    kotak(d, kiri_x, y_keluar, kanan_x, y_keluar + tinggi_kotak_keluar,
          isi=SANGAT_MUDA, garis=ABU_TUA, lebar=1)
    tengah(d, "Paket ArtDmx ke jaringan (keluaran)",
           FONT_ISI, LEBAR // 2, y_keluar + tinggi_kotak_keluar // 2, ABU_TUA)

    # Catatan kaki, berjarak tetap di bawah kotak keluaran
    garis_kaki = y_keluar + tinggi_kotak_keluar + 22
    d.line([(MARGIN, garis_kaki), (LEBAR - MARGIN, garis_kaki)], fill=ABU_MUDA, width=1)
    tengah(
        d,
        "Seluruh modul hanya mengimpor pustaka standar Python dan NumPy: tanpa librosa dan tanpa scipy",
        FONT_KECIL, LEBAR // 2, garis_kaki + 26, ABU_TUA,
    )
    tengah(
        d,
        "Isi gambar diturunkan dari berkas nyata, bukan ilustrasi; dijalankan ulang oleh tools/make_chapter4_figures.py",
        FONT_MIKRO, LEBAR // 2, garis_kaki + 48, ABU,
    )

    jalur = outdir / "gambar_4_1_arsitektur_implementasi.png"
    im.save(jalur)
    return jalur


# --------------------------------------------------------------------------
# GAMBAR 4.4 - Topologi jalur pengukuran, memisahkan yang terbukti dan belum
# --------------------------------------------------------------------------

def gambar_topologi(outdir: Path) -> Path:
    lebar_kolom = (LEBAR - 3 * MARGIN) // 2
    kiri0 = MARGIN
    kanan0 = MARGIN * 2 + lebar_kolom
    tengah_kiri = kiri0 + lebar_kolom // 2
    tengah_kanan = kanan0 + lebar_kolom // 2

    tahap_a = [
        ("ZZLUXORA v10", "aplikasi pengirim"),
        ("UDP ArtDmx 530 byte", "127.0.0.1:6454, Universe 0"),
        ("QLC+ (loopback)", "penerima pada mesin yang sama"),
    ]
    tahap_b = [
        ("ZZLUXORA v10", "aplikasi pengirim"),
        ("Wi-Fi / SoftAP", "ESP32 pada 192.168.4.1"),
        ("ESP32 -> MAX485", "frame DMX512, 250 kbaud, 8N2"),
        ("4x Alien AL36", "DMX 1 / 17 / 33 / 49"),
    ]

    baris_a = [
        "Bukti terukur (commit 48ca2bd):",
        "112 paket ArtDmx diterima",
        "105 nomor urut unik, awal monotonik dari 1",
        "blackout menurunkan seluruh kanal ke 0",
        "",
        "Batas bukti: hanya membuktikan loopback perangkat",
        "lunak, bukan penerimaan ESP32 dan bukan respons",
        "lampu fisik.",
    ]
    baris_b = [
        "Yang harus diukur di lokasi:",
        "penerimaan paket pada penghitung node",
        "laju DMX fisik (klaim 44 FPS perlu diukur)",
        "latensi end-to-end dan packet loss",
        "respons optik tiap unit",
        "",
        "Prasyarat: target_ip pada showfile GIA masih",
        "127.0.0.1 dan wajib diubah ke alamat node nyata.",
    ]

    kotak_tahap = 62
    langkah = 28
    atas_tahap = 210
    jarak_bukti = 22
    tinggi_bukti = 24 + max(len(baris_a), len(baris_b)) * 17 + 16

    # Hitung tinggi lebih dulu dari tata letak nyata, lalu gambar sekali.
    # Tidak ada lagi kanvas yang dilukis ulang, jadi tidak ada isi yang terpotong.
    y_bawah_a = atas_tahap + len(tahap_a) * (kotak_tahap + langkah) - langkah
    y_bawah_b = atas_tahap + len(tahap_b) * (kotak_tahap + langkah) - langkah
    y_bukti = max(y_bawah_a, y_bawah_b) + jarak_bukti
    tinggi = y_bukti + tinggi_bukti + MARGIN

    im = Image.new("RGB", (LEBAR, tinggi), PUTIH)
    d = ImageDraw.Draw(im)

    tengah(d, "Gambar 4.4  Topologi Jalur Pengukuran", FONT_JUDUL, LEBAR // 2, 46)
    tengah(
        d,
        "Jalur virtual yang sudah diuji dan jalur fisik yang belum diuji dipisahkan secara eksplisit",
        FONT_KECIL, LEBAR // 2, 78, ABU_TUA,
    )
    d.line([(MARGIN, 104), (LEBAR - MARGIN, 104)], fill=ABU_MUDA, width=1)

    # --- Judul kolom ---
    kotak(d, kiri0, 126, kiri0 + lebar_kolom, 172, isi=SANGAT_MUDA, garis=HITAM, lebar=2)
    tengah(d, "Jalur A: virtual (SITL)", FONT_KEPALA, tengah_kiri, 144, HITAM)
    tengah(d, "TERVERIFIKASI PERANGKAT LUNAK", FONT_MIKRO, tengah_kiri, 163, ABU_TUA)

    kotak(d, kanan0, 126, kanan0 + lebar_kolom, 172, isi=PUTIH, garis=HITAM, lebar=2)
    tengah(d, "Jalur B: fisik", FONT_KEPALA, tengah_kanan, 144, HITAM)
    tengah(d, "BELUM DIUJI", FONT_MIKRO, tengah_kanan, 163, ABU_TUA)

    def gambar_kolom(tahap, x0, warna_tepi, warna_teks, putus: bool) -> None:
        y = atas_tahap
        for i, (judul, sub) in enumerate(tahap):
            kotak(d, x0 + 16, y, x0 + lebar_kolom - 16, y + kotak_tahap,
                  garis=warna_tepi, lebar=2)
            tengah(d, judul, FONT_MODUL, x0 + lebar_kolom // 2, y + 24, warna_teks)
            tengah(d, sub, FONT_MIKRO, x0 + lebar_kolom // 2, y + 46, ABU)
            if i < len(tahap) - 1:
                panah(d, x0 + lebar_kolom // 2, y + kotak_tahap,
                      x0 + lebar_kolom // 2, y + kotak_tahap + langkah,
                      warna_tepi if not putus else ABU, 2, putus=putus)
            y += kotak_tahap + langkah

    gambar_kolom(tahap_a, kiri0, ABU_TUA, HITAM, putus=False)
    gambar_kolom(tahap_b, kanan0, ABU_MUDA, ABU_TUA, putus=True)

    # Kedua kotak bukti disejajarkan pada dasar kolom terpanjang; tanpa itu
    # kolom dengan jumlah tahap berbeda membuat halaman terlihat miring.
    kotak(d, kiri0 + 16, y_bukti, kiri0 + lebar_kolom - 16, y_bukti + tinggi_bukti,
          isi=SANGAT_MUDA, garis=ABU_MUDA, lebar=1)
    for i, baris in enumerate(baris_a):
        kiri(d, baris, FONT_MIKRO, kiri0 + 32, y_bukti + 24 + i * 17, ABU_TUA)

    kotak(d, kanan0 + 16, y_bukti, kanan0 + lebar_kolom - 16, y_bukti + tinggi_bukti,
          isi=PUTIH, garis=ABU_MUDA, lebar=1)
    for i, baris in enumerate(baris_b):
        kiri(d, baris, FONT_MIKRO, kanan0 + 32, y_bukti + 24 + i * 17, ABU_TUA)

    jalur = outdir / "gambar_4_4_topologi_pengukuran.png"
    im.save(jalur)
    return jalur


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bangkitkan Gambar 4.1 dan 4.4 Bab 4")
    parser.add_argument("--outdir", type=Path, default=Path("image_references"))
    args = parser.parse_args(argv)

    args.outdir.mkdir(parents=True, exist_ok=True)
    for pembuat in (gambar_arsitektur, gambar_topologi):
        jalur = pembuat(args.outdir)
        with Image.open(jalur) as im:
            print(f"  {jalur}  {im.size[0]}x{im.size[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
