"""Nguồn duy nhất của phân tích Vastopolis (VAST Challenge 2011, Mini-Challenge 1).

Mỗi ô (cell) là một tuple (id, loại, nội dung).  Cùng một nguồn này được dùng để:
  1. chạy thật trên dữ liệu, lưu kết quả và hình vào slide (tools/vast/run_cells.py)
  2. sinh sổ tay Colab (tools/vast/make_notebook.py)
Vì vậy mã trong slide, mã trong Colab và số liệu trên slide luôn khớp nhau.

Quy ước: loại "md" là văn bản dẫn dắt (không nêu đáp án trước khi dữ liệu chứng minh),
loại "code" là mã Python, loại "hide" là mã chạy nhưng không đưa lên slide.
"""

CELLS = []


def md(cid, text):
    CELLS.append((cid, "md", text.strip("\n")))


def code(cid, text, show=True):
    CELLS.append((cid, "code" if show else "hide", text.strip("\n")))


# ======================================================================
# PHẦN 0. MỞ ĐẦU
# ======================================================================
md("m00", """
# Điều tra dịch bệnh ở Vastopolis

*Bài thực hành khoa học dữ liệu: trực quan hóa và kể chuyện với dữ liệu.*

Bạn là nhà phân tích dữ liệu của sở y tế thành phố **Vastopolis** (khoảng 2 triệu dân). Sáng nay, bệnh viện báo có nhiều ca bệnh lạ.
Bạn chỉ có **hơn một triệu bài đăng mạng xã hội** có gắn vị trí GPS và thời gian, cùng bản đồ, dân số và thời tiết.

Ba câu hỏi cần trả lời:

1. Bệnh **lây lan bằng cách nào**?
2. Dịch đã **được kiểm soát** hay chưa?
3. Bệnh **bắt nguồn từ đâu**?

Quy tắc của một nhà điều tra giỏi: **mỗi biểu đồ chỉ trả lời một câu hỏi, mỗi kết quả dẫn đến một giả thuyết mới,
mỗi giả thuyết phải được kiểm tra bằng một loại dữ liệu khác.** Sổ tay này sẽ đi lần lượt qua bảy bước điều tra,
và **không có đáp án nào được nêu trước khi dữ liệu cho thấy nó**.

Dữ liệu: VAST Challenge 2011, Mini-Challenge 1 (đây là dữ liệu mô phỏng, thành phố Vastopolis là hư cấu).
""")

# ======================================================================
# PHẦN 1. HỒ SƠ VỤ ÁN: CÓ GÌ TRONG TAY
# ======================================================================
md("m01", """
## Bước 1. Hồ sơ vụ án: ta đang có gì trong tay?

Việc đầu tiên của người phân tích là **kiểm kê**: tải dữ liệu về, xem có những tệp nào, mỗi tệp lớn cỡ nào.
""")

code("c01_setup", """
import os, re, urllib.request, zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PIL import Image

URL = "https://visualdata.wustl.edu/varepository/VAST_Challenge_2011/datasets/MC_1_Materials_3-30-2011.zip"
FOLDER = "MC_1_Materials_3-30-2011"

if not os.path.isdir(FOLDER):              # chỉ tải khi chưa có
    urllib.request.urlretrieve(URL, "mc1.zip")
    zipfile.ZipFile("mc1.zip").extractall(".")

for name in sorted(os.listdir(FOLDER)):
    size = os.path.getsize(os.path.join(FOLDER, name)) / 1e6
    print(f"{name:26s} {size:8.2f} MB")
""")

code("c02_style", """
# Định dạng đồ thị dùng chung (bảng màu dễ nhìn, phông có dấu tiếng Việt)
plt.rcParams.update({
    "figure.dpi": 110, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "axes.titleweight": "bold",
    "axes.titlesize": 12, "axes.labelsize": 10, "font.size": 10,
})
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 60)

FLU, GI, EVT = "#E4572E", "#0077B6", "#7B2CBF"     # cam đỏ, xanh nước, tím
NAVY, GRAY, GOLD = "#1F2A44", "#9AA5B1", "#F2A900"


def ngay_thang(ax, dinh_dang="%d/%m"):
    ax.xaxis.set_major_formatter(mdates.DateFormatter(dinh_dang))


def base_map(ax, alpha=0.45):
    \"\"\"Vẽ ảnh bản đồ Vastopolis làm nền (nhạt) với trục kinh độ, vĩ độ.\"\"\"
    ax.imshow(MAP_SMALL, extent=EXTENT, alpha=alpha, aspect=1 / np.cos(np.radians(42.2)), zorder=0)
    ax.set_xlim(EXTENT[0], EXTENT[1]); ax.set_ylim(EXTENT[2], EXTENT[3])
    ax.set_xlabel("kinh độ"); ax.set_ylabel("vĩ độ"); ax.grid(False)


def table_png(frame, title, widths=None):
    \"\"\"Vẽ một bảng dữ liệu thành hình ảnh.\"\"\"
    fig, ax = plt.subplots(figsize=(11, 0.4 * len(frame) + 1.2))
    ax.axis("off")
    tb = ax.table(cellText=frame.values, colLabels=list(frame.columns), cellLoc="left",
                  colWidths=widths, loc="center")
    tb.auto_set_font_size(False); tb.set_fontsize(8.5); tb.scale(1, 1.5)
    for (r, c), cell in tb.get_celld().items():
        cell.set_edgecolor("#D5DAE1")
        if r == 0:
            cell.set_facecolor(NAVY); cell.set_text_props(color="white", weight="bold")
        elif r % 2 == 0:
            cell.set_facecolor("#F3F5F8")
    ax.set_title(title, loc="left")
    plt.tight_layout()
""", show=False)

md("m02", """
Có **năm tệp**. Tệp lớn nhất là `Microblogs.csv` (hơn 100 MB): đó là các bài đăng. Hãy đọc nó và xem **cấu trúc** (số dòng, số cột, kiểu dữ liệu).
""")

code("c03_read", """
df = pd.read_csv(f"{FOLDER}/Microblogs.csv", encoding="latin-1")
print("Số dòng, số cột:", df.shape)
print()
print(df.dtypes)
print()
print(df.head(5).to_string(max_colwidth=48))
""")

code("c04_table", """
mau = df.sample(8, random_state=7)[["ID", "Created_at", "Location", "text"]].copy()
mau["text"] = mau["text"].fillna("").str.slice(0, 78)
table_png(mau, "Tám dòng ngẫu nhiên của Microblogs.csv", widths=[0.06, 0.13, 0.17, 0.64])
plt.show()
""")

md("m03", """
Mỗi dòng là **một bài đăng**: ai đăng (`ID`), đăng lúc nào (`Created_at`), đăng ở đâu (`Location`: vĩ độ và kinh độ) và nội dung (`text`).
Ngoài ra còn hai bảng nhỏ về dân số và thời tiết.
""")

code("c05_small", """
pop = pd.read_csv(f"{FOLDER}/Population.csv")
weather = pd.read_csv(f"{FOLDER}/Weather.csv")
print("Population.csv:", pop.shape)
print(pop.head(6).to_string(index=False))
print()
print("Weather.csv:", weather.shape)
print(weather.head(6).to_string(index=False))
""")

code("c06_map", """
MAP = Image.open(f"{FOLDER}/Vastopolis_Map.png")
print("Ảnh bản đồ:", MAP.size, "điểm ảnh, chế độ", MAP.mode)
MAP_SMALL = MAP.convert("RGB").resize((2600, 1322))      # thu nhỏ để vẽ nhanh

fig, ax = plt.subplots(figsize=(10, 5.1))
ax.imshow(MAP_SMALL); ax.axis("off")
ax.set_title("Vastopolis_Map.png: 13 khu vực, đường cao tốc, bệnh viện, sông")
plt.tight_layout()
plt.show()
""")

# ======================================================================
# PHẦN 2. KIỂM TRA CHẤT LƯỢNG DỮ LIỆU
# ======================================================================
md("m04", """
## Bước 2. Kiểm tra chất lượng: dữ liệu có đáng tin không?

Một nhà điều tra không tin lời khai khi chưa kiểm tra. Ta kiểm tra ba thứ: **vị trí**, **thời gian**, **nội dung**.
Cột `Location` đang là chuỗi `"vĩ độ kinh độ"`; cần tách thành hai số và đổi cột thời gian sang kiểu ngày giờ.
""")

code("c07_parse", """
loc = df["Location"].str.split(" ", expand=True).astype(float)
print("Kinh độ thô: nhỏ nhất", loc[1].min(), "| lớn nhất", loc[1].max())

df["lat"] = loc[0]
df["lon"] = -loc[1]            # tệp ghi kinh độ Tây mà thiếu dấu trừ, ta thêm lại
df["t"] = pd.to_datetime(df["Created_at"], format="%m/%d/%Y %H:%M", errors="coerce")

bad = df[df["t"].isna()]
print("Dòng có thời gian hỏng:", len(bad))
print(bad[["ID", "Created_at"]].head(4).to_string(index=False))
print("Bài không có nội dung:", df["text"].isna().sum(), "| dòng trùng hệt:", df.duplicated().sum())
print(df[["lat", "lon"]].describe().round(4).to_string())
""")

md("m05", """
Hai điều cần ghi nhớ: (1) **kinh độ bị thiếu dấu trừ**, và (2) **một số ít dòng có thời gian hỏng**.
Đừng lật dấu một cách mù quáng: hãy vẽ thử các bài đăng lên bản đồ để xem phép chiếu có hợp lý không.
Giả định: ảnh bản đồ phủ vừa khít vùng dữ liệu (góc ảnh trùng giá trị nhỏ nhất và lớn nhất của tọa độ).
""")

code("c08_checkmap", """
EXTENT = [df["lon"].min(), df["lon"].max(), df["lat"].min(), df["lat"].max()]

fig, ax = plt.subplots(figsize=(10, 5.1))
base_map(ax)
s = df.sample(40000, random_state=1)
ax.scatter(s["lon"], s["lat"], s=1.2, c=NAVY, alpha=0.35)
ax.set_title("40 000 bài đăng ngẫu nhiên đặt lên bản đồ")
plt.tight_layout()
plt.show()
""")

code("c09_clean", """
df = df.dropna(subset=["t"]).copy()               # bỏ dòng thời gian hỏng
df["text"] = df["text"].fillna("")
df["tl"] = df["text"].str.lower()                  # bản chữ thường để tìm từ khóa

per_user = df.groupby("ID").size()
print("Sau khi làm sạch:", len(df), "bài của", df["ID"].nunique(), "người dùng")
print("Khoảng thời gian:", df["t"].min(), "->", df["t"].max())
print("Số bài mỗi người:")
print(per_user.describe().round(2).to_string())
""")

# ======================================================================
# PHẦN 3. DÒNG THỜI GIAN
# ======================================================================
md("m06", """
## Bước 3. Dòng thời gian: khi nào có điều bất thường?

Câu hỏi đầu tiên của thám tử luôn là **"khi nào?"**. Đếm số bài đăng mỗi ngày, rồi so với mức bình thường của 14 ngày đầu.
""")

code("c10_daily", """
daily = df.groupby(df["t"].dt.date).size()
base = daily.iloc[:14]                              # 14 ngày đầu làm mốc bình thường
z = (daily - base.mean()) / base.std()

print(f"Mức bình thường: {base.mean():,.0f} bài/ngày (độ lệch chuẩn {base.std():,.0f})")
print(pd.DataFrame({"bài": daily, "z": z.round(1)}).tail(7).to_string())

fig, ax = plt.subplots(figsize=(10, 4.2))
ax.plot(daily.index, daily.values, color=NAVY, lw=2, marker="o", ms=4)
hot = daily[z > 3]
ax.scatter(hot.index, hot.values, color=FLU, s=60, zorder=3, label="vượt mốc 3 độ lệch chuẩn")
ax.axhline(base.mean(), color=GRAY, ls="--", lw=1)
ax.set_title("Số bài đăng mỗi ngày"); ax.set_ylabel("số bài"); ax.legend(frameon=False)
ngay_thang(ax); plt.tight_layout()
plt.show()
""")

code("c11_hour", """
tab = df.groupby(df["t"].dt.floor("h")).size().rename("n").to_frame()
tab["gio"] = tab.index.hour
tab["ngay"] = tab.index.date
binh_thuong = tab.iloc[: 14 * 24].groupby("gio")["n"].mean()       # mức theo từng giờ trong ngày
tab["ti_le"] = tab["n"] / tab["gio"].map(binh_thuong)
ratio = tab.pivot(index="ngay", columns="gio", values="ti_le")     # hàng: ngày, cột: giờ

print("Lần đầu lượng bài vượt 1,5 lần bình thường:", tab[tab["ti_le"] > 1.5].index[0])

fig, ax = plt.subplots(figsize=(10, 4.6))
im = ax.imshow(ratio.values, aspect="auto", cmap="YlOrRd", vmin=0.8, vmax=2.2)
ax.set_xticks(range(0, 24, 3)); ax.set_xticklabels([f"{h}h" for h in range(0, 24, 3)])
ax.set_yticks(range(len(ratio))); ax.set_yticklabels([d.strftime("%d/%m") for d in ratio.index], fontsize=8)
ax.set_title("Số bài mỗi giờ so với mức bình thường của giờ đó (lần)"); ax.grid(False)
plt.colorbar(im, ax=ax, label="lần")
plt.tight_layout()
plt.show()
""")

# ======================================================================
# PHẦN 4. NGƯỜI ĐĂNG ĐANG NÓI VỀ ĐIỀU GÌ?
# ======================================================================
md("m07", """
## Bước 4. Người ta đang nói về điều gì?

Số bài tăng, nhưng **tăng vì chủ đề nào**? Không đoán từ khóa: để dữ liệu tự nói.
Với mỗi từ, ta tính **độ nổi bật (lift)** = tần suất của từ trong ngày đó chia cho tần suất của từ trong những ngày bình thường.
Từ nào có lift rất lớn là từ "bỗng dưng được nhắc nhiều".
""")

code("c12_vocab", """
from sklearn.feature_extraction.text import CountVectorizer
from scipy import sparse

vec = CountVectorizer(token_pattern=r"[a-z']{3,}", min_df=30, binary=True)
X = vec.fit_transform(df["tl"])                        # bài × từ (có hoặc không)
vocab = np.array(vec.get_feature_names_out())

ngay0 = df["t"].dt.normalize().min()
day_idx = (df["t"].dt.normalize() - ngay0).dt.days.values
D = sparse.csr_matrix((np.ones(len(df)), (np.arange(len(df)), day_idx)))
C = (X.T @ D).toarray()                                # từ × ngày: số bài chứa từ
N = np.bincount(day_idx)                               # số bài mỗi ngày


def top_words(ngay, k=10, toi_thieu=300):
    \"\"\"Từ nổi bật nhất của một ngày so với TẤT CẢ các ngày trước đó.\"\"\"
    i = (pd.Timestamp(ngay) - ngay0).days
    truoc = C[:, :i].sum(1) / N[:i].sum()               # tần suất trước ngày đó
    lift = (C[:, i] / N[i]) / (truoc + 1 / N.sum())
    lift[C[:, i] < toi_thieu] = 0                       # bỏ từ quá hiếm (lỗi chính tả)
    best = np.argsort(-lift)[:k]
    return [(vocab[j], int(C[j, i]), round(float(lift[j]))) for j in best]


for ngay in ["2011-05-18", "2011-05-19", "2011-05-20"]:
    print(ngay[5:], [f"{w} ({lift}x)" for w, c, lift in top_words(ngay)])
""")

code("c13_topwords", """
fig, axes = plt.subplots(1, 3, figsize=(11, 3.8))
for ax, ngay, col in zip(axes, ["2011-05-18", "2011-05-19", "2011-05-20"], [FLU, GI, NAVY]):
    tw = top_words(ngay, k=8)[::-1]
    ax.barh([w for w, c, l in tw], [l for w, c, l in tw], color=col)
    ax.set_xscale("log"); ax.set_title(ngay[8:] + "/05")
    ax.tick_params(axis="x", which="minor", labelbottom=False)
    ax.set_xlabel("lift (lần, thang log)")
plt.tight_layout()
plt.show()
""")

md("m08", """
Các từ nổi bật là **triệu chứng**: sốt, ớn lạnh, khó thở, mệt mỏi... rồi sang ngày sau là buồn nôn, tiêu chảy, đau bụng.
Hai nhóm triệu chứng khác nhau. Ta gom từ khóa thành hai nhóm rồi đếm theo ngày:
nhóm **giống cúm** (hô hấp) và nhóm **dạ dày - ruột**.
""")

code("c14_groups", """
FLU_WORDS = ["fever", "chills", "sweats", "fatigue", "cough", "coughing", "shortness", "breath",
             "headache", "ache", "aches", "aching", "runny", "sore throat", "pneumonia", "flu",
             "bedridden", "debilitated", "sickly", "flem", "phlegm"]
GI_WORDS = ["diarrhea", "nausea", "nauseous", "vomit", "vomiting", "vomitting", "barfed", "puking",
            "cramps", "stomach", "heartburn", "tummy", "toilet", "queasy"]


def pattern(words):
    return r"\\b(?:" + "|".join(words) + r")\\b"


df["flu"] = df["tl"].str.contains(pattern(FLU_WORDS))
df["gi"] = df["tl"].str.contains(pattern(GI_WORDS))
df["ngay"] = df["t"].dt.date

theo_ngay = df.groupby("ngay")[["flu", "gi"]].sum()
print("Trung bình 14 ngày đầu:", theo_ngay.iloc[:14].mean().round(0).to_dict())
print(theo_ngay.tail(5).to_string())

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(theo_ngay.index, theo_ngay["flu"], color=FLU, lw=2.4, marker="o", ms=4, label="giống cúm")
ax.plot(theo_ngay.index, theo_ngay["gi"], color=GI, lw=2.4, marker="o", ms=4, label="dạ dày - ruột")
ax.set_title("Số bài nhắc đến từng nhóm triệu chứng mỗi ngày"); ax.set_ylabel("số bài")
ax.legend(frameon=False); ngay_thang(ax); plt.tight_layout()
plt.show()
""")

code("c15_onset", """
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
""")

# Các phần tiếp theo nằm trong cells_part*.py (cùng danh sách CELLS)
import pathlib as _pl

for _p in sorted(_pl.Path(__file__).parent.glob("cells_part*.py")):
    exec(compile(_p.read_text("utf-8"), str(_p), "exec"))
