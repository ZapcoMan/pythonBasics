# 12306查票.py
import json
import os
import random

import requests

from train_info import TrainInfo

# 从环境变量中读取API URL和Cookie
API_URL = os.getenv('API_URL', "https://kyfw.12306.cn/otn/leftTicket/queryO")
COOKIE = os.getenv('COOKIE',
                   'guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_wfdc_flag=dc; _jc_save_fromDate=2024-12-19; _jc_save_toDate=2024-12-19; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=871367178.38945.0000')

# 定义 User-Agent 列表，用于模拟不同的浏览器请求
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
]

# 构造请求头部，包括随机选择一个User-Agent和Cookie信息
headers = {
    'User-Agent': random.choice(user_agents),  # 随机选择一个User-Agent以模拟不同的浏览器
    'Cookie': COOKIE  # 使用从环境变量中读取的Cookie
}

# 读取 city.json 文件
with open('city.json', 'r', encoding='utf-8') as f:
    city_data = json.load(f)
    fromStation = input('请输入出发的城市：')
    toStation = input("请输入目的地：")
    # goDateTime = input("请输入出发时间")

# 动态生成API URL
train_date = "2024-12-19"  # 查询日期
from_station = city_data[fromStation]  # 出发站代码
to_station = city_data[toStation]  # 到达站代码
print(f"出发站代码:{from_station}，到达站代码：{to_station}")
purpose_codes = "ADULT"  # 乘客类型
full_api_url = f"{API_URL}?leftTicketDTO.train_date={train_date}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes={purpose_codes}"  # 构造完整的API URL

try:
    # 发起GET请求，获取票务信息
    response = requests.get(url=full_api_url, headers=headers, timeout=10)  # 发起GET请求
    response.raise_for_status()  # 检查HTTP响应状态码，如果请求失败则抛出异常

    # 将响应内容解析为JSON格式
    json_data = response.json()  # 解析JSON响应

    # 获取查询结果
    result = json_data.get('data', {}).get('result', [])  # 从JSON数据中提取结果

    if not result:
        print("没有找到相关车次信息。")  # 如果没有找到相关车次信息，打印提示
    else:
        # 遍历结果并创建TrainInfo实例
        for i in result:
            index = i.split('|')  # 将结果字符串按'|'分割
            train_info = TrainInfo(
                train_number=index[3],  # 车次编号
                departure_time=index[8],  # 出发时间
                time_of_arrival=index[9],  # 到达时间
                time_consuming=index[10],  # 运行时间
                premier_class=index[32],  # 商务座
                first_class_seat=index[31],  # 一等座
                second_class=index[30],  # 二等座
                soft_sleeper=index[23],  # 软卧
                hard_sleeper=index[28],  # 硬卧
                soft_seat=index[33],  # 软座
                hard_seat=index[29],  # 硬座
                without_seat=index[26],  # 无座
                business_class=index[35],  # 商务座
                first_class_sleeping=index[34],  # 一等卧
                second_class_bedroom=index[36],  # 二等卧
                superior_soft_sleeper=index[37]  # 高级软卧
            )

    # 打印列车信息
    print(train_info)

# 异常处理
# 捕获请求异常，如网络连接问题等
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")

# 捕获JSON解析异常，如响应内容不是有效的JSON格式
except ValueError as e:
    print(f"JSON解析失败: {e}")
