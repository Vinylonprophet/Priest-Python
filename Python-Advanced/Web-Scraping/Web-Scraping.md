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

