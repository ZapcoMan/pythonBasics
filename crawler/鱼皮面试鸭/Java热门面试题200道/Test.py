# ... existing code ...
import requests

url = "https://api.mianshiya.com/api/question_bank/list_question"

payload = {
    "current": 1,
    "pageSize": 20,
    "questionBankId": "1860871861809897474",
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

for current in range(1, 11):
    payload['current'] = current
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()

        with open('output.json', 'a', encoding='utf-8') as f:
            f.write(f"{data}\n")
        print(f"Data for page {current}: {data}")
    else:
        print(f"Failed to retrieve data for page {current}")
# ... existing code ...
