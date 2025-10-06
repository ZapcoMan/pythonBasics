from pprint import pprint

import requests

from pprint import pprint

import csv

f = open('data.csv', mode='w', newline='', encoding='utf-8')
writer = csv.writer(f)
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
csv_writer.writeheader()
url = "https://ggfw.hrss.gd.gov.cn/recruitment/internet/main/internet/r/c/webpage/homepage/position/detail/1975115582866268161"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Referer": "https://ggfw.hrss.gd.gov.cn/recruitment/internet/main/",
    "Cookie": "Hm_lvt_6ab51e6b7b23ac7b2893ecb75585250d=1759740156; HMACCOUNT=F9272A1A931930E9; Hm_lpvt_6ab51e6b7b23ac7b2893ecb75585250d=1759740747"
}

# 发送GET请求
response = requests.get(url, headers=headers)
json_data = response.json()
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
pprint(dit)
csv_writer.writerow(dit)
