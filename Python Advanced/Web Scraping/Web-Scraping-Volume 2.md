# Web-Scraping-Volume 1

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

和处理代码异常一样，我们也应该编写`预防性`代码来处理意外情况

接下来的内容会提到2-gram和3-gram：

- 2-gram 是指由两个连续元素（通常是词或字符）组成的子序列
- 3-gram 是指由三个连续元素组成的子序列

总的来说，n-gram 是一种有效的工具，用于捕捉文本中的局部结构和模式

下面代码将返回在维基百科词条 **Python Programming language** 中找到的2-gram列表

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup


def getNgrams(content, n):
    content = content.split(" ")
    output = []
    for i in range(len(content) - n + 1):
        output.append(content[i : i + n])
    return output


html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bs = BeautifulSoup(html, "html.parser")
content = bs.find("div", {"id": "mw-content-text"}).get_text()
ngrams = getNgrams(content, 2)
print(ngrams)
print("2-grams count is: " + str(len(ngrams)))
```

我们用一些正则表达式来**移除转义字符(\n)**，再把**Unicode字符过滤**掉，升级后变成

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def getNgrams(content, n):
    content = re.sub("\n|[[\d+\]]", " ", content)
    content = bytes(content, "UTF-8")
    content = content.decode("ascii", "ignore")
    content = content.split(" ")
    content = [word for word in content if word != ""]
    output = []
    for i in range(len(content) - n + 1):
        output.append(content[i : i + n])
    return output


html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bs = BeautifulSoup(html, "html.parser")
content = bs.find("div", {"id": "mw-content-text"}).get_text()
ngrams = getNgrams(content, 2)
print(ngrams)
print("2-grams count is: " + str(len(ngrams)))
```

接下来我们保留单词中间的连字符，去除空字符串后面带有标点符号的字符串，同时不希望是一句句子内的词，而不会出现['management', 'It']的这种无效2-gram

参考以下代码

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string


def cleanSentence(sentence):
    sentence = sentence.split(" ")
    sentence = [word.strip(string.punctuation + string.whitespace) for word in sentence]
    sentence = [
        word
        for word in sentence
        if len(word) > 1 or (word.lower() == "a" or word.lower() == "i")
    ]
    return sentence


def cleanInput(content):
    content = re.sub("\n|\[[\d+\]]", " ", content)
    content = bytes(content, "UTF-8")
    content = content.decode("ascii", "ignore")
    sentences = content.split(". ")
    return [cleanSentence(sentence) for sentence in sentences]


def getNgramsFromSentence(content, n):
    output = []
    for i in range(len(content) - n + 1):
        output.append(content[i : i + n])
    return output


def getNgrams(content, n):
    content = cleanInput(content)
    ngrams = []
    for sentence in content:
        ngrams.extend(getNgramsFromSentence(sentence, n))
    return ngrams


html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bs = BeautifulSoup(html, "html.parser")
content = bs.find("div", {"id": "mw-content-text"}).get_text()
ngrams = getNgrams(content, 2)
print(ngrams)
print("2-grams count is: " + str(len(ngrams)))
```

cleanInput是移除所有换行符和引用，基于`句点+空格`将文本分割成句子

cleanSentence将句子分割成单词，去除标点符号和空白，去除除I和a之外的单字符单词

string.punctuation获取所有的标点符号

string.whitespace如果你print的话看不到输出什么，但是包含空白字符，不间断空格，制表符，换行符

```python
item.strip(string.punctuation)
```

此方法会去掉单词中所有的标点符号



#### 数据标准化

数据标准化得保证清洗后的数据在语言学上和逻辑学上和很多格式都一致，比如yy-mm-dd和yy/mm/dd一致



### 数据存储后再清洗

本章主要介绍了OpenRefine这个可视化程序，有兴趣请自己看书第111页



## 自然语言处理

当你浏览器中搜索东西的时候，会显示相关内容，如何做到的呢？

### 概括数据

网站用n-gram模型把文章分成许多单词，重复次数较多的单词就提取出来



### 马尔可夫模型

此块以及本章后面的内容不作为重点学习内容，略过



## 穿越网页表单与登录窗口进行抓取

### Python Requests库

`Requests`库就是一个擅长处理复杂的HTTP请求、cookie、header（响应头和请求头）等内容的Python第三方库



### 提交一个基本表单

简单，看代码

```python
import requests

params = {"firstname": "Wu", "lastname": "Vinylon"}

response = requests.post(
    "https://pythonscraping.com/pages/files/processing.php",
    data=params,
)
print(response.text)
```



### 单选按钮、复选框和其他输入

最简单的方法是使用浏览器的inspector，具体看书本P135



### 提交文件和图像

提交图片的话就是用

```python
files = {'uploadFile': open('files/python.png'， 'rb')}
requests.post('url', files=files)
```



### 处理登录和cookie

Requests库跟踪cookie

```python
import requests

params = {"username": "Vinylon", "password": "password"}

response = requests.post(
    "https://pythonscraping.com/pages/cookies/welcome.php",
    data=params,
)
print("Cookie is set to:")
print(response.cookies.get_dict())
print("Going to profile page...")
response = requests.get(
    "http://pythonscraping.com/pages/cookies/profile.php", cookies=response.cookies
)
print(response.text)
```

如果不想换cookie或者一开始就不想有cookie这个变量，可以选择Session

```python
import requests

session = requests.Session()

params = {"username": "Vinylon", "password": "password"}

response = session.post(
    "https://pythonscraping.com/pages/cookies/welcome.php",
    data=params,
)
print("Cookie is set to:")
print(response.cookies.get_dict())
print("Going to profile page...")
response = session.get("http://pythonscraping.com/pages/cookies/profile.php")
print(response.text)
```



### HTTP基本接入认证

在发明cookie前，最常用的是**HTTP基本接入认证**，Requests库有专门的**auth**模块来处理这种情况，看看下面的代码

```python
import requests
from requests.auth import HTTPBasicAuth

session = requests.Session()

auth = HTTPBasicAuth("Vinylon", "password")

response = session.post(
    "http://pythonscraping.com/pages/auth/login.php",
    auth=auth,
)

print(response.text)
```



## 抓取JavaScript

目前网上遇到的客户端语言只有两种`ActionScript`和`JavaScript`，其中ActionScript可以忽略不计，所以本章我们将介绍JavaScript



### JavaScript介绍

作者是前端科班出生，这部分请自己研究——P140



#### 常用JavaScript库

##### jQuery

如果网站使用的jQuery框架，那么抓取数据的时候要非常小心，因为HTML内容是jQuery执行之后才会显示

所以用传统方法抓取，只能获得JavaScript代码运行前的内容



##### Google Analytics

这个是最受欢迎的用户跟踪工具，如何判断页面是否用了这个库，可以观察是否有这样的类似代码：

```javascript
var _gap = _gap || [];

_gap.push(['_setAccount', 'UA-XXXXXX-X']);
_gap.push(['_trackPageview']);
_gap.push(['_gapTrackBounceViaTime', 10]);
_gap.push(['_gapTrackBounceViaScroll', 50]);
_gap.push(['_gapTrackReads', 20, 30]);
_gap.push(['_gapTrackLinkClicks']);
_gap.push(['_gapTrackMaxScroll', 25]);

(function() {
	var gap = document.createElement('script');
	gap.async = true;
	gap.type = 'text/javascript';
	gap.src = '/bower_components/gap/dst/gap.min.js'; // Change, if needed.

	var s = document.getElementsByTagName('script')[0];
	s.parentNode.insertBefore(gap, s);
})();
```

这段代码处理用于跟踪页面访问的Google Analytics的cookies

有时候对于设计用于执行JavaScript处理和处理cookie的爬虫而言会是一个问题

如果你不想让这种网站知道你在抓取它的数据，要确保把这些分析工具的cookie或者所有的cookie关掉



##### Google Maps

Python可以轻松抽取所有位置再google.maps.LatLng()的坐标，生成一组经纬度坐标值



### Ajax和动态HTML

截至目前，我们与Web服务器通信的唯一方式，就是发送**HTTP请求获取新页面**，如果提交表单/从服务器获取新信息，网站页面不需要重新加载的话，那么说明我们所访问的网站很有可能用了Ajax技术

Ajax全程Asynchronous Javascript and XML （异步JavaScript和XML）

DHTM（dynamic）会更改页面内容

有时候页面在不更改URL的情况下会重定向到另一个页面

这些都是因为爬虫没有执行网站的JavaScript脚本，导致和我们在浏览器中看到的完全不一样

**解决方法：**

1.  直接从JavaScript中抓取内容
2. 用python第三方库执行JavaScript



#### 用Selenium执行JavaScript

**功能：**

1. 自动加载网站
2. 获取数据
3. 页面截屏
4. 判断网站做了什么操作



**缺点：**

Selenium自己不带浏览器，需要和第三方浏览器结合才能运行



**处理方式：**

使用`PhantomJS`代替真实浏览器，在后台默默运行



PhantomJS是一个**无头浏览器**，会把网站加载到内存并执行页面上的Javascript，但不会向用户展示页面的图形界面，把Selenium和PhatomJS结合在一起就可以运行一个非常强大的网络爬虫来处理`cookie`、`JavaScript`、`header`以及任何我想做的事情

Selenium是一个在WebDriver上调用的API，WebDriver有点像可以加载网站的浏览器，也可以像BeautifulSoup一样用来查找页面元素，与页面元素进行交互，以及其他动作来运行网络爬虫



看到这一步的问题是什么呢？PhantomJS被Selenium废弃了。。。

所以作者写了一组用Chrome来执行的代码：

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time


chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式运行
chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速（可选）
chrome_options.add_argument("--no-sandbox")  # 在某些情况下以 root 身份运行时需要
chrome_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误

driver_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"

service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://pythonscraping.com/pages/javascript/ajaxDemo.html")

time.sleep(5)
print(driver.find_element("id", "content").text)
driver.quit()
```

driver_path需要下载对应chrome版本的chromedriver，同时记得放在同一级目录下

**注意：**Selenium选择器与BS4的也不同



如果把time.sleep(5)改成1，那么就会失败，但是5的时间又太长了，所以有了以下更优化的代码（Selenium不断检查某个元素是否存在，这里就是id为loadedButton的按钮）

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式运行
chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速（可选）
chrome_options.add_argument("--no-sandbox")  # 在某些情况下以 root 身份运行时需要
chrome_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误

driver_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"

service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://pythonscraping.com/pages/javascript/ajaxDemo.html")

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.ID, "loadedButton"))
    )
finally:
    print(driver.find_element("id", "content").text)
    driver.quit()
```

`WebDriverWait`和`expected_conditions`两个模块组合起来构成了Selenium的**隐式等待**

隐式等待是等DOM某个状态发生后再继续运行代码，有很多种期望条件：

- 弹出提示框
- 一个元素（提示框）被选中
- 页面标题改变，或者文本显示在页面上/某个元素里
- 一个元素DOM可见，或一个元素从DOM消失

大多数期望条件在使用前都需要先指定`等待元素`。元素用**定位器**（注意和**选择器**不同），定位器是抽象的查询语言，用**By对象**表示，可以用于不同场合，包括创建选择器

一个定位器被用来查找ID为loadedButton的按钮：

```python
EC.presence_of_element_located((By.ID, 'loadedButton'))
```

用来创建选择器，配合WebDriver的find_element的函数使用：

```python
print(driver.find_element(By.ID, 'content').text)
```

能不用定位器就别用，因为可以少导入一个模块，但是他在不同应用中有很强的灵活性



下面是定位器通过By对象进行选择的策略：

ID：通过HTML的id属性查找元素

CLASS_NAME：通过class属性查找

CSS_SELECTOR：通过CSS的class、id、tag属性名来查找（#idName、.className、tagName）

LINK_TEXT：通过链接文字查找HTML的< a >标签。如果一个链接的名字是"NEXT"，就可以用(By.LINK_TEXT，"NEXT")来选择

PARTIAL_LINK_TEXT：与LINK_TEXT类似，只是通过部分链接文字来查找

NAME：通过name属性查找HTML标签。这里处理HTML表单非常方便

TAG_NAME：通过标签名称查找HTML标签

XPATH：用XPath表达式选择匹配的元素



#### Selenium的其他webdriver

这里原文是指用Chrome等等。。。不用理会



### 处理重定向

重定向分`客户端重定向`和`服务器重定向`

客户端重定向比较难处理，因为他是浏览器执行JavaScript完成的页面重新跳转，除非我们有工具可以执行JavaScript

Selenium可以执行JavaScript重定向，但这类重定向的主要问题是**如何判断什么时候停止页面执行**

我们这里的处理方式是**监视**DOM中的元素，重复调用，如果抛出StaleElementReferenceException异常，就说明页面已经跳转了

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def waitForLoad(driver):
    elem = driver.find_element("tag name", "html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(0.5)
        try:
            elem == driver.find_element("tag name", "html")
        except StaleElementReferenceException:
            return


chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式运行
chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速（可选）
chrome_options.add_argument("--no-sandbox")  # 在某些情况下以 root 身份运行时需要
chrome_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误

driver_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"

service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://pythonscraping.com/pages/javascript/ajaxDemo1.html")
waitForLoad(driver)
print(driver.page_source)
```

这里每半分钟检查一次，看看html还在不在，时限为10秒



### 关于JavaScript最后提醒

学会了爬取JavaScript，不要忘记HTTP请求和CSS！



## 利用API抓取数据（P152）

我们可以不用理解JavaScript，直接获取数据源：`生成数据的API`

**备注：**作者大多都会，所以不细写了



### API概述

API文档通常将路由或**端点**描述为可以请求的URL，变量参数要么是URL路径，要么是GET请求的参数

淘宝IP地址（http://ip.taobao.com）提供了一个简单易用的API，能将IP地址翻译成实际的物理地址，可以输入以下地址发起一个简单的API请求：

http://ip.taobao.com/service/getIpInfo.php?ip=50.78.253.58



#### HTTP和API

HTTP从服务器获取信息的四种方式（其实有更多）：

- GET
- POST
- PUT
- DELETE



#### 更多关于API响应的介绍

API的重要特性是会返回良好格式的响应，最常见的是XML和JSON



### 解析JSON数据

用json.loads(...)是将json转换为python中的字典



### 无文档的API

作者懂，自己翻P157



### API与其他数据源结合

自己看



### 再说一点API

自己看



## 图像识别与文字处理（含验证码）

如果要爬取文字做成图片的情况，要么我们可以将图像转化为文字（光学字符识别）

可以mark一下，有相关工作需求的时候再细看（包括**验证码**）P167



## 避免抓取陷阱

### 道德规范

你都看这本书了还要什么道德



### 让网络机器人看着像人类用户

#### 修改请求头

我们一直用Requests库创建、发送和接收HTTP请求，HTTP请求头是我们每次向服务器发送请求时，传递的一组属性或配置信息。下面起个字段被大多数浏览器用来`初始化所有网络请求`

- Host: https://www.google.com/
- Connection: keep-alive
- Accept: text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, * / *, q=0.8
- User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/53.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36
- Referrer: https://www.google.com/
- Accept-Encoding: gzip, deflate, sdch
- Accept-Language: en-US, en; q=0.8

这种HTTP请求头更有**人性**，如果在处理一个防爬取的网站，那么请注意一些`不经常使用`的请求头



#### 用JavaScript处理cookie

cookie是双刃剑，正确处理cookie可以避免许多抓取问题。虽然一些行为可以通过关闭并重新连接网站或改变IP地址来伪装，但cookie暴露身份，再多努力也白费

这里主要讲述了使用Selenium和PhamtonJS来处理cookie，想了解可以看书P189



#### 时间是一切

一些网站会组织表单提交或快速和网页交互，我们也应尽量保证页面加载和数据请求最小化，页面访问之间增加几秒间隔

```python
import time
time.sleep(3)
```



### 常见的表单安全措施

为了区分爬虫和人，在表单和登录环节上执行了严格的安全措施

#### 隐含输入字段值

在HTML表单中，“隐含”字段让字段的值对浏览器可见，但是对用户不可见，随着越来越多的网站开始用cookie存储和传递状态变量，隐含字段现在发展出了一个新功能：**阻止爬虫自动提交表单**

用隐含字段阻止网页抓取的方式主要有两种：

1. 表单页面上的一个字段`可以用服务器生成的随机变量填充`，如果提交时这个值不在表单页面上，服务器认为他不是从原始表单页面提交的；绕开这个问题的方法是先抓取随机变量，再提交到表单处理页面
2. 第二种方式是蜜罐，如果表单包含一个具有普通名称的隐含字段，直接提交会中服务器的蜜罐陷阱。服务器会忽略所有隐含字段的真实值，而填写的隐含字段的用户甚至可能被网站封杀



#### 避免蜜罐

如果Web表单一个字段通过CSS被设置成对用户不可见，那么可以认为普通用户访问网站时不能填这个字段，因为它没有显示在浏览器上；如果这个字段被填写了，很可能是机器人干的，因此提交会失效



### 问题检查表

检查表：

- 如果web服务器返回的信息：**空白**、**缺少信息**、**不符合预期**，可能是JavaScript执行有问题
- **POST**请求可以用Chrome的检查工具检查
- 登陆网站检查**Cookie**
- HTTP错误，**403**很可能把你IP当作机器人，不再接受请求



## 用爬虫测试网站

这一章介绍测试的基础知识，以及如何用Python网络爬虫测试各种简单或复杂的网站

按需看P196



## 并行网页抓取

在一些场景中使用并行网页抓取或并行线程/进程仍有一些好处：

- 从多个数据源而不只是一个数据源收集数据
- 收集数据的同时，在已收集到的数据上执行时间更长/更复杂的操作
- 从大型Web服务收集数据，如果已经付费，并且创建多个链接是允许的情况



### 进程与线程

Python既支持多进程（**mutiprocessing**），也支持多线程(**mutithreading**)；多线程可以共享一块内存，多进程不可以

Python的**全局解释锁**（global interpreter lock，GIL）会组织多个线程同时运行同一行代码，GIL确保所有进程共享的内存不会中断



### 多线程抓取

代码：

```python
import _thread
import time


def print_time(threadName, delay, iterations):
    start = int(time.time())
    for i in range(0, iterations):
        time.sleep(delay)
        seconds_elapsed = str(int(time.time()) - start)
        print("{} {}".format(seconds_elapsed, threadName))


try:
    _thread.start_new_thread(print_time, ("Bella", 3, 33))
    _thread.start_new_thread(print_time, ("Echo", 5, 20))
    _thread.start_new_thread(print_time, ("VL", 1, 100))
except:
    print("Error: unable to start thread")

while True:
    pass
```

如果我们要用多线程抓取一个网站时，我们可以使用time.sleep(n)来防止给服务器增加太多负担



#### 竞争条件与队列

我们虽然可以使用列表进行线程间的通信，但列表不是专门为线程通信而设计的，误用很容易导致程序变慢，甚至在竞争条件中产生错误

下面这行代码实际上需要Python重写整个列表：

```python
myList.pop(0)
```

下面这行代码在多线程运行下不能获取列表末尾的元素，甚至可能引发异常：

```python
myList[len(myList)-1]
```



队列是一种类似列表的对象，有先进先出的方法，也有后进后出的方法。队列通过queue.put('My message')从任意县城接收数据，再给调用queue.get()方法的线程发送数据

详细例子可以观察P210



#### threading模块

_thread模块有许多特性

- enumerate: 获取所有活跃线程的列表，无需手动跟踪
- activeCount: 可以获得总线程数
- currentThread: 获取当前线程的名称

例子可以看P212

无论何时，只要不需要共享对象，就不要共享，保存在线程局部内存即可。为了安全地在线程中共享对象，可以使用上一节中的Queue模块



### 多进程抓取

这一块需要的时候自己看P214



### 多进程抓取的另一种方法

这一块需要的时候自己看P219



## 远程抓取

这一块讲述服务器和可变IP，P221 不需要细说



## 网页抓取的法律与道德约束

有没有道德自己知道，P228 不需要细说
