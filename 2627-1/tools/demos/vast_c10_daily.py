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
