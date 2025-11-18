#!/usr/bin/env python"
# coding: utf-8
# 作者：Threezh1
# https://threezh1.github.io/
# 来自开源脚本：https://github.com/Threezh1/JSFinder

import requests, argparse, sys, re
import urllib3
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def parse_args():
    """
    解析命令行参数

    Returns:
        Namespace: 包含所有解析后的命令行参数的对象
    """
    parser = argparse.ArgumentParser(epilog='\t示例: \r\npython ' + sys.argv[0] + " -u http://www.baidu.com")
    parser.add_argument("-u", "--url", help="目标网站")
    parser.add_argument("-c", "--cookie", help="网站Cookie")
    parser.add_argument("-f", "--file", help="包含URL或JS的文件")
    parser.add_argument("-ou", "--outputurl", help="输出文件名")
    parser.add_argument("-os", "--outputsubdomain", help="输出文件名")
    parser.add_argument("-j", "--js", help="在JS文件中查找", action="store_true")
    parser.add_argument("-d", "--deep", help="深度查找", action="store_true")
    return parser.parse_args()


# 正则表达式来源于 https://github.com/GerbenJavado/LinkFinder
def extract_URL(JS):
    """
    从JavaScript代码中提取URL链接

    Args:
        JS (str): JavaScript代码字符串

    Returns:
        list: 提取出的URL列表
    """
    pattern_raw = r"""
	  (?:"|')                               # 开始换行分隔符
	  (
	    ((?:[a-zA-Z]{1,10}://|//)           # 匹配协议 [a-Z]*1-10 或 //
	    [^"'/]{1,}\.                        # 匹配域名 (任意字符 + 点)
	    [a-zA-Z]{2,}[^"']{0,})              # 域名扩展和/或路径
	    |
	    ((?:/|\.\./|\./)                    # 以 /,../,./ 开始
	    [^"'><,;| *()(%%$^/\\\[\]]          # 下一个字符不能是...
	    [^"'><,;|()]{1,})                   # 其余字符不能是
	    |
	    ([a-zA-Z0-9_\-/]{1,}/               # 带/的相对端点
	    [a-zA-Z0-9_\-/]{1,}                 # 资源名称
	    \.(?:[a-zA-Z]{1,4}|action)          # 剩余部分 + 扩展名 (长度1-4或action)
	    (?:[\?|/][^"|']{0,}|))              # ? 标记带参数
	    |
	    ([a-zA-Z0-9_\-]{1,}                 # 文件名
	    \.(?:php|asp|aspx|jsp|json|
	         action|html|js|txt|xml)             # . + 扩展名
	    (?:\?[^"|']{0,}|))                  # ? 标记带参数
	  )
	  (?:"|')                               # 结束换行分隔符
	"""
    pattern = re.compile(pattern_raw, re.VERBOSE)
    result = re.finditer(pattern, str(JS))
    if result == None:
        return None
    js_url = []
    return [match.group().strip('"').strip("'") for match in result
            if match.group() not in js_url]


# 获取页面源码
def Extract_html(URL):
    """
    获取指定URL的页面源码

    Args:
        URL (str): 目标网页URL

    Returns:
        str: 页面HTML源码，如果获取失败则返回None
    """
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
        "Cookie": args.cookie}
    try:
        raw = requests.get(URL, headers=header, timeout=3, verify=False)
        raw = raw.content.decode("utf-8", "ignore")
        return raw
    except:
        return None


# 处理相对URL
def process_url(URL, re_URL):
    """
    处理相对URL，将其转换为绝对URL

    Args:
        URL (str): 基础URL
        re_URL (str): 需要处理的相对URL

    Returns:
        str: 转换后的绝对URL
    """
    black_url = ["javascript:"]  # 添加一些关键字用于过滤URL
    URL_raw = urlparse(URL)
    ab_URL = URL_raw.netloc
    host_URL = URL_raw.scheme
    if re_URL[0:2] == "//":
        result = host_URL + ":" + re_URL
    elif re_URL[0:4] == "http":
        result = re_URL
    elif re_URL[0:2] != "//" and re_URL not in black_url:
        if re_URL[0:1] == "/":
            result = host_URL + "://" + ab_URL + re_URL
        else:
            if re_URL[0:1] == ".":
                if re_URL[0:2] == "..":
                    result = host_URL + "://" + ab_URL + re_URL[2:]
                else:
                    result = host_URL + "://" + ab_URL + re_URL[1:]
            else:
                result = host_URL + "://" + ab_URL + "/" + re_URL
    else:
        result = URL
    return result


def find_last(string, str):
    """
    查找字符串中某个子串的所有出现位置

    Args:
        string (str): 源字符串
        str (str): 要查找的子串

    Returns:
        list: 所有匹配位置的索引列表
    """
    positions = []
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1: break
        last_position = position
        positions.append(position)
    return positions


def find_by_url(url, js=False):
    """
    通过URL查找其中包含的链接

    Args:
        url (str): 目标网站URL
        js (bool): 是否只在JS文件中查找，默认False

    Returns:
        list: 找到的URL列表
    """
    if js == False:
        try:
            print("网址:" + url)
        except:
            print("请指定一个URL，例如 https://www.baidu.com")
        html_raw = Extract_html(url)
        if html_raw == None:
            print("无法访问 " + url)
            return None
        # print(html_raw)
        html = BeautifulSoup(html_raw, "html.parser")
        html_scripts = html.findAll("script")
        script_array = {}
        script_temp = ""
        for html_script in html_scripts:
            script_src = html_script.get("src")
            if script_src == None:
                script_temp += html_script.get_text() + "\n"
            else:
                purl = process_url(url, script_src)
                script_array[purl] = Extract_html(purl)
        script_array[url] = script_temp
        allurls = []
        for script in script_array:
            # print(script)
            temp_urls = extract_URL(script_array[script])
            if len(temp_urls) == 0: continue
            for temp_url in temp_urls:
                allurls.append(process_url(script, temp_url))
        result = []
        for singerurl in allurls:
            url_raw = urlparse(url)
            domain = url_raw.netloc
            positions = find_last(domain, ".")
            miandomain = domain
            if len(positions) > 1: miandomain = domain[positions[-2] + 1:]
            # print(miandomain)
            suburl = urlparse(singerurl)
            subdomain = suburl.netloc
            # print(singerurl)
            if miandomain in subdomain or subdomain.strip() == "":
                if singerurl.strip() not in result:
                    result.append(singerurl)
        return result
    return sorted(set(extract_URL(Extract_html(url)))) or None


def find_subdomain(urls, mainurl):
    """
    从URL列表中提取子域名

    Args:
        urls (list): URL列表
        mainurl (str): 主域名URL

    Returns:
        list: 子域名列表
    """
    url_raw = urlparse(mainurl)
    domain = url_raw.netloc
    miandomain = domain
    positions = find_last(domain, ".")
    if len(positions) > 1: miandomain = domain[positions[-2] + 1:]
    subdomains = []
    for url in urls:
        suburl = urlparse(url)
        subdomain = suburl.netloc
        # print(subdomain)
        if subdomain.strip() == "": continue
        if miandomain in subdomain:
            if subdomain not in subdomains:
                subdomains.append(subdomain)
    return subdomains


def find_by_url_deep(url):
    """
    深度查找URL中的链接（递归查找页面中的链接）

    Args:
        url (str): 目标网站URL

    Returns:
        list: 找到的所有URL列表
    """
    html_raw = Extract_html(url)
    if html_raw == None:
        print("无法访问 " + url)
        return None
    html = BeautifulSoup(html_raw, "html.parser")
    html_as = html.findAll("a")
    links = []
    for html_a in html_as:
        src = html_a.get("href")
        if src == "" or src == None: continue
        link = process_url(url, src)
        if link not in links:
            links.append(link)
    if links == []: return None
    print("总共找到 " + str(len(links)) + " 个链接")
    urls = []
    i = len(links)
    for link in links:
        temp_urls = find_by_url(link)
        if temp_urls == None: continue
        print("剩余 " + str(i) + " | 在 " + link + " 中找到 " + str(len(temp_urls)) + " 个URL")
        for temp_url in temp_urls:
            if temp_url not in urls:
                urls.append(temp_url)
        i -= 1
    return urls


def find_by_file(file_path, js=False):
    """
    从文件中读取URL并查找其中的链接

    Args:
        file_path (str): 包含URL的文件路径
        js (bool): 是否只在JS文件中查找，默认False

    Returns:
        list: 找到的URL列表
    """
    with open(file_path, "r") as fobject:
        links = fobject.read().split("\n")
    if links == []: return None
    print("总共找到 " + str(len(links)) + " 个链接")
    urls = []
    i = len(links)
    for link in links:
        if js == False:
            temp_urls = find_by_url(link)
        else:
            temp_urls = find_by_url(link, js=True)
        if temp_urls == None: continue
        print(str(i) + " 在 " + link + " 中找到 " + str(len(temp_urls)) + " 个URL")
        for temp_url in temp_urls:
            if temp_url not in urls:
                urls.append(temp_url)
        i -= 1
    return urls


def giveresult(urls, domian):
    """
    输出结果并保存到文件

    Args:
        urls (list): URL列表
        domian (str): 主域名
    """
    if urls == None:
        return None
    print("找到 " + str(len(urls)) + " 个URL:")
    content_url = ""
    content_subdomain = ""
    for url in urls:
        content_url += url + "\n"
        print(url)
    subdomains = find_subdomain(urls, domian)
    print("\n找到 " + str(len(subdomains)) + " 个子域名:")
    for subdomain in subdomains:
        content_subdomain += subdomain + "\n"
        print(subdomain)
    if args.outputurl != None:
        with open(args.outputurl, "a", encoding='utf-8') as fobject:
            fobject.write(content_url)
        print("\n输出 " + str(len(urls)) + " 个URL")
        print("路径:" + args.outputurl)
    if args.outputsubdomain != None:
        with open(args.outputsubdomain, "a", encoding='utf-8') as fobject:
            fobject.write(content_subdomain)
        print("\n输出 " + str(len(subdomains)) + " 个子域名")
        print("路径:" + args.outputsubdomain)


if __name__ == "__main__":
    urllib3.disable_warnings()
    args = parse_args()
    if args.file == None:
        if args.deep is not True:
            urls = find_by_url(args.url)
            giveresult(urls, args.url)
        else:
            urls = find_by_url_deep(args.url)
            giveresult(urls, args.url)
    else:
        if args.js is not True:
            urls = find_by_file(args.file)
            giveresult(urls, urls[0])
        else:
            urls = find_by_file(args.file, js=True)
            giveresult(urls, urls[0])
