"""Mã nguồn các ví dụ trong bài 3 và bài 4.

Chạy `python tools/build_demos.py` để tách thành từng tệp trong tools/demos/,
chạy từng tệp và lưu kết quả thực vào tools/demos/out/. Slide lấy mã và kết quả
từ chính các tệp này, nên số trên slide luôn là số do máy in ra.
"""

DEMOS = {}

DEMOS["bayes"] = r'''
# Bayesian inference: dự đoán khả năng mua hàng

p_buy = 0.20
p_cart_given_buy = 0.80
p_cart = 0.30

p_buy_given_cart = (
    p_cart_given_buy * p_buy / p_cart
)

print(f"P(Mua | Thêm giỏ) = {p_buy_given_cart:.2%}")
'''

DEMOS["abtest"] = r'''
from scipy.stats import norm
import numpy as np

# Nhóm A: 500 người, 25 người mua
# Nhóm B: 500 người, 30 người mua
n_a, x_a = 500, 25
n_b, x_b = 500, 30

p_a = x_a / n_a
p_b = x_b / n_b

p_pool = (x_a + x_b) / (n_a + n_b)

se = np.sqrt(
    p_pool * (1 - p_pool) *
    (1 / n_a + 1 / n_b)
)

z = (p_b - p_a) / se
p_value = 2 * norm.sf(abs(z))

print("Conversion A:", p_a)
print("Conversion B:", p_b)
print("Z-score:", z)
print("P-value:", p_value)

if p_value < 0.05:
    print("Có bằng chứng về sự khác biệt.")
else:
    print("Chưa đủ bằng chứng về sự khác biệt.")
'''

DEMOS["pca"] = r'''
import numpy as np
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

data = load_iris()
X = data.data

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

print("Kích thước ban đầu:", X.shape)
print("Sau PCA:", X_reduced.shape)
print("Tỷ lệ phương sai giữ lại:",
      pca.explained_variance_ratio_)
'''

DEMOS["cosine"] = r'''
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

products = np.array([
    [1, 2, 3],
    [2, 4, 6],
    [1, -1, 0],
    [1, 2, 2]
])

similarity = cosine_similarity(products)

print(np.round(similarity, 3))

# Tìm sản phẩm giống sản phẩm đầu tiên nhất
scores = similarity[0].copy()
scores[0] = -1

best = np.argmax(scores)

print("Sản phẩm tương tự nhất:", best)
print("Độ tương đồng:", scores[best])
'''

DEMOS["gradient"] = r'''
w = 5.0
learning_rate = 0.1

for i in range(30):
    loss = (w - 3) ** 2
    gradient = 2 * (w - 3)

    w = w - learning_rate * gradient

    print(i, round(w, 5), round(loss, 5))

print("Nghiệm gần tối ưu:", w)
'''

DEMOS["integral"] = r'''
from scipy.integrate import quad

def sales_rate(t):
    return 2 * t + 1

total, error = quad(sales_rate, 0, 3)

print("Tổng lượng hàng bán:", total)
print("Sai số ước lượng:", error)
'''

DEMOS["linprog"] = r'''
from scipy.optimize import linprog

# scipy tìm MIN, nên đổi dấu để tìm MAX
c = [-100, -60]

A = [
    [2, 1],
    [1, 2]
]

b = [100, 80]

result = linprog(
    c,
    A_ub=A,
    b_ub=b,
    bounds=[(0, None), (0, None)],
    method="highs"
)

print("Số sản phẩm A:", result.x[0])
print("Số sản phẩm B:", result.x[1])
print("Lợi nhuận tối đa:", -result.fun, "nghìn đồng")
'''

DEMOS["sgd"] = r'''
from sklearn.datasets import make_regression
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

X, y = make_regression(
    n_samples=1000,
    n_features=5,
    noise=15,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = SGDRegressor(
    max_iter=2000,
    learning_rate="invscaling",
    eta0=0.01,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("MSE:", mean_squared_error(y_test, pred))
print("Parameters:", model.coef_)
'''

DEMOS["pagerank"] = r'''
import networkx as nx

G = nx.DiGraph()

G.add_edges_from([
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("C", "A"),
    ("D", "C"),
    ("D", "A"),
    ("E", "C")
])

scores = nx.pagerank(G, alpha=0.85)

for node, score in sorted(
    scores.items(),
    key=lambda item: item[1],
    reverse=True
):
    print(node, round(score, 4))
'''

DEMOS["shortest"] = r'''
import networkx as nx

G = nx.Graph()

G.add_weighted_edges_from([
    ("A", "B", 4),
    ("A", "C", 2),
    ("B", "C", 1),
    ("B", "D", 5),
    ("C", "D", 8),
    ("C", "E", 10),
    ("D", "E", 2)
])

path = nx.shortest_path(
    G, "A", "E", weight="weight"
)

distance = nx.shortest_path_length(
    G, "A", "E", weight="weight"
)

print("Đường đi:", path)
print("Chi phí:", distance)
'''

DEMOS["entropy"] = r'''
import numpy as np
from scipy.stats import entropy

distributions = [
    [0.5, 0.5],
    [0.9, 0.1],
    [1.0, 0.0]
]

for p in distributions:
    print(entropy(p, base=2))
'''

DEMOS["tree"] = r'''
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = DecisionTreeClassifier(
    criterion="entropy",
    max_depth=4,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))
print("Information gain:", model.feature_importances_)
'''

DEMOS["finitediff"] = r'''
def f(x):
    return x ** 2

x = 3.0
h = 0.001

numerical_derivative = (f(x + h) - f(x)) / h
exact_derivative = 2 * x

print("Đạo hàm xấp xỉ:", numerical_derivative)
print("Đạo hàm chính xác:", exact_derivative)
'''

DEMOS["newton"] = r'''
def newton_sqrt(number, initial=1.0, iterations=10):
    x = initial

    for i in range(iterations):
        x = 0.5 * (x + number / x)
        print(i + 1, x)

    return x

result = newton_sqrt(10)
print("Kết quả:", result)
'''

DEMOS["euclid"] = r'''
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

customers = np.array([
    [2, 3],
    [5, 7],
    [2, 4],
    [9, 10]
])

distances = euclidean_distances(customers)

print(distances)

# Khách hàng gần nhất với khách hàng đầu tiên
scores = distances[0].copy()
scores[0] = np.inf

nearest = np.argmin(scores)

print("Khách hàng gần nhất:", nearest)
'''

DEMOS["persistent"] = r'''
import numpy as np
import gudhi as gd
import matplotlib.pyplot as plt

# Sinh dữ liệu nằm gần một đường tròn
np.random.seed(42)

n = 100
theta = np.linspace(0, 2*np.pi, n, endpoint=False)

X = np.column_stack([
    np.cos(theta),
    np.sin(theta)
])

X += np.random.normal(0, 0.03, X.shape)

# Xây dựng Vietoris-Rips complex
rips = gd.RipsComplex(
    points=X,
    max_edge_length=1.0
)

simplex_tree = rips.create_simplex_tree(
    max_dimension=2
)

# Tính persistent homology
persistence = simplex_tree.persistence()

# In các khoảng tồn tại
for dim, interval in persistence:
    print(
        "Dimension:", dim,
        "Birth/Death:", interval
    )

# Vẽ biểu đồ persistence
gd.plot_persistence_diagram(persistence)
plt.show()
'''

DEMOS["naivebayes"] = r"""
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
"""