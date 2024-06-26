from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import random
import time

random.seed(time.time())


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
    print(1)
    if html:
        print(2)
        bs = BeautifulSoup(html, "html.parser")
        return bs.find("div", {"id": "bodyContent"}).find_all(
            "a", href=re.compile("^(/wiki/)((?!:).)*$")
        )
    else:
        print("Failed to retrieve the web page.")


def link_loop(articleUrl="/wiki/Kevin_Bacon"):
    links = get_links(get_html("http://en.wikipedia.org{}", articleUrl))
    while links:
        newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
        print(newArticle)
        link_loop(newArticle)
        break


link_loop()
