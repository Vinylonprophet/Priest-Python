personList = ["vl", "coconut", "cardinal"]
for person in personList:
    print(person)
print("loop end")

for value in range(1, 5):
    print(value)

rangeList = list(range(1, 6))
for value in rangeList:
    print(value)

rangeListStep1 = list(range(0, 11, 2))
for value in rangeListStep1:
    print(value)

rangeListStep2 = list(range(0, 101, 2))
print(min(rangeListStep2))
print(max(rangeListStep2))
print(sum(rangeListStep2))

rangeListStep3 = [value**3 for value in range(1, 12, 2)]
print(rangeListStep3)

sliceList = ["vl", "max", "bella", "nick"]
print(f"{sliceList[:1]} are 00")
print(f"{sliceList[1:]} are 95")
print(f"{sliceList[-3:]} are 95")
print(f"{sliceList[1:3]} are girls")
for girl in sliceList[1:3]:
    print(f"{girl} is girl")

sliceList1 = sliceList[:]
sliceList2 = sliceList
sliceList1.append("xiuhui")
sliceList1.append("colin")
print(f"Digital's framework team: {sliceList1}")
print(f"Digital's framework team: {sliceList2}")

dimensions = (200, 50)
print(dimensions[0])
print(dimensions[1])
# dimensions[1] = 250

for dimension in dimensions:
    print(dimension)
