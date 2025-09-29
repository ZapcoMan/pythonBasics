# -*- coding: utf-8 -*-
# @Time    : 12 2月 2025 11:02下午
# @Author  : codervibe
# @File    : mongoScan.py
# @Project : pythonBasics
import socket

import pymongo
from pymongo import errors


def scan_port(ip):
    """
    检查指定 IP 的 MongoDB 端口是否开放。

    :param ip: 需要扫描的 IP 地址
    """
    # 创建一个TCP/IP套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 设置套接字操作的超时时间，单位为秒。这里设置为0.3秒。
    s.settimeout(0.3)  # 设置超时时间

    # 尝试连接到指定IP地址和端口的服务器。这里的目标是MongoDB的默认端口27017。
    try:
        s.connect((ip, 27017))  # 尝试连接到 MongoDB 默认端口 27017
        # 如果连接成功，输出提示信息并关闭套接字，然后调用检查MongoDB连接的函数。
        print(f"[+] {ip} 的 27017 端口上有 MongoDB 服务")
        s.close()
        check_mongo_connect(ip)
    # 如果连接失败（例如，由于目标端口未开放），捕获socket.error异常并输出提示信息。
    except socket.error:
        print("[-] 27017 端口已关闭")
        return


def check_mongo_connect(ip):
    """
    检查指定 IP 的 MongoDB 是否存在未授权访问问题。

    :param ip: 需要检查的 IP 地址
    """

    # 打印正在尝试连接的IP地址
    print(f"[+] {ip} 正在尝试链接......")
    try:
        # 创建MongoDB客户端连接，指定IP地址、端口号和超时时间
        client = pymongo.MongoClient(ip, 27017, socketTimeoutMS=3000)
        # 获取数据库名称列表
        dbnames = client.list_database_names()
        # 检查服务器信息和数据库列表是否非空且长度大于0
        if client.server_info() and dbnames and len(dbnames) > 0:
            # 如果条件满足，说明存在未授权访问
            print(f"[+] {ip} 存在未授权访问")
        # 关闭客户端连接
        client.close()
    except pymongo.errors.ConnectionFailure:
        # 如果连接失败，打印不存在未授权访问的信息
        print(f"[-] {ip} 不存在未授权访问")
        return