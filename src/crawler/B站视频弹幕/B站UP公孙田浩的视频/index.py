import requests
from lxml import etree
import pandas as pd

# ---------- 配置 ----------
BVID = "BV19R4y1K7yc"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
OUTPUT_CSV = f"公孙田浩弹幕_{BVID}_danmu.csv"

# ---------- 1. 获取所有 P 的 cid ----------
def fetch_cid_list(bvid):
    cid_api = f"https://api.bilibili.com/x/player/pagelist?bvid={bvid}&jsonp=jsonp"
    try:
        response = requests.get(cid_api, headers=headers, timeout=10)
        response.raise_for_status()
        cid_data = response.json()
        return cid_data['data']
    except requests.exceptions.RequestException as e:
        print("请求 cid 列表失败:", str(e))
        raise
    except requests.exceptions.JSONDecodeError:
        print("无法解析JSON响应，响应内容为:", response.text)
        print("状态码:", response.status_code)
        raise

# ---------- 2. 获取弹幕数据 ----------
def fetch_danmu_for_cid(cid, page_index):
    danmu_url = f"https://comment.bilibili.com/{cid}.xml"
    try:
        xml_response = requests.get(danmu_url, headers=headers, timeout=10)
        xml_response.raise_for_status()
        xml_response.encoding = 'utf-8'
        xml_text = xml_response.text.strip()

        if not (xml_text.startswith('<?xml') or xml_text.startswith('<')):
            print(f"第 {page_index} P 弹幕获取异常，内容预览:")
            print(xml_text[:500])
            return []

        root = etree.fromstring(xml_text.encode('utf-8'))
        danmus = []
        for d in root.xpath("//d"):
            p_attr = d.attrib.get("p", "").split(",")
            if len(p_attr) < 8:
                continue
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
        return danmus
    except requests.exceptions.RequestException as e:
        print(f"第 {page_index} P 请求失败:", str(e))
        return []
    except etree.XMLSyntaxError as e:
        print(f"第 {page_index} P XML解析错误:", str(e))
        print(xml_text[:1000])
        return []

# ---------- 主流程 ----------
pages = fetch_cid_list(BVID)
danmus = []

for page in pages:
    cid = page['cid']
    page_index = page.get('page', 1)
    print(f"正在抓取第 {page_index} P 弹幕，cid={cid} ...")
    danmus.extend(fetch_danmu_for_cid(cid, page_index))

print(f"总共抓取弹幕数量: {len(danmus)}")

# ---------- 3. 保存到 CSV ----------
df = pd.DataFrame(danmus)
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"弹幕已保存到 {OUTPUT_CSV}")

# ---------- 4. 输出全部弹幕 ----------
print(f"弹幕内容预览 (共 {len(danmus)} 条):")
for d in danmus:
    safe_output = []
    for item in d.values():
        if isinstance(item, str):
            try:
                item.encode('gbk')
                safe_output.append(item)
            except UnicodeEncodeError:
                safe_output.append(item.encode('gbk', errors='replace').decode('gbk'))
        else:
            safe_output.append(item)
    print(tuple(safe_output))
