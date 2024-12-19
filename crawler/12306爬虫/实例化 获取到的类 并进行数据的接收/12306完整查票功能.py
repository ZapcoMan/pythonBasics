# 12306查票.py
import random
import requests
from train_info import TrainInfo

# 定义API URL，此处的URL为12306查询票务信息的接口地址
API_URL = (
    "https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=2024-12-18&leftTicketDTO.from_station=BJP&leftTicketDTO"
    ".to_station=SHH&purpose_codes=ADULT")

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
    'User-Agent': random.choice(user_agents),
    'Cookie': '_uab_collina=173449375088168679444499; JSESSIONID=758AA0BA0F6A702E9D4C41A9859C0D7F; BIGipServerpassport=1005060362.50215.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; route=495c805987d0f5c8c84b14f60212447d; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2024-12-18; _jc_save_toDate=2024-12-18; _jc_save_wfdc_flag=dc; BIGipServerotn=502268426.50210.0000'
}

# 发起GET请求，获取票务信息
response = requests.get(url=API_URL, headers=headers)

# 将响应内容解析为JSON格式
json_data = response.json()

result = json_data.get('data').get('result')

# 遍历结果并创建TrainInfo实例
for i in result:
    index = i.split('|')
    train_info = TrainInfo(
        train_number=index[3],
        departure_time=index[8],
        time_of_arrival=index[9],
        time_consuming=index[10],
        premier_class=index[32],
        first_class_seat=index[31],
        second_class=index[30],
        soft_sleeper=index[23],
        hard_sleeper=index[28],
        soft_seat=index[33],
        hard_seat=index[29],
        without_seat=index[26],
        business_class=index[35],
        first_class_sleeping=index[34],
        second_class_bedroom=index[36],
        superior_soft_sleeper=index[37]
    )
    print(train_info)
