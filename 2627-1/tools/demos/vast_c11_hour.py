tab = df.groupby(df["t"].dt.floor("h")).size().rename("n").to_frame()
tab["gio"] = tab.index.hour
tab["ngay"] = tab.index.date
binh_thuong = tab.iloc[: 14 * 24].groupby("gio")["n"].mean()       # mức theo từng giờ trong ngày
tab["ti_le"] = tab["n"] / tab["gio"].map(binh_thuong)
ratio = tab.pivot(index="ngay", columns="gio", values="ti_le")     # hàng: ngày, cột: giờ

print("Lần đầu lượng bài vượt 1,5 lần bình thường:", tab[tab["ti_le"] > 1.5].index[0])

fig, ax = plt.subplots(figsize=(10, 4.6))
im = ax.imshow(ratio.values, aspect="auto", cmap="YlOrRd", vmin=0.8, vmax=2.2)
ax.set_xticks(range(0, 24, 3)); ax.set_xticklabels([f"{h}h" for h in range(0, 24, 3)])
ax.set_yticks(range(len(ratio))); ax.set_yticklabels([d.strftime("%d/%m") for d in ratio.index], fontsize=8)
ax.set_title("Số bài mỗi giờ so với mức bình thường của giờ đó (lần)"); ax.grid(False)
plt.colorbar(im, ax=ax, label="lần")
plt.tight_layout()
plt.show()
