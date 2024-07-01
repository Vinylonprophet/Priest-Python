citi = {"department": {"icg", "gcg", "pbwm"}, "staff": {"vl", "bella", "max", "nick"}}
print(citi["department"])

print(citi)
del citi["department"]
print(citi)

my_dict = {"b": 3, "a": 1, "c": 2}
sorted_keys = sorted(my_dict.keys())
print(my_dict.keys())
for key in sorted_keys:
    print(f"{key}: {my_dict[key]}")
print(my_dict)

sorted_items = sorted(my_dict.items(), key=lambda x: x[1])
for key, value in sorted_items:
    print(f"{key}: {value}")
print(my_dict)

poinit_value = citi.get("vl", "VL has been left")
poinit_value1 = citi.get("staff", "u can get right?")
print(poinit_value)
print(poinit_value1)

citi1 = {"department": {"icg", "gcg", "pbwm"}, "staff": {"vl", "bella", "max", "nick"}}
for key, value in citi1.items():
    print(f"{key}: {value}\n")

citi2 = {
    "department": {"icg", "gcg", "pbwm"},
    "staff": {"vl", "bella", "max", "nick"},
    "staff": {"xiuhui", "colin"},
}
citi3 = {"a": "a", "b": "b", "b": "b"}
for key in set(citi2.keys()):
    print(key)
for value in set(citi3.values()):
    print(value)

pizza = {"crust": "thick", "toppings": ["mushrooms", "extra cheese"]}
print(f"Your ordered a {pizza['crust']}-crust pizza with the following toppings:")
for topping in pizza["toppings"]:
    print(f"\t{topping}")
