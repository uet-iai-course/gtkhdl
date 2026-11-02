def f(x):
    return x ** 2

x = 3.0
h = 0.001

numerical_derivative = (f(x + h) - f(x)) / h
exact_derivative = 2 * x

print("Đạo hàm xấp xỉ:", numerical_derivative)
print("Đạo hàm chính xác:", exact_derivative)
