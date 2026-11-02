vt_gi = toa_do_song(gi19["lon"], gi19["lat"])
hang = []
for ten_sk, tam in TAM.items():
    cach_song, vt_nguon = toa_do_song([tam[0]], [tam[1]])
    ha_luu = (vt_gi[1] > vt_nguon[0]) & (vt_gi[0] < 1.5)         # nằm phía hạ lưu và sát sông
    hang.append([ten_sk, round(cach_song[0], 2), 100 * ha_luu.mean()])
song = pd.DataFrame(hang, columns=["sự kiện", "cách sông (dặm)", "% ca dạ dày ở hạ lưu"]).set_index("sự kiện")
tong = diem.join(song)[["% ca trong dải xuôi gió", "cách sông (dặm)", "% ca dạ dày ở hạ lưu"]]
print(tong.round(1).sort_values("% ca trong dải xuôi gió", ascending=False).to_string())

fig, ax = plt.subplots(figsize=(7.5, 5.2))
for ten_sk, r in tong.iterrows():
    tot = ten_sk == NGUON
    ax.scatter(r["% ca trong dải xuôi gió"], r["cách sông (dặm)"], s=240 if tot else 90,
               color=GOLD if tot else GRAY, edgecolor=NAVY, zorder=3)
    ax.annotate(ten_sk, (r["% ca trong dải xuôi gió"], r["cách sông (dặm)"]),
                xytext=(7, -14) if ten_sk == "Hội nghị" else (7, 6),
                textcoords="offset points", fontsize=8, weight="bold" if tot else "normal")
ax.set_xlim(-5, 105); ax.invert_yaxis()
ax.set_xlabel("% ca giống cúm trong dải xuôi gió của sự kiện (càng sang phải càng khớp)")
ax.set_ylabel("khoảng cách từ sự kiện đến sông (dặm, càng lên cao càng gần)")
ax.set_title("Mỗi nghi phạm khớp với hai nhóm triệu chứng đến đâu?")
plt.tight_layout()
plt.show()
