"""Sinh các hình minh họa cho bài 3 và bài 4 từ chính số liệu trong ví dụ.

Chạy:  python tools/make_figures.py
Kết quả: img/lec03/*.png, img/lec04/*.png
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import Polygon, Rectangle

ROOT = Path(__file__).resolve().parent.parent
L3 = ROOT / "img" / "lec03"
L4 = ROOT / "img" / "lec04"
L3.mkdir(parents=True, exist_ok=True)
L4.mkdir(parents=True, exist_ok=True)

BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#2A7291", "#E8890C", "#2E8B57", "#E62727", "#6D4AA8", "#8A8A8A"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 12, "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#444", "axes.labelcolor": "#222", "figure.dpi": 100, "savefig.dpi": 160,
})


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", path.relative_to(ROOT))


# ------------------------------------------------------------------ bài 3
def fig_lln():
    rng = np.random.default_rng(42)
    tosses = rng.integers(0, 2, 5000)
    freq = np.cumsum(tosses) / np.arange(1, tosses.size + 1)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(np.arange(1, tosses.size + 1), freq, color=BLUE, lw=1.6, label="Tần suất mặt ngửa")
    ax.axhline(0.5, color=ORANGE, ls="--", lw=1.6, label="Xác suất lý thuyết 0,5")
    ax.set_xscale("log")
    ax.set_xlabel("Số lần tung (thang log)")
    ax.set_ylabel("Tần suất")
    ax.set_ylim(0, 1)
    ax.legend(frameon=False, loc="lower right")
    save(fig, L3 / "lln-coin.png")


def fig_bayes():
    # 100 khách: 20 mua (16 có giỏ), 80 không mua (14 có giỏ)
    cats = ["buy_cart"] * 16 + ["buy_nocart"] * 4 + ["nobuy_cart"] * 14 + ["nobuy_nocart"] * 66
    colors = {"buy_cart": ORANGE, "buy_nocart": "#F6CF9B", "nobuy_cart": BLUE, "nobuy_nocart": "#D6E6EC"}
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    for i, c in enumerate(cats):
        r, col = divmod(i, 20)
        ax.add_patch(Rectangle((col, 4 - r), 0.86, 0.86, color=colors[c]))
    ax.set_xlim(-0.2, 20.2)
    ax.set_ylim(-0.2, 5.2)
    ax.axis("off")
    handles = [
        Rectangle((0, 0), 1, 1, color=ORANGE), Rectangle((0, 0), 1, 1, color="#F6CF9B"),
        Rectangle((0, 0), 1, 1, color=BLUE), Rectangle((0, 0), 1, 1, color="#D6E6EC"),
    ]
    labels = ["Mua, có thêm giỏ: 16", "Mua, không thêm giỏ: 4", "Không mua, có thêm giỏ: 14", "Không mua, không thêm giỏ: 66"]
    ax.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=2, frameon=False, fontsize=10.5)
    ax.set_title("100 khách hàng: có giỏ = 16 + 14 = 30, trong đó mua = 16 → 16/30 = 53,33%", fontsize=11.5)
    save(fig, L3 / "bayes-100-khach.png")


def fig_ab():
    from scipy.stats import norm
    z = 0.6935419821470654
    x = np.linspace(-4, 4, 600)
    y = norm.pdf(x)
    fig, ax = plt.subplots(figsize=(7.2, 3.7))
    ax.plot(x, y, color=BLUE, lw=2)
    ax.fill_between(x, y, where=(x <= -1.96), color=RED, alpha=0.35, label="Vùng bác bỏ H₀ (α = 0,05)")
    ax.fill_between(x, y, where=(x >= 1.96), color=RED, alpha=0.35)
    ax.fill_between(x, y, where=(np.abs(x) >= z), color=ORANGE, alpha=0.25, label="Hai đuôi ứng với |z| = 0,694: p = 0,488")
    ax.axvline(z, color=ORANGE, lw=2)
    ax.annotate("z quan sát = 0,694", xy=(z, norm.pdf(z)), xytext=(1.2, 0.33), arrowprops=dict(arrowstyle="->", color="#333"), fontsize=11)
    ax.set_xlabel("Thống kê kiểm định z")
    ax.set_ylabel("Mật độ")
    ax.legend(frameon=False, loc="upper left", fontsize=9.5)
    save(fig, L3 / "ab-test-z.png")


def fig_pca():
    from sklearn.datasets import load_iris
    from sklearn.decomposition import PCA
    data = load_iris()
    pca = PCA(n_components=2)
    Z = pca.fit_transform(data.data)
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    for k, (name, col) in enumerate(zip(data.target_names, [BLUE, ORANGE, GREEN])):
        ax.scatter(Z[data.target == k, 0], Z[data.target == k, 1], s=26, color=col, label=name, alpha=0.85)
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%} phương sai)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    ax.legend(frameon=False, title="Loài (iris)")
    save(fig, L3 / "pca-iris.png")


def fig_cosine():
    from sklearn.metrics.pairwise import cosine_similarity
    P = np.array([[1, 2, 3], [2, 4, 6], [1, -1, 0], [1, 2, 2]])
    S = cosine_similarity(P)
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    im = ax.imshow(S, cmap="RdBu", vmin=-1, vmax=1)
    names = ["SP0\n[1,2,3]", "SP1\n[2,4,6]", "SP2\n[1,−1,0]", "SP3\n[1,2,2]"]
    ax.set_xticks(range(4), names, fontsize=9)
    ax.set_yticks(range(4), names, fontsize=9)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, f"{S[i, j]:.3f}", ha="center", va="center", color="white" if abs(S[i, j]) > 0.6 else "#222", fontsize=10)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.colorbar(im, fraction=0.046, pad=0.04)
    save(fig, L3 / "cosine-heatmap.png")


def fig_gd1d():
    w = 5.0
    ws = [w]
    for _ in range(30):
        w -= 0.1 * 2 * (w - 3)
        ws.append(w)
    xs = np.linspace(2.2, 5.4, 300)
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.plot(xs, (xs - 3) ** 2, color=BLUE, lw=2, label="L(w) = (w − 3)²")
    ws = np.array(ws)
    ax.plot(ws, (ws - 3) ** 2, "o-", color=ORANGE, ms=4, lw=1, label="Các bước cập nhật (η = 0,1)")
    ax.scatter([5], [4], color=RED, zorder=5)
    ax.annotate("w = 5, L = 4,\nđạo hàm = +4", xy=(5, 4), xytext=(4.1, 5.0), arrowprops=dict(arrowstyle="->"), fontsize=10.5)
    ax.set_xlabel("w")
    ax.set_ylabel("Hàm lỗi L")
    ax.legend(frameon=False, loc="upper left")
    save(fig, L3 / "gd-1d.png")


def fig_integral():
    t = np.linspace(0, 3, 200)
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.plot(t, 2 * t + 1, color=BLUE, lw=2)
    ax.fill_between(t, 2 * t + 1, color=BLUE, alpha=0.25)
    ax.text(1.5, 2.0, "Diện tích = Q = 12", ha="center", fontsize=13, color="#1F5F73", weight="bold")
    ax.set_xlabel("t (giờ)")
    ax.set_ylabel("v(t) = 2t + 1 (đơn vị/giờ)")
    ax.set_xlim(0, 3.2)
    ax.set_ylim(0, 8)
    save(fig, L3 / "integral-sales.png")


def fig_lp():
    xs = np.linspace(0, 60, 300)
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    ax.plot(xs, 100 - 2 * xs, color=BLUE, lw=2, label="2x + y ≤ 100")
    ax.plot(xs, (80 - xs) / 2, color=GREEN, lw=2, label="x + 2y ≤ 80")
    poly = Polygon([[0, 0], [50, 0], [40, 20], [0, 40]], closed=True, color="#F6CF9B", alpha=0.7, label="Miền khả thi")
    ax.add_patch(poly)
    for z, st in [(3000, ":"), (5200, "-")]:
        ax.plot(xs, (z - 100 * xs) / 60, color=ORANGE, ls=st, lw=1.6, label=f"100x + 60y = {z}")
    ax.scatter([40], [20], color=RED, zorder=5, s=50)
    ax.annotate("Tối ưu: (40, 20)\nZ = 5.200", xy=(40, 20), xytext=(44, 33), arrowprops=dict(arrowstyle="->"), fontsize=11)
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 60)
    ax.set_xlabel("x: số sản phẩm A")
    ax.set_ylabel("y: số sản phẩm B")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    save(fig, L3 / "lp-feasible.png")


def fig_gd2d():
    def loss(t):
        return (t[0] - 3) ** 2 + 4 * (t[1] + 1) ** 2

    def grad(t):
        return np.array([2 * (t[0] - 3), 8 * (t[1] + 1)])

    t = np.array([-2.0, 2.0])
    path = [t.copy()]
    for _ in range(25):
        t = t - 0.1 * grad(t)
        path.append(t.copy())
    path = np.array(path)
    g1, g2 = np.meshgrid(np.linspace(-3, 5, 200), np.linspace(-2.5, 3, 200))
    Z = (g1 - 3) ** 2 + 4 * (g2 + 1) ** 2
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    cs = ax.contour(g1, g2, Z, levels=14, cmap="Blues")
    ax.plot(path[:, 0], path[:, 1], "o-", color=ORANGE, ms=4, lw=1.4, label="Đường đi của Gradient Descent")
    ax.scatter([3], [-1], marker="*", s=180, color=RED, zorder=5, label="θ* = (3, −1)")
    ax.set_xlabel("θ₁")
    ax.set_ylabel("θ₂")
    ax.legend(frameon=False, loc="upper right", fontsize=10)
    save(fig, L3 / "gd-2d.png")


# ------------------------------------------------------------------ bài 4
def fig_pagerank():
    G = nx.DiGraph()
    G.add_edges_from([("A", "B"), ("A", "C"), ("B", "C"), ("C", "A"), ("D", "C"), ("D", "A"), ("E", "C")])
    pr = nx.pagerank(G, alpha=0.85)
    pos = {"A": (0, 0.6), "B": (1.2, 1.2), "C": (1.5, 0), "D": (-1.0, -0.8), "E": (2.6, -0.8)}
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=[pr[n] * 6500 + 300 for n in G], node_color=BLUE, alpha=0.9)
    nx.draw_networkx_edges(G, pos, ax=ax, arrows=True, arrowsize=18, edge_color="#555", width=1.5,
                           node_size=[pr[n] * 6500 + 300 for n in G], connectionstyle="arc3,rad=0.12")
    nx.draw_networkx_labels(G, pos, ax=ax, font_color="white", font_weight="bold")
    for n, (x, y) in pos.items():
        ax.text(x, y - 0.38, f"{pr[n]:.4f}", ha="center", fontsize=10, color="#333")
    ax.set_xlim(-1.5, 3.1)
    ax.set_ylim(-1.5, 1.7)
    ax.axis("off")
    save(fig, L4 / "pagerank-graph.png")


def fig_shortest():
    G = nx.Graph()
    G.add_weighted_edges_from([("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5), ("C", "D", 8), ("C", "E", 10), ("D", "E", 2)])
    pos = {"A": (0, 0.5), "C": (1.2, 1.3), "B": (1.2, -0.3), "D": (2.6, 0.9), "E": (3.8, 0.3)}
    path = nx.shortest_path(G, "A", "E", weight="weight")
    pe = list(zip(path, path[1:]))
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#B8B8B8", width=2)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=pe, edge_color=ORANGE, width=4)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=900, node_color=BLUE)
    nx.draw_networkx_labels(G, pos, ax=ax, font_color="white", font_weight="bold", font_size=13)
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=nx.get_edge_attributes(G, "weight"), font_size=11,
                                 bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    ax.set_title("Đường đi ngắn nhất A → C → B → D → E, tổng chi phí 2 + 1 + 5 + 2 = 10", fontsize=11)
    ax.axis("off")
    save(fig, L4 / "shortest-path.png")


def fig_entropy():
    p = np.linspace(0.0005, 0.9995, 500)
    H = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.6), gridspec_kw={"width_ratios": [1.3, 1]})
    a1.plot(p, H, color=BLUE, lw=2)
    for pv, hv, lab in [(0.5, 1.0, "50/50: 1 bit"), (0.9, 0.469, "90/10: 0,469 bit"), (1.0, 0.0, "100/0: 0 bit")]:
        a1.scatter([pv], [hv], color=ORANGE, zorder=5, s=50)
        a1.annotate(lab, (pv, hv), textcoords="offset points", xytext=(-8 if pv > 0.8 else 8, 10 if pv < 1 else 14), ha="right" if pv > 0.8 else "left", fontsize=10)
    a1.set_xlabel("Xác suất bóng đỏ p")
    a1.set_ylabel("Entropy H (bit)")
    a1.set_ylim(0, 1.15)
    labs = ["50 đỏ\n50 xanh", "90 đỏ\n10 xanh", "100 đỏ\n0 xanh"]
    a2.bar(labs, [1.0, 0.469, 0.0], color=[ORANGE, BLUE, GREEN])
    a2.set_ylabel("H (bit)")
    for i, v in enumerate([1.0, 0.469, 0.0]):
        a2.text(i, v + 0.02, f"{v:.3f}".rstrip("0").rstrip(".") if v else "0", ha="center", fontsize=11)
    a2.set_ylim(0, 1.15)
    save(fig, L4 / "entropy-curve.png")


def fig_tree():
    from sklearn.datasets import load_breast_cancer
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier, plot_tree
    data = load_breast_cancer()
    Xtr, Xte, ytr, yte = train_test_split(data.data, data.target, test_size=0.2, random_state=42)
    m = DecisionTreeClassifier(criterion="entropy", max_depth=4, random_state=42).fit(Xtr, ytr)
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    plot_tree(m, max_depth=2, feature_names=data.feature_names, class_names=list(data.target_names), filled=True, rounded=True, fontsize=8, ax=ax, impurity=True)
    save(fig, L4 / "decision-tree.png")


def fig_findiff():
    h = np.logspace(-16, 0, 400)
    x = 1.0
    f, d = np.exp, np.exp(1.0)
    fwd = np.abs((f(x + h) - f(x)) / h - d)
    ctr = np.abs((f(x + h) - f(x - h)) / (2 * h) - d)
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    ax.loglog(h, fwd, color=BLUE, lw=2, label="Sai phân tiến: [f(x+h) − f(x)] / h")
    ax.loglog(h, ctr, color=ORANGE, lw=2, label="Sai phân trung tâm: [f(x+h) − f(x−h)] / 2h")
    ax.set_xlabel("Bước h")
    ax.set_ylabel("Sai số tuyệt đối")
    ax.set_title("f(x) = eˣ tại x = 1: sai số giảm rồi tăng lại khi h quá nhỏ", fontsize=11)
    ax.legend(frameon=False, fontsize=9.5)
    save(fig, L4 / "finite-diff-error.png")


def fig_newton():
    x, errs = 1.0, []
    for _ in range(10):
        x = 0.5 * (x + 10 / x)
        errs.append(abs(x - np.sqrt(10)))
    errs = np.array(errs)
    errs[errs == 0] = 1e-17
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.semilogy(range(1, 11), errs, "o-", color=BLUE, lw=2)
    ax.set_xlabel("Số vòng lặp n")
    ax.set_ylabel("|xₙ − √10|")
    ax.set_title("Hội tụ rất nhanh; sau vòng 6 chạm giới hạn độ chính xác máy", fontsize=11)
    save(fig, L4 / "newton-sqrt.png")


def fig_euclid():
    C = np.array([[2, 3], [5, 7], [2, 4], [9, 10]])
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    ax.scatter(C[:, 0], C[:, 1], s=90, color=BLUE, zorder=3)
    for i, (x, y) in enumerate(C):
        ax.annotate(f"KH{i}", (x, y), textcoords="offset points", xytext=(8, -4), fontsize=11)
    ax.plot([2, 5], [3, 7], color=ORANGE, lw=2.2)
    ax.plot([2, 5], [3, 3], color=GREY, ls="--")
    ax.plot([5, 5], [3, 7], color=GREY, ls="--")
    ax.text(3.5, 2.5, "Δ₁ = 3", ha="center", fontsize=10)
    ax.text(5.15, 5, "Δ₂ = 4", fontsize=10)
    ax.text(3.2, 5.6, "d = 5", color=ORANGE, fontsize=12, weight="bold")
    ax.annotate("Gần KH0 nhất\n(d = 1)", (2, 4), xytext=(0.2, 6), arrowprops=dict(arrowstyle="->"), fontsize=10)
    ax.set_xlabel("Thu nhập (đã chuẩn hóa thủ công cho ví dụ)")
    ax.set_ylabel("Số lần mua hàng")
    ax.set_xlim(0, 10.5)
    ax.set_ylim(1.8, 11)
    save(fig, L4 / "euclid-customers.png")


def fig_swiss():
    from sklearn.datasets import make_swiss_roll
    from sklearn.manifold import Isomap
    X, t = make_swiss_roll(1500, random_state=0)
    Z = Isomap(n_neighbors=12, n_components=2).fit_transform(X)
    fig = plt.figure(figsize=(9.6, 3.9))
    a1 = fig.add_subplot(121, projection="3d")
    a1.scatter(X[:, 0], X[:, 1], X[:, 2], c=t, cmap="viridis", s=5)
    a1.view_init(10, -70)
    a1.set_title("Dữ liệu 3 chiều (cuộn lại)", fontsize=11)
    a2 = fig.add_subplot(122)
    a2.scatter(Z[:, 0], Z[:, 1], c=t, cmap="viridis", s=5)
    a2.set_title("Isomap: trải phẳng về 2 chiều", fontsize=11)
    a2.set_xticks([])
    a2.set_yticks([])
    save(fig, L4 / "swiss-roll.png")


def fig_persistence():
    import gudhi as gd
    np.random.seed(42)
    n = 100
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
    X = np.column_stack([np.cos(theta), np.sin(theta)])
    X += np.random.normal(0, 0.03, X.shape)
    st = gd.RipsComplex(points=X, max_edge_length=1.0).create_simplex_tree(max_dimension=2)
    pers = st.persistence()
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.8))
    axes[0].scatter(X[:, 0], X[:, 1], s=14, color=BLUE)
    axes[0].set_aspect("equal")
    axes[0].set_title("100 điểm gần vòng tròn", fontsize=11)
    gd.plot_persistence_diagram(pers, axes=axes[1], legend=True)
    axes[1].set_title("Persistence diagram", fontsize=11)
    gd.plot_persistence_barcode(pers, axes=axes[2], max_intervals=30, legend=True)
    axes[2].set_title("Persistence barcode (30 khoảng dài nhất)", fontsize=11)
    save(fig, L4 / "persistence.png")


if __name__ == "__main__":
    for fn in [fig_lln, fig_bayes, fig_ab, fig_pca, fig_cosine, fig_gd1d, fig_integral, fig_lp, fig_gd2d,
               fig_pagerank, fig_shortest, fig_entropy, fig_tree, fig_findiff, fig_newton, fig_euclid, fig_swiss, fig_persistence]:
        try:
            fn()
        except Exception as e:  # noqa: BLE001
            print("LỖI", fn.__name__, repr(e))
