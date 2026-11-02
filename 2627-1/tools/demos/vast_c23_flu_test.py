huong = weather.set_index("ngay").loc[date(2011, 5, 18), "gio_den"]
cua_so = df[(df["t"] >= "2011-05-18 06:00") & (df["t"] < "2011-05-18 14:00") & df["flu"]]
print(f"Gió 18/5 thổi về hướng {huong:.0f} độ (90 = Đông). Số bài giống cúm trong cửa sổ: {len(cua_so)}")


def toa_do_gio(d, tam, huong):
    """Khoảng cách dọc theo gió và lệch ngang so với đường gió đi qua `tam` (đơn vị dặm)."""
    dx, dy = (d["lon"] - tam[0]) * kx, (d["lat"] - tam[1]) * ky
    a = np.radians(huong)
    return (dx * np.sin(a) + dy * np.cos(a)).values, (-dx * np.cos(a) + dy * np.sin(a)).values


hang = []
for ten_sk, tam in TAM.items():
    doc, ngang = toa_do_gio(cua_so, tam, huong)
    hang.append([ten_sk, 100 * (doc < 0).mean(), 100 * ((doc > 0) & (np.abs(ngang) < 1.5)).mean()])
diem = pd.DataFrame(hang, columns=["sự kiện", "% ca ngược gió", "% ca trong dải xuôi gió"]).set_index("sự kiện")
print(diem.round(1).sort_values("% ca trong dải xuôi gió", ascending=False).to_string())

fig, ax = plt.subplots(figsize=(9, 3.6))
s = diem["% ca trong dải xuôi gió"].sort_values()
ax.barh(s.index, s.values, color=[FLU if v == s.max() else GRAY for v in s.values])
ax.set_xlabel("% số ca giống cúm (6h-14h, 18/5) nằm trong dải hẹp xuôi gió của sự kiện")
ax.set_title("Sự kiện nào giải thích được vị trí các ca giống cúm?")
plt.tight_layout()
plt.show()
