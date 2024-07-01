from mpmath import mp

# 设置计算的精度
mp.dps = 1000002  # 小数点后 100 万位 + 2 位，包含 "3."
pi = str(mp.pi)

# 将结果写入文件
with open('pi_million_digits.txt', 'w') as f:
    f.write(pi)

print("圆周率小数点后 100 万位已写入文件 pi_million_digits.txt")
