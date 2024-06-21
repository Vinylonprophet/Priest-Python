from pathlib import Path

path = Path("pi_digital.txt")
contents = path.read_text()
# print(contents.rstrip())
print(contents)

lines = contents.splitlines()
for line in lines:
    print(line.lstrip())


pi_string = ""
for line in lines:
    pi_string += line.lstrip()

print(pi_string)
print(len(pi_string))

print("=======================================================================")

pi_million_contents = Path("pi_million_digits.txt").read_text()
# pi_million_contents_lines = pi_million_contents.splitlines()
birthday = input("请输入你的生日：")
print(f"你的生日是{birthday}")
if birthday in pi_million_contents:
    print("Your birthday appears in the first million digits of pi!")
else:
    print("Your birthday does not appear in the first million digits of pi!")
