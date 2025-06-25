import requests
import json
import time
import os

# 创建输出目录（如不存在）
output_dir = "强化output"
txt_output_dir = "强化txt"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(txt_output_dir, exist_ok=True)  # 新增 txt 输出目录

def fetch_and_save_questions(question_bank_id, title):
    """
    根据 question_bank_id 获取面试题数据并保存到本地 JSON 文件中，
    文件名为 title.json 的格式，并统一存放在 output 目录下。
    同时提取 data.records 中的 title 并写入对应的 .txt 文件中，存放在 txt_output_dir。

    :param question_bank_id: 题库ID（字符串）
    :param title: 对应标题，用于命名输出文件
    """
    url = "https://api.mianshiya.com/api/question_bank/list_question"

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

    for current in range(1, 11):
        payload['current'] = current
        payload["questionBankId"] = question_bank_id
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                filename = os.path.join(output_dir, f"{title}.json")  # JSON 文件路径
                txt_filename = os.path.join(txt_output_dir, f"{title}.txt")  # TXT 文件路径

                # 将原始响应数据写入 JSON 文件
                with open(filename, 'a', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    f.write('\n')

                print(f"已将第 {current} 页的数据写入文件：{filename}")

                # 提取 data.data.records.title 并写入 TXT 文件
                records = data.get("data", {}).get("records", [])
                titles = [record.get("title") for record in records if record.get("title")]

                if titles:
                    with open(txt_filename, 'w', encoding='utf-8') as f:
                        for t in titles:
                            f.write(f"{t}\n")

                    print(f"已将第 {current} 页的标题写入文件：{txt_filename}")
                else:
                    print(f"第 {current} 页无有效标题可写入。")
            else:
                print(f"获取第 {current} 页数据失败，状态码：{response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"请求第 {current} 页时发生异常：{e}")

        time.sleep(2)  # 每次请求后等待 2 秒，避免请求过快


# 请求地址
url = "https://api.mianshiya.com/api/questionBankCategory/list_questionBank"

# 请求载荷
data = {
    "current": 1,
    "pageSize": 200,
    "isHasChoice": False,
    "questionBankCategoryId": "1821883312558432257"
}

# 请求头
headers = {
    "authority": "api.mianshiya.com",
    "method": "POST",
    "path": "/api/questionBankCategory/list_questionBank",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-length": "95",
    "content-type": "application/json",
    "cookie": "SESSION=NGMzMzFkYTAtOWUxMC00MGZjLTljNDItZDM4ZTAxZDA1ZGQ2; Hm_lvt_8abb85f1b5cfd5f406cdcc6454141898=1750865759; HMACCOUNT=0F4187ED15E1DA2A; Hm_lvt_c7cedf2eca8990b32ef9f1a0412e7102=1750865759; Hm_lpvt_c7cedf2eca8990b32ef9f1a0412e7102=1750870875; Hm_lpvt_8abb85f1b5cfd5f406cdcc6454141898=1750870875",
    "origin": "https://www.mianshiya.com",
    "priority": "u=1, i",
    "referer": "https://www.mianshiya.com/",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

# 发送 POST 请求
response = requests.post(url, json=data, headers=headers)

# 获取响应内容并解析为 JSON
try:
    response_json = response.json()
except requests.exceptions.JSONDecodeError:
    print("响应内容不是有效的 JSON 格式")
    response_json = {}

# 将原始 JSON 数据写入文件
output_file = os.path.join(output_dir, "response_output.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(response_json, f, ensure_ascii=False, indent=4)

print(f"JSON 数据已写入文件: {output_file}")

# 提取 data 中的 records 列表，并获取每个元素的 id 和 title
records = response_json.get("data", {}).get("records", [])
extracted_data = [{"id": record.get("id"), "title": record.get("title")} for record in records]

# 将提取的数据写入新的 JSON 文件
extracted_file = os.path.join(output_dir, "extracted_records.json")
with open(extracted_file, "w", encoding="utf-8") as f:
    json.dump(extracted_data, f, ensure_ascii=False, indent=4)

print(f"已提取 records 中的 id 和 title，并保存到文件: {extracted_file}")

# 遍历 extracted_data 并调用 fetch_and_save_questions
for item in extracted_data:
    question_bank_id = item.get("id")
    title = item.get("title")
    if question_bank_id and title:
        fetch_and_save_questions(question_bank_id, title)
