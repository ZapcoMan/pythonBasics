# -*- coding: utf-8 -*-
# @Time    : 30 12月 2024 6:24 下午
# @Author  : codervibe
# @File    : getDomainInfo.py
# @Project : pythonBasics
from whoisInfoCollect import is_registered
import whois
domain = input("请输入域名：")
if is_registered(domain=domain):
    whois_info = whois.whois(domain)
    print(f"whois_info：{whois_info}")
    print(f"whois_info.registrar:{whois_info.registrar}")
    print(f"whois serrver:{whois_info.serrver}")

