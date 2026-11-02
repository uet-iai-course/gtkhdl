SONG = np.array([(-93.350, 42.302), (-93.356, 42.290), (-93.362, 42.275), (-93.367, 42.262), (-93.375, 42.250),
                 (-93.390, 42.241), (-93.405, 42.236), (-93.418, 42.231), (-93.430, 42.226), (-93.445, 42.219),
                 (-93.46, 42.212), (-93.48, 42.204), (-93.50, 42.196), (-93.515, 42.187), (-93.525, 42.178),
                 (-93.530, 42.168), (-93.533, 42.160)])      # sông Vast, số hóa tay từ ảnh bản đồ (bắc xuống nam)
xy = np.c_[SONG[:, 0] * kx, SONG[:, 1] * ky]
doan = np.diff(xy, axis=0)
dai = np.hypot(*doan.T)
cong_don = np.r_[0, dai.cumsum()]


def toa_do_song(lon, lat):
    """Trả về (khoảng cách đến sông, vị trí dọc sông tính từ phía bắc), đơn vị dặm."""
    P = np.c_[np.asarray(lon) * kx, np.asarray(lat) * ky]
    gan, vt = np.full(len(P), 1e9), np.zeros(len(P))
    for a, v, L, c0 in zip(xy[:-1], doan, dai, cong_don[:-1]):
        t = np.clip(((P - a) @ v) / (L * L), 0, 1)
        kc = np.hypot(*(P - (a + t[:, None] * v)).T)
        tot = kc < gan
        gan[tot], vt[tot] = kc[tot], c0 + t[tot] * L
    return gan, vt


gi19 = ngay19[ngay19["gi"]]
kc_gi, _ = toa_do_song(gi19["lon"], gi19["lat"])
kc_all, _ = toa_do_song(ngay19["lon"], ngay19["lat"])
for r in (1.0, 1.5, 3.0):
    print(f"Trong {r} dặm quanh sông: {100 * (kc_gi < r).mean():.1f}% bài dạ dày - ruột, "
          f"{100 * (kc_all < r).mean():.1f}% mọi bài cùng ngày")

fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw={"width_ratios": [1.5, 1]})
base_map(axes[0], 0.3)
axes[0].scatter(gi19["lon"], gi19["lat"], s=1.5, c=GI, alpha=0.35)
axes[0].plot(SONG[:, 0], SONG[:, 1], color=NAVY, lw=1.6, ls="--")
axes[0].set_title("Bài dạ dày - ruột (19/5) và đường sông")
axes[1].hist(kc_all, bins=np.arange(0, 8, 0.25), density=True, color=GRAY, alpha=0.6, label="mọi bài")
axes[1].hist(kc_gi, bins=np.arange(0, 8, 0.25), density=True, color=GI, alpha=0.7, label="dạ dày - ruột")
axes[1].axvline(1.5, color=NAVY, ls=":")
axes[1].set_xlabel("khoảng cách đến sông (dặm)"); axes[1].set_ylabel("mật độ"); axes[1].legend(frameon=False)
axes[1].set_title("Khoảng cách đến sông")
plt.tight_layout()
plt.show()
