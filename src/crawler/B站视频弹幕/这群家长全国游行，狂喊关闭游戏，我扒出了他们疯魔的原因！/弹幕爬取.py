#
import requests
from lxml import etree
import pandas as pd

# ---------- 配置 ----------
# 目标视频 BV 号
BVID = "BV1cehyzoErb"
# 请求头信息，模拟浏览器访问
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
# 输出CSV文件名
OUTPUT_CSV = f"这群家长全国游行，狂喊关闭游戏，我扒出了他们疯魔的原因！{BVID}_danmu.csv"

# ---------- 1. 获取所有 P 的 cid ----------
# 构造获取视频分P信息的API地址
cid_api = f"https://api.bilibili.com/x/player/pagelist?bvid={BVID}&jsonp=jsonp"
response = requests.get(cid_api, headers=HEADERS)
try:
    # 解析JSON响应数据
    cid_data = response.json()
    pages = cid_data['data']  # 每个元素对应一个分 P
except requests.exceptions.JSONDecodeError:
    print("无法解析JSON响应，响应内容为:", response.text)
    print("状态码:", response.status_code)
    raise

# ---------- 2. 遍历所有 P 获取弹幕 ----------
# 存储所有弹幕数据的列表
danmus = []
# 遍历所有视频分P页面，获取每个页面的弹幕数据
for page in pages:
    cid = page['cid']
    page_index = page.get('page', 1)
    print(f"正在抓取第 {page_index} P 弹幕，cid={cid} ...")
    # 构造弹幕XML文件地址
    danmu_url = f"https://comment.bilibili.com/{cid}.xml"
    xml_response = requests.get(danmu_url, headers=HEADERS)
    xml_response.encoding = 'utf-8'
    xml_text = xml_response.text

    # 检查 XML 是否有效
    if not xml_text.strip().startswith('<?xml') and not xml_text.strip().startswith('<'):
        print(f"第 {page_index} P 弹幕获取异常，内容预览:")
        print(xml_text[:500])
        continue

    # 解析 XML
    try:
        root = etree.fromstring(xml_text.encode('utf-8'))
        # 遍历所有弹幕元素
        for d in root.xpath("//d"):
            p_attr = d.attrib["p"].split(",")
            # 提取弹幕属性信息并添加到列表
            danmus.append({
                "page": page_index,
                "time_in_video": float(p_attr[0]),
                "mode": int(p_attr[1]),
                "font_size": int(p_attr[2]),
                "color": int(p_attr[3]),
                "send_time": p_attr[4],
                "danmu_pool": p_attr[5],
                "user_hash": p_attr[6],
                "danmu_id": p_attr[7],
                "content": d.text
            })
    except etree.XMLSyntaxError as e:
        print(f"第 {page_index} P XML解析错误:", str(e))
        print(xml_text[:1000])
        continue

print(f"总共抓取弹幕数量: {len(danmus)}")

# ---------- 3. 保存到 CSV ----------
# 将弹幕数据转换为DataFrame并保存为CSV文件
df = pd.DataFrame(danmus)
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"弹幕已保存到 {OUTPUT_CSV}")

# ---------- 4. 输出全部弹幕 ----------
# 在控制台输出所有弹幕内容预览
print(f"弹幕内容预览 (共 {len(danmus)} 条):")
# 遍历所有弹幕数据并在控制台输出
for d in danmus:
    try:
        # 尝试直接输出弹幕内容
        print(tuple(d.values()))
    except UnicodeEncodeError:
        # 处理 Windows CMD 中文显示问题
        # 当出现编码错误时，对字符串进行特殊处理以确保正确显示
        safe_output = []
        for item in d.values():
            if isinstance(item, str):
                try:
                    safe_output.append(item)
                except UnicodeEncodeError:
                    # 对无法正常显示的字符串进行编码转换处理
                    safe_output.append(item.encode('gbk', errors='replace').decode('gbk'))
            else:
                safe_output.append(item)
        print(tuple(safe_output))
