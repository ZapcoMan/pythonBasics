
import parsel
import requests
import random

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

# 遍历每一行并提取所需的数据
for tr in trs:
    rank = tr.css('td:nth-child(1)::text').get()
    code = tr.css('td:nth-child(2) a::attr(href)').re_first(r'/(\d+)/')
    name = tr.css('td:nth-child(3) a::text').get()
    current_price = tr.css('td:nth-child(4)::text').get()
    change_rate = tr.css('td:nth-child(5)::text').get()
    change_amount = tr.css('td:nth-child(6)::text').get()
    change_speed = tr.css('td:nth-child(7)::text').get()
    turnover_rate = tr.css('td:nth-child(8)::text').get()
    volume_ratio = tr.css('td:nth-child(9)::text').get()
    amplitude = tr.css('td:nth-child(10)::text').get()
    turnover_volume = tr.css('td:nth-child(11)::text').get()
    circulating_shares = tr.css('td:nth-child(12)::text').get()
    market_cap = tr.css('td:nth-child(13)::text').get()
    pe_ratio = tr.css('td:nth-child(14)::text').get()

    print(f'排名: {rank}, 代码: {code}, 名称: {name}, '
          f'现价: {current_price}, 涨跌幅(%): {change_rate}, 涨跌: {change_amount}, '
          f'涨速(%): {change_speed}, 换手(%): {turnover_rate}, 量比: {volume_ratio}, '
          f'振幅(%): {amplitude}, 成交额: {turnover_volume}, 流通股: {circulating_shares}, '
          f'流通市值: {market_cap}, 市盈率: {pe_ratio}')