# Web-Scraping

## 初见爬虫

### 网络连接

#### urlopen使用方式

urlopen读取远程对象

`urlopen("https://pythonscraping.com/pages/page1.html")`

```python
from urllib.request import urlopen

html = urlopen("https://pythonscraping.com/pages/page1.html")

print(html.read())
```



### BeautifulSoup

#### BeautifulSoup使用方式

通过HTML标签来格式化和组织复杂的网页信息，用python对象为我们展示XML结构信息

`bs = BeautifulSoup(html.read(), "html.parser")`

**参数：**

1. 该对象所基于HTML文本
2. 希望BS用来创建对象的解析器

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://pythonscraping.com/pages/page1.html")
bs = BeautifulSoup(html.read(), "html.parser")

print(bs)
print(bs.html.head.title)
print(bs.html.body.h1)
print(bs.html.body.div)
```



##### 其他解析器

1. lxml

    **优点：**

    1. **性能高：** `lxml`解析器使用C语言编写，解析速度非常快，是目前性能最好的解析器之一。
    2. **功能丰富：** 支持XPath和XSLT，提供了强大的XML和HTML处理功能，适合需要复杂查询和操作的场景。
    3. **兼容性好：** 支持HTML和XML的解析，兼容性强，能够处理大多数标准的HTML和XML文档。
    4. **错误容忍度高：** `lxml`能够很好地处理一些不太规范的HTML文档。

    **缺点：**

    1. **安装复杂：** 由于依赖于libxml2和libxslt库，安装可能较为复杂，尤其是在Windows系统上。
    2. **库体积大：** 由于功能强大，库的体积较大，可能会增加项目的依赖体积。

    

2. html5lib

    **优点：**

    1. **完全兼容HTML5：** `html5lib`完全实现了HTML5规范，能够解析所有符合HTML5标准的文档。
    2. **处理不规范HTML：** 对于一些不规范的HTML文档（如遗留网页），`html5lib`有很好的兼容性和容错能力。
    3. **纯Python实现：** 由于是纯Python实现的，不依赖于外部C库，安装简单，兼容性强。

    **缺点：**

    1. **性能较低：** 相对于`lxml`，`html5lib`的解析速度较慢，因为是用纯Python实现的。
    2. **功能相对较少：** 虽然完全实现了HTML5规范，但不支持XPath和XSLT，功能相对较少。



#### 异常处理

##### HTTP错误和URL错误处理

```python
from urllib.request import urlopen
from urllib.request import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup

try:
    html = urlopen("https://pythonscraping.com/pages/page1.html")
except HTTPError as e:
    print(e)
except URLError as e:
    print("The Server could be found!")
else:
    bs = BeautifulSoup(html.read(), "html.parser")
    print(bs)
    print(bs.html.head.title)
    print(bs.html.body.h1)
    print(bs.html.body.div)
```



##### 子标签错误处理

如果tag标签不存在会返回None，如果直接调用None中的子标签会报错

```python
from urllib.request import urlopen
from urllib.request import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup

try:
    html = urlopen("https://pythonscraping.com/pages/page1.html")
except HTTPError as e:
    print(e)
except URLError as e:
    print("The Server could be found!")
    pass
else:
    bs = BeautifulSoup(html.read(), "html.parser")
    print(bs)
    try:
        badContent = bs.find("errorTag").find("anotherTag")
    except AttributeError as e:
        print("Tag was not found")
    else:
        print(badContent)
    print(bs.html.head.title)
    print(bs.html.body.h1)
    print(bs.html.body.div)
```



#### 代码重构

```python
from urllib.request import urlopen
from urllib.request import HTTPError
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html.read(), "html.parser")
        title = bs.body.h1
    except AttributeError as e:
        return None
    return title


title = getTitle("https://pythonscraping.com/pages/page1.html")
if title == None:
    print("Title could not be found!")
else:
    print(title)
```



## 复杂HTML解析

如果一级级去找我们需要的标签，那么就会导致一个问题——如果目标网站的html结构改了，那么整个爬虫就被`碾死`了！

### 根据层叠样式表解析

**重要方法：**

1. find_all()：提取标签
2. get_text()：清理所有标签，返回一个只包含文字的Unicode字符串

```python
from urllib.request import urlopen
from urllib.request import HTTPError
from bs4 import BeautifulSoup


def getTVList(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html.read(), "html.parser")
        tvList = bs.find_all("li", {"class": "item"})
    except AttributeError as e:
        return None
    return tvList


tvList = getTVList("https://bangumi.tv/anime/browser/airtime/2024-5")
if tvList == None:
    print("Title could not be found!")
else:
    for tv in tvList:
        print(tv.get_text())
```



#### find()和find_all()

**文档定义：**

1. find_all(tag, attributes, recursive, text, limit, keywords)
2. find(tag, attributes, recursive, text, keywords)

**参数：**

1. tag

   - ['h1', 'h2', 'h3']
   - 'h1'

2. attributes

   - {'class': 'item'}
   - {"class": {"item", "clearit"}}

3. recursive（递归参数）

   - True: 默认是True，遍历所有标签
   - False: 只遍历一级标签

4. text

   - 用标签的文本内容去匹配，而不是用标签的属性

   - 如果想查询页面中包含`the prince`的标签数量可以这么写：

     ```python
     nameList = bs.find_all(text='the prince')
     print(len(nameList))
     ```

5. limit（只有find_all有这个参数，如果想获取网页中前x项结果就设置它，`find相当于find_all设置limit为1时的结果`）

6. keywords

   - 可以选择那些具有指定属性的标签

     ```python
     bs.find(type="text/css")
     ```



#### 其他BeautifulSoup对象

除了之前提到的对象还有另外两种不那么常用的对象：

1. NavigableString对象

   用来表示标签里的文字而不是标签本身

2. Comment对象

   用来查找HTML文档中的注释标签，< ! -- 这种 -- >



#### 导航树

意思是层层解析，不难，读者就看看代码吧。。。

##### 处理子标签和后代标签

```python
html = urlopen("https://pythonscraping.com/pages/page3.html")
bs = BeautifulSoup(html.read(), "html.parser")

for child in bs.find("table", {"id": "giftList"}).children:
    print(child)
```

##### 处理兄弟标签

next_siblings()只调用**后面**的兄弟标签（那么你也可以理解一下previous_siblings）

next_sibling和previous_sibling这一组和上面的区别就是`有没有s`

```python
html = urlopen("https://pythonscraping.com/pages/page3.html")
bs = BeautifulSoup(html.read(), "html.parser")

for sibling in bs.find("table", {"id": "giftList"}).tr.next_siblings:
    print(sibling)
```

##### 处理父标签

记住`parents`和`parent`

```python
html = urlopen("https://pythonscraping.com/pages/page3.html")
bs = BeautifulSoup(html.read(), "html.parser")

print(
    bs.find("img", {"src": "../img/gifts/img1.jpg"}).parent.previous_sibling.get_text()
)
```



### 正则表达式

自己学吧（没必要背下来我觉得。。。）



### 正则表达式和BeautifulSoup

打印以`../img/gifts/img`开头，`.jpg`结尾的图片

```python
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://pythonscraping.com/pages/page3.html")
bs = BeautifulSoup(html.read(), "html.parser")
images = bs.find_all("img", {"src": re.compile("\.\.\/img\/gifts\/img.*\.jpg")})
for img in images:
    print(img["src"])
```



### 获取属性

对于一个标签对象，可以用下面代码获取全部属性

img.attrs

如果只要src则

img.attrs['src']



### Lambda表达式

可学可不学（看自己，反正标题给你起了）



## 编写网络爬虫

**网络爬虫**就是检查一个网站，寻找另一个URL，再获取该URL对应的网页内容，不断循环这一过程。

### 遍历单个域名

#### 最简单的遍历方式

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
bs = BeautifulSoup(html, "html.parser")

for link in bs.find_all("a"):
    if "href" in link.attrs:
        print(link.attrs["href"])
```



#### 只遍历词条链接

简单版本（因为外网问题不一定能成功，可能会有502的问题）

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")

if html:
    bs = BeautifulSoup(html, "html.parser")
    for link in bs.find("div", {"id": "bodyContent"}).find_all(
        "a", re.compile("^(/wiki/)((?!:).)*$")
    ):
        if "href" in link.attrs:
            print(link.attrs["href"])
else:
    print("Failed to visit this web page.")
```

复杂版本（新增了retry操作）

```python
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import time

def get_html(url, retries=3):
    for i in range(retries):
        try:
            return urlopen(url)
        except HTTPError as e:
            print(f"HTTP error: {e.code}")
            if e.code == 502:
                print(f"Attempt {i + 1} failed with error 502: Bad Gateway. Retrying...")
                time.sleep(2)
            else:
                return None
        except URLError as e:
            print(f"URL error: {e.reason}")
            return None
    return None

url = "https://en.wikipedia.org/wiki/Kevin_Bacon"
html = get_html(url)

if html:
    bs = BeautifulSoup(html, "html.parser")
    for link in bs.find("div", {"id": "bodyContent"}).find_all(
        "a", href=re.compile("^(/wiki/)((?!:).)*$")
    ):
        if "href" in link.attrs:
            print(link.attrs["href"])
else:
    print("Failed to retrieve the web page.")
```



#### 更正规的遍历方式

random是用来做随机处理

`format()` 方法是用来格式化字符串的一个内置方法，将变量插入到字符串中的特定位置，从而创建一个新的格式化后的字符串

请自己思考以下代码的purpose是什么？

**注意：**

1. 可能与外网有关，不一定都能成功，如果遇上了URLError的话也可以自己加上重新递归
2. 如果觉得爬取数据过多，可以选择在while的最后加一个break

```python
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import random
import time

random.seed(time.time())


def get_html(url, article, retries=10):
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
    if html:
        bs = BeautifulSoup(html, "html.parser")
        return bs.find("div", {"id": "bodyContent"}).find_all(
            "a", href=re.compile("^(/wiki/)((?!:).)*$")
        )
    else:
        print("Failed to retrieve the web page.")


links = get_links(get_html("http://en.wikipedia.org{}", "/wiki/Kevin_Bacon"))

while links:
    newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
    print(newArticle)
    get_links(get_html("http://en.wikipedia.org{}", newArticle))
```

个人练手代码（单个网站循环深入）

```python
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
```



### 抓取整个网站

由于外网原因，所以之后的例子就拿百度百科为例了

#### 上述例子改为百度百科

```python
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.parse import unquote
from bs4 import BeautifulSoup
import re
import random
import time

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
        for link in bs.find("div", {"class": "mainContent_dvM3V"}).find_all(
            "a", href=re.compile("^(/item/)((?!:).)*$")
        ):
            links.add(link)

        return links
    else:
        print("Failed to retrieve the web page.")


def link_loop(articleUrl="/item/DC漫画/725892?fr=ge_ala"):
    newArticleUrl = quote(articleUrl, safe="/?=&")
    links = get_links(get_html("https://baike.baidu.com{}", newArticleUrl))
    while links:
        newArticle = list(links)[random.randint(0, len(links) - 1)].attrs["href"]
        print(unquote(newArticle))
        link_loop(unquote(newArticle))
        break


link_loop()
```



#### 链接去重

使用set方法去重，注意global，可以对比set和列表的使用前后区别

```python
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
```

**注意：**考虑一下递归的深度



#### 收集网站数据

以网站的标题为例

```python
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
```



#### 互联网抓取

**注意：**内链和外链的检查（通俗的说就是内部网站和外部网站的处理，白名单等等一系列判断）





## 网络爬虫模型

大型、可扩展的爬虫模型一般分为几种模式，学习这些模式可以大幅改善代码的可维护性和稳健性

### 规划和定义对象

提前规划数据模型，认真思考并规划究竟需要抓取什么信息以及如何进行存储



### 处理不同的网站布局

每个网站的解析函数基本上做的几件事情：

- 选择标题元素并从标题中抽取文本
- 选择文章的主要内容
- 按需选择其他内容选项
- 返回此前由字符串实例化的Content对象

```python
import requests
from bs4 import BeautifulSoup


class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body


def getPage(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, "html.parser")


def scrapeBrookings(url):
    bs = getPage(url)
    title = bs.find("h1").text
    body = bs.find_all("div", {"class": "post-body"}).text
    return Content(url, title, body)


url = (
    "https://www.brookings.edu/blog/future-development/2018/01/26/delivering-inclusive-urban-access-3-uncomfortable-truths"
)
content = scrapeBrookings(url)
print("Title: {}".format(content.title))
print("URL: {}".format(content.url))
print("Body: {}".format(content.body))
```

现在一起写一个Crawler去爬任何网站的标题和内容

> 非常重要的一个模板!

```python
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
        # print(pageObj.select_one(".para_uWBUP"))
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
```



### 结构化爬虫

以下由于作者都掌握了，想看相关代码请向作者借书/自行购买`Python网络爬虫权威指南`

#### 通过搜索抓取网站

- 大多数网站会通过参数在URL传递
- 搜索后的其他结果链接也是个URL
- 由此我们可以通过URL进行规范化



#### 通过链接抓取网站

通俗的讲就是设置内链外链的黑白名单再反复进行深度爬取



#### 抓取多种类型的页面

由于一个网站的内链会有很多种类，所以需要进行不同的处理，那么我们要解决的就是通过一些标识去分类再爬取

- 可以选择一些缺失的特定字段判别
- 可以通过标签页中特殊的元素或者选择器去识别



## Scrapy

这次来介绍非常好用的第三方框架——`Scrapy`

### 安装Scrapy

```python
pip install Scrapy
```

#### 蜘蛛初始化

> 一个`Scrapy`项目就是一个蜘蛛（spider），不用`Scrapy`抓取网页的程序就叫`Crawler`

在目录中创建新的蜘蛛：

```python
scrapy startproject baikeSpider
```

创建完之后文件结构如下：

- scrapy.cfg
- baikeSpider
  - spiders
    - _ _ init.py _ _
  - items.py
  - middlewares.py
  - piplines.py
  - settings.py
  - _ _ init.py_ _



### 创建简易爬虫

**步骤：**

- 创建文件**article.py**（baikeSpider\baikeSpider\spiders\article.py）

- 类的名称`ArticleSpider`和文件夹名`baikeSpider`不同，表明这个类在`baikeSpider`中专门用于抓取文章网页
- 注意两个函数
  - start_requests：Scrapy定义的程序入口，用于生成Scrapy用来抓取网站的Request对象
  - parse是用户自定义的回调函数，通过callback=self.parse传递给Request对象

- 运行指令（在对应文件夹）：scrapy runspider article.py

```python
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
```

如果你没有翻墙的梯子，或者翻墙的梯子会导致DNS或者Proxy问题，那么可以用我注释掉的url，但这时会遇到一个问题（百度百科的 `robots.txt` 文件禁止了某些页面的爬取，因此你的请求被忽略了）

**解决方法：**

1. **尊重 robots.txt 文件**：

   - 默认情况下，Scrapy 会遵循网站的 `robots.txt` 文件。可以通过修改 Scrapy 配置来忽略 `robots.txt`，不过这样做可能违反网站的爬虫规则。你可以在设置文件中将 `ROBOTSTXT_OBEY` 设置为 `False`：

     ```
     pythonCopy code# settings.py
     ROBOTSTXT_OBEY = False
     ```

2. **处理被禁止的请求**：

   - 检查 `robots.txt` 文件并根据其指引调整你的爬虫。例如，你可以选择性地抓取不受限制的页面。

3. **动态内容加载**：

   - 如果页面内容是通过 JavaScript 动态加载的，可以考虑使用诸如 Splash、Selenium 等工具来渲染页面。

> 这时用第一种方法就能解决问题了



### 带规则的抓取

我们之前只是抓取了一个URL，还不具备寻找新网站的能力，所以我们需要用`Scrapy`的`CrawlSpider`来完善

以下代码会少许的复杂，请一一对应的看

**代码理解：**

1. 没有使用`start_requests`函数，而是定义了两个列表`start_urls`和`allowed_domains`，告诉蜘蛛从哪抓取，以及哪些**域名应该保留**，哪些应该忽略
2. `rules`列表，为链接的**保留**和**忽略**提供进一步说明，**正则 .*** 保留了所有链接
3. 提取器
   - `XPath`通常用于**获取包含子标签**
   - `CSS`子标签的**文字会被忽略**

```python
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

```

**注意：**这个如果不按Ctrl+C或者关闭终端程序就会一直运行！！

**详细解析：**

1. Rule对象列表（定义了所有链接的过滤规则。当设置多个规则时，每个链接都要按顺序检查。匹配的**第一个规则**用来**决定如何处理**链接。如果链接不能匹配任何规则就会被忽略）
   - link_extractor（必选参数，是一个LinkExtractor对象）
   - callback（用来解析网页内容的参数）
   - cb_kwargs（传入回调函数的参数字典。字典形式是{arg_name1: arg_value1, arg_name2: arg_value2}）
   - follow（是否将当前页面种找到的链接添加到后面的抓取里，如果没提供回调函数，那么默认是True；如果提供了回调函数，则这个参数默认是False）
2. LinkExtractor（一个简单的类，专门用于根据提供的规则识别和返回HTML内容页面中的**链接**）
   - 可以扩展，可以增加自定义参数！
   - 常用参数
     - allow（允许匹配正则表达式的所有链接）
     - deny（拒绝匹配正则表达式的所有链接）

如果我的rules是这么写的能做什么？

```python
rules = [
    Rule(
        LinkExtractor(allow="^(/wiki/)((?!:).)*$"),
        callback="parse_items",
        follow=True,
        cb_kwargs={"is_article": True},
    ),
    Rule(
        LinkExtractor(allow=".*"),
        callback="parse_items",
        cb_kwargs={"is_article": False},
    )
]
```

那我可以通过is_article的值做不同的操作（写在回调函数中）



### 创建Item

