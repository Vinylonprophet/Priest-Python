# Scrapy

## Scrapy简介

可以去看Web Scraping文件夹中的Scrapy，这里不细说



## 理解 HTML 和 XPath

挑选一部分解释



### 使用XPath选择HTML元素

#### 有用的XPath表达式

使用元素名和斜线来选择文档中的元素

```javascript
$x('/html/body/div/p')
```

对于大型文档，可以使用//语法，取得某一特定类型的元素，无需考虑其所在的层次结构

```javascript
$x('//p')
```

比如要找div元素下所有链接，可以使用//div//a，但要注意的是只是用单斜线//div/a的话只能得到一个空数组，是因为div元素下**直接下级**没有任何'a'元素

```javascript
$x('//div//a')
```

使用@符号来访问属性

```javascript
$x('//a/@href')
```

使用text()函数只获取文本

```javascript
$x('//a/text()')
```

使用*选择指定层级的所有元素

```javascript
$x('//div/*')
```

XPath也有很多像not()、contains()和starts-with()这样的函数，可以查看相关文档



## 爬虫基础

这部分我们快进到Scrapy项目，跳过scrapy shell



### 一个Scrapy项目

```sh
# scrapy startproject properties
# cd ..properties
# tree /F

.
│  scrapy.cfg
│
└─properties
    │  items.py
    │  middlewares.py
    │  pipelines.py
    │  settings.py
    │  __init__.py
    │
    └─spiders
            __init__.py
```

在本章中，我们将主要在`items.py`和`spiders`目录中工作

后续章节对`设置`、`管道`和`scrapy.cfg`进行更多探索



#### 声明item

打开items.py，重定义PropertiesItem类，我们添加几个字段，但是声明不代表我们在每个爬虫都填充该字段

items.py文件如下：

```python
from scrapy.item import Item, Field


class PropertiesItem(Item):
    title = Field()
    price = Field()
    description = Field()
    address = Field()
    image_urls = Field()

    images = Field()
    location = Field()

    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()
```



#### 编写爬虫

> 什么时候使用爬虫？什么时候使用项目？
>
> 很多网站，需要从中抽取相同类型的Item，那么可以使用一个项目；如果要处理多种不同的Item，应该使用不同的项目

使用**scrapy genspider**的话可以创建一个爬虫

现在我们使用`scrapy genspider basic web`

basic.py文件如下

```python
import scrapy


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["web"]
    start_urls = ["https://web"]

    def parse(self, response):
        pass
```

这里我们使用百度百科的蓝色监狱作为要爬取的网站，使用爬虫预定义的方法log()再修改basic.py：

```python
import scrapy


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["baike.baidu.com"]
    start_urls = [
        "https://baike.baidu.com/item/%E8%93%9D%E8%89%B2%E7%9B%91%E7%8B%B1/58149098"
    ]

    def parse(self, response):
        self.log("title: %s" % response.xpath("//h1/text()").extract())
```

记得把settings.py的ROBOTSTXT_OBEY = False改成True



#### 填充item

我们接下来引入PropertiesItem类，解锁一些新功能

basic.py

```python
import scrapy
from properties.items import PropertiesItem


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["baike.baidu.com"]
    start_urls = [
        "https://baike.baidu.com/item/%E8%93%9D%E8%89%B2%E7%9B%91%E7%8B%B1/58149098"
    ]

    def parse(self, response):
        item = PropertiesItem()
        item["title"] = response.xpath("//h1/text()").extract()
        return item
```



#### 保存文件

运行以下示例：

- scrapy crawl basic -o items.json

- scrapy crawl basic -o items.csv

- scrapy crawl basic -o items.jl



#### 清理

我们现在使用`ItemLoader`以替代那些杂乱的extract()和xpath()操作

```python
from scrapy.loader import ItemLoader
import scrapy
from properties.items import PropertiesItem


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["baike.baidu.com"]
    start_urls = [
        "https://baike.baidu.com/item/%E8%93%9D%E8%89%B2%E7%9B%91%E7%8B%B1/58149098"
    ]

    def parse(self, response):
        l = ItemLoader(item=PropertiesItem(), response=response)
        l.add_xpath("title", "//h1//text()")
        return l.load_item()
```

除了`ItemLoader`外，另一个很有意思的处理器是`MapCompose()`，通过该处理器，我们可以使用任意Python函数或Python函数链以实现复杂功能，表格如下：

| 处理器                                             | 功能描述                                             |
| -------------------------------------------------- | ---------------------------------------------------- |
| `Join()`                                           | 将多个字符串连接成一个字符串，通常用于列表合并。     |
| `MapCompose(unicode.strip)`                        | 去除每个字符串的前后空格。                           |
| `MapCompose(unicode.strip, unicode.title)`         | 去除每个字符串的前后空格，并将字符串转换为标题格式。 |
| `MapCompose(float)`                                | 将提取的字符串数据转换为浮点数。                     |
| `MapCompose(lambda i: i.replace(",", ""), float)`  | 去除字符串中的逗号，然后转换为浮点数。               |
| `MapCompose(lambda i: i.urljoin(response.url, i))` | 将相对 URL 转换为绝对 URL。                          |

可以尝试使用一下上面这张表格~~

最后使用add_value()方法，设置一些管理字段：

```python
import datetime
import socket
from scrapy.loader import ItemLoader
import scrapy
from properties.items import PropertiesItem


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["baike.baidu.com"]
    start_urls = [
        "https://baike.baidu.com/item/%E8%93%9D%E8%89%B2%E7%9B%91%E7%8B%B1/58149098"
    ]

    def parse(self, response):
        l = ItemLoader(item=PropertiesItem(), response=response)
        l.add_xpath("title", "//h1//text()")
        l.add_value("url", response.url)
        l.add_value("project", self.settings.get("BOT_NAME"))
        l.add_value("spider", self.name)
        l.add_value("server", socket.gethostname())
        l.add_value("date", datetime.datetime.now().isoformat())
        return l.load_item()
```



#### 创建contract

contract像为爬虫设计的单元测试，可以让你快速知道哪里有运行异常

contract包含在紧挨着函数名的注释（即文档字符串）中，并且以@开头

```python
import datetime
import socket
from scrapy.loader import ItemLoader
import scrapy
from properties.items import PropertiesItem


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["baike.baidu.com"]
    start_urls = [
        "https://baike.baidu.com/item/%E8%93%9D%E8%89%B2%E7%9B%91%E7%8B%B1/58149098"
    ]

    def parse(self, response):
        """This function parses a property page.

        @url https://baike.baidu.com/item/%E8%93%9D%E8%89%B2%E7%9B%91%E7%8B%B1/58149098
        @returns items 1
        @scrapes title
        @scrapes url project spider server date
        """
        l = ItemLoader(item=PropertiesItem(), response=response)
        l.add_xpath("title", "//h1//text()")
        l.add_value("url", response.url)
        l.add_value("project", self.settings.get("BOT_NAME"))
        l.add_value("spider", self.name)
        l.add_value("server", socket.gethostname())
        l.add_value("date", datetime.datetime.now().isoformat())
        return l.load_item()
```

运行 `scrapy check basic` 结果：

```python
...
----------------------------------------------------------------------
Ran 3 contracts in 7.598s

OK
```

如果url字段留空，就会失败

```python
def parse(self, response):
    """This function parses a property page.

    @url
    @returns items 1
    @scrapes title
    @scrapes url project spider server date
    """
```

代码的含义是检查该URL，并找到我列出的字段中**有值的一个Item**

附上这段整理干净的源码：

```python
import datetime
import socket
from scrapy.loader import ItemLoader
import scrapy
from properties.items import PropertiesItem


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["baike.baidu.com"]
    start_urls = [
        "https://baike.baidu.com/item/%E8%93%9D%E8%89%B2%E7%9B%91%E7%8B%B1/58149098"
    ]

    def parse(self, response):
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
```



### 抽取更多的URL

截止目前，我们在设置爬虫的start_urls属性中单一URL。该属性实际为一个**元组**

```python
start_urls = [
    "https://baike.baidu.com/item/%E8%93%9D%E8%89%B2%E7%9B%91%E7%8B%B1/58149098",
    "https://baike.baidu.com/item/%E6%8E%92%E7%90%83%E5%B0%91%E5%B9%B4%EF%BC%81%EF%BC%81/8983141"
]
```

除此之外，还可以使用文件作为URL的源，写法：

```python
start_urls = [i.strip() for i in open('todo.urls.txt').readlines()]
```

**爬取方式：**

- 水平爬取：同一层级下爬取页面（比如索引）
- 垂直爬取：从一个更高层级到一个更低层级（比如索引到详情）



#### 使用爬虫实现双向爬取

将之前的爬虫复制到spiders目录下重名为 manual.py

把原先的parse改成parse_item

```python
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
```

**注意：**yield与return在某种意义上有些相似，都是将返回值**提供给调用者**。和return不同的是，yield**不会退出函数**，而是继续执行for循环

可以执行下面的shell语句：

```python
scrapy crawl manual -o items.csv -s CLOSESPIDER_ITEMCOUNT=90
scrapy crawl manual -o items.json -s CLOSESPIDER_ITEMCOUNT=90
```

`CLOSESPIDER_ITEMCOUNT=90`是告诉爬虫在爬行指定数量（90个）的item后停止运行

这里也可以了解到Scrapy在处理请求时使用的是**后入先出（LIFO）策略**（即深度爬取优先）

我们可以通过设置Request()优先级参数修改默认顺序，大于0表示高于默认的优先级，小于0表示低于默认的优先级



#### 使用CrawlSpider实现双向爬取

设置`-t crawl`参数，使用crawl模板创建一个爬虫

```shell
scrapy genspider -t crawl easy web
```

这里的声明是继承自CrawlSpider，不再是Spider。CrawlSpider提供了一个使用rules变量实现的parse()方法，这和我们之前手工实现的功能一致

代码改为：

```python
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
```

LinkExtractor是专门用于**抽取链接**的，默认就是查找a或area的href属性，也可以通过设置它的tags和attrs参数来进行自定义

回调函数是包含回调方法名称的字符串（'parse_item'），而不是方法引用

如果你希望他跟踪链接，需要在callback方法中使用return或者yield返回它们，如果将Rule()的follow设置为true，那么spider在处理完 `callback` 方法后，会继续跟踪从该页面中提取的链接，并应用同样的规则



## 迅速的爬虫技巧

本章我们来熟悉一下Scrapy中两个最重要的类——**Request**和**Response**



### 需要登陆的爬虫

换而言之就是需要先登录获取**Cookie**

我们先将**start_urls**替换为**start_requests()**方法，因为在本例中我们要从一些更加定制化的请求开始，而不仅仅是几个URL

先看一个获取大麦cookie的例子:

```python
from scrapy import Request
from scrapy.spiders import Spider


class LoginSpider(Spider):
    name = "login"
    allowed_domains = ["search.damai.cn", "log.mmstat.com"]

    def start_requests(self):
        return [
            Request(
                "https://log.mmstat.com/v.gif?logtype=1&title=%E5%A4%A7%E9%BA%A6%E7%BD%91-%E5%85%A8%E7%90%83%E6%BC%94%E5%87%BA%E8%B5%9B%E4%BA%8B%E5%AE%98%E6%96%B9%E8%B4%AD%E7%A5%A8%E5%B9%B3%E5%8F%B0-100%25%E6%AD%A3%E5%93%81%E3%80%81%E5%85%88%E4%BB%98%E5%85%88%E6%8A%A2%E3%80%81%E5%9C%A8%E7%BA%BF%E9%80%89%E5%BA%A7%EF%BC%81&pre=https%3A%2F%2Fwww.damai.cn%2F%3Fspm%3Da2oeg.search_category.top.1.6b4b4d1565tUqm&scr=1440x900&_p_url=https%3A%2F%2Fwww.damai.cn%2F%3Fspm%3Da2oeg.home.top.1.502523e1EaYsFH&cna=GvckH9wM2UkBASYC/trmDpNJ&spm-url=a2oeg.home.top.1.502523e1EaYsFH&spm-pre=a2oeg.search_category.top.1.6b4b4d1565tUqm&spm-cnt=a2oeg.home.0.0.3a7123e1nHu1Vv&uidaplus=&aplus&pu_i=&asid=AQAAAADXyahm+CwTPwAAAADjOCNXibPF8w==&sidx=0&ckx=|&p=1&o=win10&b=chrome127&s=1440x900&w=webkit&ism=pc&cache=f43f64e&lver=8.15.23&jsver=aplus_std&pver=0.7.12&tag=1&stag=-1&lstag=-1&_slog=0"
            )
        ]

    def parse(self, response):
        print(response.headers.getlist("Set-Cookie"))
```

如果是表单提交登陆的话，可以用**FormRequest()**，参数是**formdata**去做表单提交

```python
def start_requests(self):
    return [
        FormRequest(
        	"http://web:9312/dynamic/login",
            formdata={"username": "user", "password": "pass"}
        )
    ]
```

Scrapy为我们透明的处理了Cookie，并且一旦登录成功，会在后续的请求中传输这些Cookie，和浏览器执行方式相同

如果请求一些需要实时的cookie等等，可以使用**from_response()**的方法（详细查看P81）



### 使用JSON API和AJAX页面的爬虫

Python提供了一个非常好的JSON解析库，是使用JSON.loads(response.body)解析JSON，将其转化为Pyhon原语、列表和字典组成的等效Pyhon对象

来看看作者在这一部分写的实战代码：

```python
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
```



#### 响应间传参

Request有一个名为**meta**的字典，能直接访问Response

```python
# Request处
meta={"page": page},

# Response处
response.meta["page"]
```



### 爬虫的倍速提升

就是如果可以在索引页面获取信息，就没有必要从详情页面获取信息了



### 基于Excel文件爬取的爬虫

创建一个csv文件

试试下列代码：

```python
import csv

with open("todo.csv", "rU") as f:
    reader = csv.DictReader(f)
    for line in reader:
        print(line)
```

那么你可以通过这种方式和**start_requests**结合起来，这里不多作演示，书本P92
