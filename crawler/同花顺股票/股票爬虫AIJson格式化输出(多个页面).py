import parsel
import requests
import random
import json
from prettytable import PrettyTable

# URL 模板
base_url = "https://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{}/ajax/1/"

# User-Agent 列表
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

# Cookie 头部
cookie_header = 'v=A5yLApe4F8vdieMXldnpddaibLFMFUS_wrBULnadqfhqHzLvniUQzxLJJMLF'

# 存储所有股票信息的列表
stocks_info = []

# 遍历多个页面
num_pages = 40  # 可以根据需要调整页数
for page in range(1, num_pages + 1):
    url = base_url.format(page)
    headers = {
        'User-Agent': random.choice(user_agents),
        'Cookie': cookie_header
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        responseText = response.text
        selector = parsel.Selector(responseText)

        # 获取所有表格行
        trs = selector.css('.m-table.m-pager-table tbody tr')

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
    # else:
        # print(f"Failed to fetch page {page}, status code: {response.status_code}")

# 使用PrettyTable格式化输出
table = PrettyTable()
table.field_names = ['排名', '代码', '名称', '现价', '涨跌幅(%)', '涨跌', '涨速(%)', '换手(%)', '量比', '振幅(%)', '成交额', '流通股', '流通市值', '市盈率']

for stock in stocks_info:
    table.add_row([
        stock['排名'],
        stock['代码'],
        stock['名称'],
        stock['现价'],
        stock['涨跌幅(%)'],
        stock['涨跌'],
        stock['涨速(%)'],
        stock['换手(%)'],
        stock['量比'],
        stock['振幅(%)'],
        stock['成交额'],
        stock['流通股'],
        stock['流通市值'],
        stock['市盈率']
    ])

# 打印表格
print(table)
