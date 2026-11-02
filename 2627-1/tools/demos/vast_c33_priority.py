tc19 = ngay19[ngay19["flu"] | ngay19["gi"]]
tc_nen = nen[nen["flu"] | nen["gi"]]
vuot = np.clip(luoi(tc19) - luoi(tc_nen) / n_nen, 0, None)
vuot = gaussian_filter(vuot, 1.0)

thu_tu = np.sort(vuot.ravel())[::-1]
so_o = np.searchsorted(np.cumsum(thu_tu) / thu_tu.sum(), 0.8) + 1
nguong = thu_tu[so_o - 1]
dien_tich_o = (xb[1] - xb[0]) * kx * (yb[1] - yb[0]) * ky
tong_dt = (EXTENT[1] - EXTENT[0]) * kx * (EXTENT[3] - EXTENT[2]) * ky
print(f"Vùng ưu tiên chứa 80% bài vượt mức: {so_o} ô, khoảng {so_o * dien_tich_o:.0f} dặm vuông, "
      f"bằng {100 * so_o * dien_tich_o / tong_dt:.0f}% diện tích thành phố ({tong_dt:.0f} dặm vuông)")

fig, ax = plt.subplots(figsize=(10, 5.2))
base_map(ax, 0.4)
ax.contourf((xb[:-1] + xb[1:]) / 2, (yb[:-1] + yb[1:]) / 2, vuot, levels=[nguong, vuot.max() * 2],
            colors=[FLU], alpha=0.45, zorder=2)
ax.plot(SONG[:, 0], SONG[:, 1], color=NAVY, lw=1.6, ls="--", zorder=3)
ax.plot(*TAM[NGUON], marker="*", ms=16, mfc=GOLD, mec=NAVY, zorder=5)
ax.scatter(bv[:, 0], bv[:, 1], marker="P", s=70, color=GOLD, edgecolor=NAVY, zorder=5)
ax.set_title("Vùng ưu tiên (chứa 80% bài triệu chứng vượt mức), sông, bệnh viện")
plt.tight_layout()
plt.show()
