# -*- coding: utf-8 -*-
# @Time    : 30 12月 2024 4:19 下午
# @Author  : codervibe
# @File    : scan_directories.py
# @Project : pythonBasics
"""
该脚本用于扫描指定网站的敏感目录和文件路径。通过多线程和自定义字典文件实现高效扫描。
"""
from multiprocessing import Queue
import random
import argparse

import dirPathScan


def start(url, count, filePath):
    """
    敏感路径扫描的启动函数
    :param url: 需要扫描的基础URL
    :param count: 线程数量
    :param filePath: 字典文件路径，用于扫描敏感路径
    """
    # 初始化任务队列
    queue = Queue()
    # 打开字典文件，将待扫描的路径加入队列
    with open(filePath, "r") as file:
        for i in file:
            queue.put(url + i.rstrip('\n'))
    # 初始化线程列表
    threads = []
    # 根据参数初始化线程数量
    threading_count = int(count)
    for i in range(threading_count):
        threads.append(dirPathScan.DirPathScan(queue))
    # 启动所有线程
    for t in threads:
        t.start()
    # 等待所有线程完成任务
    for t in threads:
        t.join()


# 创建 ArgumentParser 对象，用于解析命令行参数
parser = argparse.ArgumentParser(description='敏感目录扫描工具')

# 添加命令行参数，包括目标URL、文件路径和线程数量
parser.add_argument('--url', type=str, required=True, help='目标URL')
parser.add_argument('--filePath', type=str, required=True, help='文件路径')
parser.add_argument('--count', type=int, required=True, help='计数值')

# 解析命令行参数
args = parser.parse_args()

# 使用解析后的参数
url = args.url
filePath = args.filePath
count = args.count

# 调用启动函数开始扫描
start(url=url, count=count, filePath=filePath)
