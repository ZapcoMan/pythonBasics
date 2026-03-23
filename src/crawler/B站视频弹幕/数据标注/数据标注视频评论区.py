import json
import random
import requests

# Bilibili API URL for fetching reply data
Url = 'https://api.bilibili.com/x/v2/reply/wbi/main?oid=115677092512169&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid=f3f3779e36f2e7dee6095fd18cd0b3b6&wts=1774276504'

# User-Agent 列表，用于模拟不同的浏览器请求
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
]

# 构造请求头，包含随机选择的User-Agent和Cookie信息
headers = {
    'User-Agent': random.choice(user_agents),
    'Cookie': 'buvid3=FD4ACF55-91A3-A459-A0DB-DA90BBAA05FC75428infoc; b_nut=1771763275; _uuid=FBEABAA3-E10CF-BC45-2418-B75B106B5887580244infoc; buvid_fp=3863b9b4df3df55879de9f6cfc34c840; buvid4=28826CB1-6960-F560-5246-3687B13BEAC584835-026022220-hYYTO9YdfwGYr9pHQiiuU6vMM0itERjpuOVL4siYW1wB2i4sA9sGzuJgnM5VjO0O; rpdid=0zbfAHP0Ty|VILTYSbF|4bY|3w1VU8zP; SESSDATA=00b6ac65%2C1787323867%2C2ea7d%2A22CjDs_Ry6CslJPgxAGvc9RcwrdpHvDx5W_0bTbmXnyOzOzbyvtCzMw77yHICa2J-C1jsSVktEM25iSDJ3Wkw3X3pXWmpaRWlMbkZySnU3UF96bEh3VHNFb1BXNmxoYVhkWXM0a3ZXT2p2cC1ZbXhYZWVibXR1akh3bGhzUThKcUdRR3Rjc25IMHNnIIEC; bili_jct=d41ce5b5fd53688682a21bfcb643e5a9; DedeUserID=544166891; DedeUserID__ckMd5=ed1a512ca38f5634; sid=77usnso0; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; theme-switch-show=SHOWED; theme_style=dark; CURRENT_QUALITY=80; hit-dyn-v2=1; PVID=1; LIVE_BUVID=AUTO8617720258274935; home_feed_column=5; bp_t_offset_544166891=1182941053968187392; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzQ1MjUzNDYsImlhdCI6MTc3NDI2NjA4NiwicGx0IjotMX0.J31oB-DKqP7-zR-z0T_JiFo3uGKyU8K4fgkNWiCr7Fs; bili_ticket_expires=1774525286; browser_resolution=2560-1271; CURRENT_FNVAL=4048; share_source_origin=COPY; bsource=share_source_copy_link; b_lsid=CB7DB197_19D1B1EE938'
}

# 发起GET请求，获取数据
response = requests.get(url=Url, headers=headers)
# 将响应内容解析为JSON
jsonData = response.json()

# 将 jsonData 保存成json 文件
with open('数据标注视频评论.json', 'w', encoding='utf-8') as f:
    # 写入文件，确保字符正确编码，且格式化输出
    json.dump(jsonData, f, ensure_ascii=False, indent=4)
