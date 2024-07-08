from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup

html = urlopen("https://pythonscraping.com/")
bs = BeautifulSoup(html, "html.parser")
imageLocation = bs.find("div", {"class": "pagelayer-image-holder"}).find("img")["src"]
urlretrieve(imageLocation, "book_cover.jpg")
