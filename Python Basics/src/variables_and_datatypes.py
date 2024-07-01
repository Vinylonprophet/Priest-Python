msg = 'hello py'
print(msg.title())
print(msg.upper())
print(msg.lower())

first_name = "vl"
last_name = "Wu"
full_name = f"{first_name}-{last_name}"
print(full_name)

favorite_lang = ' JavaScript '
# strip 剥夺
print(f"{favorite_lang.rstrip()} is my favorite language")
print(f"{favorite_lang.lstrip()} is my favorite language")
print(f"{favorite_lang.strip()} is my favorite language")

prefixUrl = 'https://www.baidu.com'
print(prefixUrl.removeprefix('https://'))
print(prefixUrl.removesuffix('//www.baidu.com'))

universe_age = 14_000_000_000
print(universe_age)

x1, y1, z1 = 54, 1, 88
print(f"{x1}{y1}{z1}")
print(x1 + y1 + z1)

MAX_CONTANTS = 5000000
print(MAX_CONTANTS)