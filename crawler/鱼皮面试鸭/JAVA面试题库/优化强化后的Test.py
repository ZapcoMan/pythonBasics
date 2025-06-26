import requests
import json
import time
import os
import random
from concurrent.futures import ThreadPoolExecutor

# 创建输出目录（如不存在）
output_dir = "优化强化output"
txt_output_dir = "优化强化txt"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(txt_output_dir, exist_ok=True)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]


def get_session_with_headers():
    """创建带默认 headers 的 session，并随机设置 User-Agent"""
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
        'user-agent': random.choice(USER_AGENTS)  # 随机 User-Agent
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

        time.sleep(random.uniform(1, 3))  # 随机延时 1~3 秒

    # 所有数据收集完成后统一写入 JSON 文件
    if all_data:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        print(f"已将全部数据写入文件：{filename}")


def main():
    MAX_THREADS = 5  # 可根据网络状况调整线程数

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

        # 使用线程池并发执行
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = []
            for item in extracted_data:
                question_bank_id = item.get("id")
                title = item.get("title")
                if question_bank_id and title:
                    futures.append(executor.submit(fetch_and_save_questions, session, question_bank_id, title))

            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(f"线程任务出错: {e}")


if __name__ == "__main__":
    main()
