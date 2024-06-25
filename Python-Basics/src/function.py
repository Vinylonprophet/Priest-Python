def greet_user(name, adjective):
    print(f"Hello! {name} is {adjective}!")


greet_user("VL", "greeting")


def greet_user1(name, adjective="amazing"):
    print(f"Hello! {name} is {adjective}!")


greet_user1("VL")


def greet_user2(name, adjective="amazing"):
    return name


print(greet_user2("VL"))


def get_formatted_name(first_name, last_name):
    full_name = f"{first_name} {last_name}"
    return full_name.title()


while True:
    print("\nPlease tell me your name:")
    print("(enter 'q' at any time to quit.)")

    f_name = input("First Name: ")
    if f_name == "q":
        break

    l_name = input("Last Name: ")
    if l_name == "q":
        break

    print(f"\nHello, {get_formatted_name(f_name, l_name)}")


def make_pizza(*toppings):
    print(toppings)


make_pizza("pepperoni")
make_pizza("pepperoni", "mushrooms", "green peppers")


def build_profile(first, last, **user_info):
    user_info["first_name"] = first
    user_info["last_name"] = last
    return user_info


user_profile = build_profile("VL", "Wu", age="18", career="student")
print(user_profile)
