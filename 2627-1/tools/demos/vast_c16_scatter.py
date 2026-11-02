from datetime import date

ngay19 = df[df["ngay"] == date(2011, 5, 19)]
ten = {"flu": "giống cúm", "gi": "dạ dày - ruột"}

fig, axes = plt.subplots(1, 2, figsize=(12, 4.3))
for ax, cot, mau in zip(axes, ["flu", "gi"], [FLU, GI]):
    d = ngay19[ngay19[cot]]
    base_map(ax, 0.35)
    ax.scatter(d["lon"], d["lat"], s=1.5, c=mau, alpha=0.4)
    ax.set_title(f"{ten[cot]}: {len(d):,} bài ngày 19/5")
    print(ten[cot], len(d), "bài")
plt.tight_layout()
plt.show()
