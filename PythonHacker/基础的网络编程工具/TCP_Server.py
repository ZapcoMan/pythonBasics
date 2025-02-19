# -*- coding: utf-8 -*-
# @Time    : 19 2月 2025 10:11 下午
# @Author  : codervibe
# @File    : TCP_Server.py
# @Project : pythonBasics
import socket
import threading

IP = '0.0.0.0'
PORT = 19999


def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f"[*] Received: {request.decode('utf-8')}")
        sock.send(b"ACK!")


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)
    print(f"Server listening on {IP}:{PORT}")
    while True:
        # 接受客户端连接
        client, address = server.accept()
        print(f"[*] Accepted connection from {address[0]}:{address[1]}")
        client_handle = threading.Thread(target=handle_client, args=(client,))
        client_handle.start()
