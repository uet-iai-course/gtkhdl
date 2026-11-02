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
