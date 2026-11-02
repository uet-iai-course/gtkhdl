trung_vi = np.median(C, axis=1)                        # số bài chứa từ trong một ngày điển hình
dinh, ngay_dinh = C.max(1), C.argmax(1)               # ngày cao nhất của từng từ
lan = dinh / (trung_vi + 3)
chon = (dinh >= 150) & (lan >= 8)

bung_no = pd.DataFrame({"tu": vocab[chon], "ngay": ngay_dinh[chon], "lan": lan[chon]})
for i, g in bung_no.sort_values("lan", ascending=False).groupby("ngay"):
    ngay_str = (ngay0 + pd.Timedelta(days=int(i))).strftime("%d/%m")
    print(ngay_str, "|", ", ".join(g["tu"].head(6)))
