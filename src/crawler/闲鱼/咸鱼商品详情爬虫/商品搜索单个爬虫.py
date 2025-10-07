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
    "Cookie": "t=333d89bdd8d3c7f1680d61c314977359; tracknick=tb575736359; cna=5dFRIU3sMHMBASQJijx6xuFX; isg=BA4O1Z6E6rPx1V7kM_eYllnfX-TQj9KJBFr77zhXA5HMm671oBaHmbdQ18f3hsqh; sgcookie=E100lSj5ts%2Bd9eb0HAVpdFmW%2BsVh9FYgXvUZuwcDxh0BtMKbwlSXJGs5OlNCOdjXKrrUB4oRAn7SpNlLypY%2BSmUclm%2Fn0PN6lsfI%2FDaqY7Dmno6l%2F5%2BZX8Jlqq1URukGipG2; unb=2209968140617; xlly_s=1; cookie2=184bb6d7c762f3df2761ff34ab231abd; mtop_partitioned_detect=1; _m_h5_tk=f587cb55a9103086d0a7747176ea0a2c_1759886677213; _m_h5_tk_enc=ac2f8003e269ca5e9de8224ab8d1af52; tfstk=gRnSd-wxu_fSEjgTPkJVlh37idrB_K-NA9wKIvIPpuER96HTgbPz4pxQ9bVq47kz2T0m_AIr4UqFAuq3vCRwbhyoEkqpsUZrCTqYd8_pYyFRHu2UK2HT_hkoEtEp_C-wb9_WulwL9XU8k-eaM6ed2XEAkRFA2JI8pspbKSEd2yIdkteUITQLeXHvhJVY9kU-9opbKSFLvkh2YswePJHWBkCb0nL87YFfvMnJxzN_pwSCAlw8Pck8G8wSc8a76yCgucm-gvnrqrYlzkDq5XgK6I7zwVwsGPuW1gGsZJhYHbJF--gIpcqur9SE1uGQW0UfpGMT2SqbHcpFSSobaXn7kdS_8onaWu32oQzUVRGKqb6CvfHqQ04mAC1Yt4ygDJiHBwNQJgrCb5a_1w6bSMwb_K9f-wX8QDdOzH2Rlze0ehJXhs_3y-2b_K9f-w48n83whK1f-"
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