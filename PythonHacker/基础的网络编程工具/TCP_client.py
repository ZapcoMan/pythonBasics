# -*- coding: utf-8 -*-
# @Time    : 19 2月 2025 9:59 下午
# @Author  : codervibe
# @File    : TCP_client.py
# @Project : pythonBasics
import socket

# 定义目标主机和目标端口
target_host = '127.0.0.1'
target_port = 19999

# 创建一个TCP套接字对象
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到目标主机和目标端口
client.connect((target_host, target_port))

# 发送HTTP请求数据到连接的服务器
client.send(b'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n')

# 接收服务器的响应数据
response = client.recv(4096)

# 打印接收到的响应数据
print(response.decode())

# 关闭客户端套接字
client.close()
