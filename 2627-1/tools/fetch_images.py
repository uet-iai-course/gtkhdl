"""Tải ảnh từ Wikimedia Commons cho bài 3 và bài 4, ghi lại nguồn và giấy phép.

Chạy:  python tools/fetch_images.py [khóa ...]
Kết quả: img/lec03/*, img/lec04/*, và tools/image_credits.json
"""
import html
import json
import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "gtkhdl-lecture-slides/1.0 (university lecture slides; non-commercial)"}
API = "https://commons.wikimedia.org/w/api.php"
SESSION = requests.Session()
SESSION.headers.update(UA)

# khóa: (thư mục, [tên file ứng viên], từ khóa tìm kiếm dự phòng, độ rộng thumbnail)
ITEMS = {
    # ---- Bài 3, phần I: xác suất, thống kê
    "bernoulli": ("lec03", ["Jakob Bernoulli.jpg"], "Jakob Bernoulli portrait", 500),
    "ars-conjectandi": ("lec03", ["Bernoulli - Ars conjectandi, 1713 - 058.tif"], "Ars Conjectandi 1713 title page", 600),
    "bayes": ("lec03", ["Thomas Bayes.gif"], "Thomas Bayes portrait", 500),
    "legendre": ("lec03", ["Legendre.jpg"], "Legendre caricature portrait", 500),
    "laplace": ("lec03", ["Pierre-Simon Laplace.jpg"], "Pierre-Simon Laplace portrait", 500),
    "galton": ("lec03", ["Francis Galton 1850s.jpg"], "Francis Galton portrait", 500),
    "gosset": ("lec03", ["William Sealy Gosset.jpg"], "William Sealy Gosset Student portrait", 500),
    "fisher": ("lec03", ["Youngronaldfisher2.JPG"], "Ronald Fisher young portrait", 500),
    "kolmogorov": ("lec03", ["Kolmogorov.jpg"], "Andrey Kolmogorov portrait", 500),
    "efron": ("lec03", ["Bradley Efron National Medal of Science 2007 (cropped).jpg"], "Bradley Efron", 500),
    # ---- Bài 3, phần II: đại số tuyến tính
    "nine-chapters": ("lec03", ["九章算術細草圖說.jpg"], "Nine Chapters on the Mathematical Art", 600),
    "sylvester": ("lec03", ["James Joseph Sylvester.jpg"], "James Joseph Sylvester portrait", 500),
    "cayley": ("lec03", ["Arthur Cayley.jpg"], "Arthur Cayley portrait", 500),
    "weyl": ("lec03", ["Hermann Weyl ETH-Bib Portr 00890.jpg"], "Hermann Weyl portrait", 500),
    "von-neumann": ("lec03", ["JohnvonNeumann-LosAlamos.gif"], "John von Neumann Los Alamos", 500),
    "pca-scatter": ("lec03", ["GaussianScatterPCA.svg"], "GaussianScatterPCA", 700),
    "svd": ("lec03", ["Singular-Value-Decomposition.svg"], "Singular value decomposition", 700),
    # ---- Bài 3, phần III: giải tích
    "archimedes": ("lec03", ["Domenico-Fetti Archimedes 1620.jpg"], "Archimedes Domenico Fetti", 500),
    "newton": ("lec03", ["Portrait of Sir Isaac Newton, 1689.jpg"], "Isaac Newton Kneller 1689 portrait", 500),
    "leibniz": ("lec03", ["Gottfried Wilhelm Leibniz, Bernhard Christoph Francke.jpg"], "Leibniz Francke portrait", 500),
    "euler": ("lec03", ["Leonhard Euler.jpg"], "Leonhard Euler Handmann portrait", 500),
    "lagrange": ("lec03", ["Lagrange portrait.jpg"], "Joseph-Louis Lagrange portrait", 500),
    "cauchy": ("lec03", ["Augustin-Louis Cauchy 1901.jpg"], "Augustin-Louis Cauchy portrait", 500),
    "weierstrass": ("lec03", ["Karl Weierstrass x Rudolf von Voigtländer.jpg"], "Karl Weierstrass portrait", 500),
    "tangent": ("lec03", ["Tangent to a curve.svg"], "Tangent to a curve", 600),
    "integral": ("lec03", ["Integral example.svg"], "Integral example svg", 600),
    # ---- Bài 3, phần IV: tối ưu hóa
    "dantzig": ("lec03", ["George B. Dantzig at National Medal of Science Awards Ceremony, 1976 2.webp","George B Dantzig 1936.jpg"], "George Dantzig", 500),
    "bellman": ("lec03", ["Richard Ernest Bellman.jpg"], "Richard Bellman", 500),
    "boyd": ("lec03", ["Stephen Boyd.jpg"], "Stephen P. Boyd Stanford", 500),
    # ---- Bài 4, phần V: đồ thị
    "konigsberg": ("lec04", ["Konigsberg bridges.png"], "Königsberg bridges map", 600),
    "erdos": ("lec04", ["Erdos budapest fall 1992 (cropped).jpg","Paul Erdős.jpg"], "Paul Erdős portrait", 500),
    "renyi": ("lec04", ["Alfred Kato Renyi.jpg"], "Alfréd Rényi", 500),
    "page-brin": ("lec04", ["Google page brin.jpg"], "Larry Page Sergey Brin", 600),
    "pagerank": ("lec04", ["PageRanks-Example.svg"], "PageRanks-Example", 700),
    "dijkstra": ("lec04", ["Dijkstras progress animation.gif"], "Dijkstra's algorithm animation", 600),
    "social-network": ("lec04", ["Social Network Analysis Visualization.png"], "Social network analysis visualization", 700),
    # ---- Bài 4, phần VI: lý thuyết thông tin
    "hartley": ("lec04", ["Hartley ralph-vinton-lyon-001.jpg"], "Ralph V. L. Hartley", 500),
    "wiener": ("lec04", ["Norbert wiener.jpg"], "Norbert Wiener portrait", 500),
    "binary-entropy": ("lec04", ["Binary entropy plot.svg"], "Binary entropy plot", 600),
    "bell-labs": ("lec04", ["Nokia Bell Labs Murray Hill, NJ.jpg"], "Bell Labs Holmdel", 700),
    # ---- Bài 4, phần VII: toán học tính toán
    "plimpton": ("lec04", ["Plimpton 322.jpg"], "Plimpton 322 tablet", 600),
    "eniac-beck": ("lec04", ["Glen Beck and Betty Snyder program the ENIAC in building 328 at the Ballistic Research Laboratory.jpg"], "ENIAC Glen Beck Betty Snyder", 700),
    "fortran-card": ("lec04", ["FortranCardPROJ039.agr.jpg"], "Fortran punched card", 600),
    "gpu": ("lec04", ["NVidia GeForce 6600GT AGP with GPU 2009-01-27.jpg"], "NVIDIA GPU graphics card", 700),
    "hamming": ("lec04", ["Richard Hamming.jpg"], "Richard Hamming", 500),
    "forsythe": ("lec04", ["George E. Forsythe.jpg"], "George E. Forsythe", 500),
    "ieee754": ("lec04", ["IEEE 754 Double Floating Point Format.svg"], "IEEE 754 double floating point format", 800),
    # ---- Bài 4, phần VIII: hình học, tô pô
    "riemann": ("lec04", ["Georg Friedrich Bernhard Riemann.jpeg"], "Bernhard Riemann portrait", 500),
    "poincare": ("lec04", ["Henri Poincaré-2.jpg"], "Henri Poincaré portrait", 500),
    "edelsbrunner": ("lec04", ["Herbert Edelsbrunner SoCG 2011.jpg"], "Herbert Edelsbrunner", 500),
    "carlsson": ("lec04", ["Gunnar Carlsson.jpg"], "Gunnar Carlsson", 500),
    "mobius": ("lec04", ["Möbius strip.jpg"], "Möbius strip", 600),
    "knn": ("lec04", ["KnnClassification.svg"], "KnnClassification", 600),
    # ---- tổng kết
    "neural-net": ("lec04", ["Colored neural network.svg"], "Colored neural network", 600),
    "shannon": ("lec04", ["Claude Shannon 1958 MIT portrait cropped.jpg","C.E. Shannon. Tekniska museet 43069 (cropped).jpg"], "Claude Shannon", 500),
    "turing": ("lec04", ["Alan Turing (1951) (crop).jpg","Alan Turing (1912-1954) in 1936 at Princeton University.jpg"], "Alan Turing", 500),
    "dijkstra-person": ("lec04", ["Edsger Wybe Dijkstra.jpg","Edsger Dijkstra 1994.jpg"], "Edsger Dijkstra", 500),
    "pytorch": ("lec04", ["PyTorch logo icon.svg"], "PyTorch logo icon", 300),
}


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def get(url, **kw):
    """GET có chờ khi bị giới hạn tốc độ (429)."""
    for attempt in range(8):
        r = SESSION.get(url, timeout=120, **kw)
        if r.status_code == 429 or r.status_code >= 500:
            wait = int(r.headers.get("Retry-After", 0) or 0) or 10 * (attempt + 1)
            print(f"   ... {r.status_code}, chờ {wait}s")
            time.sleep(wait)
            continue
        return r
    return r


def api(params):
    for attempt in range(6):
        r = get(API, params=params)
        try:
            return r.json()
        except ValueError:
            time.sleep(8 * (attempt + 1))
    raise RuntimeError("API không trả JSON: " + r.text[:200])


def info_for(title, width):
    j = api({
        "action": "query", "titles": "File:" + title, "prop": "imageinfo",
        "iiprop": "url|extmetadata|size|mime", "iiurlwidth": width, "format": "json", "redirects": 1,
    })
    page = next(iter(j["query"]["pages"].values()))
    if "imageinfo" not in page:
        return None
    return page["title"], page["imageinfo"][0]


def search(q):
    j = api({"action": "query", "list": "search", "srsearch": q, "srnamespace": 6, "srlimit": 5, "format": "json"})
    return [h["title"].removeprefix("File:") for h in j["query"]["search"]]


def main():
    only = set(sys.argv[1:])
    credits_path = ROOT / "tools" / "image_credits.json"
    credits = json.loads(credits_path.read_text("utf-8")) if credits_path.exists() else {}
    for key, (folder, cands, query, width) in ITEMS.items():
        if only and key not in only:
            continue
        if key in credits and (ROOT / "img" / folder / credits[key]["file"]).exists():
            continue
        got = None
        for t in cands:
            got = info_for(t, width)
            if got:
                break
        if not got:
            print(f"[{key}] không thấy {cands}; gợi ý: {search(query)}")
            continue
        title, ii = got
        meta = ii.get("extmetadata", {})
        mime = ii["mime"]
        keep_original = mime in ("image/svg+xml", "image/gif") or ii["width"] <= width
        url = ii["url"] if keep_original else ii["thumburl"]
        ext = Path(url.split("?")[0]).suffix.lower()
        out = ROOT / "img" / folder / f"{key}{ext}"
        out.parent.mkdir(parents=True, exist_ok=True)
        if not out.exists():
            resp = get(url)
            if resp.status_code != 200:
                print(f"[{key}] tải lỗi {resp.status_code} {url}")
                continue
            out.write_bytes(resp.content)
            time.sleep(3.0)
        credits[key] = {
            "file": out.name,
            "folder": folder,
            "commons_title": title,
            "page": ii["descriptionurl"],
            "artist": strip(meta.get("Artist", {}).get("value")),
            "license": strip(meta.get("LicenseShortName", {}).get("value")),
            "date": strip(meta.get("DateTimeOriginal", {}).get("value")),
            "description": strip(meta.get("ImageDescription", {}).get("value"))[:200],
            "bytes": out.stat().st_size,
        }
        credits_path.write_text(json.dumps(credits, ensure_ascii=False, indent=1), "utf-8")
        print(f"[{key}] OK {title} | {credits[key]['license']} | {credits[key]['artist'][:50]} | {out.stat().st_size // 1024} KB")
        time.sleep(1.5)


if __name__ == "__main__":
    main()
