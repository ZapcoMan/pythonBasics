"""
POST /api/v2/module/module_movie_change HTTP/2
Host: api-m3-b.shunchen-gongsi.com
Referer: https://weibo.com
Device-Type: A
X-Request-Data: 7O99tGYZ0AF6xgCt4chemw==
Userid: 115515953
Deviceid: fd8313892f68cb966e37871e2b54218f
Channelid: YYM3ZHU
Allowcrossprotocolredirects: true
Token: b9topbp3AedD27JSimRd57yxd3TXYNFJ
App-Version: 1.9.7
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
Accept-Encoding: gzip, deflate, br
User-Agent: okhttp/4.11.0

page=5&id=271
"""
import requests

# 定义请求头部，包含访问API所需的各类信息和令牌
headers = {
    'Referer': 'https://weibo.com',
    'Device-Type': 'A',
    'X-Request-Data': '7O99tGYZ0AF6xgCt4chemw==',
    'Userid': '115515953',
    'Deviceid': 'fd8313892f68cb966e37871e2b54218f',
    'Channelid': 'YYM3ZHU',
    'Allowcrossprotocolredirects': 'true',
    'Token': 'b9topbp3AedD27JSimRd57yxd3TXYNFJ',
    'App-Version': '1.9.7',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'okhttp/4.11.0'
}

# 定义目标URL，即要请求的API地址
url = 'https://api-m3-b.shunchen-gongsi.com/api/v2/module/module_movie_change'

# 构建请求参数，此处为要传递给API的具体数据
data = {
    'page': 1,
    'id': 271
}

# 发送 POST 请求，并保存返回的响应
response = requests.post(url, headers=headers, data=data)

# 解析响应内容为 JSON 格式，以便于后续处理
json_data = response.text

# 设置响应的编码方式为utf-8，确保正确解析响应内容
response.encoding = 'utf-8'

# 打印解析后的响应内容
print(response.text)
