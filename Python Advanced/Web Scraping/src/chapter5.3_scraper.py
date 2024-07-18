import csv

csvFile = open("dist/5.3_test.csv", "w+")
try:
    writer = csv.writer(csvFile)
    writer.writerow(("column1", "column2", "column3"))
    for i in range(10):
        writer.writerow((i, i + 2, i * i))
finally:
    csvFile.close()
