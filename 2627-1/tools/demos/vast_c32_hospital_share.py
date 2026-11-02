def gan_benh_vien(d, r=0.35):
    """Tỉ lệ bài nằm trong r dặm quanh một bệnh viện."""
    kc = np.hypot((d["lon"].values[:, None] - bv[:, 0]) * kx, (d["lat"].values[:, None] - bv[:, 1]) * ky)
    return (kc.min(1) < r).mean()


df["flu_tu"] = df["flu"] & ~df["nguoi_khac"]               # bài cúm do người bệnh tự kể

hang = []
for ngay in [date(2011, 5, 17), date(2011, 5, 18), date(2011, 5, 19), date(2011, 5, 20)]:
    ban_ngay_ = df[(df["ngay"] == ngay) & (df["t"].dt.hour >= 8)]
    hang.append([ngay.strftime("%d/%m"), 100 * gan_benh_vien(ban_ngay_[ban_ngay_["flu_tu"]]),
                 100 * gan_benh_vien(ban_ngay_[ban_ngay_["gi"]]), 100 * gan_benh_vien(ban_ngay_[~ban_ngay_["flu"]])])
bang_bv = pd.DataFrame(hang, columns=["ngày", "% bài cúm tự báo gần BV", "% bài dạ dày gần BV", "% bài khác gần BV"])
print(bang_bv.round(1).to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 3.4))
x = np.arange(len(bang_bv)); rong = 0.27
ax.bar(x - rong, bang_bv.iloc[:, 1], rong, color=FLU, label="giống cúm (tự báo)")
ax.bar(x, bang_bv.iloc[:, 2], rong, color=GI, label="dạ dày - ruột")
ax.bar(x + rong, bang_bv.iloc[:, 3], rong, color=GRAY, label="bài khác")
ax.set_xticks(x); ax.set_xticklabels(bang_bv["ngày"])
ax.set_ylabel("% bài trong 0,35 dặm quanh bệnh viện"); ax.legend(frameon=False)
ax.set_title("Người bệnh dồn về bệnh viện vào ngày nào?")
plt.tight_layout()
plt.show()
