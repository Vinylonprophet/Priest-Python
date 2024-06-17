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



