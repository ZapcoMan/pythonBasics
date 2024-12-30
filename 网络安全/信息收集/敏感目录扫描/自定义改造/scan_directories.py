# -*- coding: utf-8 -*-
# @Time    : 30 12月 2024 4:19 下午
# @Author  : codervibe
# @File    : scan_directories.py
# @Project : pythonBasics
from multiprocessing import Queue
import random
import argparse

import dirPathScan




def start(url, count, filePath):
    """
    敏感路径扫描的启动函数
    :param url: 需要扫描的基础URL
    :param count: 线程数量
    :param ext: 扩展名，用于选择字典文件
    """
    queue = Queue()
    # 指定字典文件的完整路径
    with open(filePath, "r") as file:
        for i in file:
            queue.put(url + i.rstrip('\n'))
    # 多线程
    threads = []
    threading_count = int(count)
    for i in range(threading_count):
        threads.append(dirPathScan.DirPathScan(queue))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser(description='敏感目录扫描工具')

# 添加命令行参数
parser.add_argument('--url', type=str, required=True, help='目标URL')
parser.add_argument('--filePath', type=str, required=True, help='文件路径')
parser.add_argument('--count', type=int, required=True, help='计数值')

# 解析命令行参数
args = parser.parse_args()

# 使用解析后的参数
url = args.url
filePath = args.filePath
count = args.count

# 示例输出
print(f"URL: {url}")
print(f"FilePath: {filePath}")
print(f"Count: {count}")

start(url=url, count=count, filePath=filePath)
