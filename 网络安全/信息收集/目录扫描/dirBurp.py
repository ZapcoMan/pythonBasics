# -*- coding: utf-8 -*-
# @Time    : 09 3月 2025 9:53 上午
# @Author  : codervibe
# @File    : dirBurp.py
# @Project : pythonBasics
import requests

# 配置 SOCKS5 代理
proxies = {
    'http': 'socks5://127.0.0.1:33333',
    'https': 'socks5://127.0.0.1:33333'
}

# 目标网站的基础 URL
base_url = "http://127.0.0.1"  # 替换为目标网站的实际 URL

# 读取目录字典文件
def load_directories(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

# 进行目录爆破
def directory_brute_force(base_url, directories):
    for directory in directories:
        url = f"{base_url}/{directory}"
        try:
            response = requests.get(url, proxies=proxies, timeout=10)
            if response.status_code in [200, 500]:
                print(f"[+] Found: {url} - Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[-] Error accessing {url}: {e}")

if __name__ == "__main__":
    dir_file = "dir.txt"  # 目录字典文件路径
    directories = load_directories(dir_file)
    if not directories:
        print("[-] Directory list is empty or file not found.")
    else:
        print(f"[*] Loaded {len(directories)} directories for brute force.")
        directory_brute_force(base_url, directories)
