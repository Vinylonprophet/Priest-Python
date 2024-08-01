from scrapy import FormRequest
from scrapy.spiders import Spider


class LoginSpider(Spider):
    name = "login"
    allowed_domains = ["search.damai.cn", "log.mmstat.com"]

    def start_requests(self):
        return [
            FormRequest(
                "http://web:9312/dynamic/login",
                formdata={"username": "user", "password": "pass"},
            )
        ]

    def parse(self, response):
        print(response.headers.getlist("Set-Cookie"))
