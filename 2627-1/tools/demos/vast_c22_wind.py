HUONG = {"N": 0, "NNE": 22.5, "NE": 45, "ENE": 67.5, "E": 90, "ESE": 112.5, "SE": 135, "SSE": 157.5,
         "S": 180, "SSW": 202.5, "SW": 225, "WSW": 247.5, "W": 270, "WNW": 292.5, "NW": 315, "NNW": 337.5}
weather["ngay"] = pd.to_datetime(weather["Date"], format="%m/%d/%Y").dt.date
weather["gio_tu"] = weather["Wind_Direction"].map(HUONG)         # gió thổi TỪ hướng này
weather["gio_den"] = (weather["gio_tu"] + 180) % 360             # nên thổi ĐẾN hướng ngược lại
w = weather[weather["ngay"] >= date(2011, 5, 14)].reset_index(drop=True)
print(w[["Date", "Weather", "Average_Wind_Speed", "Wind_Direction", "gio_den"]].to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 2.9))
rad = np.radians(w["gio_den"])
mau = [GOLD if d in (date(2011, 5, 17), date(2011, 5, 18), date(2011, 5, 19)) else GRAY for d in w["ngay"]]
ax.quiver(range(len(w)), np.zeros(len(w)), np.sin(rad), np.cos(rad), color=mau, scale=9, width=0.012)
for i, r in w.iterrows():
    ax.text(i, -1.15, f"{r['ngay'].strftime('%d/%m')}\n{r['Average_Wind_Speed']} mph\ntừ {r['Wind_Direction']}",
            ha="center", va="top", fontsize=8)
ax.set_xlim(-0.6, len(w) - 0.4); ax.set_ylim(-2.3, 1); ax.axis("off")
ax.set_title("Hướng gió thổi đến (mũi tên hướng lên là về phía Bắc)")
plt.tight_layout()
plt.show()
