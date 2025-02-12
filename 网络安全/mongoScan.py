# -*- coding: utf-8 -*-
# @Time    : 12 2月 2025 11:02下午
# @Author  : codervibe
# @File    : mongoScan.py
# @Project : pythonBasics
import socket

import pymongo
from pymongo import errors


def scan_port(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout = 0.3
    try:
        s.connect((ip, 27017))
        print(f"[+] {ip} has mongo server on 27017 ")
        s.close()
    except socket.error:
        print("[-] 27017 is close")
        return


def check_mongo_connect(ip):
    try:
        client = pymongo.MongoClient(ip, 27017, socketTimeoutMS=3000)
        dbnames = client.list_database_names()
        if client.server_info() and dbnames and bool(dbnames) and len(dbnames) > 0:
            print("f[+] {ip} 存在 未授权访问 ")
        client.close()
    except pymongo.errors.ConnectionFailure:
        print("f[+] {ip} 不存在 未授权访问 ")
        return
