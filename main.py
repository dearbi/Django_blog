import math

a=int(input("请输入一个自然数："))
for i in range(2,a):
    if a%i==0:
        print("这不是一个素数")
        break
else:
    print(f"{a}是素数")