# Bayesian inference: dự đoán khả năng mua hàng

p_buy = 0.20
p_cart_given_buy = 0.80
p_cart = 0.30

p_buy_given_cart = (
    p_cart_given_buy * p_buy / p_cart
)

print(f"P(Mua | Thêm giỏ) = {p_buy_given_cart:.2%}")
