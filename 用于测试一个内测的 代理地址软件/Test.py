# -*- coding: utf-8 -*-
# @Time    : 09 3月 2025 9:25 上午
# @Author  : codervibe
# @File    : Test.py
# @Project : pythonBasics
import requests
import threading
import random

# 代理列表
proxies = [
    'socks5://127.0.0.1:33333',
    # 添加更多的代理
]

# 目标URL
target_url = 'http://baidu.com'


# 访问网站的函数
def visit_website(): 
    try:
        # 随机选择一个代理
        proxy = random.choice(proxies)
        response = requests.get(target_url, proxies={"http": proxy, "https": proxy})
        print(f"Visited {target_url} using proxy {proxy}, status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Failed to visit {target_url} using proxy {proxy}, error: {e}")


# 线程列表
threads = []

# 创建并启动多个线程
for _ in range(10):  # 创建10个线程
    thread = threading.Thread(target=visit_website)
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()
