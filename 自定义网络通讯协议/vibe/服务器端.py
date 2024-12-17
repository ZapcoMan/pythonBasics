import socket
import struct

# 定义协议格式
PROTOCOL_HEADER = b'VIBE'  # 固定的协议开头
HEADER_FORMAT = '!4sHH'  # 4个字节的固定开头，2个字节的数据包类型，2个字节的数据包长度
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

def handle_client(client_socket):
    """
    处理客户端连接

    参数:
    client_socket: 客户端套接字

    返回值:
    无
    """
    while True:
        try:
            # 接收头部
            header = client_socket.recv(HEADER_SIZE)
            if not header:
                print("Connection closed by client")
                break

            # 解析头部
            protocol_header, pkt_type, packet_length = struct.unpack(HEADER_FORMAT, header)
            if protocol_header != PROTOCOL_HEADER:
                print("Invalid protocol header")
                break

            # 接收数据
            data = client_socket.recv(packet_length)
            print(f"Received packet type: {pkt_type}, data: {data.decode('utf-8')}")

            # 处理数据...
            response_data = "Hello, Client!"
            response_bytes = response_data.encode('utf-8')
            response_packet_length = len(response_bytes)
            # 构造响应头部
            response_header = struct.pack(HEADER_FORMAT, PROTOCOL_HEADER, pkt_type, response_packet_length)
            # 发送响应
            client_socket.sendall(response_header + response_bytes)

        except Exception as e:
            print(f"Error handling client: {e}")
            break

    client_socket.close()

def start_server(host, port):
    """
    启动服务器

    参数:
    host: 主机地址
    port: 端口号

    返回值:
    无
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        # 接受客户端连接
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        # 处理客户端连接
        handle_client(client_socket)


if __name__ == "__main__":
    # 启动服务器
    start_server('192.168.1.6', 38745)
