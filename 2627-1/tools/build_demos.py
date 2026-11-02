"""Tách tools/demos_src.py thành tệp .py, chạy từng tệp, lưu kết quả vào tools/demos/out/."""
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from demos_src import DEMOS  # noqa: E402

root = Path(__file__).parent / "demos"
out = root / "out"
out.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")

for name, code in DEMOS.items():
    src = root / f"{name}.py"
    src.write_text(code.strip("\n") + "\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(src)], capture_output=True, text=True, encoding="utf-8", env=env, cwd=root)
    (out / f"{name}.txt").write_text(r.stdout, encoding="utf-8")
    status = "OK" if r.returncode == 0 else f"LỖI\n{r.stderr[-600:]}"
    print(f"{name}: {status} ({len(r.stdout.splitlines())} dòng)")
