from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from bs4 import BeautifulSoup
import re
import random
import time

from urllib.request import Request

random.seed(time.time())

links = set()


def get_html(url, article, retries=3):
    print(f"URL: {url.format(article)}")
    for i in range(retries):
        try:
            return urlopen(url.format(article))
        except HTTPError as e:
            print(f"HTTP error: {e.code}")
            if e.code == 502:
                print(
                    f"Attempt {i + 1} failed with error 502: Bad Gateway. Retrying..."
                )
                time.sleep(2)
            else:
                return None
        except URLError as e:
            print(f"URL error: {e.reason}")
            return None
    return None


def get_links(html):
    global links
    if html:
        bs = BeautifulSoup(html, "html.parser")

        try:
            print(bs.find("h1", {"class": "J-lemma-title"}).get_text())
        except AttributeError:
            print("页面少一些属性哈~")

        for link in bs.find("div", {"class": "mainContent_dvM3V"}).find_all(
            "a", href=re.compile("^(/item/)((?!:).)*$")
        ):
            links.add(link)

        print(len(links))
    else:
        print("Failed to retrieve the web page.")


get_links(
    get_html(
        "https://baike.baidu.com{}", quote("/item/DC漫画/725892?fr=ge_ala", safe="/?=&")
    )
)
