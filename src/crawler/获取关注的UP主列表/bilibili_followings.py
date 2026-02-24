import requests
import json
import sys

def get_followings(user_id, cookies_str, output_file=None):
    """获取B站用户关注的所有UP主"""
    followings = []
    pn = 1
    ps = 50

    # 解析cookies字符串
    cookies = {}
    for item in cookies_str.split('; '):
        if '=' in item:
            key, value = item.split('=', 1)
            cookies[key] = value

    # 添加请求头模拟浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://space.bilibili.com/' + user_id,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Origin': 'https://www.bilibili.com',
    }

    print(f"正在获取用户 {user_id} 的关注列表...")

    while True:
        url = f"https://api.bilibili.com/x/relation/followings?vmid={user_id}&pn={pn}&ps={ps}"
        try:
            response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
            data = response.json()

            if data['code'] != 0:
                print(f"API返回错误: {data.get('message', '未知错误')}")
                break

            list_data = data['data']['list']
            if not list_data:
                break

            followings.extend(list_data)
            print(f"已获取 {len(list_data)} 个UP主 (第 {pn} 页)")
            pn += 1

        except Exception as e:
            print(f"请求出错: {e}")
            break

    print(f"\n总共获取到 {len(followings)} 个关注的UP主\n")

    # 打印结果
    for i, f in enumerate(followings, 1):
        print(f"{i}. {f['uname']} - https://space.bilibili.com/{f['mid']}")

    # 保存到文件
    if output_file:
        result = {
            "total": len(followings),
            "followings": [
                {
                    "name": f['uname'],
                    "mid": f['mid'],
                    "url": f"https://space.bilibili.com/{f['mid']}",
                    "face": f.get('face', ''),
                    "sign": f.get('sign', '')
                }
                for f in followings
            ]
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: {output_file}")

    return followings

if __name__ == "__main__":
    print("=" * 50)
    print("B站关注UP主获取工具")
    print("=" * 50)

    # user_id = "544166891"
    # cookies_str = "buvid3=FD4ACF55-91A3-A459-A0DB-DA90BBAA05FC75428infoc; b_nut=1771763275; _uuid=FBEABAA3-E10CF-BC45-2418-B75B106B5887580244infoc; buvid_fp=3863b9b4df3df55879de9f6cfc34c840; buvid4=28826CB1-6960-F560-5246-3687B13BEAC584835-026022220-hYYTO9YdfwGYr9pHQiiuU6vMM0itERjpuOVL4siYW1wB2i4sA9sGzuJgnM5VjO0O; rpdid=0zbfAHP0Ty|VILTYSbF|4bY|3w1VU8zP; SESSDATA=00b6ac65%2C1787323867%2C2ea7d%2A22CjDs_Ry6CslJPgxAGvc9RcwrdpHvDx5W_0bTbmXnyOzOzbyvtCzMw77yHICa2J-C1jsSVktEM25iSDJ3Wkw3X3pXWmpaRWlMbkZySnU3UF96bEh3VHNFb1BXNmxoYVhkWXM0a3ZXT2p2cC1ZbXhYZWVibXR1akh3bGhzUThKcUdRR3Rjc25IMHNnIIEC; bili_jct=d41ce5b5fd53688682a21bfcb643e5a9; DedeUserID=544166891; DedeUserID__ckMd5=ed1a512ca38f5634; sid=77usnso0; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; theme-switch-show=SHOWED; theme_style=dark; CURRENT_QUALITY=80; home_feed_column=5; browser_resolution=2560-1271; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzIxNTA2NDgsImlhdCI6MTc3MTg5MTM4OCwicGx0IjotMX0.Qxr2ooRcOScsiyx4E0-zGpexTDdEFo8VsjY6Z6S48Hc; bili_ticket_expires=1772150588; CURRENT_FNVAL=4048; bp_t_offset_544166891=1172762750275813376; b_lsid=7FFFA323_19C8D1A587B"
    user_id = "3546731104963406"
    cookies_str = "buvid3=B32AEEAD-55B6-89B8-28BF-0F84F090844572692infoc; b_nut=1771848572; _uuid=3FC84D83-A89F-EE49-6E108-318F87C77F2673397infoc; home_feed_column=4; browser_resolution=1264-641; buvid_fp=55c3488c74210e8d4b5762330063fe83; buvid4=2AE4B47E-4FFC-9DA6-2F1C-B6141F95A20077781-026022320-hYYTO9YdfwGYr9pHQiiuU/bwFH1pZa/Fq1NlBA1pTheaeQMNQHNa0mwcTXNq2u/S; SESSDATA=c474c976%2C1787400602%2C984cf%2A21CjC6pQfyRWm9_jIqM07mFckrqxWpO0_Gk_SR2Zw7ozxRiGcvyXli9-az7y0Y-MUeKqwSVkROSmdlcUwwdGpSRW10TVZqR05JV0dpUDFyMUtJeWtKM3lrQzZfUDdjWm02eHU4ZklnVU5DWDRaNkNGQWxfVnNUcEtYeVdRZEJGWVhDbW1rRzl5MUFBIIEC; bili_jct=59fd69163e2c2ce7532cc360027b66ed; DedeUserID=3546731104963406; DedeUserID__ckMd5=ae6c4bb7c1b0be82; sid=7tfj2h2l; theme-tip-show=SHOWED; CURRENT_FNVAL=4048; CURRENT_QUALITY=0; rpdid=0zbfAHP0Ty|VIMLRO2x|15I|3w1VUuMj; theme-avatar-tip-show=SHOWED; theme-switch-show=SHOWED; theme_style=dark; bp_t_offset_3546731104963406=1172759919892365312; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzIxNTM0MTgsImlhdCI6MTc3MTg5NDE1OCwicGx0IjotMX0.35zd1aLOPG4yglDilsZv6PBw-WHh55HULgAanWo4f10; bili_ticket_expires=1772153358; b_lsid=281C6943_19C8D211872"
    output_file = "C:\\Users\\Administrator\\Desktop\\BeginningAll_bilibili_followings.json"
    get_followings(user_id, cookies_str, output_file)