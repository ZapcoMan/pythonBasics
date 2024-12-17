import socket
import time
import struct

# 定义协议格式
PROTOCOL_HEADER = b'VIBE'  # 固定的协议开头
HEADER_FORMAT = '!4sHH'  # 4个字节的固定开头，2个字节的数据包类型，2个字节的数据包长度
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


class Client:
    """
    客户端类，用于与服务器建立连接并进行数据包的发送和接收。

    Attributes:
        server_address (str): 服务器地址
        server_port (int): 服务器端口
        socket (socket.socket): 套接字对象，用于网络通信
    """

    def __init__(self, server_address, server_port):
        """
        初始化客户端，设置服务器地址和端口，并尝试连接服务器。

        Args:
            server_address (str): 服务器地址
            server_port (int): 服务器端口
        """
        self.server_address = server_address
        self.server_port = server_port
        self.socket = None
        self.connect()

    def connect(self):
        """
        循环尝试连接服务器，直到成功或抛出异常。
        """
        while True:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.server_address, self.server_port))
                print("Connected to server")
                break
            except ConnectionRefusedError:
                print("Connection refused. Retrying...")
                time.sleep(5)

    def send_packet(self, pkt_type, msg_data):
        """
        发送数据包到服务器。

        Args:
            pkt_type (int): 数据包类型
            msg_data (str): 消息数据
        """
        data_bytes = msg_data.encode('utf-8')
        packet_length = len(data_bytes)
        header = struct.pack(HEADER_FORMAT, PROTOCOL_HEADER, pkt_type, packet_length)
        self.socket.sendall(header + data_bytes)

    def receive_packet(self):
        """
        接收服务器发送的数据包。

        Returns:
            tuple: 数据包类型和数据内容，如果连接断开则返回(None, None)
        """
        try:
            header = self.socket.recv(HEADER_SIZE)
            if not header:
                raise ConnectionResetError("Connection closed by server")

            protocol_header, pkt_type, packet_length = struct.unpack(HEADER_FORMAT, header)
            if protocol_header != PROTOCOL_HEADER:
                raise ValueError("Invalid protocol header")

            data = self.socket.recv(packet_length)
            return pkt_type, data.decode('utf-8')
        except ConnectionResetError as e:
            print(f"Connection reset by peer: {e}")
            self.connect()
            return None, None

    def close(self):
        """
        关闭与服务器的连接。
        """
        if self.socket:
            self.socket.close()
            print("Connection closed")


if __name__ == "__main__":

    client = Client('192.168.1.6', 38745)
    try:
        client.send_packet(1, "Hello, Server!")
        while True:
            pkt_type, data = client.receive_packet()
            if pkt_type is None and data is None:
                continue
            print(f"Received packet type: {pkt_type}, data: {data}")
    finally:
        client.close()
