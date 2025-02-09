import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor
"""
群友找到的一个钓鱼链接
模拟不同的设备 请求 钓鱼链接 
"""
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
]

url = "https://figystre.pro/api/check-credentials"


def send_request(data):
    headers = {
        "Host": "figystre.pro",
        "Content-Length": "60",
        "Sec-Ch-Ua-Platform": "Windows",
        "User-Agent": random.choice(user_agents),
        "Accept": "application/json, text/plain, */*",
        "Sec-Ch-Ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "Content-Type": "application/json",
        "Sec-Ch-Ua-Mobile": "?0",
        "Origin": "https://figystre.pro",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://figystre.pro/login/home?ref=https%3A%2F%2Fxigemazhuti.com%2Fvote",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Priority": "u=1, i"
    }
    response = requests.post(url, headers=headers, json=data)
    time.sleep(20)  # 延迟50毫秒
    return response.status_code, response.json()


# 单个数据对象
data = {
    "username": "你是煞笔吗?",
    "password": "牛逼格拉斯"
}

# 创建多个相同的请求数据
data_list = [data] * 50  # 发送500次相同的请求

# 使用线程池发送请求
with ThreadPoolExecutor(max_workers=25) as executor:
    futures = [executor.submit(send_request, data) for data in data_list]
    number200 = 0
    for future in futures:
        status_code, response_json = future.result()
        print(f"Status Code: {status_code}, Response: {response_json}")
        if status_code == 201:
            number200 += 1
        if status_code == "429":
            break
    print(number200)
