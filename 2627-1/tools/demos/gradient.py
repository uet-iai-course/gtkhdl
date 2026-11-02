w = 5.0
learning_rate = 0.1

for i in range(30):
    loss = (w - 3) ** 2
    gradient = 2 * (w - 3)

    w = w - learning_rate * gradient

    print(i, round(w, 5), round(loss, 5))

print("Nghiệm gần tối ưu:", w)
