# -*- coding: utf-8 -*-
# @Time    : 19 2月 2025 10:11 下午
# @Author  : codervibe
# @File    : TCP_Server.py
# @Project : pythonBasics
import socket
import threading

# 服务器监听的IP地址和端口号
IP = '0.0.0.0'
PORT = 9998


def handle_client(client_socket):
    """
    处理客户端请求的函数。

    参数:
    - socket: 客户端套接字对象，用于接收和发送数据。

    返回值:
    无
    """
    with client_socket as sock:
        # 接收客户端发送的数据
        request = sock.recv(1024)
        print(f"[*] Received: {request.decode('utf-8')}")
        # 向客户端发送ACK确认消息
        sock.send(b"ACK!")


if __name__ == '__main__':
    # 创建TCP服务器套接字
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定服务器地址和端口
    server.bind((IP, PORT))
    # 监听客户端连接，最多允许5个未完成连接排队
    server.listen(5)
    print(f"Server listening on {IP}:{PORT}")
    while True:
        # 接受客户端连接
        client, address = server.accept()
        print(f"[*] Accepted connection from {address[0]}:{address[1]}")
        # 创建一个新的线程来处理客户端请求
        client_handle = threading.Thread(target=handle_client, args=(client,))
        client_handle.start()
