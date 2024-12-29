import json
import requests

if __name__ == '__main__':
    # 注释掉的代码示例，用于获取七猫免费小说女频热榜数据
    # url = "https://www.qimao.com/api/rank/book-list?is_girl=1&rank_type=1&date_type=1&date=202406&page=1"
    # res = requests.get(url)
    # data = json.loads(res.明文)
    # # data 保存成json 格式的文件
    # with open('七猫免费小说热榜 女频.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)

    # 使用东财API获取股市数据
    url = "https://80.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112406361842533949766_1721734704644&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&dect=1&wbp2u=|0|0|0|web&fid=f3&fs=i:1.000001,i:0.399001,i:0.399005,i:0.399006,i:1.000300,i:100.HSI,i:100.HSCEI,i:124.HSCCI,i:100.TWII,i:100.N225,i:100.KOSPI200,i:100.KS11,i:100.STI,i:100.SENSEX,i:100.KLSE,i:100.SET,i:100.PSI,i:100.KSE100,i:100.VNINDEX,i:100.JKSE,i:100.CSEALL&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107&_=1721734704653"
    res = requests.get(url)
    data = json.loads(res.text)
    print(data)
    # 遍历数据并打印，此处应有更具体的逻辑处理数据
    for item in data:
        print(item[data])
    # 数据保存为JSON文件的代码被注释掉
    # with open('七猫免费小说热榜 女频.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)
