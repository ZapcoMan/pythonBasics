import requests
import json


def fetch_and_save_questions(question_bank_id):
    """
    根据 question_bank_id 获取面试题数据并保存到本地 JSON 文件中

    :param question_bank_id: 题库ID，可以是字符串（单个ID）或列表（多个ID）
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

    # 如果是字符串，转成列表处理
    if isinstance(question_bank_id, str):
        question_bank_ids = [question_bank_id]
    else:
        question_bank_ids = question_bank_id

    for question_bank_id in question_bank_ids:
        payload["questionBankId"] = question_bank_id
        for current in range(1, 11):
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


# 示例调用
if __name__ == "__main__":
    fetch_and_save_questions("1860871861809897474")
