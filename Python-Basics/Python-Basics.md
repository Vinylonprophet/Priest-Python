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

