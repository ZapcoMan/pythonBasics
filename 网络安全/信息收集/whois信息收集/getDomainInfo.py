# -*- coding: utf-8 -*-
# @Time    : 30 12月 2024 6:24 下午
# @Author  : codervibe
# @File    : getDomainInfo.py
# @Project : pythonBasics
"""
从whoisInfoCollect模块导入is_registered函数，用于检查域名是否已注册。
"""
import re

import whois

from whoisInfoCollect import is_registered


def validate_domain(domain):
    """
    验证域名格式是否正确。
    """
    pattern = r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
    return re.match(pattern, domain) is not None


def get_whois_info(domain):
    """
    获取并打印域名的whois信息。
    """
    try:
        whois_info = whois.whois(domain)
        print(f"whois_info: {whois_info}")

        # 确保字段存在再打印
        if hasattr(whois_info, 'registrar'):
            print(f"Registrar: {whois_info.registrar}")
        if hasattr(whois_info, 'server'):
            print(f"Whois Server: {whois_info.whois_server}")
    except Exception as e:
        print(f"获取whois信息时发生错误: {e}")


domain = input("请输入域名：").strip()

# 检查输入是否为空或无效域名
if not domain or not validate_domain(domain):
    print("无效的域名，请重新输入。")
    # return

try:
    if is_registered(domain=domain):
        get_whois_info(domain)
    else:
        print("该域名未注册。")
except Exception as e:
    print(f"检查域名注册状态时发生错误: {e}")
