# Python-Basics

## 变量和简单数据类型

### 变量/字符串

```python
msg = 'Hello PY'
print(msg)
```

### 修改字符串大小写

```python
msg = 'hello py'
print(msg.title())
print(msg.upper())
print(msg.lower())
```

### 字符串中使用变量

左引号前加f

```python
first_name = "vl"
last_name = "Wu"
full_name = f"{first_name}-{last_name}"
print(full_name)
```

### 制表符和换行符

| 符号 | 效果 |
| --- | ----------- |
| Header | 空格 |
| Paragraph | 换行 |

### 删除空格

rstrip 删除右端空格

lstrip  删除左端空格

strip 删除两边空格

```python
favorite_lang = ' JavaScript '
# strip 剥夺
print(f"{favorite_lang.rstrip()} is my favorite language")
print(f"{favorite_lang.lstrip()} is my favorite language")
print(f"{favorite_lang.strip()} is my favorite language")
```

### 删除前缀&后缀

removePrefix

removeSuffix

```python
prefixUrl = 'https://www.baidu.com'
print(prefixUrl.removeprefix('https://'))
print(prefixUrl.removesuffix('//www.baidu.com'))
```

### 数字运算

最基本的加减乘除之外，附上乘方即两个乘号(**)

### 浮点数

浮点数记得注意最后的小数点

### 数字中的下划线

帮助读取数字，不会打印下划线

```python
universe_age = 14_000_000_000
print(universe_age)
```

### 同时给多个变量赋值

```python
x1, y1, z1 = 54, 1, 88
print(f"{x1}{y1}{z1}")
print(x1 + y1 + z1)
```

### 常量

```python
MAX_CONTANTS = 5000000
print(MAX_CONTANTS)
```

**总结：**python就应该**避繁就简**。



## 列表简介

### 访问列表元素

索引-1代表的是列表中最后一个元素

```python
lists = ["list0", "list1", "list2", "list3"]
print(lists)
print(lists[0])
print(lists[-1])
```

### 添加/插入元素

```python
lists = ["list0", "list1", "list2", "list3"]
lists.append("list5")
lists.insert(4, "list4")
print(lists)
```

### 删除元素

```python
lists = ["list0", "list1", "list2", "list3", "list4", "list5"]
del lists[-1]
lists.pop()
lists.pop(0)
lists.remove("list2")
print(lists)
```

### 正/反排序

| 方法 | 效果 |
| --- | ----------- |
| sort | 根据字母排序 |
| sorted | 临时排序 |
| reverse | 颠倒 |
| sort(reverse=True) | 先sort再reverse |

```python
alphabet = ["b", "d", "e", "g", "h", "a", "u", "z", "o", "l", "p"]
print(sorted(alphabet))
print(alphabet)
alphabet.sort()
alphabet.sort(reverse=True)
alphabet.reverse()
print(alphabet)
```



## 操作列表

### 遍历列表

```python
personList = ["vl", "coconut", "cardinal"]
for person in personList:
    print(person)
print("loop end")
```

### 避免缩进/冒号错误

就是要非常注意的意思

### 创建数值列表

使用range()

```python
for value in range(1, 5):
    print(value)
# 不会输出5
```

list()转列表

```python
rangeList = list(range(1, 6))
for value in rangeList:
    print(value)
```

range()带步长

```python
rangeListStep = list(range(0, 11, 2))
for value in rangeListStep:
    print(value)
```

python自带的几个简单函数

```python
rangeListStep2 = list(range(0, 101, 2))
print(min(rangeListStep2))
print(max(rangeListStep2))
print(sum(rangeListStep2))
```

列表推导式

```python
rangeListStep3 = [value**3 for value in range(1, 12, 2)]
print(rangeListStep3)
```

### 使用列表的一部分

切片

```python
sliceList = ["vl", "max", "bella", "nick"]
print(f"{sliceList[:1]} are 00")
print(f"{sliceList[1:]} are 95")
print(f"{sliceList[-3:]} are 95")
print(f"{sliceList[1:3]} are girls")
for girl in sliceList[1:3]:
    print(f"{girl} is girl")
```

复制

注意：一个是复制，一个是副本赋值

```python
sliceList1 = sliceList[:]
sliceList2 = sliceList
sliceList1.append("xiuhui")
sliceList1.append("colin")
print(f"Digital's framework team: {sliceList1}")
print(f"Digital's framework team: {sliceList2}")
```

### 元组

元组类似于列表，但是不可以给元组的元素赋值

```python
dimensions = (200, 50)
print(dimensions[0])
print(dimensions[1])
# dimensions[1] = 250
```

同样可以循环

```python
for dimension in dimensions:
    print(dimension)
```

**注意：**虽然不可以给元素赋值，但是可以直接修改元组的变量



## if语句

### 简单使用

**注意：**

1. 在python中没有`===`的存在
2. 想比较两个变量的类型和值是否相等，可以使用`is`关键字来进行身份比较
3. python中没有`else if`只有`elif`

```python
for role in ["vl", "bella", "max", "nick", "colin", "xiuhui"]:
    if role == "xiuhui":
        print(f"{role} is leader")
    elif role != "xiuhui":
        print(f"{role} is aide")
```

### 检查多个条件

and相当于&&

or相当于||

```python
age_vl = 24
if age_vl >= 18 and age_vl < 25:
    print("VL is in the prime of their youth.")
```

### 检查特定的值是否在列表中

使用in

```python
roles = ["VL", "Maggie", "Auggie", "Wency"]
print(f"Has VL resigned? ==>", "VL" in roles)
print(f"Maggie has not resigned. ==>", "Maggie" not in roles)
```

### 测试多个条件

`if-if`不会跳

`if-elif-else`会跳

```python
roles = ["VL", "Maggie", "Auggie", "Wency"]
if "VL" in roles:
    print("VL has resigned.")
if "Auggie" in roles:
    print("Auggie has resigned.")
```

### 确定列表为非空

```python
personlist = []
if personlist:
    for person in personlist:
        print(f"The {person} exists.")
else:
    print("The person does not exist.")
```



## 字典

类似于JavaScript中的对象

访问方式类似于JavaScript中的属性访问表达式

### 简单语法

```python
citi = {"department": {"icg", "gcg", "pbwm"}, "staff": {"vl", "bella", "max", "nick"}}
print(citi["department"])
```

### 使用字典

1. 修改

2. 添加

3. 删除

   ```python
   del citi["department"]
   print(citi)
   ```

4. 访问

5. 创建

### 字典排序

按键排序

```python
my_dict = {'b': 3, 'a': 1, 'c': 2}

# 按键排序
sorted_keys = sorted(my_dict.keys())

for key in sorted_keys:
    print(f'{key}: {my_dict[key]}')
```

按值排序

```python
sorted_items = sorted(my_dict.items(), key=lambda x: x[1])
for key, value in sorted_items:
    print(f'{key}: {value}')
```

**注意：**以上皆不会改变原字典顺序

### get访问值

可用于错误处理，提供一个默认值，类似于lodash库中的get

```python
poinit_value = citi.get("vl", "VL has been left")
poinit_value1 = citi.get("staff", "u can get right?")
print(poinit_value)
print(poinit_value1)
```

### 遍历字典

```python
citi1 = {"department": {"icg", "gcg", "pbwm"}, "staff": {"vl", "bella", "max", "nick"}}
for key, value in citi1.items():
    print(f"{key}: {value}\n")
```

### 熟悉items()，key()，values()

| 方法       | 描述                                                         |
| ---------- | ------------------------------------------------------------ |
| `items()`  | 返回包含字典所有键值对的视图。每个元素是一个包含键和值的元组。 |
| `keys()`   | 返回包含字典所有键的视图。                                   |
| `values()` | 返回包含字典所有值的视图。                                   |

### 剔除重复项set

```python
citi2 = {
    "department": {"icg", "gcg", "pbwm"},
    "staff": {"vl", "bella", "max", "nick"},
    "staff": {"xiuhui", "colin"},
}
citi3 = {"a": "a", "b": "b", "b": "b"}
for key in set(citi2.keys()):
    print(key)
for value in set(citi3.values()):
    print(value)
```

### 嵌套

多个字典存储在列表中或者列表存储在字典中称之为`嵌套`

```python
pizza = {"crust": "thick", "toppings": ["mushrooms", "extra cheese"]}
print(f"Your ordered a {pizza['crust']}-crust pizza with the following toppings:")
for topping in pizza["toppings"]:
    print(f"\t{topping}")
```



## 函数

### 定义函数

使用def定义

name是形参，VL是实参（针对没有学过编程语言的同学）

```python
def greet_user(name):
    print(f"Hello! {name} is greeting!")


greet_user("VL")
```

传两个参数

**注意：**如果是关键字形参的话顺序就无关紧要了

```python
def greet_user(name, adjective):
    print(f"Hello! {name} is {adjective}!")


greet_user("VL", "greeting")
```

默认形参

```python
def greet_user1(name, adjective="amazing"):
    print(f"Hello! {name} is {adjective}!")


greet_user1("VL")
```

### 返回值

return返回

```python
def greet_user2(name, adjective="amazing"):
    return name


print(greet_user2("VL"))
```

while和input结合

```python
while True:
    print("\nPlease tell me your name:")
    print("(enter 'q' at any time to quit.)")

    f_name = input("First Name: ")
    if f_name == "q":
        break

    l_name = input("Last Name: ")
    if l_name == "q":
        break

    print(f"\nHello, {get_formatted_name(f_name, l_name)}")
```

### 传递列表

函数中修改列表很简单，但是如果想禁止函数修改列表，就请注意传递列表的副本给函数

```\
function_name(list_name[:])
```

### 传递任意数量的实参

使用星号(*)创建一个元组，多用于 *args这样的名字

```python
def make_pizza(*toppings):
    print(toppings)


make_pizza("pepperoni")
make_pizza("pepperoni", "mushrooms", "green peppers")
```

使用任意数量关键字实参

```python
def build_profile(first, last, **user_info):
    user_info["first_name"] = first
    user_info["last_name"] = last
    return user_info


user_profile = build_profile("VL", "Wu", age="18", career="student")
print(user_profile)
```

### 导入模块

导入整个模块

```python
import module_name

module_name.function_name()
```

从模块中导入方法

```python
from module_name import function_name1, function_name2, function_name3
```

用as给函数指定别名

```python
from module_name import function_name as func
```

用as给模块指定别名

```python
import module_name as xxx
```

导入所有函数**（非常不建议使用！！！）**

```python
from module_name import *
```



## 类

用`类`来创建对象的过程叫`实例化`

### 创建和使用

```python
# __init__是必不可少的一个特殊的方法
# 每次创建新实例，都会自动执行


class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def sit(self):
        print(f"{self.name} is sitting now.")

    def roll(self):
        print(f"{self.name} is rolling.")


puppy1 = Dog("Smith", "3")
puppy1.sit()
puppy1.roll()

puppy2 = Dog("Lucy", "2")
puppy2.sit()
puppy2.roll()
```

### 继承

不是所有类都要从头编写，如果是基于一个现有版本的类，可以使用`继承`（当一个类继承另一个类时，将自动获得后者所有的属性和方法，这时原有的类称为`父类`，新创建的类称为`子类`）

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def sit(self):
        print(f"{self.name} is sitting now.")

    def roll(self):
        print(f"{self.name} is rolling.")


puppy1 = Dog("Smith", "3")
puppy1.sit()
puppy1.roll()

puppy2 = Dog("Lucy", "2")
puppy2.sit()
puppy2.roll()


class WorkingDog(Dog):
    def __init__(self, name, age, task):
        super().__init__(name, age)
        self.task = task

    def perform_task(self):
        print(f"{self.name} is performing {self.task}.")


puppy3 = WorkingDog("Alice", 6, "code")
puppy3.perform_task()
```

如果将大型类拆分成多个协同工作的小类，这种方法称之为`组合`

```python

class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def get_descriptive_name(self):
        long_name = f"{self.year} f{self.make} f{self.model}"
        return long_name.title()

    def read_odometer(self):
        print(f"This car has {self.odometer_reading} miles on it.")

    def update_odometer(self, mileage):
        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("You can't roll back an odometer!")

    def increment_odometer(self, miles):
        self.odometer_reading += miles


class Battery:
    def __init__(self, battery_size=40):
        self.battery_size = battery_size

    def describe_battery(self):
        print(f"This car has a {self.battery_size}-kWh battery.")


class ElectricCar(Car):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)
        self.battery = Battery()


my_leaf = ElectricCar("nissan", "leaf", 2024)
print(my_leaf.get_descriptive_name())
my_leaf.battery.describe_battery()
```

### 导入类

几种方式：

1. 导入单个类：创建一个含有Car的car.py文件

   ```python
   from car import Car
   ```

2. 一个模块存储/导入多个类/：创建一个含有Car，ElectricCar，Battery的car.py文件

   ```python
   from car import Car, ElectricCar
   ```

3. 导入整个模块

   ```python
   import car
   car.Car()
   ```

4. 导入模块中所有的类

   ```python
   from car import *
   ```

5. 使用别名

   ```python
   from electric_car import ElectricCar as EC
   ```



## 文件和异常

### 读取文件

可以一次性读取，也可以逐行读取

创建一个名为`pi_digital`文本文件

```txt
3.1415926535
    8979323846
    2643383279
    5028841971
    6939937510
    5820974944
    5923078164
    0628620899
    8628034825
    3421170679
```

使用pathlib的库，用Path对象来`核实`是否存在，`读取`内容，数据`写入`

```python
from pathlib import Path

path = Path('pi_digital.txt')
contents = path.read_text()
print(contents)
```

读取完的结果会多一个空行，因为read_text()在文件末尾会返回一个空字符串，会被显示为一个空行，可以使用`rstrip()`解决这个问题

相对路径和绝对路径的两种读取方式

```python
path = Path('text_files/filename.txt')
path = Path('/home/eric/data_files/text_files/filename.txt')
```

访问文件中的各行

```python
lines = contents.splitlines()
for line in lines:
    print(line.lstrip())
```

使用内容

```python
pi_string = ""
for line in lines:
    pi_string += line.lstrip()

print(pi_string)
print(len(pi_string))
```

判断生日是否在圆周率后小数点100w位

```python
pi_million_contents = Path("pi_million_digits.txt").read_text()
# pi_million_contents_lines = pi_million_contents.splitlines()
birthday = input("请输入你的生日：")
print(f"你的生日是{birthday}")
if birthday in pi_million_contents:
    print("Your birthday appears in the first million digits of pi!")
else:
    print("Your birthday does not appear in the first million digits of pi!")
```

如果没有100w小数点的文件可以使用以下代码（稍后会介绍写入文件）

```python
from mpmath import mp

# 设置计算的精度
mp.dps = 1000002  # 小数点后 100 万位 + 2 位，包含 "3."
pi = str(mp.pi)

# 将结果写入文件
with open('pi_million_digits.txt', 'w') as f:
    f.write(pi)

print("圆周率小数点后 100 万位已写入文件 pi_million_digits.txt")
```

