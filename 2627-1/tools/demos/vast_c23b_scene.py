co_hai = df["tl"].str.contains(r"\btrucks?\b") & df["tl"].str.contains(r"\baccident\b")
so_ngay = co_hai.groupby(df["ngay"]).sum()
print(f"Bài chứa cả 'truck' lẫn 'accident': ngày 17/5 có {so_ngay[date(2011, 5, 17)]}, "
      f"trung bình mỗi ngày trong 14 ngày đầu chỉ {so_ngay.iloc[:14].mean():.1f}")

hien_truong = df[co_hai & (df["ngay"] == date(2011, 5, 17))]
print("Giờ đăng sớm của nhóm bài này (10% đầu tiên):", hien_truong["t"].quantile(0.1).strftime("%H:%M"))
print("Ba bài đăng thật:")
for noi_dung in hien_truong["text"].sample(3, random_state=4):
    print(" -", noi_dung[:100])
