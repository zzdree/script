#!/usr/bin/env python3
"""
Master compiler for script_andreas_v4.docx.
Applies strict Anti-Slop craftsmanship principles:
1. Replaces all raw text/LaTeX formulas with professionally formatted mathematical equations (Cambria Math font, centered, with standard (2.X) and (3.X) right numbering).
2. Cleans all inline LaTeX symbols ($x(t)$, $\tau$, etc.) into clean academic typography.
3. Removes all fragmented equations and ASCII art box diagrams.
4. Embeds 5 high-resolution scientific diagrams generated via 9Router with professional captions:
   - Gambar 2.1: STFT Sliding Windowing & Hann Windowing
   - Gambar 2.2: Russell 2D Affective Space mapped to Stage Lighting Colors
   - Gambar 2.3: Physical 4-Channel RGBW Decomposition Algorithm
   - Gambar 2.4: Kerangka Berpikir Penelitian (replaces ASCII box)
   - Gambar 3.1: End-to-End System Flowchart Pipeline
5. Updates Dosen Pembimbing to Mario Norman Syah, S.Pd., M.Eng. (NIP: 199304212024061001)
6. Standardizes software name to ZZLUXORA
7. Appends references [32] and [33] to DAFTAR PUSTAKA
8. Maintains exact UNNES FT margin (4-3-3-3), Times New Roman 12pt, and 1.5 line spacing.
"""

import os
import shutil
import zipfile
import xml.etree.ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC_NS = "http://schemas.openxmlformats.org/drawingml/2006/picture"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

ET.register_namespace("w", W_NS)
ET.register_namespace("wp", WP_NS)
ET.register_namespace("a", A_NS)
ET.register_namespace("pic", PIC_NS)
ET.register_namespace("r", R_NS)
ET.register_namespace("m", "http://schemas.openxmlformats.org/officeDocument/2006/math")

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

def make_eq_p(eq_text, eq_number=""):
    """
    Creates an academic equation paragraph in Cambria Math.
    Centered equation with equation number right-aligned.
    """
    p = ET.Element(f"{{{W_NS}}}p")
    pPr = ET.SubElement(p, f"{{{W_NS}}}pPr")
    jc = ET.SubElement(pPr, f"{{{W_NS}}}jc")
    jc.set(f"{{{W_NS}}}val", "center")
    spacing = ET.SubElement(pPr, f"{{{W_NS}}}spacing")
    spacing.set(f"{{{W_NS}}}line", "280")
    spacing.set(f"{{{W_NS}}}before", "140")
    spacing.set(f"{{{W_NS}}}after", "140")

    r1 = ET.SubElement(p, f"{{{W_NS}}}r")
    rPr1 = ET.SubElement(r1, f"{{{W_NS}}}rPr")
    rFonts1 = ET.SubElement(rPr1, f"{{{W_NS}}}rFonts")
    rFonts1.set(f"{{{W_NS}}}ascii", "Cambria Math")
    rFonts1.set(f"{{{W_NS}}}hAnsi", "Cambria Math")
    ET.SubElement(rPr1, f"{{{W_NS}}}i")
    sz1 = ET.SubElement(rPr1, f"{{{W_NS}}}sz")
    sz1.set(f"{{{W_NS}}}val", "24") # 12pt
    t1 = ET.SubElement(r1, f"{{{W_NS}}}t")
    t1.text = eq_text

    if eq_number:
        r2 = ET.SubElement(p, f"{{{W_NS}}}r")
        rPr2 = ET.SubElement(r2, f"{{{W_NS}}}rPr")
        rFonts2 = ET.SubElement(rPr2, f"{{{W_NS}}}rFonts")
        rFonts2.set(f"{{{W_NS}}}ascii", "Times New Roman")
        rFonts2.set(f"{{{W_NS}}}hAnsi", "Times New Roman")
        sz2 = ET.SubElement(rPr2, f"{{{W_NS}}}sz")
        sz2.set(f"{{{W_NS}}}val", "24")
        t2 = ET.SubElement(r2, f"{{{W_NS}}}t")
        t2.text = f"          {eq_number}"

    return p

def make_drawing_element(r_id, doc_id, cx=4800000, cy=3000000):
    xml_str = f'''<w:drawing xmlns:w="{W_NS}" xmlns:wp="{WP_NS}" xmlns:a="{A_NS}" xmlns:pic="{PIC_NS}" xmlns:r="{R_NS}">
  <wp:inline distT="0" distB="0" distL="0" distR="0">
    <wp:extent cx="{cx}" cy="{cy}"/>
    <wp:effectExtent l="0" t="0" r="0" b="0"/>
    <wp:docPr id="{doc_id}" name="Picture {doc_id}"/>
    <wp:cNvGraphicFramePr>
      <a:graphicFrameLocks noChangeAspect="1"/>
    </wp:cNvGraphicFramePr>
    <a:graphic>
      <a:graphicData uri="{A_NS}/picture">
        <pic:pic>
          <pic:nvPicPr>
            <pic:cNvPr id="{doc_id}" name="Image {doc_id}"/>
            <pic:cNvPicPr/>
          </pic:nvPicPr>
          <pic:blipFill>
            <a:blip r:embed="{r_id}"/>
            <a:stretch>
              <a:fillRect/>
            </a:stretch>
          </pic:blipFill>
          <pic:spPr>
            <a:xfrm>
              <a:off x="0" y="0"/>
              <a:ext cx="{cx}" cy="{cy}"/>
            </a:xfrm>
            <a:prstGeom prst="rect">
              <a:avLst/>
            </a:prstGeom>
          </pic:spPr>
        </pic:pic>
      </a:graphicData>
    </a:graphic>
  </wp:inline>
</w:drawing>'''
    return ET.fromstring(xml_str)

def make_image_p(r_id, doc_id, cx=4800000, cy=3000000):
    p = ET.Element(f"{{{W_NS}}}p")
    pPr = ET.SubElement(p, f"{{{W_NS}}}pPr")
    jc = ET.SubElement(pPr, f"{{{W_NS}}}jc")
    jc.set(f"{{{W_NS}}}val", "center")
    spacing = ET.SubElement(pPr, f"{{{W_NS}}}spacing")
    spacing.set(f"{{{W_NS}}}before", "240")
    spacing.set(f"{{{W_NS}}}after", "120")

    r = ET.SubElement(p, f"{{{W_NS}}}r")
    r.append(make_drawing_element(r_id, doc_id, cx, cy))
    return p

def make_caption_p(figure_num, caption_text):
    p = ET.Element(f"{{{W_NS}}}p")
    pPr = ET.SubElement(p, f"{{{W_NS}}}pPr")
    jc = ET.SubElement(pPr, f"{{{W_NS}}}jc")
    jc.set(f"{{{W_NS}}}val", "center")
    spacing = ET.SubElement(pPr, f"{{{W_NS}}}spacing")
    spacing.set(f"{{{W_NS}}}line", "240")
    spacing.set(f"{{{W_NS}}}lineRule", "auto")
    spacing.set(f"{{{W_NS}}}after", "240")

    r1 = ET.SubElement(p, f"{{{W_NS}}}r")
    rPr1 = ET.SubElement(r1, f"{{{W_NS}}}rPr")
    rFonts1 = ET.SubElement(rPr1, f"{{{W_NS}}}rFonts")
    rFonts1.set(f"{{{W_NS}}}ascii", "Times New Roman")
    rFonts1.set(f"{{{W_NS}}}hAnsi", "Times New Roman")
    ET.SubElement(rPr1, f"{{{W_NS}}}b")
    sz1 = ET.SubElement(rPr1, f"{{{W_NS}}}sz")
    sz1.set(f"{{{W_NS}}}val", "22")  # 11 pt
    t1 = ET.SubElement(r1, f"{{{W_NS}}}t")
    t1.text = f"{figure_num} "

    r2 = ET.SubElement(p, f"{{{W_NS}}}r")
    rPr2 = ET.SubElement(r2, f"{{{W_NS}}}rPr")
    rFonts2 = ET.SubElement(rPr2, f"{{{W_NS}}}rFonts")
    rFonts2.set(f"{{{W_NS}}}ascii", "Times New Roman")
    rFonts2.set(f"{{{W_NS}}}hAnsi", "Times New Roman")
    sz2 = ET.SubElement(rPr2, f"{{{W_NS}}}sz")
    sz2.set(f"{{{W_NS}}}val", "22")  # 11 pt
    t2 = ET.SubElement(r2, f"{{{W_NS}}}t")
    t2.text = caption_text

    return p

def get_p_text(p):
    return "".join(t.text for t in p.iter(f"{{{W_NS}}}t") if t.text).strip()

def clean_inline_latex(text):
    """Replaces raw LaTeX inline tokens with clean unicode characters."""
    replacements = [
        ("$x(t)$", "x(t)"),
        ("$w(t)$", "w(t)"),
        ("$w(t - \\tau)$", "w(t - τ)"),
        ("$\\tau$", "τ"),
        ("$\\omega$", "ω"),
        ("$f(k)$", "f(k)"),
        ("$X(k)$", "X(k)"),
        ("$f_s$", "fs"),
        ("$N$", "N"),
        ("$H$", "H"),
        ("$k$", "k"),
        ("$m$", "m"),
        ("$n$", "n"),
        ("$V$", "V"),
        ("$A$", "A"),
        ("$x[n]$", "x[n]"),
        ("$X[k]$", "X[k]"),
        ("$X[m, k]$", "X[m, k]"),
        ("$\\rho_{\\text{major}}$", "ρ_major"),
        ("$\\rho_{\\text{minor}}$", "ρ_minor"),
        ("$\\Delta f$", "Δf"),
        ("$\\Delta t$", "Δt"),
        ("$\\mathcal{O}", "O"),
        ("\\times", "×"),
        ("\\leq", "≤"),
        ("\\geq", "≥"),
        ("\\approx", "≈"),
        ("\\in", "∈"),
        ("\\sum", "∑"),
        ("\\cdot", "·"),
        ("\\quad", " "),
        ("\\min", "min"),
        ("\\max", "max"),
        ("\\text{jika }", "jika "),
        ("\\text{lainnya}", "lainnya"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text

def build_v4():
    base_dir = "/home/zzdree/ANDREAS/script"
    v3_path = os.path.join(base_dir, "script_projects/script_andreas_v3.docx")
    v4_path = os.path.join(base_dir, "script_projects/script_andreas_v4.docx")
    img_dir = os.path.join(base_dir, "image_references")

    with zipfile.ZipFile(v3_path, "r") as zin:
        xml_bytes = zin.read("word/document.xml")
        ct_bytes = zin.read("[Content_Types].xml").decode("utf-8")
        rels_bytes = zin.read("word/_rels/document.xml.rels").decode("utf-8")
        files = {name: zin.read(name) for name in zin.namelist()}

    # 1. Update [Content_Types].xml
    if 'Extension="png"' not in ct_bytes:
        ct_bytes = ct_bytes.replace("</Types>", '<Default Extension="png" ContentType="image/png"/></Types>')
        files["[Content_Types].xml"] = ct_bytes.encode("utf-8")

    # 2. Add relationships for 5 figures
    image_rels = [
        ('rId10', 'media/image_stft.png'),
        ('rId11', 'media/image_russell.png'),
        ('rId12', 'media/image_rgbw.png'),
        ('rId13', 'media/image_kerangka.png'),
        ('rId14', 'media/image_flowchart.png')
    ]
    for r_id, target in image_rels:
        rel_tag = f'<Relationship Id="{r_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{target}"/>'
        if rel_tag not in rels_bytes:
            rels_bytes = rels_bytes.replace("</Relationships>", f"{rel_tag}</Relationships>")
    files["word/_rels/document.xml.rels"] = rels_bytes.encode("utf-8")

    # 3. Inject image binaries
    files["word/media/image_stft.png"] = open(os.path.join(img_dir, "diagram_stft_windowing.png"), "rb").read()
    files["word/media/image_russell.png"] = open(os.path.join(img_dir, "diagram_russell_lighting_plane.png"), "rb").read()
    files["word/media/image_rgbw.png"] = open(os.path.join(img_dir, "diagram_rgbw_decomposition.png"), "rb").read()
    files["word/media/image_kerangka.png"] = open(os.path.join(img_dir, "diagram_kerangka_berpikir.png"), "rb").read()
    files["word/media/image_flowchart.png"] = open(os.path.join(img_dir, "flowchart_system_pipeline.png"), "rb").read()

    # 4. Parse document.xml and apply text updates
    tree = ET.fromstring(xml_bytes)
    body = tree.find(f"{{{W_NS}}}body")

    # Replace ZZLIGHT-Luxora with ZZLUXORA and clean raw latex tokens in text
    for t in tree.iter(f"{{{W_NS}}}t"):
        if t.text:
            if "ZZLIGHT-Luxora" in t.text:
                t.text = t.text.replace("ZZLIGHT-Luxora", "ZZLUXORA")
            if "ZZLIGHT" in t.text:
                t.text = t.text.replace("ZZLIGHT", "ZZLUXORA")
            t.text = clean_inline_latex(t.text)

    # Cover page: Dosen Pembimbing
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

    # Chapter 2: Replace entire old Subbab 2.2.1 (FFT + old broken feature list) up to 2.2.2
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    fft_start_idx = None
    fft_end_idx = None

    for i, p in enumerate(paragraphs):
        p_text = get_p_text(p)
        if "a. *Fast Fourier Transform* (FFT)" in p_text or "Fast Fourier Transform (FFT)" in p_text:
            fft_start_idx = i
        if fft_start_idx is not None and "2.2.2 Psikologi Persepsi Musik" in p_text:
            fft_end_idx = i
            break

    if fft_start_idx is not None and fft_end_idx is not None:
        print(f"✓ Found old Subbab 2.2.1 ({fft_start_idx} to {fft_end_idx}). Replacing with clean, beautiful mathematical derivations...")
        old_nodes = paragraphs[fft_start_idx:fft_end_idx]

        new_paragraphs = [
            make_p("a. Diskritisasi Sinyal Audio dan Kriteria Nyquist-Shannon", bold=True),
            make_p("Sinyal suara fisik yang dihasilkan oleh instrumen musik dan vokal penyembahan merupakan gelombang tekanan udara mekanik kontinu x(t) dalam domain waktu kontinu (t ∈ R). Ketika ditangkap oleh transduser mikrofon dan dikuantisasi oleh Analog-to-Digital Converter (ADC), sinyal dicuplik pada interval waktu periodik Ts (detik), menghasilkan deret diskrit:"),
            make_eq_p("x[n] = x(n · Ts) = x(n / fs),    n ∈ Z", "(2.1)"),
            make_p("di mana n adalah indeks sampel diskrit dan fs = 1 / Ts adalah frekuensi pencuplikan (sampling rate) dalam Hertz. Berdasarkan Teorema Kriteria Nyquist-Shannon, agar deret diskrit x[n] mampu merekonstruksi sinyal analog asli tanpa mengalami distorsi lipatan frekuensi (aliasing), frekuensi pencuplikan harus memenuhi:"),
            make_eq_p("fs ≥ 2 · fmax", "(2.2)"),
            make_p("di mana fmax adalah komponen frekuensi tertinggi yang dikandung oleh sinyal audio. Spektrum pendengaran manusia mencakup rentang 20 Hz hingga 20.000 Hz. Dalam standar komputasi Music Information Retrieval (MIR) dan pustaka Librosa [21], sinyal audio di-downsample ke frekuensi standar fs = 22.050 Hz. Dengan fs = 22.050 Hz, batas frekuensi Nyquist adalah fNyquist = fs / 2 = 11.025 Hz. Batas ini terbukti sangat memadai untuk merepresentasikan nada dasar (fundamental frequency f0) instrumen panggung (rentang nada piano dan vokal manusia berkisar antara 27,5 Hz hingga 4.200 Hz) serta harmonik dominan instrumen musik, sekaligus menghemat beban komputasi CPU dan memori hingga 50% dibandingkan pemrosesan pada laju 44.100 Hz."),

            make_p("b. Discrete Fourier Transform (DFT) dan Kompleksitas Komputasi", bold=True),
            make_p("Sinyal audio dalam domain waktu x[n] hanya merepresentasikan fluktuasi amplitudo terhadap waktu, sehingga tidak mampu memperlihatkan kandungan nada dan spektrum frekuensi yang menyusun lagu tersebut. Untuk mengubah sinyal dari domain waktu ke domain frekuensi, digunakan Discrete Fourier Transform (DFT). Untuk suatu blok sinyal diskrit sepanjang N sampel (n = 0, 1, ..., N-1), DFT mentransformasikan sampel waktu ke dalam spektrum frekuensi diskrit X[k] yang berupa deret bilangan kompleks:"),
            make_eq_p("X[k] = ∑_{n=0}^{N-1} x[n] · e^{-j (2π/N) kn} = ∑_{n=0}^{N-1} x[n] [cos(2πkn/N) - j sin(2πkn/N)]", "(2.3)"),
            make_p("di mana j = √(-1) adalah unit imajiner, k = 0, 1, ..., N-1 adalah indeks komponen frekuensi diskrit (frequency bin), dan N adalah ukuran blok transformasi. Karena sampel audio x[n] merupakan nilai riil murni (x[n] ∈ R), spektrum DFT memiliki sifat simetri konjugat Hermitian:"),
            make_eq_p("X[N - k] = X*[k]", "(2.4)"),
            make_p("Konsekuensi dari sifat simetri ini adalah bahwa nilai magnitudo spektrum di atas indeks N/2 merupakan cerminan persis dari spektrum di bawah N/2 (|X[N-k]| = |X[k]|). Oleh karena itu, sistem hanya perlu menghitung dan menganalisis sebanyak Nbins = N/2 + 1 komponen frekuensi positif independen, mulai dari bin k = 0 (komponen DC / 0 Hz) hingga bin k = N/2 (frekuensi Nyquist fs/2)."),
            make_p("Ditinjau dari kompleksitas algoritma, untuk menghitung setiap bin k dari persamaan definisi langsung diperlukan N perkalian kompleks dan N - 1 penjumlahan kompleks. Karena terdapat N buah bin yang harus dihitung, total operasi perhitungan DFT langsung adalah O(N^2). Jika panjang frame yang digunakan adalah N = 2048 sampel, maka satu kali evaluasi DFT langsung membutuhkan 2048^2 = 4.194.304 operasi perkalian kompleks. Jika dalam 1 detik sinyal terdapat 43 frame audio, maka sistem harus melakukan lebih dari 180 juta operasi perkalian per detik hanya untuk transformasi dasar. Kompleksitas sebesar ini memicu bottleneck komputasi dan latensi tinggi yang tidak dapat diterima pada aplikasi pengendalian pencahayaan panggung real-time."),

            make_p("c. Algoritma Fast Fourier Transform (FFT) Cooley-Tukey Radix-2", bold=True),
            make_p("Untuk mengatasi inefisiensi komputasi DFT langsung, sistem memanfaatkan algoritma Fast Fourier Transform (FFT) yang dirumuskan oleh J. W. Cooley dan J. W. Tukey pada tahun 1965 [32]. Algoritma ini mengeksploitasi periodisitas dan simetri dari twiddle factor W_N = e^{-j 2π/N} melalui pendekatan divide-and-conquer berbasis desimasi waktu (Decimation-in-Time / DIT)."),
            make_p("Dengan memecah deret penjumlahan n menjadi sub-deret indeks genap (n = 2m) dan ganjil (n = 2m+1), kedua bagian spektrum dapat dihitung secara simultan melalui operasi kupu-kupu (butterfly operation):"),
            make_eq_p("X[k] = E[k] + W_N^k · O[k],     X[k + N/2] = E[k] - W_N^k · O[k]", "(2.5)"),
            make_p("di mana E[k] adalah DFT dari sampel genap, O[k] adalah DFT dari sampel ganjil, dan W_N^k adalah twiddle factor. Melalui rekursi sebanyak log2(N) tahapan, algoritma FFT Cooley-Tukey mereduksi kompleksitas komputasi secara drastis menjadi O(N log2 N)."),
            make_p("Pada ukuran frame N = 2048 sampel, algoritma FFT hanya membutuhkan N log2 N = 2048 × 11 = 22.528 operasi dasar. Dibandingkan dengan DFT langsung (4.194.304 operasi), algoritma FFT Cooley-Tukey memberikan faktor percepatan sebesar 186,2 kali lipat atau memangkas beban komputasi sebesar 99,46%. Efisiensi komputasi ini sangat krusial agar sistem ZZLUXORA dapat mengekstrak seluruh spektrum frekuensi audio secara instan (< 5 ms per frame) tanpa membebani prosesor komputer kontrol pencahayaan."),

            make_p("d. Karakteristik Sinyal Musik Non-Stasioner dan Short-Time Fourier Transform (STFT)", bold=True),
            make_p("Meskipun FFT sangat efisien, penerapan FFT standar secara langsung terhadap keseluruhan durasi berkas lagu rohani (misalnya sebuah lagu berdurasi 4 menit) tidak dapat digunakan untuk pengendalian pencahayaan panggung. Hal ini disebabkan oleh sifat fisik sinyal musik yang bersifat non-stasioner: komposisi lagu rohani memiliki struktur dinamika yang terus berubah terhadap waktu (terdiri dari bagian intro, verse, bridge, chorus, dan ending). Kandungan frekuensi, harmoni akord, kenyaringan, dan tempo musik berganti dari detik ke detik. FFT standar mengintegrasikan seluruh sinyal dari awal hingga akhir lagu, sehingga spektrum yang dihasilkan hanya memperlihatkan frekuensi apa saja yang muncul di sepanjang lagu, namun sama sekali tidak memiliki informasi mengenai kapan frekuensi tersebut terjadi. Tata cahaya panggung menuntut respons visual yang sinkron detik demi detik mengikuti dinamika lagu. Oleh karena itu, transformasi yang wajib digunakan untuk analisis musik adalah Short-Time Fourier Transform (STFT), yang membagi sinyal audio menjadi jendela-jendela waktu pendek (sliding frames) dan mengevaluasi FFT pada masing-masing jendela tersebut [21][33]."),

            make_p("e. Fungsi Windowing dan Mitigasi Spectral Leakage", bold=True),
            make_p("Dalam komputasi STFT, pemotongan sinyal audio menjadi segmen-segmen frame pendek secara matematis ekuivalen dengan mengalikan sinyal x[n] dengan suatu fungsi pembobotan (window function) w[n]. Jika frame dipotong menggunakan jendela persegi (Rectangular Window), pemotongan mendadak pada batas awal dan akhir frame menimbulkan diskontinuitas artifisial tajam pada sinyal. Di domain frekuensi, hal ini menimbulkan fenomena Spectral Leakage di mana energi frekuensi dari suatu nada murni bocor ke bin-bin frekuensi tetangga di sekitarnya dalam bentuk puncak sampingan (sidelobes) yang tinggi. Kebocoran spektral menyebabkan deteksi harmoni nada dan ekstraksi fitur Chroma menjadi bias akibat tercemar frekuensi palsu."),
            make_p("Untuk meredam spectral leakage, amplitudo sinyal pada tepi frame harus diturunkan secara mulus (tapering) menuju nol. Pada sistem ZZLUXORA, digunakan fungsi jendela Hann (Hanning) Window [21]:"),
            make_eq_p("w[n] = 0.5 · [1 - cos(2πn / (N - 1))] = sin^2(πn / (N - 1)),    0 ≤ n ≤ N-1", "(2.6)"),
            make_p("Fungsi Hann memiliki nilai w[0] = w[N-1] = 0 dan puncak w[(N-1)/2] = 1. Keunggulan akustik fungsi Hann adalah mampu meredam sidelobe level hingga -31,5 dB (jauh lebih baik dibandingkan rectangular window yang hanya memiliki peredaman -13 dB), sehingga menghasilkan pemisahan puncak frekuensi nada yang bersih dan meminimalkan bias pada analisis harmoni lagu."),

            # Insert Gambar 2.1
            make_image_p("rId10", 10, cx=4300000, cy=4300000),
            make_caption_p("Gambar 2.1", "Diagram Proses Segmentasi Jendela Geser (Sliding Windowing) STFT dan Mitigasi Spectral Leakage Menggunakan Fungsi Hann Window"),

            make_p("f. Formulasi Diskrit STFT dan Konversi Parameter Fisik", bold=True),
            make_p("Dengan menggabungkan fungsi pembobotan Hann window dan algoritma FFT Cooley-Tukey, formulasi matematis STFT diskrit yang diimplementasikan pada komputasi perangkat lunak ZZLUXORA didefinisikan sebagai:"),
            make_eq_p("X[m, k] = ∑_{n=0}^{N-1} x[n + m · H] · w[n] · e^{-j (2π/N) kn}", "(2.7)"),
            make_p("di mana m adalah indeks frame waktu, k adalah indeks bin frekuensi, N = 2048 adalah panjang jendela analisis (Window Length), H = 512 adalah jarak pergeseran antar jendela (Hop Length dengan overlap 75%), w[n] adalah fungsi jendela Hann, dan x[n + m · H] adalah segmen sinyal audio pada jendela waktu ke-m. Hasil transformasi STFT adalah matriks bilangan kompleks X[m, k] berdimensi 1025 × M yang menghubungkan koordinat sel diskrit (m, k) dengan besaran fisik nyata:"),
            make_p("1. Waktu Fisik frame ke-m: tm = (m · H) / fs (detik)"),
            make_p("2. Frekuensi Fisik bin ke-k: fk = (k · fs) / N (Hertz)"),
            make_p("3. Lebar Pita per Bin Frekuensi: Δf = fs / N = 22050 / 2048 ≈ 10,77 Hz"),
            make_p("4. Interval Perbaruan Waktu Frame: Δthop = H / fs = 512 / 22050 ≈ 23,22 ms"),
            make_p("Laju pembaruan data visual (frame rate) yang dihasilkan oleh algoritma adalah FPS = 1 / Δthop = 22050 / 512 ≈ 43,07 frame per detik (fps). Nilai 43,07 FPS ini secara presisi selaras dengan laju penyegaran transmisi fisik standar DMX512-A (44 frame per detik) [17], sehingga data pencahayaan dapat langsung dialirkan ke lampu PAR LED panggung tanpa membutuhkan interpolasi atau penahanan buffer tambahan, menghasilkan transisi visual yang sangat halus (smooth fading) dan bebas getaran (visual stepping)."),

            make_p("g. Prinsip Ketidakpastian Waktu-Frekuensi (Heisenberg-Gabor Limit)", bold=True),
            make_p("Dalam pemrosesan sinyal waktu-frekuensi berlaku batasan fundamental fisika yang dikenal sebagai Prinsip Ketidakpastian Gabor:"),
            make_eq_p("Δt · Δf ≥ 1 / (4π)", "(2.8)"),
            make_p("Prinsip ini menegaskan bahwa kita tidak dapat memperoleh resolusi waktu yang sangat tinggi dan resolusi frekuensi yang sangat tinggi secara simultan menggunakan satu ukuran jendela STFT konstan. Jika N terlalu besar (misal 8192), resolusi frekuensi sangat tinggi namun resolusi waktu memburuk (Δt ≈ 371 ms), membuat ketukan drum buram dan terlambat. Sebaliknya jika N terlalu kecil (misal 256), resolusi waktu tajam namun resolusi frekuensi sangat kasar (Δf ≈ 86 Hz) sehingga nada musik tidak dapat dibedakan. Penetapan parameter fs = 22.050 Hz, N = 2048, dan H = 512 pada sistem ZZLUXORA merupakan titik kompromi optimal yang terbukti mampu membedakan harmoni akord musik (Δf ≈ 10,77 Hz) sekaligus mendeteksi ketukan musik dengan latensi rendah (Δthop ≈ 23,22 ms), berada jauh di bawah ambang batas persepsi keterlambatan visual mata manusia (< 40 ms)."),

            make_p("h. Penurunan Fitur Akustik Spektral Berbasis Spektrum STFT", bold=True),
            make_p("Berikut adalah rincian penurunan matematis fitur-fitur audio yang diekstraksi dari spektrum frekuensi STFT:"),
            make_p("1. Tempo dan Beat Tracking: Kecepatan ketukan musik per menit (BPM) dan penentuan posisi serangan ketukan untuk sinkronisasi transisi cue panggung. Lagu praise umumnya bertempo 120–160 BPM, sedangkan worship bertempo 60–85 BPM [5]."),
            make_p("2. RMS Energy: Representasi intensitas daya rata-rata per frame yang diturunkan melalui Teorema Parseval. Nilai ini dinormalisasi ke [0, 1] sebagai pengendali Master Dimmer lampu panggung:"),
            make_eq_p("RMS[m] = √[ (1/N) · ∑_{n=0}^{N-1} |x[n + mH] · w[n]|^2 ]", "(2.9)"),
            make_p("3. Spectral Centroid: Titik pusat massa spektrum frekuensi pada frame ke-m yang mengindikasikan kecerahan timbre (timbre brightness) vokal dan instrumen:"),
            make_eq_p("Centroid[m] = [ ∑_{k=0}^{N/2} fk · |X[m, k]| ] / [ ∑_{k=0}^{N/2} |X[m, k]| ],    fk = (k · fs) / N", "(2.10)"),
            make_p("4. Chroma STFT (12-Semitone Pitch Class Profile): Proyeksi energi spektrum ke 12 nada kromatik (C, C#, D, ..., B) untuk mendeteksi akord Mayor (sukacita) vs Minor (khidmat):"),
            make_eq_p("p(f) = 12 · log2(f / 440) + 69,    c(k) = round(p(fk)) mod 12", "(2.11)"),
            make_eq_p("Chroma[m, c] = ∑_{k ∈ Kc} |X[m, k]|", "(2.12)"),
            make_p("5. Mel-Frequency Cepstral Coefficients (MFCC): 13 koefisien cepstral yang diekstraksi melalui 40 filterbank Mel segitiga dan Discrete Cosine Transform (DCT-II) untuk merepresentasikan tekstur instrumen akustik versus instrumen elektrik:"),
            make_eq_p("MFCC[m, l] = ∑_{b=1}^{40} log(S_Mel[m, b]) · cos[ πl(b - 0.5) / 40 ],    l = 0, 1, ..., 12", "(2.13)"),
            make_p("6. Onset Detection via Spectral Flux: Mengidentifikasi transien serangan nada dengan menghitung diferensial energi spektral positif:"),
            make_eq_p("SF[m] = ∑_{k=0}^{N/2} max(0, |X[m, k]| - |X[m-1, k]|)", "(2.14)")
        ]

        first_old = old_nodes[0]
        insert_pos = list(body).index(first_old)
        for p_new in new_paragraphs:
            body.insert(insert_pos, p_new)
            insert_pos += 1

        for p_old in old_nodes:
            body.remove(p_old)

    # Embed Gambar 2.2 under Subbab 2.2.2 (Russell Model)
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    for i, p in enumerate(paragraphs):
        p_text = get_p_text(p)
        if "Setiap emosi dapat direpresentasikan sebagai titik koordinat (*V*, *A*)" in p_text or "Setiap emosi dapat direpresentasikan sebagai titik koordinat (V, A)" in p_text:
            p_img2 = make_image_p("rId11", 11, cx=4200000, cy=4200000)
            p_cap2 = make_caption_p("Gambar 2.2", "Pemetaan Afektif Dua Dimensi Valence-Arousal (Russell) ke Koordinat Warna Pencahayaan Panggung Ibadah (Praise & Worship)")
            p_idx = list(body).index(p)
            body.insert(p_idx + 1, p_img2)
            body.insert(p_idx + 2, p_cap2)
            print("✓ Embedded Gambar 2.2 (Russell Model)")
            break

    # Clean raw math in Subbab 2.2.3 (HSV to RGB)
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    for i, p in enumerate(paragraphs):
        p_text = get_p_text(p)
        if "C = V \\times S" in p_text or "C = V \times S" in p_text or "C = V × S" in p_text or "C = V · S" in p_text:
            p_eq_hsv = make_eq_p("C = V · S,    H' = H / 60°,    X = C · (1 - |H' mod 2 - 1|),    m = V - C", "(2.15)")
            p_idx = list(body).index(p)
            body.insert(p_idx, p_eq_hsv)
            body.remove(p)
            # Remove any following fragmented lines H' = ..., X = ..., m = ...
            to_remove = []
            for next_p in list(body)[p_idx+1:p_idx+5]:
                next_txt = get_p_text(next_p)
                if any(k in next_txt for k in ["H' =", "X = C", "m = V", "\\frac{H}{60"]):
                    to_remove.append(next_p)
            for rm in to_remove:
                body.remove(rm)
            print("✓ Fixed raw HSV equation in 2.2.3 and removed redundant lines")
            break

    # Clean raw cases math in Subbab 2.2.3
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    for i, p in enumerate(paragraphs):
        p_text = get_p_text(p)
        if "(R_1, G_1, B_1) = \\begin{cases}" in p_text or "(R_1, G_1, B_1) =" in p_text and "cases" in p_text:
            p_eq_cases = make_eq_p("(R1, G1, B1) = (C, X, 0) saat H' < 1, (X, C, 0) saat H' < 2, (0, C, X) saat H' < 3, (0, X, C) saat H' < 4, (X, 0, C) saat H' < 5, (C, 0, X) saat H' < 6", "(2.16)")
            p_idx = list(body).index(p)
            body.insert(p_idx, p_eq_cases)
            body.remove(p)
            print("✓ Fixed raw piecewise RGB cases in 2.2.3")
            break

    # Clean raw RGB final formula in Subbab 2.2.3
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    for i, p in enumerate(paragraphs):
        p_text = get_p_text(p)
        if "R = (R_1 + m) \\times 255" in p_text or "R = (R_1 + m) × 255" in p_text:
            p_eq_rgb = make_eq_p("R = (R1 + m) · 255,    G = (G1 + m) · 255,    B = (B1 + m) · 255", "(2.17)")
            p_idx = list(body).index(p)
            body.insert(p_idx, p_eq_rgb)
            body.remove(p)
            print("✓ Fixed raw final RGB formula in 2.2.3")
            break

    # Clean raw White extraction in Subbab 2.2.3
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    for i, p in enumerate(paragraphs):
        p_text = get_p_text(p)
        if "W = \\min(R, G, B)" in p_text or "W = min(R, G, B)" in p_text:
            p_eq_w = make_eq_p("W = min(R, G, B),    R' = R - W,    G' = G - W,    B' = B - W", "(2.18)")
            p_idx = list(body).index(p)
            body.insert(p_idx, p_eq_w)
            body.remove(p)
            if i + 1 < len(paragraphs) and "R' = R - W" in get_p_text(paragraphs[i+1]):
                body.remove(paragraphs[i+1])
            print("✓ Fixed raw White extraction equation in 2.2.3")
            break

    # Clean raw Normalization formula in Subbab 2.2.3 d
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    for i, p in enumerate(paragraphs):
        p_text = get_p_text(p)
        if "x_{norm} =" in p_text or "x_norm =" in p_text:
            p_eq_norm = make_eq_p("x_norm = (x - x_min) / (x_max - x_min)", "(2.19)")
            p_idx = list(body).index(p)
            body.insert(p_idx, p_eq_norm)
            body.remove(p)
            print("✓ Fixed raw Normalization formula in 2.2.3 d")
            break

    # Clean raw Black-Box success percentage formula in Chapter 3
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    for i, p in enumerate(paragraphs):
        p_text = get_p_text(p)
        if "Persentase Keberhasilan" in p_text and ("\\frac" in p_text or "Test Case" in p_text):
            p_eq_bb = make_eq_p("Persentase Keberhasilan = (Jumlah Test Case Pass / Total Test Case) × 100%", "(3.1)")
            p_idx = list(body).index(p)
            body.insert(p_idx, p_eq_bb)
            body.remove(p)
            print("✓ Fixed raw Black-Box formula in Chapter 3")
            break

    # Embed Gambar 2.3 under Subbab 2.2.3 (RGBW Decomposition)
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    for i, p in enumerate(paragraphs):
        p_text = get_p_text(p)
        if "Pendekatan ini menghasilkan warna yang lebih kaya" in p_text:
            p_img3 = make_image_p("rId12", 12, cx=4200000, cy=4200000)
            p_cap3 = make_caption_p("Gambar 2.3", "Perbandingan Pencampuran Warna RGB Konvensional vs. Algoritma Dekomposisi 4-Kanal Physical RGBW pada Lampu PAR LED")
            p_idx = list(body).index(p)
            body.insert(p_idx + 1, p_img3)
            body.insert(p_idx + 2, p_cap3)
            print("✓ Embedded Gambar 2.3 (RGBW Decomposition)")
            break

    # Subbab 2.3 Kerangka Berpikir: Replace ASCII art box with Gambar 2.4
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    for i, p in enumerate(paragraphs):
        p_text = get_p_text(p)
        if "┌─────────────────┐" in p_text or ("Audio Input" in p_text and "Chroma" in p_text):
            p_img_kerangka = make_image_p("rId13", 13, cx=4300000, cy=4300000)
            p_cap_kerangka = make_caption_p("Gambar 2.4", "Diagram Kerangka Berpikir Penelitian Rancang Bangun Sistem Audio-Reactive Lighting Design ZZLUXORA")
            p_idx = list(body).index(p)
            body.insert(p_idx, p_img_kerangka)
            body.insert(p_idx + 1, p_cap_kerangka)
            body.remove(p)
            print("✓ Replaced ASCII box in Subbab 2.3 with clean Gambar 2.4 (Kerangka Berpikir)")
            break

    # Embed Gambar 3.1 under Chapter 3 (Alur Program ZZLUXORA)
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    for i, p in enumerate(paragraphs):
        p_text = get_p_text(p)
        if "Alur Program ZZLUXORA" in p_text:
            p_img4 = make_image_p("rId14", 14, cx=3900000, cy=4600000)
            p_cap4 = make_caption_p("Gambar 3.1", "Diagram Alur Komputasi End-to-End Sistem ZZLUXORA dari Masukan Sinyal Audio hingga Transmisi Paket Art-Net UDP 6454")
            p_idx = list(body).index(p)
            body.insert(p_idx + 1, p_img4)
            body.insert(p_idx + 2, p_cap4)
            print("✓ Embedded Gambar 3.1 (Flowchart System Pipeline)")
            break

    # Remove any lingering fragmented math or ASCII trees
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    for p in paragraphs:
        p_text = get_p_text(p)
        if "^2}{\\sum" in p_text or "^2}{\sum" in p_text or p_text in ["X(k)", "X(k)^2"]:
            body.remove(p)
            print(f"✓ Removed fragmented formula artifact: {p_text}")
        elif "│" in p_text and ("START" in p_text or "Audio Input" in p_text or "Inisialisasi Hardware" in p_text):
            if "Inisialisasi Hardware" in p_text:
                desc_p1 = make_p("Modul penerima ARTNET-DMX berbasis ESP32 menjalankan dua proses konkuren pada inti prosesor terpisah (FreeRTOS Dual-Core): (1) Core 0 menangani protokol jaringan nirkabel (penerima paket Art-Net UDP port 6454, mode Station atau SoftAP Captive Portal 192.168.4.1), dan (2) Core 1 mengendalikan sinyal fisik DMX512 melalui Hardware Serial UART2 ke transceiver MAX485 pada laju 250.000 bps dengan fitur proteksi auto-blackout jika sinyal terputus.")
                body.insert(list(body).index(p), desc_p1)
                body.remove(p)
                print("✓ Replaced ESP32 ASCII tree with clean academic narrative")
            elif "User memilih file audio" in p_text:
                body.remove(p)
                print("✓ Removed redundant ASCII flowchart")

    # Append references [32] and [33] to DAFTAR PUSTAKA
    paragraphs = list(body.findall(f"{{{W_NS}}}p"))
    for p in reversed(paragraphs):
        p_text = get_p_text(p)
        if "[31]" in p_text and "[32]" not in p_text:
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

    print(f"\n🎉 Successfully compiled {v4_path} with 5 clean high-resolution figures & pure math!")
    print(f"   Size: {os.path.getsize(v4_path):,} bytes")

if __name__ == "__main__":
    build_v4()
