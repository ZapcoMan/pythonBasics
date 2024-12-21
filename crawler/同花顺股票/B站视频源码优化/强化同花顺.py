# 导入所需的库
import random

import execjs
import requests
import parsel
import csv

# 打开CSV文件，准备写入数据
f = open('data.csv', mode='w', encoding='utf-8', newline='')
# 定义CSV文件的字段，并创建字典写入器
csv_writer = csv.DictWriter(f, fieldnames=[
    '代码',
    '名称',
    '现价',
    '涨跌幅(%)',
    '涨跌',
    '涨速(%)',
    '换手(%)',
    '量比',
    '振幅(%)',
    '成交额',
    '流通股',
    '流通市值',
    '市盈率',
])
# 写入CSV文件的表头
csv_writer.writeheader()

# 循环遍历每一页数据，范围从第1页到第265页
for page in range(1, 10):
    # 打印当前正在采集的页数
    print(f'正在采集第{page}页的数据内容')
    # 读取JavaScript文件内容，用于获取请求所需的cookie值
    js_file = open('同花顺.js', encoding='utf-8').read()
    # 编译JavaScript代码
    js_code = execjs.compile(js_file)
    # 调用JavaScript函数获取v参数值
    v = js_code.call('zy')
    # 构造cookie字典
    cookie = {
        'v': v
    }
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
    # 构造请求头，模拟浏览器行为
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    # 构造请求URL，根据页数变化
    url = f'https://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{page}/ajax/1/'
    # 输出一下cookie的值
    print(f'第{page}页的cookie的值为{cookie}')
    # 发送HTTP请求，获取网页内容
    response = requests.get(url=url, headers=headers, cookies=cookie)

    # 使用parsel选择器解析网页内容
    selector = parsel.Selector(response.text)
    # 提取所有的数据行，排除表头
    lis = selector.css('.m-table tr')[1:]
    # 遍历每一行数据
    for li in lis:
        # 提取数据单元格中的文本内容
        info = li.css('td::text').getall()
        # 提取数据单元格中的超链接文本内容
        info_1 = li.css('td a::text').getall()
        # 构造数据字典
        dit = {
            '代码': info_1[0],
            '名称': info_1[1],
            '现价': info[1],
            '涨跌幅(%)': info[2],
            '涨跌': info[3],
            '涨速(%)': info[4],
            '换手(%)': info[5],
            '量比': info[6],
            '振幅(%)': info[7],
            '成交额': info[8],
            '流通股': info[9],
            '流通市值': info[10],
            '市盈率': info[11],
        }
        # 将数据字典写入CSV文件
        csv_writer.writerow(dit)
        # 打印当前行的数据字典
        # print(dit)
