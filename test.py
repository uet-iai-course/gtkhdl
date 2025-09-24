# For loop
for i in range(3):
    print(i)
else:
    print("success")

# is and ==
1 == 1
1 is 1
l1 = [1, 2, 3, 4, 5]
l2 = [1, 2, 3, 4, 5]
l1 is l2

# Mutable vs Immutable
a = "abcd"
print(id(a))
a = "hello"
print(id(a))

# String
print(len("élève"))
print(len("élève"))


# Test
def add_to_list(item:str="", target: list[str] = []):
    target.append(item)

l1 = add_to_list("Bob")
add_to_list("James", l1)

l2 = add_to_list("Sandra")

print(l2)