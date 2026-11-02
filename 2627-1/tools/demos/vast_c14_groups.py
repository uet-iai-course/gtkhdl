FLU_WORDS = ["fever", "chills", "sweats", "fatigue", "cough", "coughing", "shortness", "breath",
             "headache", "ache", "aches", "aching", "runny", "sore throat", "pneumonia", "flu",
             "bedridden", "debilitated", "sickly", "flem", "phlegm"]
GI_WORDS = ["diarrhea", "nausea", "nauseous", "vomit", "vomiting", "vomitting", "barfed", "puking",
            "cramps", "stomach", "heartburn", "tummy", "toilet", "queasy"]


def pattern(words):
    return r"\b(?:" + "|".join(words) + r")\b"


df["flu"] = df["tl"].str.contains(pattern(FLU_WORDS))
df["gi"] = df["tl"].str.contains(pattern(GI_WORDS))
df["ngay"] = df["t"].dt.date

theo_ngay = df.groupby("ngay")[["flu", "gi"]].sum()
print("Trung bình 14 ngày đầu:", theo_ngay.iloc[:14].mean().round(0).to_dict())
print(theo_ngay.tail(5).to_string())

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(theo_ngay.index, theo_ngay["flu"], color=FLU, lw=2.4, marker="o", ms=4, label="giống cúm")
ax.plot(theo_ngay.index, theo_ngay["gi"], color=GI, lw=2.4, marker="o", ms=4, label="dạ dày - ruột")
ax.set_title("Số bài nhắc đến từng nhóm triệu chứng mỗi ngày"); ax.set_ylabel("số bài")
ax.legend(frameon=False); ngay_thang(ax); plt.tight_layout()
plt.show()
