mau = df.sample(8, random_state=7)[["ID", "Created_at", "Location", "text"]].copy()
mau["text"] = mau["text"].fillna("").str.slice(0, 78)
table_png(mau, "Tám dòng ngẫu nhiên của Microblogs.csv", widths=[0.06, 0.13, 0.17, 0.64])
plt.show()
