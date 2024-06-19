for role in ["vl", "bella", "max", "nick", "colin", "xiuhui"]:
    if role == "xiuhui":
        print(f"{role} is leader")
    elif role != "xiuhui":
        print(f"{role} is aide")

age_vl = 24
if age_vl >= 18 and age_vl < 25:
    print("VL is in the prime of their youth.")

roles = ["VL", "Maggie", "Auggie", "Wency"]
print(f"Has VL resigned? ==>", "VL" in roles)
print(f"Maggie has not resigned. ==>", "Maggie" not in roles)

if "VL" in roles:
    print("VL has resigned.")
if "Auggie" in roles:
    print("Auggie has resigned.")

personlist = []
if personlist:
    for person in personlist:
        print(f"The {person} exists.")
else:
    print("The person does not exist.")
