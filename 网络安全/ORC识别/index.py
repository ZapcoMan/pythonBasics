# -*- coding:utf-8 -*-
# author:f0ngf0ng

import argparse
import ddddocr                       # 导入 ddddocr
from aiohttp import web

parser = argparse.ArgumentParser()
parser.add_argument("-p", help="http port",default="8888")
args = parser.parse_args()

ocr = ddddocr.DdddOcr()
port = 8888

async def handle_cb(request):
    return web.Response(text=ocr.classification(img_base64=await request.text()))

app = web.Application()
app.add_routes([
    web.post('/reg', handle_cb),
])

if __name__ == '__main__':
    web.run_app(app, port=port)
