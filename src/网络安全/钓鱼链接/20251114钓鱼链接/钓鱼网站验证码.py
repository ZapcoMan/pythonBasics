import requests
import random
from urllib.parse import quote
import base64
import json


def send_code_request():
    """
    生成6位数验证码并发送请求
    """

    # 生成6位随机数字验证码
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    print(f"生成的验证码: {code}")

    # 构造数据并编码
    data = {"act": "sv", "data": {"code": code}}
    json_data = json.dumps(data, separators=(',', ':'))
    first_encoded = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
    second_encoded = base64.b64encode(first_encoded.encode('utf-8')).decode('utf-8')
    sv_param = quote(second_encoded)

    # 构建URL
    url = f"https://ev.gaysnboys.com/app/data.php?sv={sv_param}"

    # 设置请求头
    headers = {
        "Host": "ev.gaysnboys.com",
        "Cookie": "PHPSESSID=d344578e1494054e3002cd3ac4dba112",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept": "*/*",
        "Sec-Ch-Ua": '"Chromium";v="139", "Not;A=Brand";v="99"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://ev.gaysnboys.com/step_code/",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i"
    }

    # 发送请求
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        print(f"请求状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None, str(e)
send_code_request()