import base64
import json
import random
import time
import urllib
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

import requests


# 用户代理列表，模拟不同设备和浏览器
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


def create_sv_data(user_id, password):
    """
    构造一个包含act和data字段的JSON数据结构

    Args:
        user_id (str): 用户ID
        password (str): 用户密码

    Returns:
        dict: 包含act和data字段的字典
    """
    data_structure = {
        "act": "sv",
        "data": {
            "user": user_id,
            "pass": password
        }
    }
    return data_structure


def generate_fake_credentials(count=100):
    """
    生成虚假的用户凭证数据

    Args:
        count (int): 生成凭证数量

    Returns:
        list: 包含多个用户凭证的列表
    """
    credentials = []
    for i in range(count):
        # 生成8位随机数字用户ID
        user_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        # 生成6-12位随机字母密码
        password_length = random.randint(6, 12)
        password = ''.join([chr(random.randint(97, 122)) for _ in range(password_length)])
        credentials.append((user_id, password))
    return credentials


def send_request_to_ev_site(sv_data):
    """
    向ev.gaysnboys.com发送请求

    Args:
        sv_data: 请求数据字典

    Returns:
        tuple: 状态码和响应内容
    """
    # 使用JSON序列化确保数据格式一致
    json_data = json.dumps(sv_data, separators=(',', ':'))
    print(f"JSON序列化数据: {json_data}")

    # 第一次Base64编码
    encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
    print(f"encoded_data 第一次加密: {encoded_data}")

    # 第二次Base64编码
    encoded_data = base64.b64encode(encoded_data.encode('utf-8')).decode('utf-8')
    print(f"encoded_data 第二次加密: {encoded_data}")

    # URL编码
    encoded_data = quote(encoded_data)
    print(f"encoded_data进行一次 URL 编码: {encoded_data}")

    # 构建完整的URL
    url = f"https://ev.gaysnboys.com/app/data.php?sv={encoded_data}"

    # 设置请求头
    headers = {
        "Sec-Ch-Ua-Platform": '"Windows"',
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept": "*/*",
        "Sec-Ch-Ua": '"Chromium";v="139", "Not;A=Brand";v="99"',
        "User-Agent": random.choice(user_agents),
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://ev.gaysnboys.com/step_in/",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i",
        # 添加假IP地址
        "X-Forwarded-For": f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",
        "X-Real-IP": f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",
        "Client-IP": f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
    }

    # 设置Cookie
    cookies = {
        "PHPSESSID": "d344578e1494054e3002cd3ac4dba112"
    }

    try:
        # 发送HTTP请求并获取响应
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        response.encoding = 'utf-8'
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def process_single_request(credential):
    """
    处理单个请求

    Args:
        credential: 包含(user_id, password)的元组

    Returns:
        tuple: 状态码和响应内容
    """
    user_id, password = credential
    print(f"发送请求 - 用户名: {user_id}, 密码: {password}")

    sv_data = create_sv_data(user_id, password)
    status_code, response_text = send_request_to_ev_site(sv_data)

    # 处理 UTF-8 BOM
    if response_text.startswith('\ufeff'):
        response_text = response_text[1:]

    # 解析响应内容
    try:
        print(f"响应内容response_text: {response_text}")
        response_data = json.loads(response_text)
        print(f"错误码: {response_data.get('err')}")

        # 格式化输出响应详情
        if response_data.get("err") == 0:
            print(f"✅ 请求成功 - 用户名: {user_id}, 状态码: {status_code}")
            print(f"   响应内容: {response_data}")
            print(f"   跳转位置: {response_data.get('location', 'N/A')}")
            data_info = response_data.get('$data', {})
            print(f"   服务器记录ID: {data_info.get('lastId', 'N/A')}")
            print(f"   记录时间: {data_info.get('date', 'N/A')}")
        else:
            print(f"❌ 请求失败 - 用户名: {user_id}, 状态码: {status_code}")
    except json.JSONDecodeError:
        print(f"⚠️ 响应解析失败 - 用户名: {user_id}, 状态码: {status_code}")
        print(f"响应内容: {response_text[:100]}...")  # 打印前100个字符用于调试
    except Exception as exc:
        print(f"⚠️ 请求处理异常 - 用户名: {user_id}, 错误信息: {exc}")

    return status_code, response_text


# 主程序入口
if __name__ == "__main__":
    # 生成100组虚假凭证
    fake_credentials = generate_fake_credentials(1)

    # 打印将要使用的凭证信息
    print("🔐 生成的虚假凭证:")
    for i, (user_id, password) in enumerate(fake_credentials):
        print(f"  [{i + 1:2d}] 用户名: {user_id:>8s}, 密码: {password}")

    print("\n🚀 开始发送请求...")

    # 使用线程池并发发送请求
    with ThreadPoolExecutor(max_workers=20) as executor:
        # 提交所有任务
        futures = [executor.submit(process_single_request, cred) for cred in fake_credentials]

        success_count = 0
        total_count = len(fake_credentials)

        for i, future in enumerate(futures):
            try:
                status_code, response_text = future.result()
                if status_code == 200:
                    success_count += 1
                # 添加延迟避免过于频繁的请求
                time.sleep(0.1)
            except Exception as e:
                print(f"❌ 请求 {i + 1} 异常: {e}")

        print(f"\n📊 总结报告:")
        print(f"   成功请求: {success_count}/{total_count}")
        print(f"   成功率: {success_count / total_count * 100:.1f}%")
