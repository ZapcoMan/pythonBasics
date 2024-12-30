# -*- coding: utf-8 -*-
# @Time    : 30 12月 2024 5:02 下午
# @Author  : codervibe
# @File    : whoisInfoCollect.py
# @Project : pythonBasics
import whois


def is_registered(domain):
    """
    检查域名是否已被注册
    """
    try:
        whois_info = whois.whois(domain)
        # print(whois_info)

        # return whois_info.domain_name is not None
    except Exception:
        return False
    else:
        return bool(whois_info.domain_name)

if __name__ == '__main__':
    domainList = {
        "baidu.com",
        "google.com",
        "amazon.com",
        "facebook.com",
        "twitter.com"
    }
    for domain in domainList:
        # print(f'{domain}')
        if is_registered(domain):
            print(f'{domain}: is registered')
        else:
            print(f'{domain} is not registered')
    # print(is_registered("baidu.com"))
