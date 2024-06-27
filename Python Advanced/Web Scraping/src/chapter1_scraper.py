import re
from urllib.request import urlopen
from urllib.request import HTTPError
from bs4 import BeautifulSoup


# def getTVList(url):
#     try:
#         html = urlopen(url)
#     except HTTPError as e:
#         return None
#     try:
#         bs = BeautifulSoup(html.read(), "html.parser")
#         tvList = bs.find_all("li", {"class": "item"})
#     except AttributeError as e:
#         return None
#     return tvList


# tvList = getTVList("https://bangumi.tv/anime/browser/airtime/2024-5")
# if tvList == None:
#     print("Title could not be found!")
# else:
#     for tv in tvList:
#         print(tv.get_text())


# html = urlopen("https://pythonscraping.com/pages/page3.html")
# bs = BeautifulSoup(html.read(), "html.parser")

# for sibling in bs.find("table", {"id": "giftList"}).tr.next_siblings:
# print(sibling)


# html = urlopen("https://pythonscraping.com/pages/page3.html")
# bs = BeautifulSoup(html.read(), "html.parser")

# print(
#     bs.find("img", {"src": "../img/gifts/img1.jpg"}).parent.previous_sibling.get_text()
# )


html = urlopen("https://pythonscraping.com/pages/page3.html")
bs = BeautifulSoup(html.read(), "html.parser")
images = bs.find_all("img", {"src": re.compile("\.\.\/img\/gifts\/img.*\.jpg")})
for img in images:
    print(img.attrs)
    print(img["src"])
