# -*- coding: utf-8 -*-
# @Time    : 28 12月 2024 10:21 上午
# @Author  : codervibe
# @File    : 隐写内容字符提取.py
# @Project : pythonBasics
"""
使用kali 的 steghide  工具提取  提取命令 ：steghide extract -sf hack.jpg
"""
ext_Infor = "Perhaps you see this and wonder what the fuck is going on, What is this bullshit. Well, the solution is Right in front of your eyes, you just have to look closer. Just follow the numbers and you will find the answer. Did you find it?"
index = ["0", "4", "6", "16", "29", "72", "78", "99", "161", "155", "157", "181", "/", "163", "144", "104", "217", "3",
         "227", "182", "104"]

for msg in index:
    if msg == '/':
        print("/", end='')
    else:
        print(ext_Infor[int(msg)], end='')
print()