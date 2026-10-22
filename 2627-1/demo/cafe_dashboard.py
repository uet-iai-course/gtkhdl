"""Dashboard đối chiếu cho prompt vibe coding ở bài 1.

Đọc cafe_90_ngay.csv, loại dòng lỗi, tính doanh thu và vẽ dashboard 2×2.
Chỉ dùng pandas và matplotlib. Mọi số trên hình đều tính từ tệp.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "cafe_90_ngay.csv"
OUT = ROOT / "dashboard.png"


def load_and_audit(path: Path) -> tuple[pd.DataFrame, dict]:
    raw = pd.read_csv(path)
    n_raw = len(raw)
    df = raw.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["hour"] = pd.to_numeric(df["hour"], errors="coerce")
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce")
    df["unit_price_vnd"] = pd.to_numeric(df["unit_price_vnd"], errors="coerce")

    ok = (
        df["date"].notna()
        & df["hour"].between(0, 23)
        & df["qty"].ge(1)
        & df["unit_price_vnd"].gt(0)
        & df["product"].notna()
        & df["pay"].isin(["cash", "momo"])
    )
    clean = df.loc[ok].copy()
    clean["revenue"] = clean["qty"] * clean["unit_price_vnd"]
    audit = {
        "n_raw": n_raw,
        "n_drop": int((~ok).sum()),
        "revenue": int(clean["revenue"].sum()),
    }
    return clean, audit


def draw(clean: pd.DataFrame, audit: dict, dest: Path) -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    ink = "#221D3D"
    blue = "#2A7291"
    orange = "#E8890C"
    green = "#2E8B57"
    purple = "#6D4AA8"
    fig, axes = plt.subplots(2, 2, figsize=(11.2, 6.4), dpi=140)
    fig.patch.set_facecolor("#FFFcf7")
    for ax in axes.ravel():
        ax.set_facecolor("#FFFcf7")
        ax.tick_params(colors=ink, labelsize=8)
        for spine in ax.spines.values():
            spine.set_color("#E4DDD0")

    week = clean.copy()
    week["week"] = week["date"].dt.to_period("W-SUN").dt.start_time
    by_week = week.groupby("week")["revenue"].sum().sort_index() / 1_000_000
    axes[0, 0].plot(by_week.index, by_week.values, color=blue, marker="o", linewidth=2)
    axes[0, 0].set_title("Doanh thu theo tuần", color=ink, fontsize=12, loc="left")
    axes[0, 0].set_ylabel("triệu đồng")
    axes[0, 0].tick_params(axis="x", labelrotation=30)

    by_product = (
        clean.groupby("product")["revenue"].sum().sort_values(ascending=True) / 1_000_000
    )
    axes[0, 1].barh(by_product.index, by_product.values, color=orange)
    axes[0, 1].set_title("Doanh thu theo món", color=ink, fontsize=12, loc="left")
    axes[0, 1].set_xlabel("triệu đồng")

    by_hour = clean.groupby("hour")["revenue"].sum().reindex(range(24), fill_value=0) / 1_000_000
    axes[1, 0].bar(by_hour.index, by_hour.values, color=green)
    axes[1, 0].set_title("Doanh thu theo giờ", color=ink, fontsize=12, loc="left")
    axes[1, 0].set_xlabel("giờ")
    axes[1, 0].set_ylabel("triệu đồng")

    by_pay = clean.groupby("pay")["revenue"].sum() / 1_000_000
    colors = {"cash": purple, "momo": blue}
    axes[1, 1].bar(
        by_pay.index.map({"cash": "Tiền mặt", "momo": "MoMo"}),
        by_pay.values,
        color=[colors[k] for k in by_pay.index],
    )
    axes[1, 1].set_title("Doanh thu theo kênh", color=ink, fontsize=12, loc="left")
    axes[1, 1].set_ylabel("triệu đồng")

    total_m = audit["revenue"] / 1_000_000
    fig.suptitle(
        f"Quán cà phê 90 ngày  ·  {total_m:.1f} triệu đồng  ·  loại {audit['n_drop']} dòng / {audit['n_raw']}",
        fontsize=13,
        color=ink,
        x=0.02,
        ha="left",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(dest, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    clean, audit = load_and_audit(SRC)
    # Bốn cách cộng phải trùng một tổng.
    checks = [
        int(clean.groupby(clean["date"].dt.to_period("W"))["revenue"].sum().sum()),
        int(clean.groupby("product")["revenue"].sum().sum()),
        int(clean.groupby("hour")["revenue"].sum().sum()),
        int(clean.groupby("pay")["revenue"].sum().sum()),
    ]
    if len(set(checks)) != 1:
        raise SystemExit(f"Tổng lệch nhau: {checks}")
    draw(clean, audit, OUT)
    print(f"dong_goc={audit['n_raw']}")
    print(f"dong_loai={audit['n_drop']}")
    print(f"tong_doanh_thu_vnd={audit['revenue']}")
    print(f"anh={OUT}")


if __name__ == "__main__":
    main()
