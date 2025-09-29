import requests
import json

url = "https://api.mianshiya.com/api/question_bank/list_question"

question_bank_ids = [
    "1860871861809897474",
    "1787463103423897602",
    "1789249312885223425",
    "1791375592078610434",
    "1791003439968264194",
    "1788408712975282177",
    "1789931432793948162", "1801424748099739650",
]

# 去重处理
question_bank_ids = list(set(question_bank_ids))

payload = {
    "current": 1,
    "pageSize": 20,
    "questionBankId": "",
    "tagList": []
}

headers = {
    'authority': 'api.mianshiya.com',
    'method': 'POST',
    'path': '/api/question_bank/list_question',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-length': '79',
    'content-type': 'application/json',
    'cookie': 'SESSION=NGMzMzFkYTAtOWUxMC00MGZjLTljNDItZDM4ZTAxZDA1ZGQ2; Hm_lvt_8abb85f1b5cfd5f406cdcc6454141898=1750865759; HMACCOUNT=0F4187ED15E1DA2A; Hm_lvt_c7cedf2eca8990b32ef9f1a0412e7102=1750865759; Hm_lpvt_c7cedf2eca8990b32ef9f1a0412e7102=1750865831; Hm_lpvt_8abb85f1b5cfd5f406cdcc6454141898=1750865831',
    'origin': 'https://www.mianshiya.com',
    'priority': 'u=1, i',
    'referer': 'https://www.mianshiya.com/',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
}

for question_bank_id in question_bank_ids:
    payload["questionBankId"] = question_bank_id
    for current in range(1, 20):
        payload['current'] = current
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            filename = f"output_{question_bank_id}.json"

            # 将数据以格式化的 JSON 写入文件
            with open(filename, 'a', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                f.write('\n')  # 添加换行以便后续数据写入

            print(f"已将第 {current} 页的数据写入文件：{filename}")
        else:
            print(f"获取第 {current} 页数据失败，状态码：{response.status_code}")
