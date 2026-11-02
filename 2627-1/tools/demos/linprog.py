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
