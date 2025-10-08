import requests
# 结果是 不如 网页好用
'''
真离谱
'''

# 定义请求所需的 cookies，用于维持用户登录状态和记录客户端信息
cookies = {
    'buvid3': '7D497DA7-1779-16BB-4C8C-43BE6CBB7D1324915infoc',
    'b_nut': '1734997224',
    '_uuid': '6FB104BA4-7A2D-B87A-A576-41431010211C2B25749infoc',
    'enable_web_push': 'DISABLE',
    'home_feed_column': '4',
    'buvid_fp': 'd59d7c821cc23f5a77321a720ebe2d85',
    'buvid4': '74D06366-BF1F-44E2-F34A-C536B9AB027227372-024122323-x9CtRAD2XTsVHII8nVbKZg%3D%3D',
    'SESSDATA': '3450602d%2C1750549256%2Cb7f2a%2Ac1CjBAekFiT1t6rt8gwZeGveydsmG4EagJiXYOEMAcxa8Ugt-EASo9eJLNHVd-0t8hgnISVldLRjBxUzRvYnAzYXE3Y2E1QkhXalFVT0NuUXlUX1RkcDFxZ2cxUm54cE45YV81VlpWY0hoRUNLUFNRVmpVb19xWndSYWptcjM4Q3ZYN0tZV0ZiUmxBIIEC',
    'bili_jct': '8141e79285ccd8b116f10b63c4f8fe04',
    'DedeUserID': '544166891',
    'DedeUserID__ckMd5': 'ed1a512ca38f5634',
    'sid': '80cfckhu',
    'CURRENT_FNVAL': '16',
    'rpdid': "|(Ju|mlmk|k0J'u~JRmm~kY)",
    'header_theme_version': 'CLOSE',
    'bp_t_offset_544166891': '1014320466128535552',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzUyNjQxMTksImlhdCI6MTczNTAwNDg1OSwicGx0IjotMX0.eimKEC9LwFI3BRIxaLYqfRR_UFWellr0_F7kp74KcCA',
    'bili_ticket_expires': '1735264059',
    'b_lsid': 'A58BFED6_193F6942F7F',
    'browser_resolution': '1280-234',
}

# 定义 HTTP 请求头，模拟浏览器行为并设置必要的字段（如 referer、user-agent）
headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'text/plain',
    # 'cookie': "buvid3=7D497DA7-1779-16BB-4C8C-43BE6CBB7D1324915infoc; b_nut=1734997224; _uuid=6FB104BA4-7A2D-B87A-A576-41431010211C2B25749infoc; enable_web_push=DISABLE; home_feed_column=4; buvid_fp=d59d7c821cc23f5a77321a720ebe2d85; buvid4=74D06366-BF1F-44E2-F34A-C536B9AB027227372-024122323-x9CtRAD2XTsVHII8nVbKZg%3D%3D; SESSDATA=3450602d%2C1750549256%2Cb7f2a%2Ac1CjBAekFiT1t6rt8gwZeGveydsmG4EagJiXYOEMAcxa8Ugt-EASo9eJLNHVd-0t8hgnISVldLRjBxUzRvYnAzYXE3Y2E1QkhXalFVT0NuUXlUX1RkcDFxZ2cxUm54cE45YV81VlpWY0hoRUNLUFNRVmpVb19xWndSYWptcjM4Q3ZYN0tZV0ZiUmxBIIEC; bili_jct=8141e79285ccd8b116f10b63c4f8fe04; DedeUserID=544166891; DedeUserID__ckMd5=ed1a512ca38f5634; sid=80cfckhu; CURRENT_FNVAL=16; rpdid=|(Ju|mlmk|k0J'u~JRmm~kY); header_theme_version=CLOSE; bp_t_offset_544166891=1014320466128535552; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzUyNjQxMTksImlhdCI6MTczNTAwNDg1OSwicGx0IjotMX0.eimKEC9LwFI3BRIxaLYqfRR_UFWellr0_F7kp74KcCA; bili_ticket_expires=1735264059; b_lsid=A58BFED6_193F6942F7F; browser_resolution=1280-234",
    'origin': 'https://www.bilibili.com',
    'priority': 'u=1, i',
    'referer': 'https://www.bilibili.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

# 设置查询参数，指定日志类型及压缩选项
params = {
    'content_type': 'pbrequest',
    'logid': '021436',
    'disable_compression': 'true',
}

# 构造要发送的数据体，使用预定义的二进制数据
data = '\n\x8e\b\n\x06021436\x12/333.1007.first_level_zone_navigation.more.click\x1aÒ\a\n|\bd\x10\x05\x1a.7D497DA7-1779-16BB-4C8C-43BE6CBB7D1324915infoc ë§½\x83\x02*\n17349972242\b1280*800:\x04-480B d59d7c821cc23f5a77321a720ebe2d85J\x02pc\x12Ì\x03\n\x024g\x12\x19https://www.bilibili.com/"\x051.1.1*\x81\x03{"b_ut":null,"home_version":"V8","in_new_ab":true,"ab_version":{"for_ai_home_version":"V8","tianma_banner_live":"RENDER","in_theme_version":"CLOSE","enable_web_push":"DISABLE","ad_style_version":"NEW"},"ab_split_num":{"for_ai_home_version":182,"tianma_banner_live":182,"in_theme_version":187,"enable_web_push":14,"ad_style_version":182},"uniq_page_id":"1407480508928","is_modern":true}0\x01:\b1280*234b\x14A58BFED6_193F6942F7F\x1a/333.1007.first_level_zone_navigation.more.click"\x03333(¶\x020£¥£¶¿28£¥£¶¿2@¤¥£¶¿2H\x01b«\x01"\x1e\n\x16_BiliGreyResult_method\x12\x04gray"$\n\x1b_BiliGreyResult_grayVersion\x12\x0572719"\x17\n\rmirrorVersion\x12\x061.6.30"9\n\x06spm_id\x12/333.1007.first_level_zone_navigation.more.click"\x0f\n\nis_selfdef\x12\x011z\x1e\n\x16_BiliGreyResult_method\x12\x04grayz$\n\x1b_BiliGreyResult_grayVersion\x12\x0572719z\a\n\x05brandz\a\n\x05modelz\x14\n\x06system\x12\nWindows 10z\x17\n\rmirrorVersion\x12\x061.6.30'.encode()

# 发送 POST 请求到 Bilibili 的日志接口，并传递 cookies、headers 和 body 数据
response = requests.post('https://data.bilibili.com/v2/log/web', params=params, cookies=cookies, headers=headers, data=data)

# 打印服务器响应内容
print(response.text)
