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
