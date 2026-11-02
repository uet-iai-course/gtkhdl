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
