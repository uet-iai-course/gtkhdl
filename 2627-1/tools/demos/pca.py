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
