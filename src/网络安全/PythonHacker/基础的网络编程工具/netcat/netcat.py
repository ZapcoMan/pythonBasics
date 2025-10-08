# -*- coding: utf-8 -*-
# @Time    : 19 2月 2025 10:28下午
# @Author  : codervibe
# @File    : netcat.py
# @Project : pythonBasics
import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading
import logging

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NetCat:
    """
    NetCat类用于实现网络连接相关的功能。
    """
    def __init__(self, args, buffer=None):
        """
        初始化NetCat类。

        参数:
        - args: 命令行参数。
        - buffer: 缓存数据。
        """
        self.args = args
        self.buffer = buffer
        # 创建一个TCP套接字
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置套接字选项，以便地址可以重用
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        """
        根据命令行参数决定是监听还是发送数据。
        """
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        """
        发送数据到目标主机和端口。
        如果有缓存数据，则先发送缓存数据。
        """
        try:
            self.socket.connect((self.args.target, self.args.port))
            if self.buffer:
                self.socket.send(self.buffer)
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            logging.info('User terminated.')
        except Exception as e:
            logging.error(f'Error during send: {e}')
        finally:
            self.socket.close()

    def handle(self, client_socket):
        """
        处理客户端请求。

        参数:
        - client_socket: 客户端套接字。
        """
        try:
            if self.args.execute:
                # 如果有命令要执行，则执行命令并将输出发送回客户端
                output = execute(self.args.execute)
                client_socket.send(output.encode())
            elif self.args.upload:
                # 如果有文件要上传，则接收文件数据并保存到指定路径
                file_buffer = b''
                while True:
                    data = client_socket.recv(4096)
                    if data:
                        file_buffer += data
                    else:
                        break
                with open(self.args.upload, 'wb') as f:
                    f.write(file_buffer)
                message = f'Saved file {self.args.upload}'
                client_socket.send(message.encode())

            elif self.args.command:
                # 如果是命令行模式，则循环接收命令并执行，将结果发送回客户端
                cmd_buffer = b''
                while True:
                    client_socket.send(b'BHP: #> ')
                    while b'\n' not in cmd_buffer:
                        data = client_socket.recv(64)
                        if not data:
                            break
                        cmd_buffer += data
                    if not cmd_buffer:
                        break
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
        except Exception as e:
            logging.error(f'Error handling client: {e}')
        finally:
            client_socket.close()

    def listen(self):
        """
        监听指定端口并接受连接。
        """
        try:
            self.socket.bind((self.args.target, self.args.port))
            self.socket.listen(5)
            while True:
                client_socket, _ = self.socket.accept()
                client_thread = threading.Thread(
                    target=self.handle, args=(client_socket,)
                )
                client_thread.start()
        except Exception as e:
            logging.error(f'Error listening: {e}')
        finally:
            self.socket.close()


def execute(cmd):
    """
    执行命令并返回输出结果。

    参数:
    - cmd: 要执行的命令。

    返回:
    - output: 命令执行的输出结果。
    """
    cmd = cmd.strip()
    if not cmd:
        return
    try:
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        logging.error(f'Command failed: {e}')
        return f'Command failed: {e.output.decode()}'
    except Exception as e:
        logging.error(f'Error executing command: {e}')
        return f'Error executing command: {e}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example usage:
            netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port
            netcat.py -t 192.168.1.108 -p 5555 # connect to server
        '''))
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
    nc = NetCat(args, buffer.encode())
    nc.run()
