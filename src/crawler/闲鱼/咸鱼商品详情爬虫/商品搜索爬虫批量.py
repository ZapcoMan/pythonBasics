import csv
import time
from pprint import pprint

import requests
import hashlib


def get_sign(page_number):
    """
    生成请求签名和相关参数

    该函数根据页面编号生成用于闲鱼搜索接口的签名和时间戳参数。
    通过特定算法生成签名，确保请求能够通过接口验证。

    Args:
        page_number (int): 需要请求的搜索结果页码

    Returns:
        tuple: 包含三个元素的元组
            - str: 时间戳字符串
            - str: 请求数据的JSON字符串
            - str: 生成的MD5签名
    """
    token = '9a7fd05c49b25d5075fab51a234be307'
    '''
    # 原本我也是按照视频里的代码运行但是失败了没有数据过来，于是我就不断比对视频里的代码 和 
    # 我实际上的 数据 以及浏览器请求的参数 最终发现 浏览器请求出去的时间戳和我当前的事件和日期 做出来的时间戳 完全不一致 问过AI 发现两个时间戳 的 差值高达16个小时 
    抓包时间与当前时间的差异：
        1759801941772 对应的时间是 2025-10-06 17:52:21.772
        当前系统时间是 2025-10-07 09:53（左右）
        这说明你是在大约 16 小时前进行的抓包操作
    于是 我就将当前时间戳向后倒了 16个小时果然 数据直接过来了
    '''
    current_timestamp = int(time.time() * 1000)
    print(f"当前时间戳: {current_timestamp}")
    # hours_ago = current_timestamp -   (13 * 60 * 60 * 1000) - (37 * 60 * 1000)
    j = str(current_timestamp)
    # j = str(hours_ago)
    h = '34839810'
    c_data = '{"pageNumber":%d,"keyword":"python爬虫","fromFilter":false,"rowsPerPage":30,"sortValue":"","sortField":"","customDistance":"","gps":"","propValueStr":{},"customGps":"","searchReqFromPage":"pcSearch","extraFilterValue":"{}","userPositionJson":"{}"}' % page_number
    string = token + "&" + j + "&" + h + "&" + c_data
    print(string)
    sign = hashlib.md5(string.encode('utf-8')).hexdigest()

    return j, c_data, sign


# 打开CSV文件准备写入数据
f = open('商品搜索爬虫批量.csv', mode='w', newline='', encoding='utf-8')
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

# 设置请求头信息，包括User-Agent、Referer和Cookie等
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Referer": "https://www.goofish.com/",
    "Cookie": "t=333d89bdd8d3c7f1680d61c314977359; tracknick=tb575736359; cna=5dFRIU3sMHMBASQJijx6xuFX; isg=BA4O1Z6E6rPx1V7kM_eYllnfX-TQj9KJBFr77zhXA5HMm671oBaHmbdQ18f3hsqh; sgcookie=E100lSj5ts%2Bd9eb0HAVpdFmW%2BsVh9FYgXvUZuwcDxh0BtMKbwlSXJGs5OlNCOdjXKrrUB4oRAn7SpNlLypY%2BSmUclm%2Fn0PN6lsfI%2FDaqY7Dmno6l%2F5%2BZX8Jlqq1URukGipG2; unb=2209968140617; xlly_s=1; cookie2=184bb6d7c762f3df2761ff34ab231abd; mtop_partitioned_detect=1; _m_h5_tk=f587cb55a9103086d0a7747176ea0a2c_1759886677213; _m_h5_tk_enc=ac2f8003e269ca5e9de8224ab8d1af52; tfstk=gTWohS9ZZ_R5JIkSZkv7wvvo_pFvNL9BMwHpJpLUgE8jy4HRY2bhuNI-e9Ie-wbvlYC8NBLnxL6AwvL8PpjFWp4TWReOVg96LPUTzeU4Dd-iU4uKaqy2pH0fv_0GVg9Icm3U6sSSxVU9Z3JF8KR2fhve4e-zmI-BYpkyTYlquEteLplyaiy2AHceYwJUmi8XA4JeawR4mHT28pJEZUlyW95N3ylylxCcbz1vqQYN4USRVtuvwbsWogjP33j5-glILvWDqQX4vDNugQCFfC6RXJDXeGf23HXQbXYHs6WJ3Tz4QIOFtw-fGycHS6SR1tdjYbScKUANUImi3iJXYwRhGPD9qLCDsTf7AqSPWUfwFMngyiAGiCt2gDcye1IOdCWzEVTv1HbD6_4iENSyzjlaYKMB0kBqOXOycnYOi15Asi_tyjr0mfIBant6WoqmOXOycnYTmocOdQ-XfFC.."
}

# 循环爬取多页搜索结果数据
for pageNumber in range(1, 8):
    print(f'正在采集第{pageNumber}页的数据内容')
    url = "https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search/1.0/"
    j, c_data, sign = get_sign(pageNumber)

    # 构造请求参数
    params = {
        "jsv": "2.7.2",
        "appKey": "34839810",
        "t": j,
        "sign": sign,
        "v": "1.0",
        "type": "originaljson",
        "accountSite": "xianyu",
        "dataType": "json",
        "timeout": "20000",
        "api": "mtop.taobao.idlemtopsearch.pc.search",
        "sessionOption": "AutoLoginOnly",
        "spm_cnt": "a21ybx.search.0.0",
        "spm_pre": "a21ybx.home.searchHistory.1.4c053da6U2ak7d",
        "log_id": "4c053da6U2ak7d"
    }


    # 构造请求数据
    data = {
        'data': c_data
    }

    # 发送POST请求获取搜索结果
    response = requests.post(url, headers=headers, params=params, data=data)
    json_data = response.json()
    pprint(json_data)
    # exit()
    resultList = json_data['data']['resultList']
    # pprint(resultList)

    # 遍历搜索结果，提取并保存商品信息
    for item in resultList:
        try:
            main = item['data']['item']['main']
            # pprint(main)
            fishTags_keys = main['exContent']['fishTags'].keys()
            if 'r2' in fishTags_keys:
                tagname = ''.join(
                    [i['utParams']['args']['content'] for i in main['exContent']['fishTags']['r2']['tagList']])
            else:
                tagname = '无'
            dit = {
                '价格': main['clickParam']['args']['price'],
                '标签': main['clickParam']['args']['tagname'],
                '产品简介': tagname,
                '标题': main['exContent']['detailParams']['title'],
                '昵称': main['exContent']['userNickName'],
                '区域': main['exContent']['area'],
                '标题详情': main['exContent']['title'],
            }
            print(dit)
            csv_writer.writerow(dit)
            # break
        except KeyError as e:
            print(f"商品缺少字段{e}，跳过: {item}")
        except Exception as e:
            # 捕获其他未预期的异常并打印详细信息，但不中断程序执行
            print(f"未预期的错误: {type(e).__name__}: {e}")
            pass
