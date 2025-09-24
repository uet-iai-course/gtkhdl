a = {
    "name": "va",
    "age": 10
}

if "course" in a:
    print(a["course"])
else:
    print("no_course")

print(a.get("course", "no_course"))