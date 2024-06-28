from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

count = 0


class ArticlesSpider(CrawlSpider):
    name = "articles"

    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Benevolent_dictator_for_life"]
    rules = [Rule(LinkExtractor(allow=r".*"), callback="parse_items", follow=True)]

    def parse_items(self, response):
        global count
        count += 1
        url = response.url
        title = response.css("h1 ::text").extract_first()
        text = response.xpath("//div[@id='mw-content-text']//text()").extract()
        lastUpdated = response.css("li#footer-info-lastmod ::text").extract_first()
        lastUpdated = lastUpdated.replace("This page was last edited on ", "")
        print("URL {}".format(url))
        print("Title {}".format(title))
        # print("Text {}".format(text))
        print("Last Updated: {}".format(lastUpdated))
        print("====================={}=====================".format(count))
