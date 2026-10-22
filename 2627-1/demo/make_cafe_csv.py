"""Tạo cafe_90_ngay.csv: hóa đơn giả lập 90 ngày, có vài dòng lỗi để prompt phải lọc."""

from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / "cafe_90_ngay.csv"
RNG = np.random.default_rng(20261022)

PRODUCTS = {
    "Cà phê sữa": 29000,
    "Bạc xỉu": 32000,
    "Trà đào": 35000,
    "Bánh mì": 20000,
    "Nước suối": 10000,
}
# Trọng số theo giờ: sáng và trưa đông hơn.
HOUR_WEIGHT = np.array(
    [1, 1, 1, 1, 1, 2, 6, 10, 9, 5, 4, 8, 9, 6, 4, 4, 5, 6, 4, 3, 2, 2, 1, 1],
    dtype=float,
)
HOUR_WEIGHT /= HOUR_WEIGHT.sum()


def main() -> None:
    rows = []
    start = pd.Timestamp("2026-01-05")
    for offset in range(90):
        day = start + pd.Timedelta(days=offset)
        weekend = day.day_of_week >= 5
        n_bills = int(RNG.integers(8, 13) + (3 if weekend else 0))
        for _ in range(n_bills):
            hour = int(RNG.choice(24, p=HOUR_WEIGHT))
            n_items = int(RNG.integers(1, 4))
            for _item in range(n_items):
                product = RNG.choice(list(PRODUCTS))
                qty = int(RNG.integers(1, 4))
                rows.append(
                    {
                        "date": day.strftime("%Y-%m-%d"),
                        "hour": hour,
                        "product": product,
                        "qty": qty,
                        "unit_price_vnd": PRODUCTS[product],
                        "pay": "momo" if RNG.random() < 0.62 else "cash",
                    }
                )
    df = pd.DataFrame(rows)
    # Ba dòng hỏng có chủ đích, để bước kiểm tra phải phát hiện.
    bad = pd.DataFrame(
        [
            {"date": "2026-02-01", "hour": 25, "product": "Cà phê sữa", "qty": 1, "unit_price_vnd": 29000, "pay": "cash"},
            {"date": "2026-02-02", "hour": 9, "product": "Bạc xỉu", "qty": 0, "unit_price_vnd": 32000, "pay": "momo"},
            {"date": "không-phải-ngày", "hour": 8, "product": "Trà đào", "qty": 1, "unit_price_vnd": 35000, "pay": "momo"},
        ]
    )
    pd.concat([df, bad], ignore_index=True).to_csv(OUT, index=False)
    print(f"{len(df) + len(bad)} dòng -> {OUT}")


if __name__ == "__main__":
    main()
