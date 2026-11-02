"""Sinh sổ tay Colab từ tools/vast/cells.py (không kèm kết quả, để học viên tự chạy và tự khám phá)."""
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
from cells import CELLS  # noqa: E402

OUT = ROOT / "vastopolis-dieu-tra-dich-benh.ipynb"

cells = []
for cid, kind, text in CELLS:
    if kind == "md":
        cells.append(new_markdown_cell(text))
    else:
        c = new_code_cell(text)
        c.metadata["id"] = cid
        cells.append(c)

nb = new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
nb.metadata["language_info"] = {"name": "python"}
nb.metadata["colab"] = {"name": OUT.name, "provenance": []}
nbformat.validate(nb)
nbformat.write(nb, OUT)
n_code = sum(1 for c in cells if c.cell_type == "code")
print(f"{OUT.name}: {len(cells)} ô ({n_code} ô mã, {len(cells) - n_code} ô văn bản), không có kết quả đính kèm")
