"""Ghép các mảnh slide trong tools/slides/<bài>/ thành tệp HTML hoàn chỉnh.

Chạy:  python tools/build_slides.py            (cả bài 3 và bài 4)
       python tools/build_slides.py bai-03

Chỗ giữ chỗ trong mảnh:
  {{code:tên}} / {{code:tên|a-b}}   mã nguồn thật trong tools/demos (tùy chọn lấy dòng a..b), lớp CSS thêm bằng |cls=sm
  {{out:tên}} / {{out:tên|n}}       kết quả thật khi chạy mã, n dòng đầu
  {{i:khóa}}                        đường dẫn ảnh đã tải (tools/image_credits.json)
  {{pf:khóa|Tên|chú thích}}         <figure> chân dung kèm chú thích và giấy phép
  {{cap:khóa|mô tả}}               nội dung <figcaption> kèm giấy phép
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
CREDITS = json.loads((TOOLS / "image_credits.json").read_text("utf-8"))

DECKS = {
    "bai-03": {
        "out": "bai-03-toan-hoc-trong-khoa-hoc-du-lieu-phan-1.html",
        "title": "Khoa học dữ liệu | Bài 3: Toán học trong khoa học dữ liệu (phần 1)",
        "footer": "Giới thiệu khoa học dữ liệu · Bài 3: Toán học trong khoa học dữ liệu (phần 1)",
    },
    "bai-04": {
        "out": "bai-04-toan-hoc-trong-khoa-hoc-du-lieu-phan-2.html",
        "title": "Khoa học dữ liệu | Bài 4: Toán học trong khoa học dữ liệu (phần 2)",
        "footer": "Giới thiệu khoa học dữ liệu · Bài 4: Toán học trong khoa học dữ liệu (phần 2)",
    },
}

HEAD = """<!doctype html>
<html lang="vi">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>{title}</title>
  <link rel="stylesheet" href="revealjs/dist/reset.css">
  <link rel="stylesheet" href="revealjs/dist/reveal.css">
  <link rel="stylesheet" href="revealjs/dist/theme/white.css">
  <link rel="stylesheet" href="plugin/highlight/zenburn.css">
  <link rel="stylesheet" href="lecture-style.css">
  <link rel="stylesheet" href="lecture-03.css?v=3">
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
</head>

<body>
  <div class="reveal">
    <div class="slides">
"""

FOOT = """
      <div class="footer">
        {footer}
      </div>
    </div>
  </div>

  <script src="revealjs/dist/reveal.js"></script>
  <script src="plugin/highlight/highlight.js"></script>
  <script src="plugin/math/math.js"></script>
  <script>
    Reveal.initialize({{
      controlsLayout: "edges",
      slideNumber: true,
      hash: true,
      hashOneBasedIndex: true,
      katex: {{ local: "plugin/katex" }},
      plugins: [RevealHighlight, RevealMath.KaTeX],
      width: 1100,
      height: 700,
      margin: 0.04
    }});
  </script>
</body>

</html>
"""

LICENSE_VI = {
    "Public domain": "Phạm vi công cộng",
}


def lic(key):
    c = CREDITS[key]
    l = c["license"]
    return LICENSE_VI.get(l, l)


def credit_line(key):
    c = CREDITS[key]
    l = lic(key)
    parts = []
    if l != "Phạm vi công cộng" and c["artist"]:
        parts.append(re.sub(r"\s+", " ", c["artist"])[:60])
    parts.append(l)
    return ", ".join(parts) + f', <a href="{c["page"]}" target="_blank" rel="noopener">Wikimedia Commons</a>'


def img_path(key):
    c = CREDITS[key]
    return f"img/{c['folder']}/{c['file']}"


def sub(match):
    kind, rest = match.group(1), match.group(2)
    args = rest.split("|")
    name = args[0]
    if kind == "i":
        return img_path(name)
    if kind == "cap":
        return f"{args[1]}. {credit_line(name)}"
    if kind == "pf":
        who = args[1]
        extra = args[2] if len(args) > 2 else ""
        extra = (extra + "<br>") if extra else ""
        return (f'<figure><img src="{img_path(name)}" alt="{html.escape(who)}">'
                f'<figcaption><b>{who}</b>{extra}{credit_line(name)}</figcaption></figure>')
    if kind == "code":
        text = (TOOLS / "demos" / f"{name}.py").read_text("utf-8").rstrip("\n")
        cls = "lab"
        for a in args[1:]:
            if a.startswith("cls="):
                cls = a[4:]
            elif re.fullmatch(r"\d+-\d+", a):
                s, e = map(int, a.split("-"))
                text = "\n".join(text.splitlines()[s - 1:e])
        return f'<pre class="demo-code {cls}"><code class="language-python" data-trim>\n{html.escape(text)}\n</code></pre>'
    if kind == "out":
        lines = (TOOLS / "demos" / "out" / f"{name}.txt").read_text("utf-8").rstrip("\n").splitlines()
        cls = ""
        n = None
        for a in args[1:]:
            if a.startswith("cls="):
                cls = " " + a[4:]
            elif a.isdigit():
                n = int(a)
            elif re.fullmatch(r"\d+-\d+", a):
                s, e = map(int, a.split("-"))
                lines = lines[s - 1:e]
        tail = 0
        for a in args[1:]:
            if a.startswith("tail="):
                tail = int(a[5:])
        if n is not None and len(lines) > n + tail:
            lines = lines[:n] + ["…"] + (lines[-tail:] if tail else [])
        return f'<pre class="result-out{cls}">{html.escape(chr(10).join(lines))}</pre>'
    raise ValueError(kind)


PLACEHOLDER = re.compile(r"\{\{(code|out|i|pf|cap):([^}]*)\}\}")


def build(deck):
    cfg = DECKS[deck]
    parts = sorted((TOOLS / "slides" / deck).glob("*.html"))
    body = "\n".join(p.read_text("utf-8") for p in parts)
    body = PLACEHOLDER.sub(sub, body)
    leftovers = re.findall(r"\{\{[^}]*\}\}", body)
    if leftovers:
        raise SystemExit(f"Còn chỗ giữ chỗ chưa thay: {leftovers[:5]}")
    text = HEAD.format(title=cfg["title"]) + body + FOOT.format(footer=cfg["footer"])
    (ROOT / cfg["out"]).write_text(text, "utf-8")
    n = len(re.findall(r"<section", body)) - len(re.findall(r"<section>\s*<section", body))
    print(f"{cfg['out']}: {len(parts)} mảnh, {len(text.splitlines())} dòng")


if __name__ == "__main__":
    targets = sys.argv[1:] or list(DECKS)
    for d in targets:
        build(d)
