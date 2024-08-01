import csv

with open("todo.csv", "rU") as f:
    reader = csv.DictReader(f)
    for line in reader:
        print(line)
