import base64

import requests
import urllib.parse
from urllib.parse import unquote




def send_request_with_requests(sv):


    # 构建完整的URL
    url = f"https://ev.gaysnboys.com/app/data.php?sv={sv}"

    # 设置请求头
    headers = {
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
        "Referer": "https://ev.gaysnboys.com/step_in/",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i",
        # 添加假IP地址
        "X-Forwarded-For": "192.168.1.100",
        "X-Real-IP": "192.168.1.100",
        "Client-IP": "192.168.1.100"
    }


    # 设置Cookie
    cookies = {
        "PHPSESSID": "d344578e1494054e3002cd3ac4dba112"
    }

    # 发送请求
    # 发送HTTP请求并处理响应数据
    # 参数:
    #     url: 请求的URL地址
    #     headers: 请求头字典
    #     cookies: Cookie字典
    # 返回值:
    #     无返回值，直接打印响应数据或错误信息
    try:
        # 发送HTTP请求并获取响应
        response = requests.get(url, headers=headers, cookies=cookies)

        # 自动处理gzip解压和编码
        response.encoding = 'utf-8'

        # 打印响应包里的全部信息
        print(response.text)
    # 捕获HTTP错误异常并打印错误信息
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")

sv = "ZXlKaFkzUWlPaUp6ZGlJc0ltUmhkR0VpT25zaWRYTmxjaUk2SWpZek5USTVPRFUySWl3aWNHRnpjeUk2SW1kb2FtdHNiVzVpZG1wa0luMTk%3D"
# 调用函数执行请求
send_request_with_requests(sv)
