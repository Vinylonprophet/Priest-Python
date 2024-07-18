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

Scrapy提供了一个可以帮助组织已收集的item，将它们保存到带有明确定义的字段的自定义对象中

[item定义模型参考文档](https://doc.scrapy.org/en/latest/topics/items.html)

创建items.py文件

```python
import scrapy


class Article(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    lastUpdated = scrapy.Field()
```

创建articleItems.py文件

```python
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import Article


class ArticleSpider(CrawlSpider):
    name = "articleItems"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Benevolent_dictator_for_life"]
    rules = [
        Rule(
            LinkExtractor(allow="(/wiki/)((?!:).)*$"),
            callback="parse_items",
            follow=True,
        )
    ]

    def parse_items(self, response):
        article = Article()
        article["url"] = response.url
        article["title"] = response.css("h1 ::text").extract_first()
        article["text"] = response.xpath(
            "//div[@id='mw-content-text']//text()"
        ).extract()
        lastUpdated = response.css("li#footer-info-lastmod ::text").extract_first()
        article["lastUpdated"] = lastUpdated.replace(
            "This page was last edited on ", ""
        )
        return article
```



### 输出Item

**Scrapy可以将信息保存为不同格式，例如CSV，JSON，XML文件**

scrapy runspider articleItems.py -o articles.csv -t csv

scrapy runspider articleItems.py -o articles.json -t json

scrapy runspider articleItems.py -o articles.xml -t xml



### Item管线组件

虽然Scrapy是`单线程`的，但是能够`异步发出`和`处理多个请求`，这样会比之前介绍的爬虫快~

Scrapy的item管线组件可以进一步提高网页爬取速度，因为可以**在等待请求返回结果的过程中完成所有数据**，而不是**等待数据处理完成之后再发起新请求**。

使用步骤：

1. 为了创建一个item管线组件，用到创建仓库时自带的`settings.py`文件，注意注释的**ITEM_PIPELINES**打开

   ```python
   #ITEM_PIPELINES = {
   #    "baikeSpider.pipelines.BaikespiderPipeline": 300,
   #}
   ```

   并且改为**WikispiderPipeline**，因为我们现在做的操作是爬取wiki百科，所以我们将会创建一个**WikispiderPipeline**类

   ```python
   ITEM_PIPELINES = {
      "baikeSpider.pipelines.WikispiderPipeline": 300,
   }
   ```

   **注意：**

   1. 300这个整数是指管线组件的顺序，1，2，3 ··· ··· 一直到1000，**管线组件按照顺序方式运行**
   2. 增加管线组件类可以在收集数据的同时，由**管线组件承担数据处理的重任**

2. Scrapy必须要求返回一个item，所以我们还是要在parse_items中进行**数据提取**，然后传给**管线**

   `articlePipelines.py`

   ```python
   from scrapy.linkextractors import LinkExtractor
   from scrapy.spiders import CrawlSpider, Rule
   from baikeSpider.spiders.items import Article
   
   
   class ArticleSpider(CrawlSpider):
       name = "articlePipelines"
       allowed_domains = ["wikipedia.org"]
       start_urls = ["https://en.wikipedia.org/wiki/Benevolent_dictator_for_life"]
       rules = [
           Rule(
               LinkExtractor(allow="(/wiki/)((?!:).)*$"),
               callback="parse_items",
               follow=False,
           )
       ]
   
       def parse_items(self, response):
           article = Article()
           article["url"] = response.url
           article["title"] = response.css("h1 ::text").extract_first()
           article["text"] = response.xpath(
               "//div[@id='mw-content-text']//text()"
           ).extract()
           article["lastUpdated"] = response.css(
               "li#footer-info-lastmod ::text"
           ).extract_first()
           print(article)
           return article
   ```

3. 把创建仓库自带的`pipelines.py`文件给写成新的组件代码

   `pipelines.py`

   ```python
   from datetime import datetime
   from baikeSpider.spiders.items import Article
   from string import whitespace
   
   
   class WikispiderPipeline(object):
       def process_item(self, article, spider):
           dateStr = article["lastUpdated"]
           article["lastUpdated"] = article["lastUpdated"].replace(
               "This page was last edited on ", ""
           )
           article["lastUpdated"] = article["lastUpdated"].strip()
           article["lastUpdated"] = datetime.strptime(
               article["lastUpdated"], "%d %B %Y, at %H:%M"
           )
   
           article["text"] = [line for line in article["text"] if line not in whitespace]
           article["text"] = "".join(article["text"])
           return article
   ```

   **process_item**是必选方法，Scrapy用这个方法异步处理收集到的Items

4. items.py文件保持不变

   ```python
   import scrapy
   
   
   class Article(scrapy.Item):
       url = scrapy.Field()
       title = scrapy.Field()
       text = scrapy.Field()
       lastUpdated = scrapy.Field()
   ```

5. 运行指令：

   > scrapy crawl articlePipelines -o articles.csv -t csv

**总结：**

1. 两个地方处理数据，一个是spider中的**parse_items**方法，另一个是管线组件中的**process_item**

2. 如果解析要花费很长时间，可以考虑将数据类型移动到管线组件中，并且增加一个item类过滤

   ```python
   def process_item(self, item, spider):
       if isinstance(item, Article):
           # 面向具体Article类型数据解析
   ```



### Scrapy日志管理

`settings.py`文件中新增代码

```python
LOG_LEVEL = "ERROR"
```

日志等级制度如下：

- CRITICAL（关键）
- ERROR（错误）
- WARNING（警告）
- DEBUG（调试）
- INFO（信息）

如果要输出日志文件就运行这行指令：

```python
scrapy crawl aritcles -s LOG_FILE=wiki.org
```



### 更多资源

学习书记推荐《精通Python爬虫框架Scrapy》



### 作者踩坑分享

> 爬取这个网站的时候心血来潮就用Scrapy框架来爬取 https://www.sylvanianfamilies.com/zh-hk/catalog/categorieslist.php?category_id=1

代码其实也写得差不多了：

```python
import json
from scrapy import FormRequest, Request, Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from sylvanianFamiliesSpider.spiders.items import Good


class GoodsSpider(CrawlSpider):
    name = "GoodItems"
    allowed_domains = ["sylvanianfamilies.com"]
    start_urls = [
        "https://www.sylvanianfamilies.com/zh-hk/catalog/categorieslist.php?category_id=1"
    ]
    rules = [
        Rule(
            LinkExtractor(allow=r".*item_detail.*"),
            callback="parse_items",
            follow=False,
            cb_kwargs={"is_good": True},
        ),
    ]

    def parse_items(self, response, is_good):
        good = Good()
        self.logger.info(f"Parsing item page: {response.url}")

        if is_good:
            l_content = response.xpath('//*[@id="l-content"]').extract_first()
            if l_content:
                selector = Selector(text=l_content)
                good["name"] = selector.xpath("//h1/text()").extract_first()
                if "name" in good:
                    good["name"] = good["name"].strip()
                good["category"] = selector.css(
                    ".m-icon-item .m-icon-s ::text"
                ).extract_first()
                good["introduction"] = " ".join(
                    [
                        Selector(text=part).xpath("string()").get()
                        for part in selector.css(".m-txt-p.m-box-line2").getall()
                    ]
                )
                good["product_id"] = selector.css(".m-table-gr td ::text").get()

                img_urls = selector.css(".nav-slide img::attr(src)").extract()
                good["img_urls"] = img_urls
                return good

        print(f"URL: {response.url}")
```

但是写到这里才发现，这个网站有的页面需要点击一个叫做**更多内容**的按钮才能显示更多的product，那我就裂开了，试图模拟页面的点击事件去拉取更多的产品。。。

终于最后问chatgpt。。。

> **Ask:**
>
> scrapy框架可以模拟点击事件吗？
>
> **Answer:**
>
> Scrapy本身是一个基于Python的爬虫框架，它主要用于抓取静态页面数据。对于需要模拟点击事件才能获取内容的网站，Scrapy通常不能直接处理，因为它无法执行JavaScript或模拟用户交互动作。
>
> 不过，你可以考虑以下几种方法来处理需要点击事件的情况：
>
> 1. **分析XHR请求**: 使用浏览器开发者工具分析点击事件后发送的XHR（XMLHttpRequest）请求，直接模拟这些请求来获取数据。
> 2. **使用Splash或Selenium**: Splash是一个JavaScript渲染服务，可以与Scrapy结合使用，用来处理需要JavaScript渲染的页面。另外，Selenium是一个自动化测试工具，可以模拟用户在浏览器中的操作，也可以与Scrapy集成来处理点击事件。
> 3. **直接分析API**: 如果网站有提供API接口，通常这是获取数据的更好方式，因为API返回的数据更结构化，而且不需要模拟点击事件。
>
> 你可以根据具体的网站和需求选择最合适的方法来解决。

所以最后还是用API的方式去解决这个问题，当然目前没有深入学习Scrapy我也无法判断ChatGPT的这个回答是对是错！



## 存储数据

如果要创建一个网站的后端服务或者自己创建API，需要让爬虫把数据写入数据库

如果要快速简单的手机网上的文档存到硬盘里，那么需要创建一个文件流

### 媒体文件

两中存储方式，保存URL和保存源文件

URL保存优点：

- 节流，不用下文件
- 节约存储空间
- 存URL的代码容易
- 降低主机服务器的负载

URL保存缺点：

- 网站会采取`盗链`措施
- 链接根据别人服务器走
- 盗链的目标地址很容易改变
- 下载文件（比如css，js，MP4等等）可以做到模仿浏览器访问，更真实

**从远程下载图片：**

```python
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup

html = urlopen("https://pythonscraping.com/")
bs = BeautifulSoup(html, "html.parser")
imageLocation = bs.find("div", {"class": "pagelayer-image-holder"}).find("img")["src"]
urlretrieve(imageLocation, "logo.jpg")
```

**把网站上所有src属性的内部文件下载下来：**

```python
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
import os

downloadDirectory = "download"
baseUrl = "https://pythonscraping.com"


def getAbsoluteURL(baseUrl, source):
    if source.startswith("https://www."):
        url = "https://{}".format(source[12:])
    elif source.startswith("https://"):
        url = source
    elif source.startswith("www."):
        url = source[4:]
        url = "https://{}".format(source)
    else:
        url = "{}/{}".format(baseUrl, source)
    if baseUrl not in url:
        return None
    return url


def getDownloadPath(baseUrl, absoluteUrl, downloadDirectory):
    path = absoluteUrl.replace("www.", "")
    path = path.replace(baseUrl, "")
    path = downloadDirectory + path.split("?")[0]
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    return path


html = urlopen("https://pythonscraping.com")
bs = BeautifulSoup(html, "html.parser")
downloadList = bs.findAll(src=True)

for download in downloadList:
    fileUrl = getAbsoluteURL(baseUrl, download["src"])
    print(fileUrl)
    if fileUrl is not None:
        urlretrieve(fileUrl, getDownloadPath(baseUrl, fileUrl, downloadDirectory))
```

这个程序显示对`URL链接进行清理和标准化`，获取文件绝对路径`（去掉外链）`，最后全部下载到downloaded文件夹里



### 把数据存储到CSV

**CSV**是存储`表格数据`的常用文件格式，CSV的每一行都用**换行符**分隔，列与列之间用逗号分隔

python的csv库支持非常简单的修改CSV文件，甚至可以从零开始创建CSV文件

```python
import csv

csvFile = open("dist/5.3_test.csv", "w+")
try:
    writer = csv.writer(csvFile)
    writer.writerow(("column1", "column2", "column3"))
    for i in range(10):
        writer.writerow((i, i + 2, i * i))
finally:
    csvFile.close()
```

**注意：**如果csv文件已经存在了，那么将覆写该文件



一个获取HTML表格并写入CSV文件的代码

```python
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup


html = urlopen("http://en.wikipedia.org/wiki/Comparison_of_text_editors")
bs = BeautifulSoup(html, "html.parser")

table = bs.find_all("table", {"class": "wikitable"})[0]
rows = table.find_all("tr")

csvFile = open("dist/5.4_test.csv", "wt+", encoding="utf-8")
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
        for cell in row.find_all(["td", "th"]):
            csvRow.append(cell.get_text())
        writer.writerow(csvRow)
finally:
    csvFile
```



### MySQL

爬取结束录入数据库，这一部分因为作者最近用的是**MongoDB**，所以先不进行具体学习，感兴趣的可以翻到书本第75页

这里有个推荐的项目例子：

每一小时检查https://isitchristmas.com网站，如果页面信息不是NO，就发送一封电子邮件到邮箱，通知你今天是圣诞节



## 读取文档

### 纯文本

```python
from urllib.request import urlopen

textPage = urlopen("https://www.pythonscraping.com/pages/warandpeace/chapter1.txt")
print(textPage.read())
```



#### 文本和全球网络

了解UTF-8和ISO标准，如果访问到一些文本，你需要转换成UTF-8

```python
from urllib.request import urlopen

textPage = urlopen("https://www.pythonscraping.com/pages/warandpeace/chapter1-ru.txt")
print(str(textPage.read(), "utf-8"))
```

统一对之后的文本转换成UTF-8，至于要不要这么做，以后**可以打开inspect的meta标签看编码格式**

```python
html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bs = BeautifulSoup(html, "html.parser")
content = bs.find('div', {"id": "mw-content-text"}).get_text()
content = bytes(content, 'UTF-8')
content = content.decode('UTF-8')
```



### CSV

python的csv库主要是面向本地csv文件，如果我们要抓取在线的csv文件可以参考下面的例子

```python
from urllib.request import urlopen
from io import StringIO
import csv

data = (
    urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv")
    .read()
    .decode("ascii", "ignore")
)
dataFile = StringIO(data)
csvReader = csv.reader(dataFile)

for row in csvReader:
    print(row)
```

这时候我们发现输出了header行，参考以下代码解决这一问题

```python
from urllib.request import urlopen
from io import StringIO
import csv

data = (
    urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv")
    .read()
    .decode("ascii", "ignore")
)
dataFile = StringIO(data)
csvReader = csv.DictReader(dataFile)

for row in csvReader:
    print(row)
```

与csvReader相比，DictReader会花费多一点点时间，但是我们不在乎这几微秒



### PDF

不常用，参考书本P100



### 微软Word和.docx

不常用，参考书本P102

大致流程：BytesIO 读成一个二进制文件对象 -> 用python标准库 zipfile解压（所有的.docx都是经过压缩的） -> document.read('word/document.xml') 变成xml文件

之后的提取请自己参考



## 数据清洗

### 编写代码清洗数据

