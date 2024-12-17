import socket
import threading
import time
import logging

# 目标端口
TARGET_PORT = 24

# 记录攻击者的IP地址
attacker_ips = []
# 用户名和密码
USERNAME = b"honeypot"
PASSWORD = b"password"
# 设置日志记录
logging.basicConfig(filename='honeypot.log', level=logging.INFO, format='%(asctime)s - %(message)s', encoding='utf-8')


def handle_client(client_socket):
    try:
        with client_socket:
            ip_address = client_socket.getpeername()[0]
            logging.info(f"[!] 新的连接: {ip_address}")
            attacker_ips.append(ip_address)

            # 发送SSH协议消息
            client_socket.sendall(b"SSH-2.0-OpenSSH_4.3\r\n")
            client_socket.sendall(b"Server public key is 1024 bit\r\n")
            client_socket.sendall(b"Host key fingerprint is MD5:ab:cd:ef:12:34:56:78:90:ab:cd:ef:12:34:56:78:90\r\n")
            client_socket.sendall(b"SSH-2.0-OpenSSH_4.3\r\n")
            client_socket.sendall(b"No more authentication methods available.\r\n")
            client_socket.sendall(b"Connection closed.\r\n")
            username = client_socket.recv(1024).strip()
            if username == USERNAME:
                client_socket.sendall(b"Password: \r\n")
                password = client_socket.recv(1024).strip()
                if password == PASSWORD:
                    message = "你被我抓到了\r\n"
                    client_socket.sendall(message.encode('utf-8'))
                else:
                    client_socket.sendall(b"Authentication failed.\r\n")
            else:
                client_socket.sendall(b"Authentication failed.\r\n")

            client_socket.sendall(b"Connection closed.\r\n")
            # 模拟一些延迟
            time.sleep(1)

    except Exception as e:
        logging.error(f"处理客户端时出错: {e}")
    finally:
        client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', TARGET_PORT))
    server_socket.listen(5)
    logging.info(f"[*] 蜜罐启动，监听端口 {TARGET_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()
