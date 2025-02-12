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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3)  # 设置超时时间
    try:
        s.connect((ip, 27017))  # 尝试连接到 MongoDB 默认端口 27017
        print(f"[+] {ip} 的 27017 端口上有 MongoDB 服务")
        s.close()
        check_mongo_connect(ip)
    except socket.error:
        print("[-] 27017 端口已关闭")
        return


def check_mongo_connect(ip):
    """
    检查指定 IP 的 MongoDB 是否存在未授权访问问题。

    :param ip: 需要检查的 IP 地址
    """

    print(f"[+] {ip} 正在尝试链接......")
    try:
        client = pymongo.MongoClient(ip, 27017, socketTimeoutMS=3000)  # 创建 MongoDB 客户端连接
        dbnames = client.list_database_names()  # 获取数据库名称列表
        if client.server_info() and dbnames and len(dbnames) > 0:  # 检查服务器信息和数据库列表
            print(f"[+] {ip} 存在未授权访问")
        client.close()
    except pymongo.errors.ConnectionFailure:
        print(f"[-] {ip} 不存在未授权访问")
        return
