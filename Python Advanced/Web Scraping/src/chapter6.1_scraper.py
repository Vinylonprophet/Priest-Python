from urllib.request import urlopen
from bs4 import BeautifulSoup

# textPage = urlopen("https://www.pythonscraping.com/pages/warandpeace/chapter1.txt")
# print(textPage.read())

# textPage = urlopen("https://www.pythonscraping.com/pages/warandpeace/chapter1-ru.txt")
# print(str(textPage.read(), "utf-8"))

html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bs = BeautifulSoup(html, "html.parser")
content = bs.find('div', {"id": "mw-content-text"}).get_text()
content = bytes(content, 'UTF-8')
content = content.decode('UTF-8')