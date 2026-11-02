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
