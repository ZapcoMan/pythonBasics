# -*- coding: utf-8 -*-
# @Time    : 20 2月 2025 1:34 下午
# @Author  : codervibe
# @File    : netcat_Auto_ZhCN.py
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
            if self.args.chinese:
                logging.info('用户终止了程序。')
            else:
                logging.info('User terminated.')
        except Exception as e:
            if self.args.chinese:
                logging.error(f'发送数据时出错: {e}')
            else:
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
                if self.args.chinese:
                    message = f'文件 {self.args.upload} 已保存。'
                else:
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
            if self.args.chinese:
                logging.error(f'处理客户端请求时出错: {e}')
            else:
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
            if self.args.chinese:
                logging.error(f'监听端口时出错: {e}')
            else:
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
        logging.error(f'命令执行失败: {e}')
        return f'命令执行失败: {e.output.decode()}'
    except Exception as e:
        logging.error(f'执行命令时出错: {e}')
        return f'执行命令时出错: {e}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net 工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''示例用法:
            netcat.py -t 192.168.1.108 -p 5555 -l -c # 命令行模式
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # 上传文件
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # 执行命令
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # 发送文本到服务器端口
            netcat.py -t 192.168.1.108 -p 5555 # 连接到服务器
        '''))
    parser.add_argument('-c', '--command', action='store_true', help='命令行模式')
    parser.add_argument('-e', '--execute', help='执行指定命令')
    parser.add_argument('-l', '--listen', action='store_true', help='监听')
    parser.add_argument('-p', '--port', type=int, default=5555, help='指定端口')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='指定IP')
    parser.add_argument('-u', '--upload', help='上传文件')
    parser.add_argument('-C','--chinese', action='store_true', help='使用中文提示')
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
    nc = NetCat(args, buffer.encode())
    nc.run()
