import json
import random
import time

import requests

# 定义用户代理列表
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

# 定义请求头部模板
base_headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://stockx.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site'
}

# 定义目标URL
url = 'https://cdn.cookielaw.org/consent/137eafd0-59e4-44a7-a76f-e26ddbde8f33/0192f800-42db-714e-a9ed-699858ab46d3/en.json'

# 定义输出文件名
output_file = 'spider_test2_optimize.json'

try:
    # 每次请求时随机选择一个 User-Agent
    headers = base_headers.copy()
    headers['User-Agent'] = random.choice(user_agents)

    # 发送 GET 请求获取 JSON 数据
    response = requests.get(url, headers=headers, timeout=10)
    time.sleep(random.uniform(1, 3))
    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应内容为 JSON 格式
        json_data = response.json()

        # 将解析后的 JSON 数据写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        # 打印解析后的 JSON 数据
        print(json_data)
    else:
        print(f"请求失败，状态码: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"请求过程中发生异常: {e}")
except json.JSONDecodeError as e:
    print(f"JSON 解析失败: {e}")
