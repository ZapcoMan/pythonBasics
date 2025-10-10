import requests
from lxml import etree
import pandas as pd

# ---------- 配置 ----------
# BVID: B站视频的BV号，用于获取该视频的所有分P信息
BVID = "BV19R4y1K7yc"
# headers: 请求头配置，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
# OUTPUT_CSV: 输出的CSV文件名，格式为“视频标题_弹幕.csv”
OUTPUT_CSV = f"公孙田浩弹幕_{BVID}_danmu.csv"

# ---------- 1. 获取所有 P 的 cid ----------
def fetch_cid_list(bvid):
    """
    根据视频的BV号获取所有分P的cid列表。

    参数:
        bvid (str): 视频的BV号

    返回:
        list: 包含每个分P信息的字典列表，每个字典包含 'cid', 'page' 等字段

    异常:
        requests.exceptions.RequestException: 网络请求失败时抛出
        requests.exceptions.JSONDecodeError: 响应内容无法解析为JSON时抛出
    """
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
    """
    根据cid获取指定分P的弹幕数据。

    参数:
        cid (int): 分P对应的cid
        page_index (int): 当前分P的索引编号（从1开始）

    返回:
        list: 弹幕信息列表，每个元素是一个包含弹幕属性的字典
    """
    danmu_url = f"https://comment.bilibili.com/{cid}.xml"
    try:
        xml_response = requests.get(danmu_url, headers=headers, timeout=10)
        xml_response.raise_for_status()
        xml_response.encoding = 'utf-8'
        xml_text = xml_response.text.strip()

        # 检查是否是合法的XML内容
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
                "time_in_video": float(p_attr[0]),      # 弹幕在视频中的出现时间（秒）
                "mode": int(p_attr[1]),                 # 弹幕类型（1: 滚动, 4: 底部, 5: 顶部）
                "font_size": int(p_attr[2]),            # 字体大小
                "color": int(p_attr[3]),                # 颜色RGB值
                "send_time": p_attr[4],                 # 发送时间戳
                "danmu_pool": p_attr[5],                # 弹幕池分类
                "user_hash": p_attr[6],                 # 用户ID哈希值
                "danmu_id": p_attr[7],                  # 弹幕唯一ID
                "content": d.text                       # 弹幕文本内容
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
# 获取所有分P的cid信息
pages = fetch_cid_list(BVID)
danmus = []

# 遍历所有分P并抓取弹幕
for page in pages:
    cid = page['cid']
    page_index = page.get('page', 1)
    print(f"正在抓取第 {page_index} P 弹幕，cid={cid} ...")
    danmus.extend(fetch_danmu_for_cid(cid, page_index))

print(f"总共抓取弹幕数量: {len(danmus)}")

# ---------- 3. 保存到 CSV ----------
# 将弹幕数据转换为DataFrame并保存为CSV文件
df = pd.DataFrame(danmus)
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"弹幕已保存到 {OUTPUT_CSV}")

# ---------- 4. 输出全部弹幕 ----------
# 打印所有弹幕内容，处理可能存在的编码问题
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
