import asyncio
import aiohttp
import requests

async def validate_id_card(id_card, fixed_name):
    """
    异步验证身份证号码是否有效。
    """
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
        "idcard": id_card,
        "name": fixed_name
    }

    try:
        response = requests.post('https://www.renshenet.org.cn/mobile/person/register/checkidcard', headers=headers, json=data)
        response.raise_for_status()
        result = response.json().get("data", {}).get("isSucces")

        print(response.json().get("data", {}))
        if result:
            print(f"身份证号码 {id_card} ✅验证通过")
            return True
        else:
            print(f"身份证号码 {id_card} ❌验证未通过")
            return False
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return False

async def validate_id_cards(id_card_list, fixed_name):
    for user in id_card_list:
        result = await validate_id_card(user['id_card'], fixed_name)
        if result:  # 如果验证通过，则停止后续验证
            return

# 示例调用
fixed_name = "朱振宇"
id_card_list = [
    {"id_card": "371526199906046011"},
    {"id_card": "371526199906046010"},
    {"id_card": "371526199906046012"}
]

asyncio.run(validate_id_cards(id_card_list, fixed_name))
