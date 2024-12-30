# -*- coding: utf-8 -*-
# @Time    : 30 12月 2024 10:20 上午
# @Author  : codervibe
# @File    : dirPathScan.py
# @Project : pythonBasics
"""
敏感路径扫描
"""
import random
import threading
from multiprocessing import Queue

import requests

# 定义 User-Agent 列表，用于模拟不同的浏览器请求
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/14.TG 短信轰炸接口.2 Safari/605.TG 短信轰炸接口.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
]
# 构造请求头部，包括随机选择一个User-Agent和Cookie信息
headers = {
    'User-Agent': random.choice(user_agents),
}


# statusCodeList = ['200', '304', '302']


class DirPathScan(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        # 获取队列中的Url
        while not self.queue.empty():
            url = self.queue.get()
            try:
                res = requests.get(url=url, headers=headers)

                if res.status_code == 200:
                    print(f"{url} 存在敏感路径")
                if res.status_code == 403:
                    print(f"{url} 存在敏感路径")
                if res.status_code == 404:
                    print(f"{url} 存在敏感路径")
            except Exception as e:
                pass


def start(url, count, ext):
    queue = Queue()
    # 打开扫描用的字典
    file = open('%s.txt' % ext, "r")
    for i in file:
        queue.put(url + i.rstrip('\n'))
    # 多线程
    threads = []
    threading_count = int(count)
    for i in range(threading_count):
        threads.append(DirPathScan(queue))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    url = 'https://www.baidu.com'
    ext = 'PHP'
    count = 16
    start(url=url, count=count, ext=ext)
