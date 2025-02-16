# -*- coding: utf-8 -*-
# @Time    : 16 2月 2025 4:34 下午
# @Author  : codervibe
# @File    : 小红书登录验证码.py
# @Project : pythonBasics
import requests

url = "https://edith.xiaohongshu.com/api/sns/v1/system_service/vfc_code"
params = {
    "phone": "15066427783",
    "zone": "86",
    "type": "login"
}
headers = {
    "Host": "edith.xiaohongshu.com",
    "X-B3-Traceid": "55559532df1c0100",
    "X-Xray-Traceid": "ca86e59b4ac6384a4773fd55b4e33253",
    "X-Legacy-Smid": "202502161604359465a1bdda99e00bd5359b9c03e97d4f016a222ebefd9c24",
    "X-Legacy-Did": "5d4f68e6-fe7a-3bb3-ae4b-ea317994da00",
    "X-Legacy-Fid": "173969307510a288e4665a166514549b7c308b406b59",
    "X-Legacy-Sid": "session.1739693080971325948725",
    "X-Mini-Gid": "7c3f3c5a0aee540a781607dca0a92e4848102b294735917f774bc28c",
    "X-Mini-Sig": "7fb2f47b6575c9794a99aab1311b7c1cacbbdae5f61ccc2aeda46386221196cb",
    "X-Mini-Mua": "eyJhIjoiRUNGQUFGMDEiLCJjIjozOCwiayI6IjQ5ZDQ5NGUzZWY3MjkzZTA4NjU4MDdlYzUxYTY1MThkOGVhZmNiYTc5NjVlZDc5ZDBjNzk3OTc3Y2YzZTYzMGEiLCJwIjoiYSIsInMiOiJkMjU3ZTlmMmQ1ZjlmMjhjMzZjNzE5YWNiN2Q4NjU5NiIsInQiOnsiYyI6NDgsImQiOjcsImYiOjIsInMiOjQwOTgsInQiOjEyMTczNjI4OTksInR0IjpbMV19LCJ1IjoiMDAwMDAwMDAxZWY1MjdiZTExMmZiNGQ4Zjk1ZGYwYWZmYjA4MjIwYSIsInYiOiIyLjcuMTUifQ.CQEMfQoBfMJ-oFFBf5U2qLAWgt6Kn2gsw8V_wNFHRW_ioFtUMqDHZQdoC6Tty8AZThxHPuN9uA06LSKUVgyccJjxbHjhaPQraCQTOhKjb0Ilh22TjRcjuQgg2xRHaL3aGn6WbtvBJ8AlPO7pJIrzcfP0EFiaSQ2v6hoW7M43mGdUUz-QG4IG56qQ72Td1ACpACD2NAXqP-E8S3nQfaVDHmYVZtUliWVvLRQAe85kLDxuBAvR18Ol1xiD6U6yjPG1ay1i0GdN8kYeEopfz0q6hkNRZ8ImUjCbJo8kCvpykIozKeKRU9XkJw2l8L4-lyMgbHgteHlmK5kTY35wYXVeMdVpUmmsnO9YxTNvLdlGlB6C3nS35nd_MZAV3C23fMNoMgmAoRKQI4a0Y-g1m-5lgQuADqIRc16x2iVo9Nw8k945v3ZPOVlZeJjA_5NvsAVuJgFyhRrK_du0yJWL7jqGTxxATU7OezQxsvsWX1JZIyTZXORroLOTRlOxkN0nZCi9F9YtwXZZibY62ZyYU_Kqoq--t1Uit0gCPOZUcUblCrqu4BAMk5ETO-CTpfNfueh2h2R-6l0vgLOotcSWuvek8LjY7BUobWfQsh571AOYDfcMuviOxnyrHzgnAvQ1HLxfLClntYAwPK-aRGouySQpHucCX7lLmLfBTDko4JjT49BZyNApzLx44Nj-c6Qpfb0bdVRxo6cHcIl1O3AslieW0cXaQbvqju3VKU8P66Tc9a1A1UN8y8pEtcna5C0AFIP7GMZJRcRPuFeTevRAXnuFkzKQLUybtugNPtnXqsqcs_UPy6F2wmducdPXme0rSaclPLo5F-mCFO5uCVAVe9o2MRFTQ8GxgEa_HOf9bLsW7ZK9w-53iD7kjXHFc9d9b5cu5JPFKfA75ofjgVK8vTyR8A0ZhmHYf6BcW8uZftMJ2-VP3aNwfwcpQX2yG-AsR0Tmhi5hwLZzPxV6Zzzd7erhkSSXvk2-koiq0w-Dtw9sepiozxI70-x6JA2Pq1vFyv5NQncSwP0_XHJzLfI0_19HJlZrJ6QVNaSII4c9aeJPQ5qxUFz9nGmqsxqrbvhzIxYkrwcLsd0kLvmsBbcBfxfDHI2lDHfG_i0_UL2QUI5ucefwF2FMYRk5xFsyEdW0Pn4j5JwauJ5RLWEXVQz2PegwwCByhvsM0Djo9FY4eDpdtgz9z6RTIGUdSjuys1cyrMM7mPZSaO1kxzT4ReoUalnlxA.",
    "Xy-Common-Params": "fid=173969307510a288e4665a166514549b7c308b406b59&device_fingerprint1=202502161604359465a1bdda99e00bd5359b9c03e97d4f016a222ebefd9c24&gid=7c3f3c5a0aee540a781607dca0a92e4848102b294735917f774bc28c&device_model=phone&tz=Asia%2FShanghai&channel=YingYongBao&versionName=8.70.0&deviceId=5d4f68e6-fe7a-3bb3-ae4b-ea317994da00&platform=android&sid=session.1739693080971325948725&identifier_flag=0&project_id=ECFAAF&x_trace_page_current=login_full_screen_sms_page&lang=zh-Hans&app_id=ECFAAF01&uis=light&teenager=0&device_fingerprint=202502161604359465a1bdda99e00bd5359b9c03e97d4f016a222ebefd9c24&cpu_name=Qualcomm+Technologies%2C+Inc+MSM8996&dlang=zh&launch_id=1739693075&overseas_channel=0&folder_type=none&t=1739693176&build=8700313",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ONEPLUS A3000 Build/QQ3A.200805.001) Resolution/1080*1920 Version/8.70.0 Build/8700313 Device/(OnePlus;ONEPLUS A3000) discover/8.70.0 NetType/WiFi",
    "Referer": "https://app.xhs.cn/",
    "Shield": "XYAAAAAQAAAAEAAABTAAAAUzUWEe0xG1IbD9/c+qCLOlKGmTtFa+lG434JfOFVRa5HkYDmmL4ySp2uqucOz8N4js5+gPc2QgwbQGaJY7L92H8xhuRIdkJveBUW6Qg5IwDr3OWM",
    "Xy-Platform-Info": "platform=android&build=8700313&deviceId=5d4f68e6-fe7a-3bb3-ae4b-ea317994da00",
    "Accept-Encoding": "gzip, deflate, br"
}

response = requests.get(url, headers=headers, params=params)

print(response.status_code)
print(response.text)
