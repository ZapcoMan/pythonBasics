# -*- coding: utf-8 -*-
# @Time    : 09 2月 2025 5:17 下午
# @Author  : codervibe
# @File    : 钓鱼链接制裁.py
# @Project : pythonBasics
import requests

url = "https://figystre.pro/api/check-credentials"
headers = {
    "Host": "figystre.pro",
    "Content-Length": "60",
    "Sec-Ch-Ua-Platform": "Windows",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Sec-Ch-Ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "Content-Type": "application/json",
    "Sec-Ch-Ua-Mobile": "?0",
    "Origin": "https://figystre.pro",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://figystre.pro/login/home?ref=https%3A%2F%2Fxigemazhuti.com%2Fvote",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Priority": "u=1, i"
}
data = {
    "username": "你是煞笔吗?",
    "password": "牛逼格拉斯"
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.json())
