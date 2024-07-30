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
