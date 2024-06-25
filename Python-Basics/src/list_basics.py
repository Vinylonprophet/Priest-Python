lists = ["list0", "list1", "list2", "list3"]
print(lists)
print(lists[0])
print(lists[-1])

lists.append("list5")
lists.insert(4, "list4")
print(lists)

del lists[-1]
lists.pop()
lists.pop(0)
lists.remove("list2")
print(lists)

alphabet = ["b", "d", "e", "g", "h", "a", "u", "z", "o", "l", "p"]
print(sorted(alphabet))
print(alphabet)
alphabet.sort()
alphabet.sort(reverse=True)
alphabet.reverse()
print(alphabet)