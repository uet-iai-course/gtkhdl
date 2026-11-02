"""Chạy toàn bộ các ô trong cells.py trên dữ liệu thật.

Kết quả:
  tools/demos/vast_<id>.py        mã nguồn của ô (để slide trích dẫn)
  tools/demos/out/vast_<id>.txt   kết quả in ra khi chạy
  img/vast/<id>[_k].png           mỗi lần gọi plt.show() lưu một hình
Chạy:  python tools/vast/run_cells.py [id_cuối]
"""
import contextlib
import io
import os
import sys
import time
import traceback
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
from cells import CELLS  # noqa: E402

DEMOS = ROOT / "tools" / "demos"
OUT = DEMOS / "out"
IMG = ROOT / "img" / "vast"
for p in (DEMOS, OUT, IMG):
    p.mkdir(parents=True, exist_ok=True)

warnings.filterwarnings("ignore")
stop_after = sys.argv[1] if len(sys.argv) > 1 else None
os.chdir(ROOT / "data" / "vast")

state = {"cid": None, "k": 0}


def save_show(*a, **k):
    fig = plt.gcf()
    name = state["cid"] + (f"_{state['k']}" if state["k"] else "")
    fig.savefig(IMG / f"{name}.png", dpi=150, facecolor="white", bbox_inches="tight")
    state["k"] += 1
    plt.close(fig)


plt.show = save_show
g = {"__name__": "__vast__", "display": print}

for cid, kind, text in CELLS:
    if kind == "md":
        continue
    state["cid"], state["k"] = cid, 0
    if kind == "code":
        (DEMOS / f"vast_{cid}.py").write_text(text + "\n", encoding="utf-8")
    buf = io.StringIO()
    t0 = time.time()
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(text, f"<{cid}>", "exec"), g)
    except Exception:
        print(buf.getvalue())
        traceback.print_exc()
        sys.exit(f"LỖI ở ô {cid}")
    if kind == "code":
        (OUT / f"vast_{cid}.txt").write_text(buf.getvalue(), encoding="utf-8")
    print(f"{cid}: {time.time() - t0:5.1f}s, {len(buf.getvalue().splitlines())} dòng, {state['k']} hình")
    if stop_after and cid == stop_after:
        break

for gif in Path.cwd().glob("*.gif"):          # ảnh động do ô mã tạo ra
    (IMG / gif.name).write_bytes(gif.read_bytes())
