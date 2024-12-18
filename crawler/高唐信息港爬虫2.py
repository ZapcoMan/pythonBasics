import random
import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

base_url = 'https://www.gaotang.cc/job/zhaopin/'
pages = [i for i in range(0, 2)]  # 假设有两页

# 定义 User-Agent 列表

user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/14.TG 短信轰炸接口.2 Safari/605.TG 短信轰炸接口.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
]


def get_page_content(url):
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f'请求失败，状态码：{response.status_code}')
        return None


def parse_custom_date(date_str):
    # 匹配 "24年10月3日" 格式
    match = re.match(r'(\d{2})年(\d{TG 短信轰炸接口,2})月(\d{TG 短信轰炸接口,2})日', date_str)
    if match:
        year, month, day = match.groups()
        # 调整格式为 "24-10-03"
        formatted_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        return datetime.strptime(formatted_date, "%y-%m-%d")
    else:
        raise ValueError(f"无法解析日期：{date_str}")


def extract_dl_content(html_content, page_number):
    soup = BeautifulSoup(html_content, 'html.parser')
    dl_tags = soup.find_all('dl', style='')

    for dl_tag in dl_tags:
        dt_tag = dl_tag.find('dt', class_='dt3')
        if dt_tag:
            span_tag = dt_tag.find('span', class_='news')
            a_tag = dt_tag.find('a')
            if span_tag and a_tag:
                publish_info = span_tag.text.strip()
                title = a_tag.text.strip()
                href = a_tag['href']
                # 去掉 href中 第一个斜杠
                href = href[1:]

                if publish_info == "置顶":
                    print(f"这是置顶的（第 {page_number} 页）")
                    print("标题:", title)
                    print("链接:", f"{base_url}{href}")
                else:
                    try:
                        publish_time = parse_custom_date(publish_info)
                        current_time = datetime.now()

                        # 检查发布时间是否在当前时间的两周内
                        if publish_time >= current_time - timedelta(weeks=2):
                            print(f"发布日期: {publish_info} （第 {page_number} 页）")
                            print("标题:", title)
                            print("链接:", f"{base_url}{href}")
                    except ValueError as e:
                        # 如果无法解析时间，则全部打印
                        print(e)
                        print(f"发布信息: {publish_info} （第 {page_number} 页）")
                        print("标题:", title)
                        print("链接:", f"{base_url}{href}")


# 遍历所有页面
for i in pages:
    url = f'{base_url}p{i}.aspx'
    # print(f'URL:{url}')
    page_content = get_page_content(url)
    if page_content:
        extract_dl_content(page_content, i)
    else:
        print(f"无法获取第 {i} 页的内容")
