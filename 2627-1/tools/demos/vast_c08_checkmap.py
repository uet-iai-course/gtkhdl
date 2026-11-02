EXTENT = [df["lon"].min(), df["lon"].max(), df["lat"].min(), df["lat"].max()]

fig, ax = plt.subplots(figsize=(10, 5.1))
base_map(ax)
s = df.sample(40000, random_state=1)
ax.scatter(s["lon"], s["lat"], s=1.2, c=NAVY, alpha=0.35)
ax.set_title("40 000 bài đăng ngẫu nhiên đặt lên bản đồ")
plt.tight_layout()
plt.show()
