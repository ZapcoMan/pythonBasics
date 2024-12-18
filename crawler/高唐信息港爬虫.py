import random

import requests
from bs4 import BeautifulSoup

base_url = 'https://www.gaotang.cc/job/zhaopin/'
pages = [i for i in range(1, 11)]  # 假设有两页

# 定义 User-Agent 列表
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

                if publish_info == "置顶":
                    print(f"这是置顶的（第 {page_number} 页）")
                    print("标题:", title)
                    print("链接:", f"{base_url}{href}")
                else:

                    print(f"发布日期: {publish_info} （第 {page_number} 页）")
                    print("标题:", title)
                    print("链接:", f"{base_url}{href}")

                    # 提取其他信息
                    dd1_tag = dl_tag.find('dd', class_='dd3_xx')
                    dd1_text = dd1_tag.text.strip() if dd1_tag else ""

                    dd2_tag = dl_tag.find('dd', class_='dd3_jj')
                    dd2_text = dd2_tag.text.strip() if dd2_tag else ""

                    print("详细信息:")
                    print(dd1_text)
                    print(dd2_text)
                    print("-" * 40)


# 遍历所有页面
for i in pages:
    url = f'{base_url}p{i}.aspx'
    print(f'URL:{url}')
    page_content = get_page_content(url)
    if page_content:
        extract_dl_content(page_content, i)
    else:
        print(f"无法获取第 {i} 页的内容")
