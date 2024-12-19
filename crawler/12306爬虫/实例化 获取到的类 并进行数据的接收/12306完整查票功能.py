import json
import random

import requests
from prettytable import PrettyTable

from train_info import TrainInfo

# 定义API URL，此处的URL为12306查询票务信息的接口地址
API_URL = "https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=2024-12-19&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT"

# 读取 city.json 文件，该文件包含了城市名与对应车站代码的映射
with open('city.json', 'r', encoding='utf-8') as f:
    city_data = json.load(f)
    # 获取用户输入的出发城市和目的地
    fromStation = input('请输入出发的城市：')
    toStation = input("请输入目的地：")
    # goDateTime = input("请输入出发时间")

# 动态生成API URL，根据用户输入的城市和日期
train_date = "2024-12-19"  # 查询日期
from_station = city_data[fromStation]  # 出发站代码
to_station = city_data[toStation]  # 到达站代码
# print(f"出发站代码:{from_station}，到达站代码：{to_station}")

# 定义 User-Agent 列表，用于模拟不同的浏览器请求
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/14.TG 短信轰炸接口.2 Safari/605.TG 短信轰炸接口.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
]
# 构造请求头部，包括随机选择一个User-Agent和Cookie信息
headers = {
    'User-Agent': random.choice(user_agents),
    'Cookie': '_uab_collina=173449375088168679444499; JSESSIONID=60CD7C21677293CF3570C9946BE42019; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_wfdc_flag=dc; _jc_save_fromDate=2024-12-19; _jc_save_toDate=2024-12-19; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=871367178.38945.0000; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_wfdc_flag=dc; BIGipServerotn=1658388746.50210.0000; BIGipServerpassport=921174282.50215.0000; route=6f50b51faa11b987e576cdb301e545c4; _jc_save_fromDate=2024-12-19; _jc_save_toDate=2024-12-19'
}

# 发起GET请求，获取票务信息
response = requests.get(url=API_URL, headers=headers)

try:
    # 解析JSON数据，并使用PrettyTable进行格式化输出
    json_data = response.json()
    tb = PrettyTable()
    tb.field_names = ['序号', '车次', '出发时间', '到达时间', '耗时', '特等座', '一等座', '二等座', '软卧', '硬卧',
                      '软座', '硬座', '无座', '商务座', '一等卧', '二等卧', '高级软卧']
    page = 1
    result = json_data.get('data').get('result')
    for i in result:
        index = i.split('|')
        # 创建TrainInfo对象，用于存储和处理列车信息
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

        # 将列车信息添加到表格中
        tb.add_row([page, train_info.train_number, train_info.departure_time, train_info.time_of_arrival,
                    train_info.time_consuming, train_info.premier_class, train_info.first_class_seat,
                    train_info.second_class, train_info.soft_sleeper, train_info.hard_sleeper, train_info.soft_seat,
                    train_info.hard_seat, train_info.without_seat, train_info.business_class,
                    train_info.first_class_sleeping,
                    train_info.second_class_bedroom, train_info.superior_soft_sleeper
                    ])
        page += 1
    # 打印格式化后的列车信息表格
    print(tb)
except ValueError as e:
    print(f"Failed to decode JSON: {e}")
except IndexError as e:
    print(f"Index error: {e}")
