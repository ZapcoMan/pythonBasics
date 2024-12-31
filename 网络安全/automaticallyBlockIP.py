# -*- coding: utf-8 -*-
# @Time    : 31 12月 2024 8:21 上午
# @Author  : codervibe
# @File    : automaticallyBlockIP.py
# @Project : pythonBasics
# 自动封禁IP
# 安全日志
import re
import subprocess
import time

# 定义安全日志文件路径
securityLog = '/var/log/secure'
# 定义黑名单文件路径
hostDeny = '/etc/hosts.deny'
# 定义封禁阈值，即密码错误的次数达到多少次后触发封禁
BlockThreshold = 5

def getDenies():
    """
    读取黑名单文件，将已经封禁的IP地址加载到内存中
    :return: 返回一个字典，键为已封禁的IP地址，值为标记'1'
    """
    deniedDict = {}
    blackIPList = open(hostDeny, 'r').readlines()
    for ip in blackIPList:
        group = re.search(r'(\d+\.\d+\.d+\.\d+)', ip)
        if group:
            deniedDict[group[1]] = '1'
    return deniedDict

def monitor(securityLog):
    """
    监控安全日志，自动封禁可疑IP地址
    :param securityLog: 安全日志文件路径
    """
    # 初始化临时字典，用于记录每个IP的密码错误次数
    tempIp = {}
    # 初始化已封禁IP字典，加载已存在的封禁IP
    deniedDict = getDenies()
    # 使用subprocess实时读取安全日志的新增内容
    popen = subprocess.Popen('tail -f ' + securityLog, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # 开始监控日志流
    while True:
        time.sleep(0.1)
        line = popen.stdout.readline().strip()
        if line:
            print(line)
            # 搜索无效用户登录尝试的IP地址
            group = re.search('Invalid user \w+ from (\d+\.\d+\.\d+\.\d+) port \d+.+user not known', str(line))
            # 如果找到无效用户且该IP未被封禁，则将其加入黑名单
            if group and not deniedDict.get(group[1]):
                subprocess.getoutput('echo \'sshd:{}\' >> {}'.format(group[1], hostDeny))
                deniedDict[group[1]] = '1'
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                print('{} 加入黑名单 {}'.format(time_str, group[1]))
                print('{} >>>> add ip:{} to host.deny for invalid user'.format(time_str, group[1]))
                continue
            # 搜索有效用户密码错误的IP地址
            group = re.search('Failed password for invalid user \w+ from (\d+\.\d+\.\d+\.\d+) port \d+.+user not known', str(line))
            if group:
                ip = group[1]
                # 统计该IP的密码错误次数
                if not tempIp.get(ip):
                    tempIp[ip] = 1
                else:
                    tempIp[ip] += 1
                # 如果密码错误次数超过阈值且该IP未被封禁，则将其加入黑名单
                if tempIp[ip] > BlockThreshold and not deniedDict.get(ip):
                    del tempIp[ip]
                    subprocess.getoutput('echo \'sshd:{}\' >> {}'.format(ip, hostDeny))
                    deniedDict[ip] = '1'
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print('{} 加入黑名单 {}'.format(time_str, ip))
                    print('{} >>>> add ip:{} to host.deny for invalid password'.format(time_str, ip))

if __name__ == '__main__':
    # 程序入口，启动监控安全日志的功能
    monitor(securityLog)
