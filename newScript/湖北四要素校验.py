# -*- coding: utf-8 -*-
import requests

def verify_fouryaosu(real_name, idcard, bankcard, mobile):
    url = "https://wsgaj.chutianyun.gov.cn/apis/member/hubei/v3/verify-bankcard"
    headers = {'Host': 'wsgaj.chutianyun.gov.cn', 'Connection': 'keep-alive', 'Content-Length': '130',
               'Accept': 'application/json, text/plain, */*', 'Cache-Control': 'no-cache',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 13; NX679S Build/TKQ1.221013.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20231201 MMWEBID/4362 MicroMessenger/8.0.45.2521(0x28002D34) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
               'Content-Type': 'application/json;charset=UTF-8', 'Origin': 'https://wsgaj.chutianyun.gov.cn',
               'X-Requested-With': 'com.tencent.mm', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Dest': 'empty', 'Referer': 'https://wsgaj.chutianyun.gov.cn/weixin/',
               'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
    data = {"acctName": real_name, "certType": "01", "certNo": idcard, "acctNo": bankcard,
            "mobilePhone": mobile}
    resp = requests.post(url, headers=headers, json=data)
    ret = resp.json()
    # print(resp.json())
    if "msg" in ret:
        res = ret.get("msg", "无结果，请检查接口...")
        print(f"{real_name}, {idcard}, {bankcard}, {mobile} 四要素校验结果: {res}\n")

if __name__ == '__main__':
    verify_fouryaosu(input("请输入姓名: "), input("请输入身份证号: "), input("请输入银行卡号: "), input("请输入手机号: "))