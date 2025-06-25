import requests
import json

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
output_file = "response_output.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(response_json, f, ensure_ascii=False, indent=4)

print(f"JSON 数据已写入文件: {output_file}")

# 提取 data 中的 records 列表，并获取每个元素的 id 和 title
records = response_json.get("data", {}).get("records", [])
extracted_data = [{"id": record.get("id"), "title": record.get("title")} for record in records]

# 将提取的数据写入新的 JSON 文件
extracted_file = "extracted_records.json"
with open(extracted_file, "w", encoding="utf-8") as f:
    json.dump(extracted_data, f, ensure_ascii=False, indent=4)

print(f"已提取 records 中的 id 和 title，并保存到文件: {extracted_file}")
