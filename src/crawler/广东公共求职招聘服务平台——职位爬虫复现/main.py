import csv
from pprint import pprint

import requests

# 打开CSV文件准备写入数据
f = open('data.csv', mode='w', newline='', encoding='utf-8')
writer = csv.writer(f)
# 创建DictWriter对象，指定列名
csv_writer = csv.DictWriter(f, fieldnames=[
    '岗位名称',
    '公司名称',
    '公司规模',
    '工作地区',
    '学历要求',
    '工作经验',
    '薪资',
    '联系电话',
    '工作地点',
    '全职/兼职',
    '岗位描述',
])
# 写入表头
csv_writer.writeheader()

# 设置请求头信息
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Referer": "https://ggfw.hrss.gd.gov.cn/recruitment/internet/main/",
    "Cookie": "Hm_lvt_6ab51e6b7b23ac7b2893ecb75585250d=1759740156; HMACCOUNT=F9272A1A931930E9; Hm_lpvt_6ab51e6b7b23ac7b2893ecb75585250d=1759740747"
}

# 循环爬取多页数据
for current in range(1, 10):
    # 构造职位列表请求URL
    link = 'https://ggfw.hrss.gd.gov.cn/recruitment/internet/main/internet/retrieval/c/recruitment/homepage/positions'
    # 请求参数
    data = {"bce055": "", "acb241": "", "acb242": "", "aab056": "", "lately": -1, "bze433": "", "aac011": "", "aae162": "",
            "acb239": "", "acb204": "440000000000", "acb204Name": "广东省", "gzxz": "0", "releaseType": "1",
            "pageTag": "01", "acb118": None, "bae045": "05", "orderType": "01", "current": current, "size": 40, "bcb687": ""}

    # 发送POST请求获取职位列表
    link_data = requests.post(link, json=data, headers=headers)
    jsonLinkData = link_data.json()
    records = jsonLinkData['data']['records']

    # 遍历职位列表，逐个获取详细信息
    for record in records:
        # 构造职位详情页URL
        url = "https://ggfw.hrss.gd.gov.cn/recruitment/internet/main/internet/r/c/webpage/homepage/position/detail/" + record['bcb009']

        # 发送GET请求获取职位详情
        response = requests.get(url, headers=headers)
        json_data = response.json()

        # 提取所需字段信息
        dit = {
            '岗位名称': json_data['data']['bce055'],
            '公司名称': json_data['data']['aab004'],
            '公司规模': json_data['data']['aab056Name'],
            '工作地区': json_data['data']['acb204Name'],
            '学历要求': json_data['data']['aac011Name'],
            '工作经验': json_data['data']['aae162Name'],
            '薪资': json_data['data']['bcca68'],
            '联系电话': json_data['data']['aae005'],
            '工作地点': json_data['data']['acc530'],
            '全职/兼职': json_data['data']['acb239Name'],
            '岗位描述': json_data['data']['acb22a'],
        }

        # pprint(json_data)
        # pprint(dit)
        # 将数据写入CSV文件
        csv_writer.writerow(dit)

