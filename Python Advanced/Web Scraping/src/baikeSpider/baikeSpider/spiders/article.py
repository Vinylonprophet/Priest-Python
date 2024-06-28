import scrapy
from scrapy.http import Response


class ArticleSpider(scrapy.Spider):
    name = "article"

    def start_requests(self):
        # urls = ["https://baike.baidu.com/item/DC%E6%BC%AB%E7%94%BB/725892?fr=ge_ala"]
        urls = ["https://en.wikipedia.org/wiki/Kevin_Bacon"]
        return [scrapy.Request(url=url, callback=self.parse) for url in urls]

    def parse(self, response: Response):
        url = response.url
        title = response.css("h1 ::text").extract_first()
        print("URL {}".format(url))
        print("Title {}".format(title))
