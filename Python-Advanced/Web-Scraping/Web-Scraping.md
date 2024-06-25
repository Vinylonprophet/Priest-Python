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
