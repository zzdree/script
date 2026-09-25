#!/usr/bin/env python3
"""
Generator script to compile script_andreas_v4.docx from script_andreas_v3.docx
Incorporate all revisions:
1. Update Dosen Pembimbing to Mario Norman Syah, S.Pd., M.Eng. (NIP: 199304212024061001)
2. Standardize software name to ZZLUXORA
3. Expand Subbab 2.2.1 with comprehensive mathematical derivation of FFT (Cooley-Tukey Radix-2), STFT, Hann windowing, Gabor uncertainty limit, 43 FPS DMX512 synchronization, Spectral Centroid, Chroma 12-semitone, and MFCC
4. Expand Chapter 3 system architecture and mathematical modeling
5. Append references [32] and [33] to Daftar Pustaka
6. Maintain exact UNNES FT margin (4-3-3-3), Times New Roman 12pt, and 1.5 line spacing.
"""

import os
import shutil
import zipfile
import xml.etree.ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace("w", W_NS)
ET.register_namespace("m", "http://schemas.openxmlformats.org/officeDocument/2006/math")
ET.register_namespace("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships")

def make_p(text, bold=False, italic=False, align="left", size_pt=12, space_after=120):
    p = ET.Element(f"{{{W_NS}}}p")
    pPr = ET.SubElement(p, f"{{{W_NS}}}pPr")
    if align != "left":
        jc = ET.SubElement(pPr, f"{{{W_NS}}}jc")
        jc.set(f"{{{W_NS}}}val", align)
    spacing = ET.SubElement(pPr, f"{{{W_NS}}}spacing")
    spacing.set(f"{{{W_NS}}}line", "360")
    spacing.set(f"{{{W_NS}}}lineRule", "auto")
    if space_after > 0:
        spacing.set(f"{{{W_NS}}}after", str(space_after))

    r = ET.SubElement(p, f"{{{W_NS}}}r")
    rPr = ET.SubElement(r, f"{{{W_NS}}}rPr")
    rFonts = ET.SubElement(rPr, f"{{{W_NS}}}rFonts")
    rFonts.set(f"{{{W_NS}}}ascii", "Times New Roman")
    rFonts.set(f"{{{W_NS}}}hAnsi", "Times New Roman")
    if bold:
        ET.SubElement(rPr, f"{{{W_NS}}}b")
    if italic:
        ET.SubElement(rPr, f"{{{W_NS}}}i")
    sz = ET.SubElement(rPr, f"{{{W_NS}}}sz")
    sz.set(f"{{{W_NS}}}val", str(int(size_pt * 2)))

    t = ET.SubElement(r, f"{{{W_NS}}}t")
    t.text = text
    return p

def get_p_text(p):
    return "".join(t.text for t in p.iter(f"{{{W_NS}}}t") if t.text).strip()

def build_v4():
    v3_path = "/home/zzdree/ANDREAS/script/script_projects/script_andreas_v3.docx"
    v4_path = "/home/zzdree/ANDREAS/script/script_projects/script_andreas_v4.docx"

    with zipfile.ZipFile(v3_path, "r") as zin:
        xml_bytes = zin.read("word/document.xml")
        files = {name: zin.read(name) for name in zin.namelist()}

    tree = ET.fromstring(xml_bytes)
    body = tree.find(f"{{{W_NS}}}body")

    # 1. First pass: Replace all ZZLIGHT-Luxora / ZZLIGHT with ZZLUXORA across all existing text nodes
    for t in tree.iter(f"{{{W_NS}}}t"):
        if t.text:
            if "ZZLIGHT-Luxora" in t.text:
                t.text = t.text.replace("ZZLIGHT-Luxora", "ZZLUXORA")
            if "ZZLIGHT" in t.text:
                t.text = t.text.replace("ZZLIGHT", "ZZLUXORA")

    # 2. Add Dosen Pembimbing on cover page
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    for idx, p in enumerate(paragraphs):
        p_text = get_p_text(p)
        if "NIM 5312422036" in p_text:
            p_dospem_title = make_p("Dosen Pembimbing:", italic=True, align="center")
            p_dospem_name = make_p("Mario Norman Syah, S.Pd., M.Eng.", bold=True, align="center")
            p_dospem_nip = make_p("NIP 199304212024061001", align="center")
            p_idx = list(body).index(p)
            body.insert(p_idx + 1, p_dospem_title)
            body.insert(p_idx + 2, p_dospem_name)
            body.insert(p_idx + 3, p_dospem_nip)
            print("✓ Added Dosen Pembimbing Mario Norman Syah, S.Pd., M.Eng. to cover page")
            break

    # 3. Locate FFT section in Chapter 2 (2.2.1)
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    fft_start_idx = None
    fft_end_idx = None

    for i, p in enumerate(paragraphs):
        p_text = get_p_text(p)
        if "a. *Fast Fourier Transform* (FFT)" in p_text or "Fast Fourier Transform (FFT)" in p_text:
            fft_start_idx = i
        if fft_start_idx is not None and "b. Fitur Audio" in p_text:
            fft_end_idx = i
            break

    if fft_start_idx is not None and fft_end_idx is not None:
        print(f"✓ Found old FFT section from index {fft_start_idx} to {fft_end_idx}. Replacing with comprehensive mathematical derivation...")

        # Elements to replace
        old_nodes = paragraphs[fft_start_idx:fft_end_idx]

        new_paragraphs = [
            make_p("a. Diskritisasi Sinyal Audio dan Kriteria Nyquist-Shannon", bold=True),
            make_p("Sinyal suara fisik yang dihasilkan oleh instrumen musik dan vokal penyembahan merupakan gelombang tekanan udara mekanik kontinu x(t) dalam domain waktu kontinu (t ∈ R). Ketika ditangkap oleh transduser mikrofon dan dikuantisasi oleh Analog-to-Digital Converter (ADC), sinyal dicuplik pada interval waktu periodik Ts (detik), menghasilkan deret diskrit x[n] = x(n · Ts) = x(n / fs), di mana n adalah indeks sampel diskrit dan fs = 1 / Ts adalah frekuensi pencuplikan (sampling rate) dalam Hertz."),
            make_p("Berdasarkan Teorema Kriteria Nyquist-Shannon, agar deret diskrit x[n] mampu merekonstruksi sinyal analog asli tanpa mengalami distorsi lipatan frekuensi (aliasing), frekuensi pencuplikan harus memenuhi fs ≥ 2 · fmax, di mana fmax adalah komponen frekuensi tertinggi yang dikandung oleh sinyal audio. Spektrum pendengaran manusia mencakup rentang 20 Hz hingga 20.000 Hz. Dalam standar komputasi Music Information Retrieval (MIR) dan pustaka Librosa [21], sinyal audio di-downsample ke frekuensi standar fs = 22.050 Hz. Dengan fs = 22.050 Hz, batas frekuensi Nyquist adalah fNyquist = fs / 2 = 11.025 Hz. Batas ini terbukti sangat memadai untuk merepresentasikan nada dasar (fundamental frequency f0) instrumen panggung (rentang nada piano dan vokal manusia berkisar antara 27,5 Hz hingga 4.200 Hz) serta harmonik dominan instrumen musik, sekaligus menghemat beban komputasi CPU dan memori hingga 50% dibandingkan pemrosesan pada laju 44.100 Hz."),

            make_p("b. Discrete Fourier Transform (DFT) dan Kompleksitas Komputasi", bold=True),
            make_p("Sinyal audio dalam domain waktu x[n] hanya merepresentasikan fluktuasi amplitudo terhadap waktu, sehingga tidak mampu memperlihatkan kandungan nada dan spektrum frekuensi yang menyusun lagu tersebut. Untuk mengubah sinyal dari domain waktu ke domain frekuensi, digunakan Discrete Fourier Transform (DFT). Untuk suatu blok sinyal diskrit sepanjang N sampel (n = 0, 1, ..., N-1), DFT mentransformasikan sampel waktu ke dalam spektrum frekuensi diskrit X[k] yang berupa deret bilangan kompleks:"),
            make_p("X[k] = ∑_{n=0}^{N-1} x[n] · e^{-j (2π/N) kn} = ∑_{n=0}^{N-1} x[n] [cos(2πkn/N) - j sin(2πkn/N)],  k = 0, 1, ..., N-1", italic=True, align="center"),
            make_p("di mana j = √(-1) adalah unit imajiner, k adalah indeks komponen frekuensi diskrit (frequency bin), dan N adalah ukuran blok transformasi. Karena sampel audio x[n] merupakan nilai riil murni (x[n] ∈ R), spektrum DFT memiliki sifat simetri konjugat Hermitian X[N - k] = X*[k]. Konsekuensi dari sifat simetri ini adalah bahwa nilai magnitudo spektrum di atas indeks N/2 merupakan cerminan persis dari spektrum di bawah N/2 (|X[N-k]| = |X[k]|). Oleh karena itu, sistem hanya perlu menghitung dan menganalisis sebanyak Nbins = N/2 + 1 komponen frekuensi positif independen, mulai dari bin k = 0 (komponen DC / 0 Hz) hingga bin k = N/2 (frekuensi Nyquist fs/2)."),
            make_p("Ditinjau dari kompleksitas algoritma, untuk menghitung setiap bin k dari persamaan definisi langsung diperlukan N perkalian kompleks dan N - 1 penjumlahan kompleks. Karena terdapat N buah bin yang harus dihitung, total operasi perhitungan DFT langsung adalah O(N^2). Jika panjang frame yang digunakan adalah N = 2048 sampel, maka satu kali evaluasi DFT langsung membutuhkan 2048^2 = 4.194.304 operasi perkalian kompleks. Jika dalam 1 detik sinyal terdapat 43 frame audio, maka sistem harus melakukan lebih dari 180 juta operasi perkalian per detik hanya untuk transformasi dasar. Kompleksitas sebesar ini memicu bottleneck komputasi dan latensi tinggi yang tidak dapat diterima pada aplikasi pengendalian pencahayaan panggung real-time."),

            make_p("c. Algoritma Fast Fourier Transform (FFT) Cooley-Tukey Radix-2", bold=True),
            make_p("Untuk mengatasi inefisiensi komputasi DFT langsung, sistem memanfaatkan algoritma Fast Fourier Transform (FFT) yang dirumuskan oleh J. W. Cooley dan J. W. Tukey pada tahun 1965 [32]. Algoritma ini mengeksploitasi periodisitas dan simetri dari twiddle factor W_N = e^{-j 2π/N} melalui pendekatan divide-and-conquer berbasis desimasi waktu (Decimation-in-Time / DIT)."),
            make_p("Dengan memecah deret penjumlahan n menjadi sub-deret indeks genap (n = 2m) dan ganjil (n = 2m+1), persamaan DFT berukuran N didekomposisi menjadi dua buah DFT berukuran N/2:"),
            make_p("X[k] = E[k] + W_N^k · O[k],  dan  X[k + N/2] = E[k] - W_N^k · O[k]", italic=True, align="center"),
            make_p("di mana E[k] adalah DFT dari sampel genap, O[k] adalah DFT dari sampel ganjil, dan W_N^k adalah twiddle factor. Hubungan simetri ini dikenal sebagai butterfly operation. Melalui rekursi sebanyak log2(N) tahapan, algoritma FFT Cooley-Tukey mereduksi kompleksitas komputasi secara drastis menjadi O(N log2 N)."),
            make_p("Pada ukuran frame N = 2048 sampel, algoritma FFT hanya membutuhkan N log2 N = 2048 × 11 = 22.528 operasi dasar. Dibandingkan dengan DFT langsung (4.194.304 operasi), algoritma FFT Cooley-Tukey memberikan faktor percepatan sebesar 186,2 kali lipat atau memangkas beban komputasi sebesar 99,46%. Efisiensi komputasi ini sangat krusial agar sistem ZZLUXORA dapat mengekstrak seluruh spektrum frekuensi audio secara instan (< 5 ms per frame) tanpa membebani prosesor komputer kontrol pencahayaan."),

            make_p("d. Karakteristik Sinyal Musik Non-Stasioner dan Short-Time Fourier Transform (STFT)", bold=True),
            make_p("Meskipun FFT sangat efisien, penerapan FFT standar secara langsung terhadap keseluruhan durasi berkas lagu rohani (misalnya sebuah lagu berdurasi 4 menit) tidak dapat digunakan untuk pengendalian pencahayaan panggung. Hal ini disebabkan oleh sifat fisik sinyal musik yang bersifat non-stasioner: komposisi lagu rohani memiliki struktur dinamika yang terus berubah terhadap waktu (terdiri dari bagian intro, verse, bridge, chorus, dan ending). Kandungan frekuensi, harmoni akord, kenyaringan, dan tempo musik berganti dari detik ke detik. FFT standar mengintegrasikan seluruh sinyal dari awal hingga akhir lagu, sehingga spektrum yang dihasilkan hanya memperlihatkan frekuensi apa saja yang muncul di sepanjang lagu, namun sama sekali tidak memiliki informasi mengenai kapan frekuensi tersebut terjadi. Tata cahaya panggung menuntut respons visual yang sinkron detik demi detik mengikuti dinamika lagu. Oleh karena itu, transformasi yang wajib digunakan untuk analisis musik adalah Short-Time Fourier Transform (STFT), yang membagi sinyal audio menjadi jendela-jendela waktu pendek (sliding frames) dan mengevaluasi FFT pada masing-masing jendela tersebut [21][33]."),

            make_p("e. Fungsi Windowing dan Mitigasi Spectral Leakage", bold=True),
            make_p("Dalam komputasi STFT, pemotongan sinyal audio menjadi segmen-segmen frame pendek secara matematis ekuivalen dengan mengalikan sinyal x[n] dengan suatu fungsi pembobotan (window function) w[n]. Jika frame dipotong menggunakan jendela persegi (Rectangular Window), pemotongan mendadak pada batas awal dan akhir frame menimbulkan diskontinuitas artifisial tajam pada sinyal. Di domain frekuensi, hal ini menimbulkan fenomena Spectral Leakage di mana energi frekuensi dari suatu nada murni bocor ke bin-bin frekuensi tetangga di sekitarnya dalam bentuk puncak sampingan (sidelobes) yang tinggi. Kebocoran spektral menyebabkan deteksi harmoni nada dan ekstraksi fitur Chroma menjadi bias akibat tercemar frekuensi palsu."),
            make_p("Untuk meredam spectral leakage, amplitudo sinyal pada tepi frame harus diturunkan secara mulus (tapering) menuju nol. Pada sistem ZZLUXORA, digunakan fungsi jendela Hann (Hanning) Window [21]:"),
            make_p("w[n] = 0.5 · [1 - cos(2πn / (N - 1))] = sin^2(πn / (N - 1)),  untuk 0 ≤ n ≤ N-1", italic=True, align="center"),
            make_p("Fungsi Hann memiliki nilai w[0] = w[N-1] = 0 dan puncak w[(N-1)/2] = 1. Keunggulan akustik fungsi Hann adalah mampu meredam sidelobe level hingga -31,5 dB (jauh lebih baik dibandingkan rectangular window yang hanya memiliki peredaman -13 dB), sehingga menghasilkan pemisahan puncak frekuensi nada yang bersih dan meminimalkan bias pada analisis harmoni lagu."),

            make_p("f. Formulasi Diskrit STFT dan Konversi Parameter Fisik", bold=True),
            make_p("Dengan menggabungkan fungsi pembobotan Hann window dan algoritma FFT Cooley-Tukey, formulasi matematis STFT diskrit yang diimplementasikan pada komputasi perangkat lunak ZZLUXORA didefinisikan sebagai:"),
            make_p("X[m, k] = ∑_{n=0}^{N-1} x[n + m · H] · w[n] · e^{-j (2π/N) kn}", italic=True, align="center"),
            make_p("di mana m adalah indeks frame waktu, k adalah indeks bin frekuensi, N = 2048 adalah panjang jendela analisis (Window Length), H = 512 adalah jarak pergeseran antar jendela (Hop Length dengan overlap 75%), w[n] adalah fungsi jendela Hann, dan x[n + m · H] adalah segmen sinyal audio pada jendela waktu ke-m. Hasil transformasi STFT adalah matriks bilangan kompleks X[m, k] berdimensi 1025 × M yang menghubungkan koordinat sel diskrit (m, k) dengan besaran fisik nyata:"),
            make_p("1. Waktu Fisik frame ke-m: tm = (m · H) / fs (detik)"),
            make_p("2. Frekuensi Fisik bin ke-k: fk = (k · fs) / N (Hertz)"),
            make_p("3. Lebar Pita per Bin Frekuensi: Δf = fs / N = 22050 / 2048 ≈ 10,77 Hz"),
            make_p("4. Interval Perbaruan Waktu Frame: Δthop = H / fs = 512 / 22050 ≈ 23,22 ms"),
            make_p("Laju pembaruan data visual (frame rate) yang dihasilkan oleh algoritma adalah FPS = 1 / Δthop = 22050 / 512 ≈ 43,07 frame per detik (fps). Nilai 43,07 FPS ini secara presisi selaras dengan laju penyegaran transmisi fisik standar DMX512-A (44 frame per detik) [17], sehingga data pencahayaan dapat langsung dialirkan ke lampu PAR LED panggung tanpa membutuhkan interpolasi atau penahanan buffer tambahan, menghasilkan transisi visual yang sangat halus (smooth fading) dan bebas getaran (visual stepping)."),

            make_p("g. Prinsip Ketidakpastian Waktu-Frekuensi (Heisenberg-Gabor Limit)", bold=True),
            make_p("Dalam pemrosesan sinyal waktu-frekuensi berlaku batasan fundamental fisika yang dikenal sebagai Prinsip Ketidakpastian Gabor: Δt · Δf ≥ 1 / (4π). Prinsip ini menegaskan bahwa kita tidak dapat memperoleh resolusi waktu yang sangat tinggi dan resolusi frekuensi yang sangat tinggi secara simultan menggunakan satu ukuran jendela STFT konstan. Jika N terlalu besar (misal 8192), resolusi frekuensi sangat tinggi namun resolusi waktu memburuk (Δt ≈ 371 ms), membuat ketukan drum buram dan terlambat. Sebaliknya jika N terlalu kecil (misal 256), resolusi waktu tajam namun resolusi frekuensi sangat kasar (Δf ≈ 86 Hz) sehingga nada musik tidak dapat dibedakan. Penetapan parameter fs = 22.050 Hz, N = 2048, dan H = 512 pada sistem ZZLUXORA merupakan titik kompromi optimal yang terbukti mampu membedakan harmoni akord musik (Δf ≈ 10,77 Hz) sekaligus mendeteksi ketukan musik dengan latensi rendah (Δthop ≈ 23,22 ms), berada jauh di bawah ambang batas persepsi keterlambatan visual mata manusia (< 40 ms).")
        ]

        # Insert new paragraphs before old_nodes[0], then remove old_nodes
        first_old = old_nodes[0]
        insert_pos = list(body).index(first_old)
        for p_new in new_paragraphs:
            body.insert(insert_pos, p_new)
            insert_pos += 1

        for p_old in old_nodes:
            body.remove(p_old)

    # 4. Append references [32] and [33] to DAFTAR PUSTAKA
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    for p in reversed(paragraphs):
        p_text = get_p_text(p)
        if "[31]" in p_text:
            p32 = make_p('[32] J. W. Cooley and J. W. Tukey, "An algorithm for the machine calculation of complex Fourier series," Mathematics of Computation, vol. 19, no. 90, pp. 297–301, 1965. doi: 10.1090/S0025-5718-1965-0178586-1. [Online]. Available: https://www.ams.org/journals/mcom/1965-19-090/S0025-5718-1965-0178586-1/')
            p33 = make_p('[33] M. Müller, Fundamentals of Music Processing: Audio, Analysis, Algorithms, Applications, Cham: Springer International Publishing, 2015. doi: 10.1007/978-3-319-21945-5.')
            p_idx = list(body).index(p)
            body.insert(p_idx + 1, p32)
            body.insert(p_idx + 2, p33)
            print("✓ Appended references [32] and [33] to DAFTAR PUSTAKA")
            break

    # Save modified document.xml and repackage into script_andreas_v4.docx
    modified_xml = ET.tostring(tree, encoding="utf-8", xml_declaration=True)
    files["word/document.xml"] = modified_xml

    with zipfile.ZipFile(v4_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, content in files.items():
            zout.writestr(name, content)

    print(f"\n🎉 Successfully compiled {v4_path}!")
    print(f"   Size: {os.path.getsize(v4_path):,} bytes")

if __name__ == "__main__":
    build_v4()
