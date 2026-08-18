import requests
import json

# 手动输入姓名与身份证号
name = input("请输入姓名：")
credentialsNumber = input("请输入身份证号：")

url = "https://m.xiangdian.com/api/member/mini/member/verified/checkName"

payload = {
    "identityFrontPic": "",
    "identityBackPic": "",
    "credentialsType": "0",
    "credentialsNumber": credentialsNumber,
    "name": name
}

headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 13; M2103K19C Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/142.0.7444.173 Mobile Safari/537.36 XWEB/1420283 MMWEBSDK/20260201 MMWEBID/8329 MicroMessenger/8.0.69.3040(0x2800455B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
    'Content-Type': "application/json",
    'dtdtoken': "自己抓值",
    'auth-token': "自己抓值",
    'loginId': "自己抓值",
    'AKC-OS': "mini-program",
    'AKC-APP-VERSION': "1.0.0",
    'ls': "true",
    'app-request-id': "自己抓值",
    'app-login-channel': "xdApplets",
    'TRACKER-SESSION-ID': "自己抓值",
    'charset': "utf-8",
    'Referer': "https://servicewechat.com/wx5242aafbfd09a262/791/page-frame.html",
    'Cookie': "自己抓值"
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.text)
