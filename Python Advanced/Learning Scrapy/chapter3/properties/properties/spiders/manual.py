import datetime
import socket
from scrapy.loader import ItemLoader
from scrapy.http import Request
import scrapy
from urllib.parse import urljoin
from properties.items import PropertiesItem


class ManualSpider(scrapy.Spider):
    name = "manual"
    allowed_domains = ["baike.baidu.com"]
    start_urls = [
        "https://baike.baidu.com/item/%E8%93%9D%E8%89%B2%E7%9B%91%E7%8B%B1/58149098"
    ]

    def parse(self, response):
        next_selector = response.xpath('//a[contains(@class,"innerLink_c04Ns")]//@href')
        for url in next_selector.extract():
            yield Request(urljoin(response.url, url), callback=self.parse_item)

    def parse_item(self, response):
        """This function parses a property page.

        @url https://baike.baidu.com/item/%E8%93%9D%E8%89%B2%E7%9B%91%E7%8B%B1/58149098
        @returns items 1
        @scrapes title
        @scrapes url project spider server date
        """

        # Create the loader using the response
        l = ItemLoader(item=PropertiesItem(), response=response)

        # Load fields using XPath expressions
        l.add_xpath("title", "//h1//text()")

        # Housekeeping fields
        l.add_value("url", response.url)
        l.add_value("project", self.settings.get("BOT_NAME"))
        l.add_value("spider", self.name)
        l.add_value("server", socket.gethostname())
        l.add_value("date", datetime.datetime.now().isoformat())

        return l.load_item()
