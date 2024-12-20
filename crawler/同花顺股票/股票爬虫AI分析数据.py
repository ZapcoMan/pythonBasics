import random

import requests
from bs4 import BeautifulSoup

url = "https://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/2/ajax/1/"
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
headers = {
    'User-Agent': random.choice(user_agents),
    'Cookie': 'v=A5yLApe4F8vdieMXldnpddaibLFMFUS_wrBULnadqfhqHzLvniUQzxLJJMLF'
}
response = requests.get(url, headers=headers)

# print(response.text)

soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', {'class': 'm-table m-pager-table'})
rows = table.tbody.find_all('tr')
stock_data = []
for row in rows:
    cols = row.find_all('td')
    data = [col.text.strip() for col in cols]
    stock_data.append(data)

# 打印或保存数据
for stock in stock_data:
    print(stock)
