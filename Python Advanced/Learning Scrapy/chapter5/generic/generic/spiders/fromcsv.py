import scrapy


class FromcsvSpider(scrapy.Spider):
    name = "fromcsv"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        pass
