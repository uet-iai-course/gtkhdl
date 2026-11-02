def thoi_diem_bat_dau(cot, so_lan=5):
    gio = df.groupby(df["t"].dt.floor("h"))[cot].sum()
    nen_gio = gio.iloc[: 14 * 24]
    nguong = nen_gio.mean() + so_lan * nen_gio.std()
    vuot = gio[gio > nguong]
    return vuot.index[0], round(nguong)


for cot, ten in [("flu", "giống cúm"), ("gi", "dạ dày - ruột")]:
    t0, nguong = thoi_diem_bat_dau(cot)
    print(f"Nhóm {ten}: vượt ngưỡng {nguong} bài/giờ lần đầu lúc {t0}")

gio = df.groupby(df["t"].dt.floor("h"))[["flu", "gi"]].sum()
gio = gio["2011-05-17":"2011-05-20"]
fig, ax = plt.subplots(figsize=(10, 3.6))
ax.fill_between(gio.index, gio["flu"], color=FLU, alpha=0.35); ax.plot(gio.index, gio["flu"], color=FLU, label="giống cúm")
ax.fill_between(gio.index, gio["gi"], color=GI, alpha=0.35); ax.plot(gio.index, gio["gi"], color=GI, label="dạ dày - ruột")
ax.set_title("Bài đăng triệu chứng theo giờ, 17 đến 20/5"); ax.set_ylabel("bài mỗi giờ")
ax.legend(frameon=False); ngay_thang(ax, "%d/%m %Hh"); plt.tight_layout()
plt.show()
