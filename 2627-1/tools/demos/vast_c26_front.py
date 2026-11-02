d = df[(df["t"] >= "2011-05-18") & (df["t"] < "2011-05-21") & df["flu"]].copy()
huong_ngay = d["ngay"].map(weather.set_index("ngay")["gio_den"])        # hướng gió của chính ngày đó
dx, dy = (d["lon"] - TAM[NGUON][0]) * kx, (d["lat"] - TAM[NGUON][1]) * ky
a = np.radians(huong_ngay)
d["doc"] = dx * np.sin(a) + dy * np.cos(a)                                 # dặm dọc theo hướng gió
d["khung"] = d["t"].dt.floor("6h")

tk = d.groupby("khung")["doc"].agg(trung_vi="median", p90=lambda s: s.quantile(0.9), so_bai="size")
print(tk.round(2).to_string())

fig, ax = plt.subplots(figsize=(10, 3.6))
ax.plot(tk.index, tk["trung_vi"], color=FLU, lw=2.4, marker="o", label="trung vị")
ax.plot(tk.index, tk["p90"], color=NAVY, lw=2.4, marker="s", label="90% ca nằm gần hơn mốc này")
ax.set_ylabel("khoảng cách xuôi gió từ nghi phạm (dặm)"); ax.set_ylim(0)
ax.set_title("Vùng có ca bệnh có mở rộng thêm theo thời gian không?")
ax.legend(frameon=False); ngay_thang(ax, "%d/%m %Hh"); plt.tight_layout()
plt.show()
