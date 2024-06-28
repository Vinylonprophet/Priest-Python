import requests
from bs4 import BeautifulSoup


class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print("URL: {}".format(self.url))
        print("Title: {}".format(self.title))
        print("Body: {}".format(self.body))


class Website:
    def __init__(self, name, url, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.titleTag = titleTag
        self.bodyTag = bodyTag


class Crawler:
    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, "html.parser")

    def safeGet(self, pageObj, selector):
        # print(pageObj.select_one("div .para_uWBUP"))
        # print(pageObj.select_one("h1"))
        selectedElems = pageObj.select_one(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return "".join([elem.get_text() for elem in selectedElems])
        return ""

    def parse(self, site, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title != "" and body != "":
                content = Content(url, title, body)
                content.print()


crawler = Crawler()

siteData = [
    [
        "DC漫画",
        "https://baike.baidu.com/item/DC%E6%BC%AB%E7%94%BB/725892?fr=ge_ala",
        "h1",
        ".para_uWBUP",
    ],
    [
        "沙赞",
        "https://baike.baidu.com/item/%E6%AF%94%E5%88%A9%C2%B7%E5%B7%B4%E7%89%B9%E6%A3%AE/20102445?fromtitle=%E6%B2%99%E8%B5%9E&fromid=13009441",
        "h1",
        ".para_uWBUP",
    ],
]

websites = []

for row in siteData:
    websites.append(Website(row[0], row[1], row[2], row[3]))

crawler.parse(
    websites[0], "https://baike.baidu.com/item/DC%E6%BC%AB%E7%94%BB/725892?fr=ge_ala"
)
print("\n")
crawler.parse(
    websites[1],
    "https://baike.baidu.com/item/%E6%AF%94%E5%88%A9%C2%B7%E5%B7%B4%E7%89%B9%E6%A3%AE/20102445?fromtitle=%E6%B2%99%E8%B5%9E&fromid=13009441",
)
