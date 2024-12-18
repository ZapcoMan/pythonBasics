import json
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import random
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, app

# 初始化Flask应用
app = Flask(__name__)

# 定义基础URL，用于构建完整的链接
base_url = 'https://www.gaotang.cc/job/zhaopin/'

# 定义用户代理列表，用于发送请求时伪装
user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/14.TG 短信轰炸接口.2 Safari/605.TG 短信轰炸接口.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',

    # macOS 用户代理
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/14.TG 短信轰炸接口.2 Safari/605.TG 短信轰炸接口.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',

    # Windows 用户代理
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',

    # Android 用户代理
    'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36',

    # iOS 用户代理
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.TG 短信轰炸接口',
    'Mozilla/5.0 (iPad; CPU OS 14_4_2 like Mac OS X) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.TG 短信轰炸接口',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.TG 短信轰炸接口',

    # Linux 用户代理
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.TG 短信轰炸接口',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'

    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/15.TG 短信轰炸接口 Mobile/15E148 Safari/604.TG 短信轰炸接口',
    'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0',
    'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.TG 短信轰炸接口',
    'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-N975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-A505U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-G988U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
    # Android 用户代理
    'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; ONEPLUS A6003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36'

    # Android 手机用户代理
    'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; ONEPLUS A6003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; Redmi Note 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 8.TG 短信轰炸接口.0; Nexus 6P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.0; Pixel C Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36',

    # Android 手表用户代理
    'Mozilla/5.0 (Linux; Android 10; SM-R810) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 9; Wear OS) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 8.0.0; Wear OS) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Safari/537.36',

    # 旧版本 Android 用户代理
    'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; Nexus 5 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.114 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; Nexus 4 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.TG 短信轰炸接口 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.TG 短信轰炸接口',
    'Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.TG 短信轰炸接口 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.TG 短信轰炸接口',
    'Mozilla/5.0 (Linux; U; Android 2.TG 短信轰炸接口; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17'
]

def get_page_content(url):
    """
    获取页面内容
    :param url: 请求的URL
    :return: 页面内容的字符串，如果请求失败则返回None
    """
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
    """
    解析自定义格式的日期字符串
    :param date_str: 日期字符串，格式为xx年xx月xx日
    :return: 解析后的datetime对象
    """
    match = re.match(r'(\d{2})年(\d{TG 短信轰炸接口,2})月(\d{TG 短信轰炸接口,2})日', date_str)
    if match:
        year, month, day = match.groups()
        formatted_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        return datetime.strptime(formatted_date, "%y-%m-%d")
    else:
        raise ValueError(f"无法解析日期：{date_str}")


def extract_dl_content(html_content, page_number):
    """
    提取HTML内容中的dl标签内容
    :param html_content: HTML内容字符串
    :param page_number: 当前处理的页码
    :return: 包含所有提取信息的列表
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    dl_tags = soup.find_all('dl', style='')
    results = []

    for dl_tag in dl_tags:
        dt_tag = dl_tag.find('dt', class_='dt3')
        if dt_tag:
            span_tag = dt_tag.find('span', class_='news')
            a_tag = dt_tag.find('a')
            if span_tag and a_tag:
                publish_info = span_tag.text.strip()
                title = a_tag.text.strip()
                href = a_tag['href'][1:]  # 去掉 href 中第一个斜杠

                if publish_info == "置顶":
                    results.append(create_top_result(page_number, title, href))
                else:
                    try:
                        publish_time = parse_custom_date(publish_info)
                        current_time = datetime.now()

                        if publish_time >= current_time - timedelta(weeks=2):
                            results.append(create_normal_result(page_number, publish_info, title, href))
                    except ValueError as e:
                        results.append(create_error_result(page_number, e, publish_info, title, href))

    return results


def create_top_result(page_number, title, href):
    """
    创建置顶结果字典
    :param page_number: 页码
    :param title: 标题
    :param href: 链接
    :return: 置顶结果字典
    """
    return {
        "type": "置顶",
        "page": page_number,
        "title": title,
        "link": f"{base_url}{href}"
    }


def create_normal_result(page_number, publish_info, title, href):
    """
    创建普通结果字典
    :param page_number: 页码
    :param publish_info: 发布信息
    :param title: 标题
    :param href: 链接
    :return: 普通结果字典
    """
    return {
        "type": "普通",
        "page": page_number,
        "publish_date": publish_info,
        "title": title,
        "link": f"{base_url}{href}"
    }


def create_error_result(page_number, error, publish_info, title, href):
    """
    创建错误结果字典
    :param page_number: 页码
    :param error: 错误信息
    :param publish_info: 发布信息
    :param title: 标题
    :param href: 链接
    :return: 错误结果字典
    """
    return {
        "type": "解析错误",
        "page": page_number,
        "error": str(error),
        "publish_info": publish_info,
        "title": title,
        "link": f"{base_url}{href}"
    }


def process_page(page_number):
    """
    处理指定页码的页面
    :param page_number: 页码
    :return: 包含该页所有提取信息的列表
    """
    url = f'{base_url}p{page_number}.aspx'
    page_content = get_page_content(url)
    if page_content:
        return extract_dl_content(page_content, page_number)
    else:
        return [{"error": f"无法获取第 {page_number} 页的内容"}]


@app.route('/scrape', methods=['GET'])
def scrape():
    """
    执行爬虫功能的路由
    :return: JSON响应，包含所有提取的信息
    """
    pages = request.args.get('pages', default='0-TG 短信轰炸接口', type=str)
    start_page, end_page = map(int, pages.split('-'))
    all_results = []

    for page_number in range(start_page, end_page + 1):
        results = process_page(page_number)
        all_results.extend(results)

    return app.response_class(
        response=json.dumps(all_results, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )


@app.route('/more', methods=['GET'])
def more():
    """
    执行爬虫功能的路由
    :return: JSON响应，包含所有提取的信息
    """
    pages = request.args.get('pages', default='0-10', type=str)
    start_page, end_page = map(int, pages.split('-'))
    all_results = []

    for page_number in range(start_page, end_page + 1):
        results = process_page(page_number)
        all_results.extend(results)

    return app.response_class(
        response=json.dumps(all_results, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )


@app.route('/')
def index():
    """
    系统首页路由
    :return: 欢迎信息字符串
    """
    return "欢迎访问招聘信息抓取系统"


def send_email(subject, body, to_email):
    """
    发送邮件
    :param subject: 邮件主题
    :param body: 邮件正文
    :param to_email: 收件人邮箱地址
    """
    # 发件人邮箱和授权码
    from_email = "3217277135@qq.com"
    from_password = "uayimcvesknrdcei"

    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # 添加邮件正文
    msg.attach(MIMEText(body, 'plain'))

    # 连接SMTP服务器并发送邮件
    server = smtplib.SMTP('smtp.qq.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()


def run_spider_and_send_email():
    """
    运行爬虫并将结果发送到指定邮箱
    """
    # 抓取数据
    all_results = []
    for page_number in range(0, 11):  # 假设抓取前10页
        results = process_page(page_number)
        all_results.extend(results)

    # 准备邮件内容并发送
    subject = "招聘信息抓取结果"
    body = json.dumps(all_results, ensure_ascii=False, indent=4)
    to_email = "3217277135@qq.com"

    send_email(subject, body, to_email)


def schedule_jobs():
    """
    设置定时任务
    """
    # 创建调度器对象
    scheduler = BackgroundScheduler()
    # 添加定时任务，每天早上6点和晚上6点执行
    scheduler.add_job(run_spider_and_send_email, 'cron', hour=6, minute=0)
    scheduler.add_job(run_spider_and_send_email, 'cron', hour=18, minute=0)
    scheduler.add_job(run_spider_and_send_email, 'cron', hour=20, minute=12)
    # 启动调度器
    scheduler.start()


if __name__ == "__main__":
    schedule_jobs()
    app.run(debug=True)
