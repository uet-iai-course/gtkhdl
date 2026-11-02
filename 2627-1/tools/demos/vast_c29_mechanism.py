def chi_so(d, huong):
    """Hai chỉ số cho một tập bài: % trong dải xuôi gió của nguồn, và % sát sông (<= 1,5 dặm)."""
    doc, ngang = toa_do_gio(d, TAM[NGUON], huong)
    trong_dai = ((doc > 0) & (doc < 12) & (np.abs(ngang) < 1.5)).mean()
    sat_song = (toa_do_song(d["lon"], d["lat"])[0] < 1.5).mean()
    return [100 * trong_dai, 100 * sat_song]


g = weather.set_index("ngay")["gio_den"]
cum = df[(df["ngay"] == date(2011, 5, 18)) & df["flu"]]
da_day = df[(df["ngay"] == date(2011, 5, 19)) & df["gi"]]
thuong = df[df["ngay"] == date(2011, 5, 19)]

bang_cs = pd.DataFrame([chi_so(cum, g[date(2011, 5, 18)]), chi_so(da_day, g[date(2011, 5, 19)]),
                        chi_so(thuong, g[date(2011, 5, 19)])],
                       index=["ca giống cúm (18/5)", "ca dạ dày - ruột (19/5)", "mọi bài (19/5)"],
                       columns=["% trong dải xuôi gió (không khí)", "% sát sông (nước)"])
print(bang_cs.round(1).to_string())

fig, ax = plt.subplots(figsize=(7.5, 3.2))
im = ax.imshow(bang_cs.values, cmap="Blues", vmin=0, vmax=100, aspect="auto")
ax.set_xticks([0, 1]); ax.set_xticklabels(["xuôi gió\n(không khí)", "sát sông\n(nước)"])
ax.set_yticks(range(3)); ax.set_yticklabels(bang_cs.index)
for i in range(3):
    for j in range(2):
        v = bang_cs.values[i, j]
        ax.text(j, i, f"{v:.0f}%", ha="center", va="center", color="white" if v > 55 else NAVY, weight="bold")
ax.grid(False); ax.set_title("Mỗi nhóm triệu chứng khớp với cơ chế nào?")
plt.tight_layout()
plt.show()
