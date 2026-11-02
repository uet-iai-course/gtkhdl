# ======================================================================
# PHẦN 5. Ở ĐÂU?
# ======================================================================
md("m09", """
## Bước 5. Khoanh vùng: các ca bệnh ở đâu?

Biết **khi nào** rồi, giờ hỏi **ở đâu**. Vẽ riêng hai nhóm triệu chứng của ngày 19/5 lên bản đồ.
Nếu cả hai nhóm cùng một bệnh, ta mong thấy chúng chồng lên nhau. Có đúng vậy không?
""")

code("c16_scatter", """
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
""")

code("c17_density", """
from scipy.ndimage import gaussian_filter

xb = np.linspace(EXTENT[0], EXTENT[1], 140)
yb = np.linspace(EXTENT[2], EXTENT[3], 70)


def luoi(d):
    \"\"\"Đếm số bài trong từng ô lưới.\"\"\"
    H, _, _ = np.histogram2d(d["lat"], d["lon"], bins=[yb, xb])
    return H


nen = df[df["ngay"] < date(2011, 5, 15)]
n_nen = nen["ngay"].nunique()

fig, axes = plt.subplots(1, 2, figsize=(12, 4.3))
for ax, cot, cmap in zip(axes, ["flu", "gi"], ["Oranges", "Blues"]):
    vuot = luoi(ngay19[ngay19[cot]]) - luoi(nen[nen[cot]]) / n_nen     # trừ mức bình thường mỗi ngày
    vuot = gaussian_filter(np.clip(vuot, 0, None), 1.2)
    iy, ix = np.unravel_index(vuot.argmax(), vuot.shape)
    print(f"{ten[cot]}: ô đậm nhất quanh kinh độ {xb[ix]:.3f}, vĩ độ {yb[iy]:.3f}")
    base_map(ax, 0.3)
    ax.imshow(np.ma.masked_less(vuot, vuot.max() * 0.04), extent=EXTENT, origin="lower", cmap=cmap,
              aspect=1 / np.cos(np.radians(42.2)), alpha=0.85, zorder=2)
    ax.set_title(f"Mật độ bài {ten[cot]} vượt mức bình thường")
plt.tight_layout()
plt.show()
""")

md("m10", """
Hai nhóm **không chồng lên nhau**: một nhóm tập trung ở trung tâm thành phố, nhóm kia kéo dài về phía tây nam.
Nhưng thành phố có khu rất đông, có khu rất thưa. Số bài thô dễ đánh lừa, nên ta **chuẩn hóa theo dân số**:
số bài triệu chứng trên **1000 cư dân** của từng khu.
Bản đồ chỉ cho ảnh chứ không có tệp ranh giới, nên ta ước lượng ranh giới 13 khu bằng nhiều điểm mốc đọc từ ảnh.
""")

code("c18_zones", """
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
""")

# ======================================================================
# PHẦN 6. NGUỒN GỐC
# ======================================================================
md("m11", """
## Bước 6. Nguồn bệnh: có chuyện gì xảy ra trước đó?

Bệnh không tự nhiên xuất hiện. Thám tử luôn hỏi: **trước ngày bệnh bùng phát, thành phố đã xảy ra sự kiện gì?**
Ta không đoán mà tìm các **từ bùng nổ**: từ nào bỗng được nhắc rất nhiều trong đúng một ngày rồi biến mất.
""")

code("c19_bursts", """
trung_vi = np.median(C, axis=1)                        # số bài chứa từ trong một ngày điển hình
dinh, ngay_dinh = C.max(1), C.argmax(1)               # ngày cao nhất của từng từ
lan = dinh / (trung_vi + 3)
chon = (dinh >= 150) & (lan >= 8)

bung_no = pd.DataFrame({"tu": vocab[chon], "ngay": ngay_dinh[chon], "lan": lan[chon]})
for i, g in bung_no.sort_values("lan", ascending=False).groupby("ngay"):
    ngay_str = (ngay0 + pd.Timedelta(days=int(i))).strftime("%d/%m")
    print(ngay_str, "|", ", ".join(g["tu"].head(6)))
""")

md("m12", """
Có **nhiều ngày** có chuyện: một triển lãm, một lễ hội, một hội nghị, một vụ máy bay, một lời dọa đánh bom...
Ngày 17/5 có **hai** nhóm từ cùng lúc. Chưa thể kết luận gì. Việc cần làm: với mỗi sự kiện, tìm **vị trí**
(tâm của các bài đăng nhắc đến nó) và **độ tản** của chúng.
Tên sự kiện do ta đặt theo từ khóa nổi bật.
""")

code("c20_events", """
SU_KIEN = {   # tên đặt theo từ khóa nổi bật, mẫu tìm kiếm, ngày
    "Triển lãm đồ cổ": (r"\\bantique\\b", "2011-05-04"),
    "Lễ hội": (r"\\bfestival\\b", "2011-05-07"),
    "Hội nghị": (r"\\bconvention\\b", "2011-05-11"),
    "Máy bay rơi": (r"\\b(?:plane|airport|crashed|crashing)\\b", "2011-05-13"),
    "Tòa nhà Capital": (r"\\b(?:capital|blaze)\\b", "2011-05-14"),
    "Dọa đánh bom": (r"\\b(?:bomb|bombs|threats?)\\b", "2011-05-16"),
    "Xe tải, tai nạn": (r"\\b(?:truck|trucks|accident|wrecked|bridge)\\b", "2011-05-17"),
    "Nổ, khói bụi": (r"\\b(?:explosions?|smog|rattle|shook|boom|blast)\\b", "2011-05-17"),
}
kx, ky = 69.17 * np.cos(np.radians(42.2)), 69.0          # số dặm ứng với 1 độ kinh độ, vĩ độ

hang, TAM, BAI_SK = [], {}, {}
for ten_sk, (mau_tu, ngay) in SU_KIEN.items():
    d = df[(df["ngay"] == pd.Timestamp(ngay).date()) & df["tl"].str.contains(mau_tu)]
    BAI_SK[ten_sk] = d
    tam = (d["lon"].median(), d["lat"].median())
    ban_kinh = np.median(np.hypot((d["lon"] - tam[0]) * kx, (d["lat"] - tam[1]) * ky))
    TAM[ten_sk] = tam
    hang.append([ten_sk, ngay[5:], len(d), round(tam[1], 4), round(tam[0], 4), round(ban_kinh, 2),
                 d["t"].quantile(0.1).strftime("%H:%M")])
bang_sk = pd.DataFrame(hang, columns=["sự kiện", "ngày", "số bài", "vĩ độ", "kinh độ", "tản (dặm)", "10% bài đầu"])
print(bang_sk.to_string(index=False))
""")

code("c21_eventmap", """
mau_sk = ["#8D99AE", "#2A9D8F", "#6A994E", "#264653", "#E07A5F", "#B5838D", EVT, "#F2A900"]
lech = {"Triển lãm đồ cổ": (-40, 32), "Lễ hội": (12, -14), "Hội nghị": (14, 16), "Dọa đánh bom": (-120, -30),
        "Tòa nhà Capital": (-50, 22)}                  # độ lệch nhãn để không đè lên nhau
fig, ax = plt.subplots(figsize=(10, 5.2))
base_map(ax, 0.4)
for (ten_sk, (mau_tu, ngay)), mau in zip(SU_KIEN.items(), mau_sk):
    d = BAI_SK[ten_sk]
    ax.scatter(d["lon"], d["lat"], s=3, color=mau, alpha=0.3)
    x, y = TAM[ten_sk]
    ax.scatter([x], [y], s=150, color=mau, edgecolor="white", linewidth=1.6, zorder=4)
    ax.annotate(f"{ten_sk} ({ngay[8:]}/5)", (x, y), xytext=lech.get(ten_sk, (8, 7)), textcoords="offset points",
                fontsize=8, weight="bold", color=NAVY, zorder=5,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8))
ax.set_title("Tám sự kiện bất thường trước 18/5, mỗi sự kiện một chỗ")
plt.tight_layout()
plt.show()
""")

md("m13", """
Tám sự kiện ở bảy địa điểm khác nhau. **Ai là thủ phạm?** Cần một dữ kiện độc lập để lọc: **gió**.
Nếu độc tố bay trong không khí thì nó phải đi theo hướng gió. Xem bảng thời tiết.
""")

code("c22_wind", """
HUONG = {"N": 0, "NNE": 22.5, "NE": 45, "ENE": 67.5, "E": 90, "ESE": 112.5, "SE": 135, "SSE": 157.5,
         "S": 180, "SSW": 202.5, "SW": 225, "WSW": 247.5, "W": 270, "WNW": 292.5, "NW": 315, "NNW": 337.5}
weather["ngay"] = pd.to_datetime(weather["Date"], format="%m/%d/%Y").dt.date
weather["gio_tu"] = weather["Wind_Direction"].map(HUONG)         # gió thổi TỪ hướng này
weather["gio_den"] = (weather["gio_tu"] + 180) % 360             # nên thổi ĐẾN hướng ngược lại
w = weather[weather["ngay"] >= date(2011, 5, 14)].reset_index(drop=True)
print(w[["Date", "Weather", "Average_Wind_Speed", "Wind_Direction", "gio_den"]].to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 2.9))
rad = np.radians(w["gio_den"])
mau = [GOLD if d in (date(2011, 5, 17), date(2011, 5, 18), date(2011, 5, 19)) else GRAY for d in w["ngay"]]
ax.quiver(range(len(w)), np.zeros(len(w)), np.sin(rad), np.cos(rad), color=mau, scale=9, width=0.012)
for i, r in w.iterrows():
    ax.text(i, -1.15, f"{r['ngay'].strftime('%d/%m')}\\n{r['Average_Wind_Speed']} mph\\ntừ {r['Wind_Direction']}",
            ha="center", va="top", fontsize=8)
ax.set_xlim(-0.6, len(w) - 0.4); ax.set_ylim(-2.3, 1); ax.axis("off")
ax.set_title("Hướng gió thổi đến (mũi tên hướng lên là về phía Bắc)")
plt.tight_layout()
plt.show()
""")

md("m14", """
Gió đổi hướng liên tục, nhưng từ 16 đến 19/5 nó ổn định, **thổi từ Tây sang Đông**.
Giả thuyết cần kiểm tra: *nếu nguồn bệnh giống cúm là một sự kiện ở đâu đó, thì các ca của sáng 18/5 phải nằm
**xuôi gió** của nguồn đó, trong một dải hẹp dọc theo hướng gió, và hầu như không có ca nào ở **ngược gió**.*
Ta kiểm tra từng nghi phạm với các bài giống cúm từ 6h đến 14h ngày 18/5.
""")

code("c23_flu_test", """
huong = weather.set_index("ngay").loc[date(2011, 5, 18), "gio_den"]
cua_so = df[(df["t"] >= "2011-05-18 06:00") & (df["t"] < "2011-05-18 14:00") & df["flu"]]
print(f"Gió 18/5 thổi về hướng {huong:.0f} độ (90 = Đông). Số bài giống cúm trong cửa sổ: {len(cua_so)}")


def toa_do_gio(d, tam, huong):
    \"\"\"Khoảng cách dọc theo gió và lệch ngang so với đường gió đi qua `tam` (đơn vị dặm).\"\"\"
    dx, dy = (d["lon"] - tam[0]) * kx, (d["lat"] - tam[1]) * ky
    a = np.radians(huong)
    return (dx * np.sin(a) + dy * np.cos(a)).values, (-dx * np.cos(a) + dy * np.sin(a)).values


hang = []
for ten_sk, tam in TAM.items():
    doc, ngang = toa_do_gio(cua_so, tam, huong)
    hang.append([ten_sk, 100 * (doc < 0).mean(), 100 * ((doc > 0) & (np.abs(ngang) < 1.5)).mean()])
diem = pd.DataFrame(hang, columns=["sự kiện", "% ca ngược gió", "% ca trong dải xuôi gió"]).set_index("sự kiện")
print(diem.round(1).sort_values("% ca trong dải xuôi gió", ascending=False).to_string())

fig, ax = plt.subplots(figsize=(9, 3.6))
s = diem["% ca trong dải xuôi gió"].sort_values()
ax.barh(s.index, s.values, color=[FLU if v == s.max() else GRAY for v in s.values])
ax.set_xlabel("% số ca giống cúm (6h-14h, 18/5) nằm trong dải hẹp xuôi gió của sự kiện")
ax.set_title("Sự kiện nào giải thích được vị trí các ca giống cúm?")
plt.tight_layout()
plt.show()
""")

md("m14b", """
Đã có một nghi phạm dẫn đầu. Trước khi đi tiếp, quay lại **hiện trường**: những người dân thật sự viết gì
về sự kiện đó trong ngày 17/5, và con số có lớn bất thường so với ngày thường không?
""")

code("c23b_scene", """
co_hai = df["tl"].str.contains(r"\\btrucks?\\b") & df["tl"].str.contains(r"\\baccident\\b")
so_ngay = co_hai.groupby(df["ngay"]).sum()
print(f"Bài chứa cả 'truck' lẫn 'accident': ngày 17/5 có {so_ngay[date(2011, 5, 17)]}, "
      f"trung bình mỗi ngày trong 14 ngày đầu chỉ {so_ngay.iloc[:14].mean():.1f}")

hien_truong = df[co_hai & (df["ngay"] == date(2011, 5, 17))]
print("Giờ đăng sớm của nhóm bài này (10% đầu tiên):", hien_truong["t"].quantile(0.1).strftime("%H:%M"))
print("Ba bài đăng thật:")
for noi_dung in hien_truong["text"].sample(3, random_state=4):
    print(" -", noi_dung[:100])
""")