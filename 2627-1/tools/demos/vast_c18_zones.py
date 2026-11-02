ZONES = {   # vài điểm mốc (kinh độ, vĩ độ) bên trong mỗi khu, đọc từ ảnh bản đồ
    "Cornertown": [(-93.55, 42.295), (-93.53, 42.292), (-93.515, 42.295), (-93.52, 42.285)],
    "Northville": [(-93.47, 42.29), (-93.44, 42.295), (-93.45, 42.275), (-93.435, 42.248), (-93.455, 42.262)],
    "Riverside": [(-93.395, 42.285), (-93.37, 42.29), (-93.40, 42.26), (-93.375, 42.265), (-93.36, 42.28)],
    "Westside": [(-93.50, 42.255), (-93.485, 42.235), (-93.52, 42.235), (-93.51, 42.215), (-93.485, 42.215),
                 (-93.465, 42.235), (-93.47, 42.255)],
    "Villa": [(-93.555, 42.26), (-93.555, 42.23), (-93.55, 42.205), (-93.545, 42.215), (-93.55, 42.24)],
    "Smogtown": [(-93.55, 42.175), (-93.53, 42.165), (-93.54, 42.185), (-93.56, 42.17)],
    "Plainville": [(-93.47, 42.18), (-93.45, 42.195), (-93.49, 42.17), (-93.43, 42.2), (-93.44, 42.18),
                   (-93.50, 42.185), (-93.42, 42.208)],
    "Southville": [(-93.40, 42.172), (-93.42, 42.19), (-93.39, 42.165), (-93.38, 42.19), (-93.43, 42.17)],
    "Downtown": [(-93.38, 42.218), (-93.36, 42.21), (-93.40, 42.212), (-93.34, 42.225), (-93.375, 42.228),
                 (-93.39, 42.222)],
    "Uptown": [(-93.345, 42.24), (-93.33, 42.245), (-93.36, 42.243), (-93.35, 42.232)],
    "Lakeside": [(-93.30, 42.18), (-93.25, 42.19), (-93.22, 42.17), (-93.30, 42.165), (-93.32, 42.20),
                 (-93.345, 42.185), (-93.26, 42.205), (-93.22, 42.20), (-93.30, 42.198)],
    "Eastside": [(-93.28, 42.225), (-93.23, 42.225), (-93.21, 42.23), (-93.30, 42.232), (-93.25, 42.218),
                 (-93.31, 42.222), (-93.22, 42.218)],
    "Suburbia": [(-93.27, 42.275), (-93.22, 42.27), (-93.25, 42.25), (-93.30, 42.29), (-93.22, 42.30),
                 (-93.32, 42.265), (-93.28, 42.245), (-93.325, 42.29), (-93.22, 42.248), (-93.30, 42.248)],
}
ten_khu = list(ZONES)
mot = np.array([p for k in ten_khu for p in ZONES[k]])
nhan = np.array([i for i, k in enumerate(ten_khu) for _ in ZONES[k]])

co = np.cos(np.radians(42.2))                      # co dãn kinh độ ở vĩ độ 42 độ
gx = np.linspace(EXTENT[0], EXTENT[1], 700)
gy = np.linspace(EXTENT[3], EXTENT[2], 350)
GX, GY = np.meshgrid(gx, gy)
gan_nhat = ((GX[..., None] - mot[:, 0]) * co) ** 2 + (GY[..., None] - mot[:, 1]) ** 2
RASTER = nhan[gan_nhat.argmin(-1)]                 # mỗi ô lưới thuộc khu có điểm mốc gần nhất


def khu_cua(lon, lat):
    ix = np.clip(((lon - EXTENT[0]) / (EXTENT[1] - EXTENT[0]) * 699).astype(int), 0, 699)
    iy = np.clip(((EXTENT[3] - lat) / (EXTENT[3] - EXTENT[2]) * 349).astype(int), 0, 349)
    return RASTER[iy, ix]


df["khu"] = khu_cua(df["lon"].values, df["lat"].values)
dan = pop.set_index("Zone_Name")["Population_Density"].reindex(ten_khu).values

trieu_chung = df["flu"] | df["gi"]
d19 = df[(df["ngay"] == date(2011, 5, 19)) & trieu_chung]
d_nen = df[(df["ngay"] < date(2011, 5, 15)) & trieu_chung]
so_19 = d19.groupby("khu").size().reindex(range(13), fill_value=0).values
so_nen = d_nen.groupby("khu").size().reindex(range(13), fill_value=0).values / d_nen["ngay"].nunique()

ban_ngay = pop.set_index("Zone_Name")["Daytime_Population"].reindex(ten_khu).values
bang = pd.DataFrame({"khu": ten_khu, "dân": dan, "bài 19/5": so_19, "bình thường": so_nen.round(0),
                     "trên 1000 dân": (so_19 / dan * 1000).round(1),
                     "trên 1000 (ban ngày)": (so_19 / ban_ngay * 1000).round(1)})
print(bang.sort_values("trên 1000 dân", ascending=False).to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(12, 4.3))
for ax, gia_tri, cmap, tieu_de in zip(axes, [so_19, so_19 / dan * 1000], ["YlOrBr", "YlOrRd"],
                                      ["Số bài triệu chứng thô", "Số bài trên 1000 cư dân"]):
    base_map(ax, 0.15)
    im = ax.imshow(gia_tri[RASTER], extent=EXTENT, cmap=cmap, alpha=0.75, aspect=1 / co, zorder=2)
    plt.colorbar(im, ax=ax, shrink=0.8)
    for k, ten_k in enumerate(ten_khu):
        x, y = np.mean(ZONES[ten_k], axis=0)
        ax.text(x, y, ten_k, fontsize=6.5, ha="center", color=NAVY, zorder=3)
    ax.set_title(tieu_de + " (19/5)")
plt.tight_layout()
plt.show()
