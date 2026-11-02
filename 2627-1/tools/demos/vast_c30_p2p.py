# Bài "nói về người khác": có tên riêng + has/is, hoặc các đại từ he/she/they...
NGUOI_KHAC = r"\b[A-Z][a-z]{2,} (?:has|is|had) |\b(?:[Tt]hey|[Tt]hem|[Tt]heir|[Ss]he|[Hh]e|[Hh]is|[Hh]er)\b"
df["nguoi_khac"] = df["text"].str.contains(NGUOI_KHAC)
print("Ví dụ bài nói về người khác:")
print(df[df["flu"] & df["nguoi_khac"]]["text"].head(3).to_string(index=False))


def thong_ke_nguoi(cot):
    d = df[df[cot] & (df["t"] >= "2011-05-17")]
    tu_bao = d[~d["nguoi_khac"]]                                    # bài tự kể về mình
    lan_dau = tu_bao.groupby("ID")["ngay"].min().value_counts().sort_index()
    return pd.DataFrame({
        "bài": d.groupby("ngay").size(),
        "% nói về người khác": (100 * d.groupby("ngay")["nguoi_khac"].mean()).round(0),
        "người tự báo": tu_bao.groupby("ngay")["ID"].nunique(),
        "người tự báo mới": lan_dau}).fillna(0).astype(int)


tk_flu, tk_gi = thong_ke_nguoi("flu"), thong_ke_nguoi("gi")
print("Nhóm giống cúm:"); print(tk_flu.to_string())
print("Nhóm dạ dày - ruột:"); print(tk_gi.to_string())

fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.6))
x = np.arange(len(tk_flu))
nhan_ngay = [d.strftime("%d/%m") for d in tk_flu.index]
axes[0].bar(x, tk_flu["người tự báo"], color=FLU, alpha=0.35, label="người tự báo (tổng)")
axes[0].bar(x, tk_flu["người tự báo mới"], color=FLU, label="trong đó, người mới")
axes[0].set_xticks(x); axes[0].set_xticklabels(nhan_ngay); axes[0].legend(frameon=False, fontsize=8)
axes[0].set_title("Người tự báo triệu chứng cúm: số người mới mỗi ngày")
axes[1].plot(x, tk_flu["% nói về người khác"], color=FLU, marker="o", lw=2.4, label="giống cúm")
axes[1].plot(tk_gi.index.map(lambda d: (d - tk_flu.index[0]).days), tk_gi["% nói về người khác"],
             color=GI, marker="o", lw=2.4, label="dạ dày - ruột")
axes[1].set_xticks(x); axes[1].set_xticklabels(nhan_ngay); axes[1].legend(frameon=False, fontsize=8)
axes[1].set_ylabel("% bài nói về người khác"); axes[1].set_title("Bài nói về người khác")
plt.tight_layout()
plt.show()
