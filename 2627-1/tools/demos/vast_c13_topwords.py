fig, axes = plt.subplots(1, 3, figsize=(11, 3.8))
for ax, ngay, col in zip(axes, ["2011-05-18", "2011-05-19", "2011-05-20"], [FLU, GI, NAVY]):
    tw = top_words(ngay, k=8)[::-1]
    ax.barh([w for w, c, l in tw], [l for w, c, l in tw], color=col)
    ax.set_xscale("log"); ax.set_title(ngay[8:] + "/05")
    ax.tick_params(axis="x", which="minor", labelbottom=False)
    ax.set_xlabel("lift (lần, thang log)")
plt.tight_layout()
plt.show()
