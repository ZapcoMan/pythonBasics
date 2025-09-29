# -*- coding:utf-8 -*-
# author:f0ngf0ng
# 这个脚本是BP 用来自动识别验证码图片的识别脚本
import argparse

# 导入 ddddocr 模块，用于验证码识别
import ddddocr
# 导入 aiohttp 框架，用于创建异步HTTP服务器
from aiohttp import web

# 创建命令行参数解析器
parser = argparse.ArgumentParser()
# 添加端口参数，以便用户指定HTTP服务器的端口
parser.add_argument("-p", help="http port", default="8888")
# 解析命令行参数
args = parser.parse_args()

# 初始化OCR引擎
ocr = ddddocr.DdddOcr()
# 设置HTTP服务器端口
port = 8888

# 定义处理客户端请求的协程函数
async def handle_cb(request):
    # 使用OCR引擎识别请求体中的图片，并返回识别结果
    return web.Response(text=ocr.classification(img_base64=await request.text()))

# 创建aiohttp应用实例
app = web.Application()
# 为应用添加路由规则，指定POST请求到/reg路径时使用handle_cb处理函数
app.add_routes([
    web.post('/reg', handle_cb),
])

# 主程序入口
if __name__ == '__main__':
    # 启动HTTP服务器
    web.run_app(app, port=port)

