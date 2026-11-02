from sklearn.cluster import DBSCAN

sang20 = df[(df["t"] >= "2011-05-20 08:00") & df["flu"]]
P = np.c_[sang20["lon"] * kx, sang20["lat"] * ky]
nhan_cum = DBSCAN(eps=0.15, min_samples=80).fit_predict(P)              # cụm: ít nhất 80 bài trong bán kính 0,15 dặm
cum_tam = np.array([[sang20["lon"][nhan_cum == k].mean(), sang20["lat"][nhan_cum == k].mean()]
                    for k in range(nhan_cum.max() + 1)])
print(f"DBSCAN tìm thấy {len(cum_tam)} cụm, chiếm {100 * (nhan_cum >= 0).mean():.0f}% bài giống cúm ngày 20/5")

BENH_VIEN = {   # tên bệnh viện (theo README) và tọa độ biểu tượng trên ảnh bản đồ
    "Corner": (-93.5317, 42.2987), "Westside": (-93.4788, 42.2565), "Northside": (-93.42, 42.2526),
    "Villa": (-93.5567, 42.2043), "Smogtown": (-93.4947, 42.2019), "Plainville": (-93.4451, 42.2048),
    "Southville": (-93.3908, 42.174), "Vastopolis City": (-93.3622, 42.2201), "St. Georges": (-93.3303, 42.2404),
    "Lakeside": (-93.3432, 42.1682), "St. Kristin's": (-93.2469, 42.2197), "St. Mark's": (-93.2339, 42.2947),
    "River": (-93.3649, 42.2844),
}
bv = np.array(list(BENH_VIEN.values()))
for k, c in enumerate(cum_tam):
    kc = np.hypot((bv[:, 0] - c[0]) * kx, (bv[:, 1] - c[1]) * ky)
    ten_bv = list(BENH_VIEN)[kc.argmin()] if kc.min() < 0.3 else "không phải bệnh viện"
    print(f"cụm {k:2d}: {np.round(c, 4)}  {(nhan_cum == k).sum():4d} bài  ->  {ten_bv}")

fig, ax = plt.subplots(figsize=(10, 5.2))
base_map(ax, 0.4)
ax.scatter(sang20["lon"], sang20["lat"], s=1, c=FLU, alpha=0.25)
ax.scatter(cum_tam[:, 0], cum_tam[:, 1], s=260, facecolor="none", edgecolor=NAVY, linewidth=2, zorder=4, label="cụm DBSCAN")
ax.scatter(bv[:, 0], bv[:, 1], marker="P", s=70, color=GOLD, edgecolor=NAVY, zorder=5, label="bệnh viện")
ax.set_title("Bài giống cúm từ 8h ngày 20/5: các cụm trùng với bệnh viện")
ax.legend(frameon=True, loc="lower right"); plt.tight_layout()
plt.show()
