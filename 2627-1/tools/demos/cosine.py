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
