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
