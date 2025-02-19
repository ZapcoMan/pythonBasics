# -*- coding: utf-8 -*-
# @Time    : 19 2月 2025 10:05 下午
# @Author  : codervibe
# @File    : UDP_client.py
# @Project : pythonBasics
import socket
target_host = '127.0.0.1'
target_port = 8999

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b'AAABBBCCC', (target_host, target_port))
data,address = client.recvfrom(4096)
print(f"{data.decode()}")
client.close()
