# -*- coding: utf-8 -*-
# @Time    : 09 3月 2025 9:53 上午
# @Author  : codervibe
# @File    : dirBurp.py
# @Project : pythonBasics
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# 配置 SOCKS5 代理
proxies = {
    'http': 'socks5://127.0.0.1:33333',
    'https': 'socks5://127.0.0.1:33333'
}

# 目标网站的基础 URL
base_url = "http://192.168.1.11:9999"  # 替换为目标网站的实际 URL


# 读取目录字典文件
def load_directories(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


# 进行单个目录的请求
def request_directory(directory):
    url = f"{base_url}/{directory}"
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        if response.status_code in [200]:
            print(f"[+] 找到: {url} - 状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # print(f"[-] 访问 {url} 时出错: {e}")
        pass





# 进行目录爆破
def directory_brute_force(base_url, directories, max_workers=10):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_directory = {executor.submit(request_directory, directory): directory for directory in directories}
        for future in as_completed(future_to_directory):
            directory = future_to_directory[future]
            try:
                future.result()
            except Exception as e:
                print(f"[-] 处理 {directory} 时发生异常: {e}")


if __name__ == "__main__":
    dir_file = "dir.txt"  # 目录字典文件路径
    directories = load_directories(dir_file)
    if not directories:
        print("[-] 目录列表为空或文件未找到。")
    else:
        print(f"[*] 已加载 {len(directories)} 个目录进行爆破。")
        directory_brute_force(base_url, directories)
