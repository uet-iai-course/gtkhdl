from PIL import Image as PILImage

khung = []
moc3 = pd.date_range("2011-05-18", periods=24, freq="3h")
for t0 in moc3:
    d = df[(df["t"] >= t0) & (df["t"] < t0 + pd.Timedelta(hours=3)) & df["flu"]]
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=80)
    base_map(ax, 0.3)
    ax.scatter(d["lon"], d["lat"], s=1.2, c=FLU, alpha=0.4)
    ax.plot(*TAM[NGUON], marker="*", ms=13, mfc=GOLD, mec=NAVY, zorder=5)
    ax.set_title(f"Ca giống cúm, {t0:%d/%m %Hh} đến {t0 + pd.Timedelta(hours=3):%Hh}  ({len(d):,} bài)", fontsize=9)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel(""); ax.set_ylabel("")
    fig.tight_layout(); fig.canvas.draw()
    khung.append(PILImage.fromarray(np.asarray(fig.canvas.buffer_rgba())).convert("P", palette=PILImage.ADAPTIVE))
    plt.close(fig)

khung[0].save("flu_spread.gif", save_all=True, append_images=khung[1:], duration=450, loop=0)
print("Đã lưu flu_spread.gif:", len(khung), "khung hình, mỗi khung 3 giờ")
try:
    from IPython.display import Image as GifImage, display
    display(GifImage("flu_spread.gif"))
except ImportError:
    pass
