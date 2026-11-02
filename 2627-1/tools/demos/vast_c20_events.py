SU_KIEN = {   # tên đặt theo từ khóa nổi bật, mẫu tìm kiếm, ngày
    "Triển lãm đồ cổ": (r"\bantique\b", "2011-05-04"),
    "Lễ hội": (r"\bfestival\b", "2011-05-07"),
    "Hội nghị": (r"\bconvention\b", "2011-05-11"),
    "Máy bay rơi": (r"\b(?:plane|airport|crashed|crashing)\b", "2011-05-13"),
    "Tòa nhà Capital": (r"\b(?:capital|blaze)\b", "2011-05-14"),
    "Dọa đánh bom": (r"\b(?:bomb|bombs|threats?)\b", "2011-05-16"),
    "Xe tải, tai nạn": (r"\b(?:truck|trucks|accident|wrecked|bridge)\b", "2011-05-17"),
    "Nổ, khói bụi": (r"\b(?:explosions?|smog|rattle|shook|boom|blast)\b", "2011-05-17"),
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
