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

