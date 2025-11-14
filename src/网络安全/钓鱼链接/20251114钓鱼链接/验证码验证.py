import base64
import json

# 原始数据
data = {"act":"sv","data":{"code":"145638"}}
print(f"原始数据: {data}")

# 第一次Base64编码
json_data = json.dumps(data, separators=(',', ':'))
first_encoded = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
print(f"第一次Base64编码: {first_encoded}")

# 第二次Base64编码
second_encoded = base64.b64encode(first_encoded.encode('utf-8')).decode('utf-8')
print(f"第二次Base64编码: {second_encoded}")

# URL编码
from urllib.parse import quote
url_encoded = quote(second_encoded)
print(f"URL编码后: {url_encoded}")
