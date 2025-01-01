# -*- coding: utf-8 -*-
# @Time    : 31 12月 2024 11:28 上午
# @Author  : codervibe
# @File    : punchyAutoMaticallyBlockIP.py
# @Project : pythonBasics

# 自动封禁IP
# 安全日志
import re
import subprocess
import time
from collections import defaultdict

# 定义安全日志文件路径
securityLog = '/var/log/secure'
# 定义黑名单文件路径
hostDeny = '/etc/hosts.deny'
# 定义封禁阈值，即密码错误的次数达到多少次后触发封禁
BlockThreshold = 5
# 定义时间窗口（秒）
TimeWindow = 900  # 15分钟

# 定义白名单文件路径
whiteList = '/etc/hosts.allow'


def getDenies():
    """
    读取黑名单文件，将已经封禁的IP地址加载到内存中
    :return: 返回一个字典，键为已封禁的IP地址，值为标记'1'
    """
    deniedDict = {}
    with open(hostDeny, 'r') as f:
        blackIPList = f.readlines()
    for ip in blackIPList:
        group = re.search(r'(\d+\.\d+\.\d+\.\d+)', ip)
        if group:
            deniedDict[group[1]] = '1'
    return deniedDict


def getWhites():
    """
    读取白名单文件，将可信的IP地址加载到内存中
    :return: 返回一个字典，键为可信的IP地址，值为标记'1'
    """
    whiteDict = {}
    with open(whiteList, 'r') as f:
        whiteIPList = f.readlines()
    for ip in whiteIPList:
        group = re.search(r'(\d+\.\d+\.\d+\.\d+)', ip)
        if group:
            whiteDict[group[1]] = '1'
    return whiteDict


def monitor(securityLog):
    """
    监控安全日志，自动封禁可疑IP地址
    :param securityLog: 安全日志文件路径
    """
    # 初始化临时字典，用于记录每个IP的密码错误次数
    tempIp = defaultdict(list)
    # 初始化已封禁IP字典，加载已存在的封禁IP
    deniedDict = getDenies()
    # 初始化白名单IP字典，加载已存在的可信IP
    whiteDict = getWhites()
    # 使用subprocess实时读取安全日志的新增内容
    popen = subprocess.Popen(['tail', '-f', securityLog], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 开始监控日志流
    while True:
        time.sleep(0.1)
        line = popen.stdout.readline().strip().decode('utf-8')
        if line:
            print(line)
            # 搜索无效用户登录尝试的IP地址
            group = re.search(r'Invalid user \w+ from (\d+\.\d+\.\d+\.\d+) port \d+.+user not known', line)
            if group:
                ip = group[1]
                # 检查IP是否在白名单中
                if whiteDict.get(ip):
                    continue
                # 如果找到无效用户且该IP未被封禁，则将其加入黑名单
                if not deniedDict.get(ip):
                    subprocess.getoutput(f'echo \'sshd:{ip}\' >> {hostDeny}')
                    deniedDict[ip] = '1'
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print(f'{time_str} 加入黑名单 {ip}')
                    print(f'{time_str} >>>> add ip:{ip} to host.deny for invalid user 用户名无效')
                continue
            # 搜索有效用户密码错误的IP地址
            group = re.search(
                r'Failed password for invalid user \w+ from (\d+\.\d+\.\d+\.\d+) port \d+.+user not known', line)
            if group:
                ip = group[1]
                # 检查IP是否在白名单中
                if whiteDict.get(ip):
                    continue
                # 统计该IP的密码错误次数
                current_time = time.time()
                tempIp[ip].append(current_time)
                # 移除时间窗口外的记录
                tempIp[ip] = [t for t in tempIp[ip] if current_time - t <= TimeWindow]
                if len(tempIp[ip]) > BlockThreshold and not deniedDict.get(ip):
                    del tempIp[ip]
                    subprocess.getoutput(f'echo \'sshd:{ip}\' >> {hostDeny}')
                    deniedDict[ip] = '1'
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print(f'{time_str} 加入黑名单 {ip}')
                    print(
                        f'{time_str} >>>> add ip:{ip} to host.deny for invalid password 密码无效次数超过阈值 自动封禁')


if __name__ == '__main__':
    # 程序入口，启动监控安全日志的功能
    monitor(securityLog)
