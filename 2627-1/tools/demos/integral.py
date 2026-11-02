from scipy.integrate import quad

def sales_rate(t):
    return 2 * t + 1

total, error = quad(sales_rate, 0, 3)

print("Tổng lượng hàng bán:", total)
print("Sai số ước lượng:", error)
