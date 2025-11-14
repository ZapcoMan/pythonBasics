import base64
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote
import requests

# 用户代理列表
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
    构造账号密码数据结构
    """
    return {
        "act": "sv",
        "data": {
            "user": user_id,
            "pass": password
        }
    }

def generate_code_data(code):
    """
    构造验证码数据结构
    """
    return {
        "act": "sv",
        "data": {
            "code": code
        }
    }

def generate_fake_credentials(count=100):
    """
    生成虚假的用户凭证数据
    """
    credentials = []
    for i in range(count):
        user_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        password_length = random.randint(6, 12)
        password = ''.join([chr(random.randint(97, 122)) for _ in range(password_length)])
        credentials.append((user_id, password))
    return credentials

def generate_random_code():
    """
    生成6位随机数字验证码
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def encode_sv_parameter(data):
    """
    对数据进行两次Base64编码和一次URL编码
    """
    json_data = json.dumps(data, separators=(',', ':'))
    first_encoded = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
    second_encoded = base64.b64encode(first_encoded.encode('utf-8')).decode('utf-8')
    return quote(second_encoded)

def parse_response_data(response_text, request_type="account"):
    """
    解析钓鱼网站响应数据

    Args:
        response_text (str): 响应文本内容
        request_type (str): 请求类型 ("account" 或 "code")

    Returns:
        dict: 解析后的响应数据
    """
    # 处理 UTF-8 BOM
    if response_text.startswith('\ufeff'):
        response_text = response_text[1:]

    try:
        response_data = json.loads(response_text)

        # 打印基本响应信息
        print(f"   错误码: {response_data.get('err')}")

        if response_data.get("err") == 0:
            # 区分不同请求类型的跳转位置显示
            if request_type == "account":
                print(f"   跳转位置: {response_data.get('location', 'N/A')}")
            elif request_type == "code":
                location = response_data.get('location', None)
                if location is None:
                    print(f"   跳转位置: None")
                else:
                    print(f"   跳转位置: {location}")

            # 如果有详细数据信息
            if '$data' in response_data:
                data_info = response_data.get('$data', {})
                print(f"   服务器记录ID: {data_info.get('lastId', 'N/A')}")
                print(f"   记录时间: {data_info.get('date', 'N/A')}")
                print(f"   IP地址: {data_info.get('ip', 'N/A')}")
                print(f"   地理位置: {data_info.get('city', 'N/A')}")

            # 如果有服务验证信息
            if '$sv' in response_data:
                sv_info = response_data.get('$sv', {})
                print(f"   服务操作: {sv_info.get('act', 'N/A')}")
                sv_data = sv_info.get('data', {})
                if request_type == "account":
                    print(f"   用户名: {sv_data.get('user', 'N/A')}")
                    print(f"   密码: {sv_data.get('pass', 'N/A')}")
                elif request_type == "code":
                    print(f"   验证码: {sv_data.get('code', 'N/A')}")

        return response_data
    except json.JSONDecodeError as e:
        print(f"   响应解析失败: {e}")
        print(f"   响应内容预览: {response_text[:100]}...")
        return None
    except Exception as e:
        print(f"   响应处理异常: {e}")
        return None

def send_request_to_ev_site(sv_data, referer="https://ev.gaysnboys.com/step_in/"):
    """
    向钓鱼网站发送请求
    """
    # 编码参数
    sv_param = encode_sv_parameter(sv_data)
    url = f"https://ev.gaysnboys.com/app/data.php?sv={sv_param}"

    # 设置请求头
    headers = {
        "Host": "ev.gaysnboys.com",
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
        "Referer": referer,
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i",
        "X-Forwarded-For": f"{random.randint(1, 100)}.{random.randint(1, 150)}.{random.randint(1, 254)}.{random.randint(1, 254)}",
        "X-Real-IP": f"{random.randint(1, 100)}.{random.randint(1, 150)}.{random.randint(1, 254)}.{random.randint(1, 254)}",
        "Client-IP": f"{random.randint(1, 100)}.{random.randint(1, 150)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
    }

    # 设置Cookie
    cookies = {
        "PHPSESSID": "d344578e1494054e3002cd3ac4dba112"
    }

    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        response.encoding = 'utf-8'
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)

def process_complete_request(credential):
    """
    处理完整的请求流程：先发送账号密码，再发送验证码
    """
    user_id, password = credential
    print(f"🚀 开始处理用户 - 用户名: {user_id}, 密码: {password}")

    # 1. 发送账号密码请求
    print(f"📧 发送账号密码请求 - 用户名: {user_id}")
    sv_data = create_sv_data(user_id, password)
    status_code1, response_text1 = send_request_to_ev_site(sv_data)

    if status_code1 == 200:
        print(f"✅ 账号密码请求成功 - 用户名: {user_id}，密码: {password}")
        # 解析账号密码响应
        account_response = parse_response_data(response_text1, "account")
    else:
        print(f"❌ 账号密码请求失败 - 用户名: {user_id}, 状态码: {status_code1}")
        return False

    # 2. 等待10秒
    print(f"⏳ 等待10秒左右后发送验证码请求 - 用户名: {user_id}")
    tm= random.randint(10, 21)
    print(f"   等待时间: {tm}秒")
    time.sleep(tm)

    # 3. 发送验证码请求
    result = sendAVerificationCodeRequest(user_id)
    return result

def sendAVerificationCodeRequest(user_id):
    """
    发送验证码请求

    Args:
        user_id (str): 用户ID
    """
    # 生成验证码
    code = generate_random_code()
    print(f"🔢 发送验证码请求 - 用户名: {user_id}, 验证码: {code}")

    # 构造并输出请求内容
    code_data = generate_code_data(code)
    print(f"   请求数据: {code_data}")

    # 编码参数并输出
    sv_param = encode_sv_parameter(code_data)
    print(f"   编码参数: {sv_param}")

    status_code2, response_text2 = send_request_to_ev_site(
        code_data,
        referer="https://ev.gaysnboys.com/step_code/"
    )

    if status_code2 == 200:
        print(f"✅ 验证码请求成功 - 用户名: {user_id}, 验证码: {code}")
        # 解析验证码响应
        code_response = parse_response_data(response_text2, "code")
        return True
    else:
        print(f"❌ 验证码请求失败 - 用户名: {user_id}, 状态码: {status_code2}")
        return False

# 主程序入口
if __name__ == "__main__":
    # 生成虚假凭证
    fake_credentials = generate_fake_credentials(1000)  # 减少数量用于测试

    print("🔐 生成的虚假凭证:")
    for i, (user_id, password) in enumerate(fake_credentials):
        print(f"  [{i + 1:2d}] 用户名: {user_id:>8s}, 密码: {password}")

    print("\n🚀 开始发送请求序列...")

    # 使用线程池并发发送请求
    with ThreadPoolExecutor(max_workers=50) as executor:
        # 提交所有任务
        futures = [executor.submit(process_complete_request, cred) for cred in fake_credentials]

        success_count = 0
        total_count = len(fake_credentials)

        for i, future in enumerate(futures):
            try:
                result = future.result()
                if result:
                    success_count += 1
                # 添加延迟避免过于频繁的请求
                time.sleep(0.5)
            except Exception as e:
                print(f"❌ 请求 {i + 1} 异常: {e}")

        print(f"\n📊 总结报告:")
        print(f"   成功处理: {success_count}/{total_count}")
        print(f"   成功率: {success_count / total_count * 100:.1f}%")
