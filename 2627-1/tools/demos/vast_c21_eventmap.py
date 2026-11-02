mau_sk = ["#8D99AE", "#2A9D8F", "#6A994E", "#264653", "#E07A5F", "#B5838D", EVT, "#F2A900"]
lech = {"Triển lãm đồ cổ": (-40, 32), "Lễ hội": (12, -14), "Hội nghị": (14, 16), "Dọa đánh bom": (-120, -30),
        "Tòa nhà Capital": (-50, 22)}                  # độ lệch nhãn để không đè lên nhau
fig, ax = plt.subplots(figsize=(10, 5.2))
base_map(ax, 0.4)
for (ten_sk, (mau_tu, ngay)), mau in zip(SU_KIEN.items(), mau_sk):
    d = BAI_SK[ten_sk]
    ax.scatter(d["lon"], d["lat"], s=3, color=mau, alpha=0.3)
    x, y = TAM[ten_sk]
    ax.scatter([x], [y], s=150, color=mau, edgecolor="white", linewidth=1.6, zorder=4)
    ax.annotate(f"{ten_sk} ({ngay[8:]}/5)", (x, y), xytext=lech.get(ten_sk, (8, 7)), textcoords="offset points",
                fontsize=8, weight="bold", color=NAVY, zorder=5,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8))
ax.set_title("Tám sự kiện bất thường trước 18/5, mỗi sự kiện một chỗ")
plt.tight_layout()
plt.show()
