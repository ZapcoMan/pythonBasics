import csv

import requests
# 打开CSV文件准备写入数据
f = open('单个商品搜索数据.csv', mode='w', newline='', encoding='utf-8')
writer = csv.writer(f)
# 创建DictWriter对象，指定列名
csv_writer = csv.DictWriter(f, fieldnames=[
    '价格',
    '标签',
    '产品简介',
    '标题',
    '昵称',
    '区域',
    '标题详情',
])
# 写入表头
csv_writer.writeheader()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Referer": "https://www.goofish.com/",
    "Cookie": "t=333d89bdd8d3c7f1680d61c314977359; tracknick=tb575736359; cna=5dFRIU3sMHMBASQJijx6xuFX; isg=BA4O1Z6E6rPx1V7kM_eYllnfX-TQj9KJBFr77zhXA5HMm671oBaHmbdQ18f3hsqh; cookie2=1bd479bb51a7304737dd39912bcce0eb; _samesite_flag_=true; sgcookie=E100lSj5ts%2Bd9eb0HAVpdFmW%2BsVh9FYgXvUZuwcDxh0BtMKbwlSXJGs5OlNCOdjXKrrUB4oRAn7SpNlLypY%2BSmUclm%2Fn0PN6lsfI%2FDaqY7Dmno6l%2F5%2BZX8Jlqq1URukGipG2; csg=2de4d3fd; _tb_token_=3f65e75e137d5; unb=2209968140617; sdkSilent=1759879902293; xlly_s=1; mtop_partitioned_detect=1; _m_h5_tk=9a7fd05c49b25d5075fab51a234be307_1759808103035; _m_h5_tk_enc=c4118ef3c44e5a8a979739e9dba2c653; tfstk=gBw-nFcf0ZbkVK8y2yfcKGNY-0IcssqzZzr6K20kOrUYfl8oO8DuJBUuYycCzY2LkkaO4DbzK3P4Sl9uE_kHpYkEdNbGIOmz4vkB0iYP2UJjbD6HVLgIUxO_ruBOIOqzV3m5jo6gKL3BIDuIdbGIcKgqvpOQRXgjlqoEAUiBFiEjuqiBRpOSlniixeT7RvsYcqoEVvG7RxsxYqgIdvGkzg32V0pLNHUa4cQlNCRaH0h-Jp0vpVwDIb01eq9ppqzIwQqSkp9QHWdeq235_n0EE4rq2yWwUYGLO8DbFZ6IC5zYpfMOtgkTDSViwSQWpq2ouf2SBH67DY3-1-h6vdz_DkNiM-j1QYHSPWDzxhQuD8Uu4-EHAIM-EShTeA6wP2V0XJnLLwWYWkZaOjepyglzIRHPLF0txQsADBRENmRxupw3Fgv2Bm3GVbOeTXmqDVjADBRENmoxSg9WTBln0"
}

url = "https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search/1.0/"

params = {
    "jsv": "2.7.2",
    "appKey": "34839810",
    "t": "1759795344200",
    "sign": "8e4f63f339cc4eaea8dc3a9a778a94a5",
    "v": "1.0",
    "type": "originaljson",
    "accountSite": "xianyu",
    "dataType": "json",
    "timeout": "20000",
    "api": "mtop.taobao.idlemtopsearch.pc.search",
    "sessionOption": "AutoLoginOnly",
    "spm_cnt": "a21ybx.search.0.0",
    "spm_pre": "a21ybx.search.searchInput.0"
}

data = {
    'data':'{"pageNumber":1,"keyword":"python爬虫","fromFilter":false,"rowsPerPage":30,"sortValue":"","sortField":"","customDistance":"","gps":"","propValueStr":{},"customGps":"","searchReqFromPage":"pcSearch","extraFilterValue":"{}","userPositionJson":"{}"}'
}

response = requests.post(url, headers=headers, params=params, data=data)
json_data = response.json()
# pprint(json_data)
resultList = json_data['data']['resultList']
# pprint(resultList)
for item in resultList:
    try:
        main = item['data']['item']['main']
        # pprint(main)
        fishTags_keys = main['exContent']['fishTags'].keys()
        if 'r2' in fishTags_keys:
            tagname = ''.join([i['utParams']['args']['content']for i in main['exContent']['fishTags']['r2']['tagList']])
        else:
            tagname = '无'
        dit = {
            '价格':main['clickParam']['args']['price'],
            '标签':main['clickParam']['args']['tagname'],
            '产品简介':tagname,
            '标题':main['exContent']['detailParams']['title'],
            '昵称':main['exContent']['userNickName'],
            '区域':main['exContent']['area'],
            '标题详情':main['exContent']['title'],
        }
        print(dit)
        csv_writer.writerow(dit)
        # break
    except Exception as e:
        # 捕获其他未预期的异常并打印详细信息，但不中断程序执行
        print(f"未预期的错误: {type(e).__name__}: {e}")
        pass