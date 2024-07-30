import datetime
import socket
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from properties.items import PropertiesItem


class EasySpider(CrawlSpider):
    name = "easy"
    allowed_domains = ["baike.baidu.com"]
    start_urls = [
        "https://baike.baidu.com/item/%E8%93%9D%E8%89%B2%E7%9B%91%E7%8B%B1/58149098"
    ]

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths='//*[contains(@class,"innerLink_c04Ns")]'),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
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
