from scipy.ndimage import gaussian_filter

xb = np.linspace(EXTENT[0], EXTENT[1], 140)
yb = np.linspace(EXTENT[2], EXTENT[3], 70)


def luoi(d):
    """Đếm số bài trong từng ô lưới."""
    H, _, _ = np.histogram2d(d["lat"], d["lon"], bins=[yb, xb])
    return H


nen = df[df["ngay"] < date(2011, 5, 15)]
n_nen = nen["ngay"].nunique()

fig, axes = plt.subplots(1, 2, figsize=(12, 4.3))
for ax, cot, cmap in zip(axes, ["flu", "gi"], ["Oranges", "Blues"]):
    vuot = luoi(ngay19[ngay19[cot]]) - luoi(nen[nen[cot]]) / n_nen     # trừ mức bình thường mỗi ngày
    vuot = gaussian_filter(np.clip(vuot, 0, None), 1.2)
    iy, ix = np.unravel_index(vuot.argmax(), vuot.shape)
    print(f"{ten[cot]}: ô đậm nhất quanh kinh độ {xb[ix]:.3f}, vĩ độ {yb[iy]:.3f}")
    base_map(ax, 0.3)
    ax.imshow(np.ma.masked_less(vuot, vuot.max() * 0.04), extent=EXTENT, origin="lower", cmap=cmap,
              aspect=1 / np.cos(np.radians(42.2)), alpha=0.85, zorder=2)
    ax.set_title(f"Mật độ bài {ten[cot]} vượt mức bình thường")
plt.tight_layout()
plt.show()
