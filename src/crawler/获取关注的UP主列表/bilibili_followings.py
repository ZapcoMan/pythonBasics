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

    user_id = "544166891"
    cookies_str = "buvid3=FD4ACF55-91A3-A459-A0DB-DA90BBAA05FC75428infoc; b_nut=1771763275; _uuid=FBEABAA3-E10CF-BC45-2418-B75B106B5887580244infoc; buvid_fp=3863b9b4df3df55879de9f6cfc34c840; buvid4=28826CB1-6960-F560-5246-3687B13BEAC584835-026022220-hYYTO9YdfwGYr9pHQiiuU6vMM0itERjpuOVL4siYW1wB2i4sA9sGzuJgnM5VjO0O; rpdid=0zbfAHP0Ty|VILTYSbF|4bY|3w1VU8zP; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; theme-switch-show=SHOWED; hit-dyn-v2=1; LIVE_BUVID=AUTO8617720258274935; dy_spec_agreed=1; PVID=1; bp_t_offset_3546731104963406=1234882283912036352; DedeUserID=544166891; DedeUserID__ckMd5=ed1a512ca38f5634; theme_style=light; CURRENT_QUALITY=80; home_feed_column=5; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODY5NTY5MzIsImlhdCI6MTc4NjY5NzY3MiwicGx0IjotMX0.-iLxX0qT9p1MwrDYXVBFOhNN6nqhfdXZKZDLiA1DYIg; bili_ticket_expires=1786956872; SESSDATA=dcaa34f5%2C1802249742%2C9a69c%2A82CjBAeznNB9VrQ_qvvhqdiTIEJMIRDrET12nCPTS-nueaRaPjOV00ZHtNdOO4Sjk5tVwSVjZfZGtCTGdKVWRLT3draE1OU2ROOGVGYzFPaE43d1h4X1YtNzZvR0dPT2tYZkp5ZndNNTNCdTBVQlV1YmVXVXliNngwclFWZ1RsU01zb3NhR1Q5a3pRIIEC; bili_jct=c26a35977e57727c2124305868d8a0b0; browser_resolution=2327-1155; sid=8dlt3xcr; CURRENT_FNVAL=4048; bp_t_offset_544166891=1237125489496162304; b_lsid=4641FF32_1A00A619D3D"
    output_file = r"E:\python\Python_project\01_My_Projects\pythonBasics\src\crawler\获取关注的UP主列表\WallyVibe_bilibili_followings.json"
    get_followings(user_id, cookies_str, output_file)
    user_id2 = "3546731104963406"
    cookies_str2 = "buvid3=E0EE41E2-D748-90CC-9607-AD53F10DB6EE40662infoc; b_nut=1786253240; _uuid=215F65AB-6466-17BB-59DA-A432FF669A4C39874infoc; buvid_fp=655563e50400da60f83edb9e725c13a6; buvid4=4490F65C-5455-4F4E-E37B-1C0BD09CF75A06597-026022419-AXmvqGFW9krOnzv5fmWtD/4JiDgwkm+vqvO6I6VDUj56OzwkYck6f14HqUCNGK/7; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; rpdid=|(u~RY~kJ~~u0J'u~)YklJJYk; theme-switch-show=SHOWED; DedeUserID=3546731104963406; DedeUserID__ckMd5=ae6c4bb7c1b0be82; theme_style=light; home_feed_column=5; browser_resolution=2552-1274; CURRENT_QUALITY=64; SESSDATA=e00081de%2C1802267004%2C0a8bf%2A81CjA2D4jEhrQ0mERrRiRmJRXFPn_Gtrckrjm3EANNHuvbdJyuUWyX8FG2VQVmHenI3vUSVktZYUx4aEcxbE1aWnl2dXdkaXRJYjJYTTN5X1dIY3AyVnhObE9zQjM1TXpwRTkyN1ZBeTlDbGNDaUQwaFFidXR1a2trWUNOR19jaGlOb08wcHpLTHlnIIEC; bili_jct=ac3c469b77c0647699a33b641ca138bc; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODcwNjUzMjQsImlhdCI6MTc4NjgwNjA2NCwicGx0IjotMX0.Uyo-r1iMGHyu5rql0nYe8o99JjG7c_NznjPkLvJrGkk; bili_ticket_expires=1787065264; bp_t_offset_3546731104963406=1237105084106539008; CURRENT_FNVAL=4048; b_lsid=93564E17_1A00A6C96BF"
    output_file2 = r"E:\python\Python_project\01_My_Projects\pythonBasics\src\crawler\获取关注的UP主列表\BeginningAll_bilibili_followings.json"
    get_followings(user_id2, cookies_str2, output_file2)
