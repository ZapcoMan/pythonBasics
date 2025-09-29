import parsel
import requests
import random
import json

url = "https://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/1/ajax/1/"
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
headers = {
    'User-Agent': random.choice(user_agents),
    'Cookie': 'v=A5yLApe4F8vdieMXldnpddaibLFMFUS_wrBULnadqfhqHzLvniUQzxLJJMLF'
}

response = requests.get(url, headers=headers)
responseText = response.text
selector = parsel.Selector(responseText)

# 获取所有表格行
trs = selector.css('.m-table.m-pager-table tbody tr')

# 存储所有股票信息的列表
stocks_info = []

# 遍历每一行并提取所需的数据
for tr in trs:
    stock = {
        '排名': tr.css('td:nth-child(1)::text').get(),
        '代码': tr.css('td:nth-child(2) a::attr(href)').re_first(r'/(\d+)/'),
        '名称': tr.css('td:nth-child(3) a::text').get(),
        '现价': tr.css('td:nth-child(4)::text').get(),
        '涨跌幅(%)': tr.css('td:nth-child(5)::text').get(),
        '涨跌': tr.css('td:nth-child(6)::text').get(),
        '涨速(%)': tr.css('td:nth-child(7)::text').get(),
        '换手(%)': tr.css('td:nth-child(8)::text').get(),
        '量比': tr.css('td:nth-child(9)::text').get(),
        '振幅(%)': tr.css('td:nth-child(10)::text').get(),
        '成交额': tr.css('td:nth-child(11)::text').get(),
        '流通股': tr.css('td:nth-child(12)::text').get(),
        '流通市值': tr.css('td:nth-child(13)::text').get(),
        '市盈率': tr.css('td:nth-child(14)::text').get()
    }
    stocks_info.append(stock)

# 将列表转换为JSON字符串
stocks_json = json.dumps(stocks_info, ensure_ascii=False, indent=4)
print(stocks_json)
