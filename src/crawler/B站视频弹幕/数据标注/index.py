import requests
from lxml import etree
import pandas as pd
import json
import random
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba

# ---------- 配置 ----------
# BVID: B站视频的 BV 号，用于获取该视频的所有分 P 信息
# 【《大学生就业避雷第十四期：数据标注》】 https://www.bilibili.com/video/BV1YcmFBzE7s/?share_source=copy_web&vd_source=bf7b15a6934bd320caa6a54c169415d1
BVID = "BV1YcmFBzE7s"

# Cookie（需要替换成你自己的）
COOKIE = 'buvid3=FD4ACF55-91A3-A459-A0DB-DA90BBAA05FC75428infoc; b_nut=1771763275; _uuid=FBEABAA3-E10CF-BC45-2418-B75B106B5887580244infoc; buvid_fp=3863b9b4df3df55879de9f6cfc34c840; buvid4=28826CB1-6960-F560-5246-3687B13BEAC584835-026022220-hYYTO9YdfwGYr9pHQiiuU6vMM0itERjpuOVL4siYW1wB2i4sA9sGzuJgnM5VjO0O; rpdid=0zbfAHP0Ty|VILTYSbF|4bY|3w1VU8zP; SESSDATA=00b6ac65%2C1787323867%2C2ea7d%2A22CjDs_Ry6CslJPgxAGvc9RcwrdpHvDx5W_0bTbmXnyOzOzbyvtCzMw77yHICa2J-C1jsSVktEM25iSDJ3Wkw3X3pXWmpaRWlMbkZySnU3UF96bEh3VHNFb1BXNmxoYVhkWXM0a3ZXT2p2cC1ZbXhYZWVibXR1akh3bGhzUThKcUdRR3Rjc25IMHNnIIEC; bili_jct=d41ce5b5fd53688682a21bfcb643e5a9; DedeUserID=544166891; DedeUserID__ckMd5=ed1a512ca38f5634; sid=77usnso0; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; theme-switch-show=SHOWED; theme_style=dark; CURRENT_QUALITY=80; hit-dyn-v2=1; PVID=1; LIVE_BUVID=AUTO8617720258274935; home_feed_column=5; bp_t_offset_544166891=1182941053968187392; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzQ1MjUzNDYsImlhdCI6MTc3NDI2NjA4NiwicGx0IjotMX0.J31oB-DKqP7-zR-z0T_JiFo3uGKyU8K4fgkNWiCr7Fs; bili_ticket_expires=1774525286; browser_resolution=2560-1271; CURRENT_FNVAL=4048; share_source_origin=COPY; bsource=share_source_copy_link; b_lsid=CB7DB197_19D1B1EE938'

# headers: 请求头配置，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': COOKIE,
    'Referer': 'https://www.bilibili.com',
}

# OUTPUT_CSV: 输出的CSV文件名，格式为"视频标题_弹幕.csv"
OUTPUT_CSV = f"数据标注_{BVID}_danmu.csv"
# 评论输出文件名
COMMENTS_JSON = f"数据标注_{BVID}_comments.json"
# 词云图输出文件名
WORDCLOUD_DANMU_PNG = f"数据标注_{BVID}_danmu_wordcloud.png"
WORDCLOUD_COMMENTS_PNG = f"数据标注_{BVID}_comments_wordcloud.png"

# ---------- 1. 获取所有 P 的 cid ----------
def fetch_cid_list(bvid):
    """
    根据视频的 BV 号获取所有分 P 的 cid 列表。

    参数:
        bvid (str): 视频的 BV 号

    返回:
        list: 包含每个分 P 信息的字典列表，每个字典包含 'cid', 'page' 等字段

    异常:
        requests.exceptions.RequestException: 网络请求失败时抛出
        requests.exceptions.JSONDecodeError: 响应内容无法解析为 JSON 时抛出
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
        print("无法解析 JSON 响应，响应内容为:", response.text)
        print("状态码:", response.status_code)
        raise

# ---------- 2. 获取弹幕数据 ----------
def fetch_danmu_for_cid(cid, page_index):
    """
    根据 cid 获取指定分 P 的弹幕数据。

    参数:
        cid (int): 分 P 对应的 cid
        page_index (int): 当前分 P 的索引编号（从 1 开始）

    返回:
        list: 弹幕信息列表，每个元素是一个包含弹幕属性的字典
    """
    danmu_url = f"https://comment.bilibili.com/{cid}.xml"
    try:
        xml_response = requests.get(danmu_url, headers=headers, timeout=10)
        xml_response.raise_for_status()
        xml_response.encoding = 'utf-8'
        xml_text = xml_response.text.strip()

        # 检查是否是合法的 XML 内容
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
                "mode": int(p_attr[1]),                 # 弹幕类型（1: 滚动，4: 底部，5: 顶部）
                "font_size": int(p_attr[2]),            # 字体大小
                "color": int(p_attr[3]),                # 颜色 RGB 值
                "send_time": p_attr[4],                 # 发送时间戳
                "danmu_pool": p_attr[5],                # 弹幕池分类
                "user_hash": p_attr[6],                 # 用户 ID 哈希值
                "danmu_id": p_attr[7],                  # 弹幕唯一 ID
                "content": d.text                       # 弹幕文本内容
            })
        return danmus
    except requests.exceptions.RequestException as e:
        print(f"第 {page_index} P 请求失败:", str(e))
        return []
    except etree.XMLSyntaxError as e:
        print(f"第 {page_index} P XML 解析错误:", str(e))
        print(xml_text[:1000])
        return []

# ---------- 3. 获取评论数据 ----------
def fetch_comments(oid, pn=1):
    """
    获取指定视频的评论

    参数:
        oid: 视频的 cid
        pn: 页码

    返回:
        list: 评论列表，每条评论包含用户名、内容、点赞数等信息
    """
    api = f"https://api.bilibili.com/x/v2/reply/wbi/main?oid={oid}&type=1&mode=2&pn={pn}&ps=20&plat=1"

    try:
        response = requests.get(api, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data['code'] == 0:
            replies = data['data'].get('replies', [])
            if not replies:
                return []

            comments = []
            for reply in replies:
                comment = {
                    'user': reply['member']['uname'],
                    'content': reply['content']['message'],
                    'like': reply['like'],
                    'reply_count': reply['rcount'],
                    'ctime': reply['ctime'],
                }
                comments.append(comment)

            return comments
        else:
            print(f"评论 API 返回错误：{data['message']}")
            return []
    except Exception as e:
        print(f"评论请求失败：{str(e)}")
        return []

# ---------- 4. 生成词云图 ----------
def generate_wordcloud(text_list, output_path, title="词云图"):
    """
    根据文本列表生成词云图

    参数:
        text_list: 文本内容列表
        output_path: 输出图片路径
        title: 词云图标题
    """
    # 使用 jieba 分词
    text = ' '.join(text_list)
    words = jieba.cut(text)
    word_string = ' '.join(words)

    # 创建词云
    wordcloud = WordCloud(
        font_path='simhei.ttf',  # 中文字体
        width=1920,
        height=1080,
        background_color='white',
        max_words=200,
        max_font_size=300,
        min_font_size=10,
    ).generate(word_string)

    # 显示词云
    plt.figure(figsize=(19.2, 10.8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=30)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\n✅ 词云图已保存为 {output_path}")

# ---------- 主流程 ----------
if __name__ == "__main__":
    print("=" * 60)
    print(f"开始爬取视频 {BVID} 的弹幕和评论")
    print("=" * 60)

    # 步骤 1: 获取 CID
    print("\n【步骤 1】正在获取视频信息...")
    pages = fetch_cid_list(BVID)
    if not pages:
        print("获取视频信息失败")
        exit(1)

    first_cid = pages[0]['cid']
    print(f"✅ 视频 CID: {first_cid}")

    # 步骤 2: 获取弹幕
    print("\n【步骤 2】正在抓取弹幕...")
    danmus = []
    for page in pages:
        cid = page['cid']
        page_index = page.get('page', 1)
        print(f"  → 正在抓取第 {page_index} P 弹幕，cid={cid} ...")
        danmus.extend(fetch_danmu_for_cid(cid, page_index))

    print(f"✅ 总共抓取弹幕数量：{len(danmus)}")

    # 步骤 3: 保存弹幕到 CSV
    print("\n【步骤 3】正在保存弹幕数据...")
    df = pd.DataFrame(danmus)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"✅ 弹幕已保存到 {OUTPUT_CSV}")

    # 步骤 4: 获取评论
    print("\n【步骤 4】正在抓取评论...")
    all_comments = []
    page_num = 1

    while True:
        print(f"  → 正在爬取第 {page_num} 页评论...")
        comments = fetch_comments(first_cid, page_num)

        if not comments:
            print("  → 没有更多评论了")
            break

        all_comments.extend(comments)
        print(f"  → 已获取 {len(comments)} 条评论，总计 {len(all_comments)} 条")

        # 最多爬 10 页
        if page_num >= 10:
            print("  → 已达到最大页数限制")
            break

        page_num += 1
        time.sleep(1)  # 避免请求过快

    print(f"✅ 总共抓取评论数量：{len(all_comments)}")

    # 步骤 5: 保存评论到 JSON
    print("\n【步骤 5】正在保存评论数据...")
    with open(COMMENTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(all_comments, f, ensure_ascii=False, indent=4)
    print(f"✅ 评论已保存到 {COMMENTS_JSON}")

    # 步骤 6: 生成弹幕词云
    print("\n【步骤 6】正在生成弹幕词云...")
    danmu_texts = [d['content'] for d in danmus if d['content']]
    if danmu_texts:
        generate_wordcloud(danmu_texts, WORDCLOUD_DANMU_PNG, "弹幕词云图")
    else:
        print("⚠️ 没有弹幕内容，跳过词云生成")

    # 步骤 7: 生成评论词云
    print("\n【步骤 7】正在生成评论词云...")
    comment_texts = [c['content'] for c in all_comments if c['content']]
    if comment_texts:
        generate_wordcloud(comment_texts, WORDCLOUD_COMMENTS_PNG, "评论词云图")
    else:
        print("⚠️ 没有评论内容，跳过词云生成")

    print("\n" + "=" * 60)
    print("✅ 全部任务完成！")
    print("=" * 60)
    print(f"\n生成的文件:")
    print(f"  📄 弹幕数据：{OUTPUT_CSV}")
    print(f"  📄 评论数据：{COMMENTS_JSON}")
    print(f"  🖼️  弹幕词云：{WORDCLOUD_DANMU_PNG}")
    print(f"  🖼️  评论词云：{WORDCLOUD_COMMENTS_PNG}")
