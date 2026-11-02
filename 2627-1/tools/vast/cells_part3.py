# ======================================================================
# PHẦN 7. LAN TRUYỀN
# ======================================================================
md("m15", """
Có **một** nghi phạm khớp với hướng gió nhất: khoảng 90% ca giống cúm nằm trong một dải hẹp xuôi gió của nó,
và rất ít ca ở ngược gió (một nghi phạm khác cũng đạt mức khá cao, nên ta vẫn phải thử bằng dữ liệu khác). Ta tạm gọi đó là **nghi phạm số một** (một *giả thuyết*, chưa phải kết luận).
Giả thuyết cần được thử thách bằng dữ liệu khác, và còn một nhóm triệu chứng chưa giải thích: nhóm dạ dày - ruột.

## Bước 7. Lan truyền: bệnh đi như thế nào?

Trước hết, quan sát **sự lan rộng theo thời gian**: các ca giống cúm, mỗi khung 6 giờ, từ 18/5 đến 20/5.
Ngôi sao vàng là nghi phạm số một.
""")

code("c24_panels", """
NGUON = diem["% ca trong dải xuôi gió"].idxmax()           # nghi phạm số một theo kiểm tra trước
print("Nghi phạm số một:", NGUON, "tại", np.round(TAM[NGUON], 4))

moc = pd.date_range("2011-05-18", periods=12, freq="6h")
fig, axes = plt.subplots(3, 4, figsize=(12, 6.6))
for ax, t0 in zip(axes.ravel(), moc):
    d = df[(df["t"] >= t0) & (df["t"] < t0 + pd.Timedelta(hours=6)) & df["flu"]]
    base_map(ax, 0.25)
    ax.scatter(d["lon"], d["lat"], s=0.6, c=FLU, alpha=0.35)
    ax.plot(*TAM[NGUON], marker="*", ms=11, mfc=GOLD, mec=NAVY, zorder=5)
    ax.set_title(t0.strftime("%d/%m %Hh") + f": {len(d):,} bài", fontsize=8)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel(""); ax.set_ylabel("")
plt.tight_layout()
plt.show()
""")

code("c25_gif", """
from PIL import Image as PILImage

khung = []
moc3 = pd.date_range("2011-05-18", periods=24, freq="3h")
for t0 in moc3:
    d = df[(df["t"] >= t0) & (df["t"] < t0 + pd.Timedelta(hours=3)) & df["flu"]]
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=80)
    base_map(ax, 0.3)
    ax.scatter(d["lon"], d["lat"], s=1.2, c=FLU, alpha=0.4)
    ax.plot(*TAM[NGUON], marker="*", ms=13, mfc=GOLD, mec=NAVY, zorder=5)
    ax.set_title(f"Ca giống cúm, {t0:%d/%m %Hh} đến {t0 + pd.Timedelta(hours=3):%Hh}  ({len(d):,} bài)", fontsize=9)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel(""); ax.set_ylabel("")
    fig.tight_layout(); fig.canvas.draw()
    khung.append(PILImage.fromarray(np.asarray(fig.canvas.buffer_rgba())).convert("P", palette=PILImage.ADAPTIVE))
    plt.close(fig)

khung[0].save("flu_spread.gif", save_all=True, append_images=khung[1:], duration=450, loop=0)
print("Đã lưu flu_spread.gif:", len(khung), "khung hình, mỗi khung 3 giờ")
try:
    from IPython.display import Image as GifImage, display
    display(GifImage("flu_spread.gif"))
except ImportError:
    pass
""")

code("c26_front", """
d = df[(df["t"] >= "2011-05-18") & (df["t"] < "2011-05-21") & df["flu"]].copy()
huong_ngay = d["ngay"].map(weather.set_index("ngay")["gio_den"])        # hướng gió của chính ngày đó
dx, dy = (d["lon"] - TAM[NGUON][0]) * kx, (d["lat"] - TAM[NGUON][1]) * ky
a = np.radians(huong_ngay)
d["doc"] = dx * np.sin(a) + dy * np.cos(a)                                 # dặm dọc theo hướng gió
d["khung"] = d["t"].dt.floor("6h")

tk = d.groupby("khung")["doc"].agg(trung_vi="median", p90=lambda s: s.quantile(0.9), so_bai="size")
print(tk.round(2).to_string())

fig, ax = plt.subplots(figsize=(10, 3.6))
ax.plot(tk.index, tk["trung_vi"], color=FLU, lw=2.4, marker="o", label="trung vị")
ax.plot(tk.index, tk["p90"], color=NAVY, lw=2.4, marker="s", label="90% ca nằm gần hơn mốc này")
ax.set_ylabel("khoảng cách xuôi gió từ nghi phạm (dặm)"); ax.set_ylim(0)
ax.set_title("Vùng có ca bệnh có mở rộng thêm theo thời gian không?")
ax.legend(frameon=False); ngay_thang(ax, "%d/%m %Hh"); plt.tight_layout()
plt.show()
""")

md("m16", """
Điều đáng chú ý: **ngay từ khung đầu tiên, dải bệnh đã dài sẵn** và các ngày sau gần như lặp lại cùng một dải;
vùng bệnh *không* lan dần ra xa nghi phạm. Một nguồn phát tán một lần theo gió sẽ cho hình ảnh như vậy;
một bệnh lây dần từ người sang người thường sẽ cho vòng tròn nở rộng theo thời gian.
Nhưng đây mới là **một** nhóm triệu chứng. Còn nhóm dạ dày - ruột? Nó nằm ở phía tây nam, khá giống một **con sông**.
Ta số hóa đường đi của sông Vast từ ảnh bản đồ, rồi đo khoảng cách từ mỗi bài đăng đến sông.
""")

code("c27_river", """
SONG = np.array([(-93.350, 42.302), (-93.356, 42.290), (-93.362, 42.275), (-93.367, 42.262), (-93.375, 42.250),
                 (-93.390, 42.241), (-93.405, 42.236), (-93.418, 42.231), (-93.430, 42.226), (-93.445, 42.219),
                 (-93.46, 42.212), (-93.48, 42.204), (-93.50, 42.196), (-93.515, 42.187), (-93.525, 42.178),
                 (-93.530, 42.168), (-93.533, 42.160)])      # sông Vast, số hóa tay từ ảnh bản đồ (bắc xuống nam)
xy = np.c_[SONG[:, 0] * kx, SONG[:, 1] * ky]
doan = np.diff(xy, axis=0)
dai = np.hypot(*doan.T)
cong_don = np.r_[0, dai.cumsum()]


def toa_do_song(lon, lat):
    \"\"\"Trả về (khoảng cách đến sông, vị trí dọc sông tính từ phía bắc), đơn vị dặm.\"\"\"
    P = np.c_[np.asarray(lon) * kx, np.asarray(lat) * ky]
    gan, vt = np.full(len(P), 1e9), np.zeros(len(P))
    for a, v, L, c0 in zip(xy[:-1], doan, dai, cong_don[:-1]):
        t = np.clip(((P - a) @ v) / (L * L), 0, 1)
        kc = np.hypot(*(P - (a + t[:, None] * v)).T)
        tot = kc < gan
        gan[tot], vt[tot] = kc[tot], c0 + t[tot] * L
    return gan, vt


gi19 = ngay19[ngay19["gi"]]
kc_gi, _ = toa_do_song(gi19["lon"], gi19["lat"])
kc_all, _ = toa_do_song(ngay19["lon"], ngay19["lat"])
for r in (1.0, 1.5, 3.0):
    print(f"Trong {r} dặm quanh sông: {100 * (kc_gi < r).mean():.1f}% bài dạ dày - ruột, "
          f"{100 * (kc_all < r).mean():.1f}% mọi bài cùng ngày")

fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw={"width_ratios": [1.5, 1]})
base_map(axes[0], 0.3)
axes[0].scatter(gi19["lon"], gi19["lat"], s=1.5, c=GI, alpha=0.35)
axes[0].plot(SONG[:, 0], SONG[:, 1], color=NAVY, lw=1.6, ls="--")
axes[0].set_title("Bài dạ dày - ruột (19/5) và đường sông")
axes[1].hist(kc_all, bins=np.arange(0, 8, 0.25), density=True, color=GRAY, alpha=0.6, label="mọi bài")
axes[1].hist(kc_gi, bins=np.arange(0, 8, 0.25), density=True, color=GI, alpha=0.7, label="dạ dày - ruột")
axes[1].axvline(1.5, color=NAVY, ls=":")
axes[1].set_xlabel("khoảng cách đến sông (dặm)"); axes[1].set_ylabel("mật độ"); axes[1].legend(frameon=False)
axes[1].set_title("Khoảng cách đến sông")
plt.tight_layout()
plt.show()
""")

md("m17", """
Bài dạ dày - ruột **dồn sát bờ sông**, còn bài thông thường rải đều khắp thành phố.
Một con sông chảy từ đâu đến đâu? Theo README, sông Vast **chảy về phía nam** với tốc độ 3 dặm/giờ.
Nếu nguồn nằm trên sông, ca bệnh phải ở **phía hạ lưu** của nguồn.
Một nguồn gây bệnh qua nước phải **nằm sát sông**, và ca bệnh phải ở **hạ lưu** của nó.
Giờ ta làm phép thử chung cho **cả hai nhóm triệu chứng**: mỗi nghi phạm giải thích được bao nhiêu phần trăm ca cúm
(theo gió) *và* có nằm sát sông không (đo bằng khoảng cách từ nghi phạm đến sông)?
""")

code("c28_both", """
vt_gi = toa_do_song(gi19["lon"], gi19["lat"])
hang = []
for ten_sk, tam in TAM.items():
    cach_song, vt_nguon = toa_do_song([tam[0]], [tam[1]])
    ha_luu = (vt_gi[1] > vt_nguon[0]) & (vt_gi[0] < 1.5)         # nằm phía hạ lưu và sát sông
    hang.append([ten_sk, round(cach_song[0], 2), 100 * ha_luu.mean()])
song = pd.DataFrame(hang, columns=["sự kiện", "cách sông (dặm)", "% ca dạ dày ở hạ lưu"]).set_index("sự kiện")
tong = diem.join(song)[["% ca trong dải xuôi gió", "cách sông (dặm)", "% ca dạ dày ở hạ lưu"]]
print(tong.round(1).sort_values("% ca trong dải xuôi gió", ascending=False).to_string())

fig, ax = plt.subplots(figsize=(7.5, 5.2))
for ten_sk, r in tong.iterrows():
    tot = ten_sk == NGUON
    ax.scatter(r["% ca trong dải xuôi gió"], r["cách sông (dặm)"], s=240 if tot else 90,
               color=GOLD if tot else GRAY, edgecolor=NAVY, zorder=3)
    ax.annotate(ten_sk, (r["% ca trong dải xuôi gió"], r["cách sông (dặm)"]),
                xytext=(7, -14) if ten_sk == "Hội nghị" else (7, 6),
                textcoords="offset points", fontsize=8, weight="bold" if tot else "normal")
ax.set_xlim(-5, 105); ax.invert_yaxis()
ax.set_xlabel("% ca giống cúm trong dải xuôi gió của sự kiện (càng sang phải càng khớp)")
ax.set_ylabel("khoảng cách từ sự kiện đến sông (dặm, càng lên cao càng gần)")
ax.set_title("Mỗi nghi phạm khớp với hai nhóm triệu chứng đến đâu?")
plt.tight_layout()
plt.show()
""")

md("m18", """
Chỉ **một** nghi phạm nằm ở góc trên bên phải: nó vừa **nằm trên sông** vừa giải thích hầu hết ca cúm theo gió.
Các nghi phạm khác hoặc xa sông, hoặc không khớp hướng gió, hoặc ca bệnh nằm *ngược* phía so với nó.
Đây là bằng chứng *hội tụ* từ nhiều nguồn dữ liệu độc lập (vị trí bài đăng, thời tiết, bản đồ). Nhưng cần so sánh ba cơ chế lây lan có thể có:
**không khí**, **nước**, **người sang người**.
""")

code("c29_mechanism", """
def chi_so(d, huong):
    \"\"\"Hai chỉ số cho một tập bài: % trong dải xuôi gió của nguồn, và % sát sông (<= 1,5 dặm).\"\"\"
    doc, ngang = toa_do_gio(d, TAM[NGUON], huong)
    trong_dai = ((doc > 0) & (doc < 12) & (np.abs(ngang) < 1.5)).mean()
    sat_song = (toa_do_song(d["lon"], d["lat"])[0] < 1.5).mean()
    return [100 * trong_dai, 100 * sat_song]


g = weather.set_index("ngay")["gio_den"]
cum = df[(df["ngay"] == date(2011, 5, 18)) & df["flu"]]
da_day = df[(df["ngay"] == date(2011, 5, 19)) & df["gi"]]
thuong = df[df["ngay"] == date(2011, 5, 19)]

bang_cs = pd.DataFrame([chi_so(cum, g[date(2011, 5, 18)]), chi_so(da_day, g[date(2011, 5, 19)]),
                        chi_so(thuong, g[date(2011, 5, 19)])],
                       index=["ca giống cúm (18/5)", "ca dạ dày - ruột (19/5)", "mọi bài (19/5)"],
                       columns=["% trong dải xuôi gió (không khí)", "% sát sông (nước)"])
print(bang_cs.round(1).to_string())

fig, ax = plt.subplots(figsize=(7.5, 3.2))
im = ax.imshow(bang_cs.values, cmap="Blues", vmin=0, vmax=100, aspect="auto")
ax.set_xticks([0, 1]); ax.set_xticklabels(["xuôi gió\\n(không khí)", "sát sông\\n(nước)"])
ax.set_yticks(range(3)); ax.set_yticklabels(bang_cs.index)
for i in range(3):
    for j in range(2):
        v = bang_cs.values[i, j]
        ax.text(j, i, f"{v:.0f}%", ha="center", va="center", color="white" if v > 55 else NAVY, weight="bold")
ax.grid(False); ax.set_title("Mỗi nhóm triệu chứng khớp với cơ chế nào?")
plt.tight_layout()
plt.show()
""")

code("c30_p2p", """
# Bài "nói về người khác": có tên riêng + has/is, hoặc các đại từ he/she/they...
NGUOI_KHAC = r"\\b[A-Z][a-z]{2,} (?:has|is|had) |\\b(?:[Tt]hey|[Tt]hem|[Tt]heir|[Ss]he|[Hh]e|[Hh]is|[Hh]er)\\b"
df["nguoi_khac"] = df["text"].str.contains(NGUOI_KHAC)
print("Ví dụ bài nói về người khác:")
print(df[df["flu"] & df["nguoi_khac"]]["text"].head(3).to_string(index=False))


def thong_ke_nguoi(cot):
    d = df[df[cot] & (df["t"] >= "2011-05-17")]
    tu_bao = d[~d["nguoi_khac"]]                                    # bài tự kể về mình
    lan_dau = tu_bao.groupby("ID")["ngay"].min().value_counts().sort_index()
    return pd.DataFrame({
        "bài": d.groupby("ngay").size(),
        "% nói về người khác": (100 * d.groupby("ngay")["nguoi_khac"].mean()).round(0),
        "người tự báo": tu_bao.groupby("ngay")["ID"].nunique(),
        "người tự báo mới": lan_dau}).fillna(0).astype(int)


tk_flu, tk_gi = thong_ke_nguoi("flu"), thong_ke_nguoi("gi")
print("Nhóm giống cúm:"); print(tk_flu.to_string())
print("Nhóm dạ dày - ruột:"); print(tk_gi.to_string())

fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.6))
x = np.arange(len(tk_flu))
nhan_ngay = [d.strftime("%d/%m") for d in tk_flu.index]
axes[0].bar(x, tk_flu["người tự báo"], color=FLU, alpha=0.35, label="người tự báo (tổng)")
axes[0].bar(x, tk_flu["người tự báo mới"], color=FLU, label="trong đó, người mới")
axes[0].set_xticks(x); axes[0].set_xticklabels(nhan_ngay); axes[0].legend(frameon=False, fontsize=8)
axes[0].set_title("Người tự báo triệu chứng cúm: số người mới mỗi ngày")
axes[1].plot(x, tk_flu["% nói về người khác"], color=FLU, marker="o", lw=2.4, label="giống cúm")
axes[1].plot(tk_gi.index.map(lambda d: (d - tk_flu.index[0]).days), tk_gi["% nói về người khác"],
             color=GI, marker="o", lw=2.4, label="dạ dày - ruột")
axes[1].set_xticks(x); axes[1].set_xticklabels(nhan_ngay); axes[1].legend(frameon=False, fontsize=8)
axes[1].set_ylabel("% bài nói về người khác"); axes[1].set_title("Bài nói về người khác")
plt.tight_layout()
plt.show()
""")

md("m19", """
Nếu bệnh lây từ người sang người, số **người mới** tự báo bệnh mỗi ngày thường *tăng dần theo cấp số nhân*.
Ở đây số người tự báo mới **sụt xuống rất nhanh** sau ngày đầu, và phần lớn người bệnh **đăng lại** những ngày sau.
Trong khi đó, tỉ lệ bài *nói về người khác* lại tăng: lượng bài đăng tăng chủ yếu vì **nỗi lo và tin đồn**,
không phải vì có thêm nhiều người bệnh. Điều này *không hỗ trợ* giả thuyết lây theo cấp số nhân,
nhưng cũng **chưa thể loại trừ** hoàn toàn: bài đăng không phải xét nghiệm y tế, và cách nhận diện bài nói về người khác
chỉ là một quy tắc đoán.
""")

# ======================================================================
# PHẦN 8. HỆ THỐNG Y TẾ VÀ HÀNH ĐỘNG
# ======================================================================
md("m20", """
## Bước 8. Hệ thống y tế và hành động

Ngày 20/5 người bệnh bắt đầu tìm đến bệnh viện. Nếu đúng, các bài giống cúm của ngày này phải **dồn thành từng cụm nhỏ**.
Dùng thuật toán gom cụm theo mật độ (DBSCAN) để tìm các cụm đó, rồi đặt lên bản đồ.
""")

code("c31_hospital", """
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
""")

code("c32_hospital_share", """
def gan_benh_vien(d, r=0.35):
    \"\"\"Tỉ lệ bài nằm trong r dặm quanh một bệnh viện.\"\"\"
    kc = np.hypot((d["lon"].values[:, None] - bv[:, 0]) * kx, (d["lat"].values[:, None] - bv[:, 1]) * ky)
    return (kc.min(1) < r).mean()


df["flu_tu"] = df["flu"] & ~df["nguoi_khac"]               # bài cúm do người bệnh tự kể

hang = []
for ngay in [date(2011, 5, 17), date(2011, 5, 18), date(2011, 5, 19), date(2011, 5, 20)]:
    ban_ngay_ = df[(df["ngay"] == ngay) & (df["t"].dt.hour >= 8)]
    hang.append([ngay.strftime("%d/%m"), 100 * gan_benh_vien(ban_ngay_[ban_ngay_["flu_tu"]]),
                 100 * gan_benh_vien(ban_ngay_[ban_ngay_["gi"]]), 100 * gan_benh_vien(ban_ngay_[~ban_ngay_["flu"]])])
bang_bv = pd.DataFrame(hang, columns=["ngày", "% bài cúm tự báo gần BV", "% bài dạ dày gần BV", "% bài khác gần BV"])
print(bang_bv.round(1).to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 3.4))
x = np.arange(len(bang_bv)); rong = 0.27
ax.bar(x - rong, bang_bv.iloc[:, 1], rong, color=FLU, label="giống cúm (tự báo)")
ax.bar(x, bang_bv.iloc[:, 2], rong, color=GI, label="dạ dày - ruột")
ax.bar(x + rong, bang_bv.iloc[:, 3], rong, color=GRAY, label="bài khác")
ax.set_xticks(x); ax.set_xticklabels(bang_bv["ngày"])
ax.set_ylabel("% bài trong 0,35 dặm quanh bệnh viện"); ax.legend(frameon=False)
ax.set_title("Người bệnh dồn về bệnh viện vào ngày nào?")
plt.tight_layout()
plt.show()
""")

md("m21", """
Còn việc cuối: **khoanh vùng hành động**. Nếu nguồn lực có hạn, nên tập trung vào đâu?
Ta tìm tập ô lưới nhỏ nhất chứa **80%** số bài triệu chứng vượt mức bình thường của ngày 19/5.
""")

code("c33_priority", """
tc19 = ngay19[ngay19["flu"] | ngay19["gi"]]
tc_nen = nen[nen["flu"] | nen["gi"]]
vuot = np.clip(luoi(tc19) - luoi(tc_nen) / n_nen, 0, None)
vuot = gaussian_filter(vuot, 1.0)

thu_tu = np.sort(vuot.ravel())[::-1]
so_o = np.searchsorted(np.cumsum(thu_tu) / thu_tu.sum(), 0.8) + 1
nguong = thu_tu[so_o - 1]
dien_tich_o = (xb[1] - xb[0]) * kx * (yb[1] - yb[0]) * ky
tong_dt = (EXTENT[1] - EXTENT[0]) * kx * (EXTENT[3] - EXTENT[2]) * ky
print(f"Vùng ưu tiên chứa 80% bài vượt mức: {so_o} ô, khoảng {so_o * dien_tich_o:.0f} dặm vuông, "
      f"bằng {100 * so_o * dien_tich_o / tong_dt:.0f}% diện tích thành phố ({tong_dt:.0f} dặm vuông)")

fig, ax = plt.subplots(figsize=(10, 5.2))
base_map(ax, 0.4)
ax.contourf((xb[:-1] + xb[1:]) / 2, (yb[:-1] + yb[1:]) / 2, vuot, levels=[nguong, vuot.max() * 2],
            colors=[FLU], alpha=0.45, zorder=2)
ax.plot(SONG[:, 0], SONG[:, 1], color=NAVY, lw=1.6, ls="--", zorder=3)
ax.plot(*TAM[NGUON], marker="*", ms=16, mfc=GOLD, mec=NAVY, zorder=5)
ax.scatter(bv[:, 0], bv[:, 1], marker="P", s=70, color=GOLD, edgecolor=NAVY, zorder=5)
ax.set_title("Vùng ưu tiên (chứa 80% bài triệu chứng vượt mức), sông, bệnh viện")
plt.tight_layout()
plt.show()
""")

code("c34_timeline", """
t_sk = BAI_SK[NGUON]["t"].quantile(0.1)
t_cum = thoi_diem_bat_dau("flu")[0]
gio_flu = df.groupby(df["t"].dt.floor("h"))["flu"].sum()
t_bung = gio_flu[gio_flu > 20 * gio_flu.iloc[: 14 * 24].mean()].index[0]
t_gi = thoi_diem_bat_dau("gi")[0]
hai_20 = df[(df["t"] >= "2011-05-19") & df["flu_tu"]]
ti_le_bv = hai_20.groupby(hai_20["t"].dt.floor("h")).apply(gan_benh_vien)
t_bv = ti_le_bv[ti_le_bv > 0.3].index[0]

cac_moc = [(t_sk, f"{NGUON}\\n(10% bài đăng đầu)", EVT), (t_cum, "bắt đầu có\\nca giống cúm", FLU),
           (t_bung, "ca giống cúm\\nbùng nổ", FLU), (t_gi, "bắt đầu có ca\\ndạ dày - ruột", GI),
           (t_bv, "người bệnh dồn\\nvề bệnh viện", GOLD)]
for t, ten_moc, _ in cac_moc:
    print(f"{t:%d/%m %H:%M}  {ten_moc.replace(chr(10), ' ')}")

fig, ax = plt.subplots(figsize=(11, 2.8))
ax.hlines(0, cac_moc[0][0] - pd.Timedelta(hours=8), cac_moc[-1][0] + pd.Timedelta(hours=8), color=NAVY, lw=2)
for i, (t, ten_moc, mau) in enumerate(cac_moc):
    ax.scatter([t], [0], s=150, color=mau, edgecolor=NAVY, zorder=3)
    ax.annotate(f"{t:%d/%m %Hh}\\n{ten_moc}", (t, 0), xytext=(0, 20 if i % 2 == 0 else -50),
                textcoords="offset points", ha="center", fontsize=8.5)
ax.set_ylim(-1, 1); ax.axis("off"); ax.set_title("Dòng thời gian của vụ dịch (rút ra từ dữ liệu)")
plt.tight_layout()
plt.show()
""")

code("c35_dashboard", """
fig = plt.figure(figsize=(12, 5.2))
gs = fig.add_gridspec(2, 2, width_ratios=[1.8, 1])
ax = fig.add_subplot(gs[:, 0])
base_map(ax, 0.35)
mau_flu = df[(df["t"] >= "2011-05-18") & (df["t"] < "2011-05-21") & df["flu"]].sample(9000, random_state=2)
mau_gi = df[(df["t"] >= "2011-05-19") & (df["t"] < "2011-05-21") & df["gi"]].sample(5000, random_state=2)
ax.scatter(mau_flu["lon"], mau_flu["lat"], s=1.2, c=FLU, alpha=0.3, label="ca giống cúm")
ax.scatter(mau_gi["lon"], mau_gi["lat"], s=1.2, c=GI, alpha=0.3, label="ca dạ dày - ruột")
ax.plot(SONG[:, 0], SONG[:, 1], color=NAVY, lw=1.4, ls="--")
ax.scatter(bv[:, 0], bv[:, 1], marker="P", s=60, color=GOLD, edgecolor=NAVY, zorder=5, label="bệnh viện")
ax.plot(*TAM[NGUON], marker="*", ms=16, mfc=GOLD, mec=NAVY, zorder=6, label=NGUON)
ax.legend(loc="lower right", fontsize=8, markerscale=4); ax.set_title("Bản đồ tổng hợp")
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(theo_ngay.index, theo_ngay["flu"], color=FLU, lw=2); ax2.plot(theo_ngay.index, theo_ngay["gi"], color=GI, lw=2)
ngay_thang(ax2); ax2.set_title("Bài triệu chứng mỗi ngày", fontsize=10); ax2.tick_params(labelsize=7)
ax3 = fig.add_subplot(gs[1, 1])
ax3.bar(range(4), bang_bv.iloc[:, 1], color=FLU); ax3.set_xticks(range(4)); ax3.set_xticklabels(bang_bv["ngày"])
ax3.set_title("% bài cúm gần bệnh viện", fontsize=10); ax3.tick_params(labelsize=7)
plt.tight_layout()
plt.show()
""")

md("m22", """
## Kết luận và lưu ý

Từ dữ liệu, ta rút ra các **giả thuyết được dữ liệu hỗ trợ** (không phải kết quả xét nghiệm):

1. Hai nhóm triệu chứng có hai dạng phân bố khác nhau: một nhóm theo **hướng gió**, một nhóm theo **dòng sông**.
2. Một sự kiện duy nhất (nghi phạm số một) giải thích được cả hai nhóm.
3. Số người mới mỗi ngày không tăng theo cấp số nhân, nên **không có bằng chứng cho lây từ người sang người** trong dữ liệu này.
4. Từ 20/5, người bệnh dồn về các bệnh viện; cần tập trung nguồn lực vào vùng ưu tiên và các bệnh viện.

Lưu ý khi kể chuyện với dữ liệu:

- **Tương quan không phải nhân quả.** Ta chỉ có vị trí và thời gian của *bài đăng*, không có xét nghiệm.
- **Bài đăng không phải ca bệnh.** Một người có thể đăng nhiều lần, và có người đăng về người khác.
- **Vị trí bài đăng không chắc là nơi bị nhiễm.** Người ta đi làm, di chuyển.
- Đây là **dữ liệu mô phỏng** do ban tổ chức tạo ra, nên con số không phản ánh bệnh thật.
- Các nhóm tham gia VAST Challenge 2011 không hoàn toàn thống nhất (ví dụ về mức độ kiểm soát dịch và khả năng
  lây từ người sang người); kết luận trên chỉ là cách đọc của riêng bài này.

### Đối chiếu với đáp án chính thức

Ban tổ chức công bố *Answer Guide* của Mini-Challenge 1 (xem phần nguồn). Hãy mở nó và so với kết quả của bạn:
tai nạn xe tải trên cầu I-610 ngày 17/5 (42,22655 độ Bắc, 93,42752 độ Tây), gió Tây thổi sang Đông,
ca giống cúm lan theo gió từ 18/5, ca dạ dày - ruột đi theo dòng sông từ 19/5, người bệnh chọn bệnh viện ngẫu nhiên từ 20/5.

### Nguồn

- VAST Challenge 2011, Mini-Challenge 1: Characterization of an Epidemic Spread (Visual Analytics Benchmark Repository, HCIL, ĐH Maryland).
- Answer Guide MC1 (tệp `MC1.pdf` trong kho lưu trữ trên).
""")
