def newton_sqrt(number, initial=1.0, iterations=10):
    x = initial

    for i in range(iterations):
        x = 0.5 * (x + number / x)
        print(i + 1, x)

    return x

result = newton_sqrt(10)
print("Kết quả:", result)
