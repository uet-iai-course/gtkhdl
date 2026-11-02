khung_gi = []
moc3_gi = pd.date_range("2011-05-19", periods=16, freq="3h")
for t0 in moc3_gi:
    d = df[(df["t"] >= t0) & (df["t"] < t0 + pd.Timedelta(hours=3)) & df["gi"]]
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=80)
    base_map(ax, 0.3)
    ax.scatter(d["lon"], d["lat"], s=1.6, c=GI, alpha=0.45)
    ax.plot(SONG[:, 0], SONG[:, 1], color=NAVY, lw=1.4, ls="--")
    ax.plot(*TAM[NGUON], marker="*", ms=13, mfc=GOLD, mec=NAVY, zorder=5)
    ax.set_title(f"Ca dạ dày - ruột, {t0:%d/%m %Hh} đến {t0 + pd.Timedelta(hours=3):%Hh}  ({len(d):,} bài)", fontsize=9)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel(""); ax.set_ylabel("")
    fig.tight_layout(); fig.canvas.draw()
    khung_gi.append(PILImage.fromarray(np.asarray(fig.canvas.buffer_rgba())).convert("P", palette=PILImage.ADAPTIVE))
    plt.close(fig)

khung_gi[0].save("gi_spread.gif", save_all=True, append_images=khung_gi[1:], duration=500, loop=0)
print("Đã lưu gi_spread.gif:", len(khung_gi), "khung hình, mỗi khung 3 giờ")
try:
    display(GifImage("gi_spread.gif"))
except NameError:
    pass
