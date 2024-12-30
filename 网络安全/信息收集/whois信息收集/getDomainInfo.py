# -*- coding: utf-8 -*-
# @Time    : 30 12月 2024 6:24 下午
# @Author  : codervibe
# @File    : getDomainInfo.py
# @Project : pythonBasics
"""
从whoisInfoCollect模块导入is_registered函数，用于检查域名是否已注册。
"""
from whoisInfoCollect import is_registered
import whois

"""
获取用户输入的域名。
"""
domain = input("请输入域名：")

"""
检查域名是否已注册，如果已注册，则获取并打印whois信息。
"""
if is_registered(domain=domain):
    """
    使用whois库获取域名的whois信息。
    """
    whois_info = whois.whois(domain)

    """
    打印完整的whois信息。
    """
    print(f"whois_info：{whois_info}")

    """
    打印域名注册商信息。
    """
    print(f"whois_info.registrar:{whois_info.registrar}")

    """
    打印whois服务器信息，注意这里有一个拼写错误'serrver'，应该为'server'。
    """
    print(f"whois serrver:{whois_info.serrver}")
