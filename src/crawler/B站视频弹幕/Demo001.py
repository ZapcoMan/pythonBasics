import requests
from lxml import etree
import sys

# 设置标准输出编码为utf-8，解决Windows cmd乱码问题
sys.stdout.reconfigure(encoding='utf-8')

# 1. 获取 cid (每个视频分 P 对应一个 cid)
cid_api = "https://api.bilibili.com/x/player/pagelist?bvid=BV1xx411c7mD&jsonp=jsonp"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(cid_api, headers=headers)
try:
    cid_data = response.json()
    cid = cid_data['data'][0]['cid']  # 取第一个分P
except requests.exceptions.JSONDecodeError:
    print("无法解析JSON响应，响应内容为:", response.text)
    print("状态码:", response.status_code)
    raise

# 2. 根据 cid 获取弹幕 XML
danmu_url = f"https://comment.bilibili.com/{cid}.xml"
# 添加headers来避免被反爬虫机制拦截
xml_response = requests.get(danmu_url, headers=headers)
xml_text = xml_response.text

# 检查是否获取到了有效的XML数据
if not xml_text.strip().startswith('<?xml') and not xml_text.strip().startswith('<'):
    print("获取的不是有效的XML数据，实际内容为:")
    print(xml_text[:500])  # 打印前500个字符用于调试
    raise ValueError("获取弹幕数据失败，可能是访问受限")

# 3. 解析 XML
try:
    root = etree.fromstring(xml_text.encode('utf-8'))
    danmus = []
    for d in root.xpath("//d"):
        content = d.text
        p_attr = d.attrib["p"].split(",")
        time_in_video = float(p_attr[0])
        send_time = p_attr[4]
        user_hash = p_attr[6]
        danmus.append((time_in_video, send_time, user_hash, content))
except etree.XMLSyntaxError as e:
    print("XML解析错误:", str(e))
    print("XML内容预览:")
    print(xml_text[:1000])  # 打印前1000个字符用于调试
    raise

# 4. 简单输出
for d in danmus[:10]:
    print(d)
