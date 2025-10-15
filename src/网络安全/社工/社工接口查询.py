import requests
from html import unescape


def qqNumberQueryBindingMobilePhone(qq_number: str):
    cookies = {
        'PHPSESSID': 'd4439s79ogqeq420l6usjtbeb9',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://qb.heikebook.com',
        'priority': 'u=1, i',
        'referer': 'https://qb.heikebook.com/index',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        # 'cookie': 'PHPSESSID=d4439s79ogqeq420l6usjtbeb9',
    }

    params = {
        's': 'text.row',
    }

    json_data = {
        'text': qq_number,
        'ai': False,
        'sign': '0188bfe62c7948d5c4a970153c0a2c28',
    }

    response = requests.post(
        'https://qb.heikebook.com/api/backend/public/',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    if response.status_code == 200:
        json_data = response.json()
        print(f"json_data：{json_data}")
        dataStr = json_data["data"]["str"]
        cleaned_str = unescape(dataStr).replace("<br>", "\n")
        # print(cleaned_str)
        # cleaned_str 转化为 json
        # cleaned_str = json.loads(cleaned_str)
        resultStr = parse_query_result(cleaned_str)
        # print(resultStr)
        return resultStr
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None


def parse_query_result(result_str):
    """解析查询结果字符串为结构化数据"""
    if isinstance(result_str, str):
        lines = result_str.strip().split('\n')
        parsed_data = {}
        for line in lines:
            if '：' in line:
                key, value = line.split('：', 1)
                parsed_data[key.strip()] = value.strip()
        return parsed_data
    return result_str


if __name__ == '__main__':
    qq_number = ""
    result = qqNumberQueryBindingMobilePhone(qq_number)
    print(result)
