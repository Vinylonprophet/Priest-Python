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



## 配置与管理

设置是最重要的基本机制之一，除了`调优`和`配置`之外，还可以`启用功能`，以及允许`拓展框架`



### 使用Scrapy设置

Scrapy有五个递增的优先级：

1. 默认设置，在系统的Scrapy源码或Scrapy的github可以找到
2. 项目<project_name>/settings.py文件中修改配置
3. 每个爬虫的设置，在爬虫定义中使用custom_settings为每个爬虫自定义设置（为一个指定爬虫启用或者禁用Item管道）
4. 对一些临时修改，可以使用命令行参数-s，在该级别中可能会设置`API Secrets`、`密码`
5. 可以通过环境变量来设置 Scrapy 的配置，这些环境变量的优先级最高，会覆盖上述所有配置



### 基本设置

#### 分析

##### 1. 日志

**LOG_LEVEL** 是 Scrapy 设置中的一个选项，用于配置日志记录的详细程度。它可以接受以下值，每个值代表不同的日志记录级别：

`CRITICAL` - 只记录严重错误。

`ERROR` - 记录所有错误信息。

`WARNING` - 记录警告信息（默认值）。

`INFO` - 记录一般运行信息。

`DEBUG` - 记录调试信息，最详细的日志记录级别。



**LOGSTATS_INTERVAL** 是 Scrapy 设置中的一个选项，用于配置记录统计信息的时间间隔。该选项的值是一个整数，表示以秒为单位的时间间隔。

`默认值`是60s



**LOG_FILE** 是 Scrapy 设置中的一个选项，用于配置日志文件的路径。通过设置 `LOG_FILE`，你可以将 Scrapy 生成的日志输出到指定的文件中，而不是输出到标准输出（控制台）。

**示例设置：**

如果你希望将日志输出到名为 `scrapy_log.txt` 的文件中，可以在 `settings.py` 中这样设置：

```
python
Copy code
LOG_FILE = 'scrapy_log.txt'
```

这将使 Scrapy 在项目的根目录下生成一个名为 `scrapy_log.txt` 的文件，并将所有日志信息写入其中。

你也可以指定一个绝对路径，例如：

```
python
Copy code
LOG_FILE = '/path/to/your/log/scrapy_log.txt'
```

通过设置 `LOG_FILE`，可以方便地将日志记录保存到文件中，便于后续的查看和分析。这样在调试、监控和管理爬虫时，日志信息会更加直观和系统化。



**LOG_STDOUT** 是 Scrapy 设置中的一个选项，用于控制标准输出（stdout）是否被捕获并记录到 Scrapy 的日志中。默认情况下，标准输出不会被记录到日志文件中，但通过设置 `LOG_STDOUT`，你可以将所有标准输出的信息（例如 `print` 函数的输出）也写入日志文件。

**示例设置：**

如果你希望将标准输出的信息也记录到日志中，可以在 `settings.py` 中这样设置：

```
python
Copy code
LOG_STDOUT = True
```

设置为 `True` 后，所有标准输出的信息都会被捕获并记录到 Scrapy 的日志中。如果你不希望捕获标准输出，可以将其设置为 `False`（这是默认值）：

```
python
Copy code
LOG_STDOUT = False
```

通过设置 `LOG_STDOUT`，你可以更全面地记录和管理爬虫运行过程中的所有信息，这在调试和问题排查时尤其有用。



##### 2. 统计

**STATS_DUMP** 是 Scrapy 设置中的一个选项，用于控制在爬虫结束时是否将统计信息输出到日志中。通过设置 `STATS_DUMP`，你可以选择是否在爬虫运行结束时记录详细的统计数据。

**示例设置：**

如果你希望在爬虫结束时将统计信息输出到日志中，可以在 `settings.py` 中这样设置：

```python
STATS_DUMP = True
```

这将使 Scrapy 在爬虫运行结束时，将所有的统计信息（例如抓取的页面数量、处理的项目数量、请求的数量、响应的数量等）输出到日志中。

如果你不希望在爬虫结束时输出统计信息，可以将其设置为 `False`：

```python
STATS_DUMP = False
```

**作用和功能：**

1. **记录统计信息**：在爬虫结束时输出统计信息，可以帮助你了解爬虫的整体运行情况，包括爬取效率和处理能力。
2. **调试和优化**：通过查看统计信息，可以帮助发现爬虫运行中的瓶颈和问题，从而进行针对性的调试和优化。
3. **日志管理**：输出统计信息到日志中，可以在一个地方集中查看所有信息，便于管理和分析。

通过设置 `STATS_DUMP`，你可以更好地记录和管理爬虫的统计信息，从而提高调试和优化的效率。



**DOWNLOADER_STATS** 是 Scrapy 设置中的一个选项，用于控制是否启用下载器统计信息。下载器统计信息包括关于请求和响应的数据，例如请求数量、响应数量、下载的字节数等。通过设置 `DOWNLOADER_STATS`，你可以选择是否收集这些统计信息。

**示例设置：**

如果你希望启用下载器统计信息，可以在 `settings.py` 中这样设置：

```python
DOWNLOADER_STATS = True
```

这将使 Scrapy 收集并记录所有与下载器相关的统计信息。

如果你不希望启用下载器统计信息，可以将其设置为 `False`：

```python
DOWNLOADER_STATS = False
```

**作用和功能：**

1. **监控请求和响应**：启用下载器统计信息可以帮助你监控爬虫发送的请求和接收到的响应数量，这对于评估爬虫性能和发现问题非常有帮助。
2. **评估性能**：通过收集下载器统计信息，你可以评估爬虫的下载速度、响应时间和数据传输量，从而优化爬虫性能。
3. **调试和优化**：详细的下载器统计信息可以帮助你发现爬虫运行中的瓶颈，例如慢速响应的 URL 或者频繁失败的请求，从而进行针对性的调试和优化。

**示例统计信息：**

启用 `DOWNLOADER_STATS` 后，Scrapy 会收集并记录以下类型的统计信息：

- `downloader/request_count`：发送的请求数量
- `downloader/request_method_count/GET`：使用 GET 方法的请求数量
- `downloader/response_count`：接收到的响应数量
- `downloader/response_status_count/200`：状态码为 200 的响应数量
- `downloader/response_bytes`：下载的总字节数

**示例日志输出：**

当爬虫运行结束时，如果启用了 `DOWNLOADER_STATS`，你可以在日志中看到类似如下的统计信息：

```shell
INFO: Dumping Scrapy stats:
{'downloader/request_count': 150,
 'downloader/request_method_count/GET': 150,
 'downloader/response_count': 150,
 'downloader/response_status_count/200': 140,
 'downloader/response_status_count/404': 10,
 'downloader/response_bytes': 1024000,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2024, 8, 5, 10, 0, 0, 0)}
```

通过设置 `DOWNLOADER_STATS`，你可以获取到详细的下载器统计信息，从而更好地监控和优化爬虫的性能。



**DEPTH_STATS** 是 Scrapy 设置中的一个选项，用于控制是否启用抓取深度统计信息。抓取深度统计信息包括有关爬虫抓取的页面深度的数据，这些数据可以帮助你了解爬虫在抓取过程中所达到的深度。通过设置 `DEPTH_STATS`，你可以选择是否收集这些统计信息。

**示例设置：**

如果你希望启用抓取深度统计信息，可以在 `settings.py` 中这样设置：

```python
DEPTH_STATS = True
```

这将使 Scrapy 收集并记录所有与抓取深度相关的统计信息。

如果你不希望启用抓取深度统计信息，可以将其设置为 `False`：

```python
DEPTH_STATS = False
```

**作用和功能：**

1. **监控抓取深度**：启用抓取深度统计信息可以帮助你监控爬虫抓取的页面深度，这对于评估爬虫的广度和深度非常有帮助。
2. **优化抓取策略**：通过收集抓取深度统计信息，你可以了解爬虫在不同深度的表现，从而调整抓取策略以提高效率。
3. **调试和分析**：详细的抓取深度统计信息可以帮助你发现爬虫在不同深度遇到的问题，例如页面链接深度过大导致的抓取效率低下，从而进行针对性的调试和优化。

**示例统计信息：**

启用 `DEPTH_STATS` 后，Scrapy 会收集并记录以下类型的统计信息：

- `depth/0`：抓取深度为 0 的页面数量
- `depth/1`：抓取深度为 1 的页面数量
- `depth/2`：抓取深度为 2 的页面数量
- 等等...

**示例日志输出：**

当爬虫运行结束时，如果启用了 `DEPTH_STATS`，你可以在日志中看到类似如下的统计信息：

```shell
INFO: Dumping Scrapy stats:
{'depth/0': 50,
 'depth/1': 100,
 'depth/2': 75,
 'depth/3': 25,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2024, 8, 5, 10, 0, 0, 0)}
```

通过设置 `DEPTH_STATS`，你可以获取到详细的抓取深度统计信息，从而更好地监控和优化爬虫的抓取策略和性能。



**DEPTH_STATS_VERBOSE** 是 Scrapy 设置中的一个选项，用于控制是否输出更详细的抓取深度统计信息。当设置为 `True` 时，Scrapy 会提供更详细的统计数据，包括每个深度的详细信息，这些信息可以帮助你更全面地了解爬虫的抓取深度分布情况。

**示例设置：**

如果你希望输出更详细的抓取深度统计信息，可以在 `settings.py` 中这样设置：

```python
DEPTH_STATS_VERBOSE = True
```

这将使 Scrapy 在统计信息中包含每个深度的详细数据。

如果你希望只输出基本的抓取深度统计信息，可以将其设置为 `False`：

```python
DEPTH_STATS_VERBOSE = False
```

**作用和功能：**

1. **详细分析**：启用详细统计可以帮助你深入分析爬虫在各个深度层次的表现，提供每个深度的详细数据，方便发现深度相关的潜在问题。
2. **优化策略**：更详细的统计信息可以帮助你调整抓取策略，例如优化深度限制，以提高抓取效率和覆盖范围。
3. **调试和分析**：通过详细的深度统计数据，你可以更清楚地了解爬虫的抓取行为，发现可能的抓取瓶颈或深度层次的异常情况。



**STATSMAILER_RCPTS** 是 Scrapy 设置中的一个选项，用于配置在爬虫结束时接收统计信息的电子邮件地址。通过设置 `STATSMAILER_RCPTS`，你可以将爬虫运行结束后的统计信息通过电子邮件发送给指定的收件人。

**示例设置：**

如果你希望将统计信息发送到某个电子邮件地址，可以在 `settings.py` 中这样设置：

```python
STATSMAILER_RCPTS = ['example@example.com']
```

这将使 Scrapy 在爬虫结束时将统计信息发送到 `example@example.com`。

你可以指定多个电子邮件地址，使用逗号分隔，如下所示：

```python
STATSMAILER_RCPTS = ['example1@example.com', 'example2@example.com']
```

**作用和功能：**

1. **自动报告**：通过配置 `STATSMAILER_RCPTS`，你可以在爬虫运行结束后自动接收爬虫的统计信息报告，这对于远程监控爬虫运行状态非常有用。
2. **监控和分析**：收到统计信息邮件后，你可以快速了解爬虫的性能和运行状态，从而进行进一步的分析和优化。
3. **便于管理**：通过将统计信息发送到电子邮件，你可以方便地记录和存档爬虫运行的统计数据，便于长期管理和审计。



##### 3. Telnet

**TELNETCONSOLE_ENABLED** 是 Scrapy 设置中的一个选项，用于启用或禁用 Telnet 控制台。Telnet 控制台允许你通过 Telnet 连接到正在运行的 Scrapy 爬虫，并实时查看和控制爬虫的状态。

**示例设置：**

如果你希望启用 Telnet 控制台，可以在 `settings.py` 中这样设置：

```python
TELNETCONSOLE_ENABLED = True
```

这将启用 Telnet 控制台，允许你通过 Telnet 连接到爬虫。

如果你希望禁用 Telnet 控制台，可以将其设置为 `False`：

```python
TELNETCONSOLE_ENABLED = False
```

**作用和功能：**

1. **实时控制**：通过 Telnet 控制台，你可以实时查看爬虫的运行状态、执行命令、查看爬取的数据等，这对于调试和实时监控非常有帮助。
2. **调试和管理**：Telnet 控制台提供了一个交互式的方式来管理和调试爬虫，例如，检查队列状态、修改爬虫设置等。
3. **访问方便**：在某些情况下，你可能需要远程访问爬虫进行管理和调试，Telnet 控制台提供了这种访问的便利。



**TELNETCONSOLE_PORT** 是 Scrapy 设置中的一个选项，用于配置 Telnet 控制台监听的端口号。通过设置 `TELNETCONSOLE_PORT`，你可以指定 Telnet 控制台使用的端口，以便通过该端口连接到正在运行的 Scrapy 爬虫。

**示例设置：**

如果你希望将 Telnet 控制台的端口设置为 6025，可以在 `settings.py` 中这样设置：

```python
TELNETCONSOLE_PORT = 6025
```

这将使 Telnet 控制台监听 6025 端口。



**连接 Telnet 控制台：**

在设置了 `TELNETCONSOLE_PORT` 后，你可以通过指定的端口连接到 Telnet 控制台。例如，如果你设置了端口为 6025，可以使用以下命令连接：

```bash
telnet localhost 6025
```



