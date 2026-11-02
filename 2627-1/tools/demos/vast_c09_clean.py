df = df.dropna(subset=["t"]).copy()               # bỏ dòng thời gian hỏng
df["text"] = df["text"].fillna("")
df["tl"] = df["text"].str.lower()                  # bản chữ thường để tìm từ khóa

per_user = df.groupby("ID").size()
print("Sau khi làm sạch:", len(df), "bài của", df["ID"].nunique(), "người dùng")
print("Khoảng thời gian:", df["t"].min(), "->", df["t"].max())
print("Số bài mỗi người:")
print(per_user.describe().round(2).to_string())
