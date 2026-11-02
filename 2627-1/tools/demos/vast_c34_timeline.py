t_sk = BAI_SK[NGUON]["t"].quantile(0.1)
t_cum = thoi_diem_bat_dau("flu")[0]
gio_flu = df.groupby(df["t"].dt.floor("h"))["flu"].sum()
t_bung = gio_flu[gio_flu > 20 * gio_flu.iloc[: 14 * 24].mean()].index[0]
t_gi = thoi_diem_bat_dau("gi")[0]
hai_20 = df[(df["t"] >= "2011-05-19") & df["flu_tu"]]
ti_le_bv = hai_20.groupby(hai_20["t"].dt.floor("h")).apply(gan_benh_vien)
t_bv = ti_le_bv[ti_le_bv > 0.3].index[0]

cac_moc = [(t_sk, f"{NGUON}\n(10% bài đăng đầu)", EVT), (t_cum, "bắt đầu có\nca giống cúm", FLU),
           (t_bung, "ca giống cúm\nbùng nổ", FLU), (t_gi, "bắt đầu có ca\ndạ dày - ruột", GI),
           (t_bv, "người bệnh dồn\nvề bệnh viện", GOLD)]
for t, ten_moc, _ in cac_moc:
    print(f"{t:%d/%m %H:%M}  {ten_moc.replace(chr(10), ' ')}")

fig, ax = plt.subplots(figsize=(11, 2.8))
ax.hlines(0, cac_moc[0][0] - pd.Timedelta(hours=8), cac_moc[-1][0] + pd.Timedelta(hours=8), color=NAVY, lw=2)
for i, (t, ten_moc, mau) in enumerate(cac_moc):
    ax.scatter([t], [0], s=150, color=mau, edgecolor=NAVY, zorder=3)
    ax.annotate(f"{t:%d/%m %Hh}\n{ten_moc}", (t, 0), xytext=(0, 20 if i % 2 == 0 else -50),
                textcoords="offset points", ha="center", fontsize=8.5)
ax.set_ylim(-1, 1); ax.axis("off"); ax.set_title("Dòng thời gian của vụ dịch (rút ra từ dữ liệu)")
plt.tight_layout()
plt.show()
