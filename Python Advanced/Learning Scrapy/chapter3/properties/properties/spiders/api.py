import json
import scrapy
from properties.items import CardItem


class ApiSpider(scrapy.Spider):
    name = "api"
    allowed_domains = ["decksofkeyforge.com"]

    def start_requests(self):
        url = "https://decksofkeyforge.com/api/decks/filter-count"
        params = {
            "houses": [],
            "excludeHouses": [],
            "page": 0,
            "constraints": [],
            "expansions": [],
            "pageSize": 20,
            "title": "",
            "notes": "",
            "tags": [],
            "notTags": [],
            "notesUser": "",
            "sort": "SAS_RATING",
            "titleQl": False,
            "notForSale": False,
            "forTrade": False,
            "withOwners": False,
            "teamDecks": False,
            "myFavorites": False,
            "cards": [],
            "tokens": [],
            "sortDirection": "DESC",
            "owner": "",
            "owners": [],
            "tournamentIds": [],
            "previousOwner": "",
        }
        yield scrapy.Request(
            url=url,
            method="POST",
            body=json.dumps(params),
            headers={"Content-Type": "application/json"},
            callback=self.parse_total_cards,
        )

    def parse_total_cards(self, response):
        data = json.loads(response.body)
        total_cards = data.get("count", 0)
        page_size = 900
        total_pages = total_cards // page_size + (
            1 if total_cards % page_size > 0 else 0
        )
        print("===总页数===", total_pages)

        base_url = "https://decksofkeyforge.com/api/decks/filter"
        for page in range(total_pages):
            json_data = {
                "houses": [],
                "excludeHouses": [],
                "page": page,
                "constraints": [],
                "expansions": [],
                "pageSize": page_size,
                "title": "",
                "notes": "",
                "tags": [],
                "notTags": [],
                "notesUser": "",
                "sort": "SAS_RATING",
                "titleQl": False,
                "notForSale": False,
                "forTrade": False,
                "withOwners": False,
                "teamDecks": False,
                "myFavorites": False,
                "cards": [],
                "tokens": [],
                "sortDirection": "DESC",
                "owner": "",
                "owners": [],
                "tournamentIds": [],
                "previousOwner": "",
            }

            body = json.dumps(json_data)
            yield scrapy.Request(
                url=base_url,
                method="POST",
                body=body,
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
                    "Cache-Control": "no-cache",
                    "Content-Type": "application/json",
                    "Cookie": "_gid=GA1.2.1150512372.1721983105; _gat_gtag_UA_132818841_1=1; _ga_YH39DY77CE=GS1.1.1721983104.1.1.1721986236.0.0.0; _ga=GA1.1.1039020519.1721983105",
                    "Origin": "https://decksofkeyforge.com",
                    "Pragma": "no-cache",
                    "Priority": "u=1, i",
                    "Referer": "https://decksofkeyforge.com/decks",
                    "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "Timezone": "480",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                },
                callback=self.parse_cards,
                meta={"page": page},
            )

    def parse_cards(self, response):
        data = json.loads(response.body)
        decks = data.get("decks", [])
        page_num = response.meta["page"]

        if not decks:
            return

        for card in decks:
            card_item = CardItem()
            card_item["keyforge_id"] = card["keyforgeId"]
            yield card_item
