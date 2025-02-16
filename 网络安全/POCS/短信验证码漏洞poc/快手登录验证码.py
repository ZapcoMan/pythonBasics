# -*- coding: utf-8 -*-
# @Time    : 16 2月 2025 4:22 下午
# @Author  : codervibe
# @File    : 快手登录验证码.py
# @Project : pythonBasics
import requests

url = "https://apissl.gifshow.com/rest/n/user/requestMobileCode"
params = {
    "earphoneMode": "1",
    "mod": "OnePlus(ONEPLUS A3000)",
    "appver": "13.1.20.40460",
    "isp": "",
    "language": "zh-cn",
    "ud": "0",
    "did_tag": "0",
    "egid": "DFPA31A86F104DEF0867537AB6AF36DDE4C38E36B2507655E8EE843A6BDC60B1",
    "thermal": "10000",
    "net": "WIFI",
    "kcv": "1596",
    "app": "0",
    "kpf": "ANDROID_PHONE",
    "bottom_navigation": "false",
    "ver": "13.1",
    "android_os": "0",
    "oDid": "ANDROID_20371baed3a1c312",
    "boardPlatform": "msm8996",
    "kpn": "KUAISHOU",
    "newOc": "ANDROID_GDT_TX_XXLCXHZT_CPC_DS_GCL6,3",
    "androidApiLevel": "29",
    "slh": "0",
    "country_code": "CN",
    "nbh": "0",
    "hotfix_ver": "",
    "did_gt": "1739690746265",
    "keyconfig_state": "2",
    "cdid_tag": "2",
    "sys": "ANDROID_10",
    "max_memory": "256",
    "cold_launch_time_ms": "1739690716423",
    "oc": "ANDROID_GDT_TX_XXLCXHZT_CPC_DS_GCL6,3",
    "sh": "1920",
    "deviceBit": "0",
    "browseType": "4",
    "ddpi": "420",
    "socName": "Qualcomm MSM8996",
    "is_background": "0",
    "c": "ANDROID_GDT_TX_XXLCXHZT_CPC_DS_GCL6,3",
    "sw": "1080",
    "ftt": "",
    "abi": "arm64",
    "userRecoBit": "0",
    "device_abi": "arm64",
    "icaver": "1",
    "totalMemory": "5733",
    "grant_browse_type": "AUTHORIZED",
    "iuid": "",
    "rdid": "ANDROID_2040cfda11a66266",
    "sbh": "63",
    "darkMode": "false",
    "did": "ANDROID_eaf8078047962614",
    "sig": "d4911ac352c38c702ccd8fa44c9510f5",
    "__NS_sig3": "362752740735844d297e7d7cd614fe419ef5d403626f6177",
    "__NS_xfalcon": "HUDR_sFnX+n5uAUNVsMPNK3DOP5wnti1Lc8Axjy5z88T61A==%24TE_eef1680e0ed2fdff9f80a5d2fdff9f80a5a4a2a7a5927a3d091fb77f8410bb0b8dfc2ca4fff39b7fdef39b5ea5"
}
headers = {
    "X-REQUESTID": "173969100104068043",
    "User-Agent": "kwai-android aegon/4.3.2",
    "Accept-Language": "zh-cn",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Client-Info": "model=ONEPLUS A3000;os=Android;nqe-score=-1;network=WIFI;"
}
data = {
    "mobileCountryCode": "+86",
    "mobile": "3sCt3iAAMzEyODc5NDY0AM8HAO7Jtk8nC4JRDBAAAADanqT08oz8oQBbiNP3ND4j",
    "type": "27",
    "cs": "false",
    "client_key": "3c2cd3f3",
    "videoModelCrowdTag": "1_99",
    "os": "android",
    "uQaTag": ""
}

response = requests.post(url, params=params, headers=headers, data=data)

print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")
