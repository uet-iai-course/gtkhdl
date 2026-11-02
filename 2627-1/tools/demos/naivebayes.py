import pandas as pd

# Dữ liệu mô phỏng: 10 khách hàng
df = pd.DataFrame({
    "Age":     ["Young", "Senior", "Middle", "Young", "Middle",
                "Senior", "Young", "Young", "Middle", "Senior"],
    "Student": ["Yes", "No", "Yes", "Yes", "Yes",
                "No", "No", "Yes", "Yes", "No"],
    "Income":  ["High", "High", "Medium", "Low", "Low",
                "Medium", "Medium", "Medium", "High", "Low"],
    "Credit":  ["Fair", "Excellent", "Fair", "Fair", "Excellent",
                "Excellent", "Excellent", "Fair", "Excellent", "Fair"],
    "Buys":    ["No", "Yes", "Yes", "No", "Yes",
                "No", "Yes", "Yes", "Yes", "No"],
})

# Khách hàng mới cần dự đoán
new = {"Age": "Young", "Student": "Yes",
       "Income": "Medium", "Credit": "Fair"}

# Naive Bayes tự cài đặt: P(C) * tích các P(x_i | C)
score = {}
for label, g in df.groupby("Buys"):
    s = len(g) / len(df)                  # P(C)
    for col, val in new.items():
        s *= (g[col] == val).mean()       # P(x_i | C)
    score[label] = s

total = sum(score.values())
for label, s in score.items():
    print(f"{label}: điểm = {s:.5f}, xác suất = {s / total:.2%}")

# Đối chiếu với scikit-learn
from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import OrdinalEncoder

features = ["Age", "Student", "Income", "Credit"]
enc = OrdinalEncoder()
X = enc.fit_transform(df[features])
x_new = enc.transform(pd.DataFrame([new])[features])

for alpha in (1e-10, 1.0):
    model = CategoricalNB(alpha=alpha).fit(X, df["Buys"])
    proba = model.predict_proba(x_new)[0]
    # model.classes_ = ['No', 'Yes']
    print(f"alpha={alpha:g}: P(No)={proba[0]:.4f}, "
          f"P(Yes)={proba[1]:.4f} -> {model.predict(x_new)[0]}")
