import requests
import json
import time
import os

# 创建输出目录（如不存在）
output_dir = "优化强化output"
txt_output_dir = "优化强化txt"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(txt_output_dir, exist_ok=True)

def get_session_with_headers():
    """创建带默认 headers 的 session"""
    session = requests.Session()
    session.headers.update({
        'authority': 'api.mianshiya.com',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': 'SESSION=NGMzMzFkYTAtOWUxMC00MGZjLTljNDItZDM4ZTAxZDA5ZGQ6; Hm_lvt_8abb85f1b5cfd5f406cdcc6454141898=1750865759; HMACCOUNT=0F4187ED15E1DA2A; Hm_lvt_c7cedf2eca8990b32ef9f1a0412e7102=1750865759; Hm_lpvt_c7cedf2eca8990b32ef9f1a0412e7102=1750865831; Hm_lpvt_8abb85f1b5cfd5f406cdcc6454141898=1750865831',
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
    })
    return session

def fetch_and_save_questions(session, question_bank_id, title):
    """
    获取面试题数据并保存到本地 JSON 和 TXT 文件中
    """
    url = "https://api.mianshiya.com/api/question_bank/list_question"

    payload = {
        "current": 1,
        "pageSize": 20,
        "questionBankId": "",
        "tagList": []
    }

    filename = os.path.join(output_dir, f"{title}.json")
    txt_filename = os.path.join(txt_output_dir, f"{title}.txt")

    all_data = []

    for current in range(1, 11):
        payload['current'] = current
        payload["questionBankId"] = question_bank_id

        try:
            response = session.post(url, json=payload, timeout=(3, 10))
            if response.status_code == 200:
                data = response.json()
                all_data.append(data)

                print(f"已将第 {current} 页的数据写入缓存")

                records = data.get("data", {}).get("records", [])
                titles = [record.get("title") for record in records if record.get("title")]

                # 写入 TXT 文件（覆盖模式）
                if titles:
                    with open(txt_filename, 'w', encoding='utf-8') as f:
                        for t in titles:
                            f.write(f"{t}\n")
                    print(f"已将标题写入文件：{txt_filename}")

                # 判断是否结束
                if current > 1 and not records:
                    print(f"第 {current} 页 records 为空，判断数据已请求完毕，切换到下一个题库 ID...")
                    break

            else:
                print(f"获取第 {current} 页数据失败，状态码：{response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"请求第 {current} 页时发生异常：{e}")
            continue

        time.sleep(2)

    # 所有数据收集完成后统一写入 JSON 文件
    if all_data:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        print(f"已将全部数据写入文件：{filename}")

def main():
    with get_session_with_headers() as session:
        # 请求地址
        url = "https://api.mianshiya.com/api/questionBankCategory/list_questionBank"

        # 请求载荷
        data = {
            "current": 1,
            "pageSize": 20,
            "isHasChoice": False,
            "questionBankCategoryId": "1821883312558432257"
        }

        try:
            response = session.post(url, json=data, timeout=(3, 10))
            response.raise_for_status()
            response_json = response.json()
        except requests.exceptions.RequestException as e:
            print("请求失败:", e)
            return
        except requests.exceptions.JSONDecodeError:
            print("响应内容不是有效的 JSON 格式")
            return

        # 写入原始响应
        output_file = os.path.join(output_dir, "response_output.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(response_json, f, ensure_ascii=False, indent=4)
        print(f"JSON 数据已写入文件: {output_file}")

        # 提取 records
        records = response_json.get("data", {}).get("records", [])
        if not records:
            print("records 为空，无数据可处理。")
            return

        extracted_data = [{"id": record.get("id"), "title": record.get("title")} for record in records]

        # 写入提取数据
        extracted_file = os.path.join(output_dir, "extracted_records.json")
        with open(extracted_file, "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=4)
        print(f"已提取 records 中的 id 和 title，并保存到文件: {extracted_file}")

        # 调用抓取函数
        for item in extracted_data:
            question_bank_id = item.get("id")
            title = item.get("title")
            if question_bank_id and title:
                fetch_and_save_questions(session, question_bank_id, title)

if __name__ == "__main__":
    main()
