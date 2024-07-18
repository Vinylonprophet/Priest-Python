import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup


html = urlopen("http://en.wikipedia.org/wiki/Comparison_of_text_editors")
bs = BeautifulSoup(html, "html.parser")

table = bs.find_all("table", {"class": "wikitable"})[0]
rows = table.find_all("tr")

csvFile = open("dist/5.4_test.csv", "wt+", encoding="utf-8")
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
        for cell in row.find_all(["td", "th"]):
            csvRow.append(cell.get_text())
        writer.writerow(csvRow)
finally:
    csvFile
