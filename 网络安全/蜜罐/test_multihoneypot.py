#!/usr/bin/env python3
# test_honeypot.py
# 多协议蜜罐测试脚本

import socket
import ssl
import json
import time
import threading
import requests
from pathlib import Path

# 配置信息
HOST = "127.0.0.1"
PORTS = {
    "tcp": 9000,
    "http": 8080,
    "https": 8443,
    "ssh": 2222,
    "telnet": 2323,
    "ftp": 2121,
}

LOG_FILE = "honeypot_sessions.jsonl"

def test_tcp():
    """测试TCP回显服务"""
    print("测试TCP回显服务...")
    try:
        # 进行多次TCP连接测试
        for i in range(3):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORTS["tcp"]))
                test_msg = f"Hello TCP Honeypot - Test {i+1}!"
                s.sendall(test_msg.encode())
                data = s.recv(1024)
                print(f"TCP回显数据 {i+1}: {data.decode()}")
                time.sleep(0.5)  # 等待一下再进行下次测试
        print("TCP测试完成\n")
    except Exception as e:
        print(f"TCP测试失败: {e}\n")

def test_http():
    """测试HTTP服务"""
    print("测试HTTP服务...")
    try:
        # 进行多次HTTP请求测试
        test_paths = ['/', '/index.html', '/test', '/api/data']
        for i, path in enumerate(test_paths):
            response = requests.get(f"http://{HOST}:{PORTS['http']}{path}", timeout=5)
            print(f"HTTP请求 {i+1} - 路径: {path}, 状态码: {response.status_code}")
            time.sleep(0.5)  # 等待一下再进行下次测试

        # 测试不同的HTTP方法
        methods = ['POST', 'PUT', 'DELETE']
        for i, method in enumerate(methods):
            if method == 'POST':
                response = requests.post(f"http://{HOST}:{PORTS['http']}/test",
                                       data={'key': f'value{i}'}, timeout=5)
            elif method == 'PUT':
                response = requests.put(f"http://{HOST}:{PORTS['http']}/test",
                                      data={'key': f'value{i}'}, timeout=5)
            else:  # DELETE
                response = requests.delete(f"http://{HOST}:{PORTS['http']}/test", timeout=5)
            print(f"HTTP {method} 请求 {i+1}, 状态码: {response.status_code}")
            time.sleep(0.5)

        print("HTTP测试完成\n")
    except Exception as e:
        print(f"HTTP测试失败: {e}\n")

def test_https():
    """测试HTTPS服务"""
    print("测试HTTPS服务...")
    try:
        # 禁用SSL验证，因为使用的是自签名证书
        # 进行多次HTTPS请求测试
        test_paths = ['/', '/secure', '/api/secure-data']
        for i, path in enumerate(test_paths):
            response = requests.get(f"https://{HOST}:{PORTS['https']}{path}",
                                  timeout=5, verify=False)
            print(f"HTTPS请求 {i+1} - 路径: {path}, 状态码: {response.status_code}")
            time.sleep(0.5)  # 等待一下再进行下次测试

        # 测试不同的HTTPS方法
        methods = ['POST', 'PUT', 'DELETE']
        for i, method in enumerate(methods):
            if method == 'POST':
                response = requests.post(f"https://{HOST}:{PORTS['https']}/secure",
                                       data={'key': f'secure_value{i}'},
                                       timeout=5, verify=False)
            elif method == 'PUT':
                response = requests.put(f"https://{HOST}:{PORTS['https']}/secure",
                                      data={'key': f'secure_value{i}'},
                                      timeout=5, verify=False)
            else:  # DELETE
                response = requests.delete(f"https://{HOST}:{PORTS['https']}/secure",
                                         timeout=5, verify=False)
            print(f"HTTPS {method} 请求 {i+1}, 状态码: {response.status_code}")
            time.sleep(0.5)

        print("HTTPS测试完成\n")
    except Exception as e:
        print(f"HTTPS测试失败: {e}\n")

def test_ssh():
    """测试SSH服务（仅测试连接和横幅获取）"""
    print("测试SSH服务...")
    try:
        # 进行多次SSH连接测试
        for i in range(3):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORTS["ssh"]))
                # 接收SSH横幅
                banner = s.recv(1024)
                print(f"SSH连接 {i+1} - 横幅: {banner.decode(errors='ignore')}")
                time.sleep(0.5)  # 等待一下再进行下次测试
        print("SSH测试完成\n")
    except Exception as e:
        print(f"SSH测试失败: {e}\n")

def test_telnet():
    """测试Telnet服务"""
    print("测试Telnet服务...")
    try:
        # 进行多次Telnet会话测试
        for session in range(2):
            print(f"Telnet会话 {session+1}:")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORTS["telnet"]))

                # 接收欢迎横幅
                banner = s.recv(1024)
                print(f"  Telnet横幅: {banner.decode(errors='ignore')}")

                # 发送用户名
                username = f"testuser{session}"
                s.sendall(f"{username}\n".encode())

                # 接收密码提示
                prompt = s.recv(1024)
                print(f"  Telnet密码提示: {prompt.decode(errors='ignore')}")

                # 发送密码
                password = f"testpass{session}"
                s.sendall(f"{password}\n".encode())

                # 接收登录成功消息和提示符
                success = s.recv(1024)
                print(f"  Telnet登录响应: {success.decode(errors='ignore')}")

                prompt = s.recv(1024)
                print(f"  Telnet命令提示符: {prompt.decode(errors='ignore')}")

                # 发送多个测试命令
                test_commands = ["whoami", "get files", "ls -la", "pwd", "help"]
                for i, cmd in enumerate(test_commands):
                    s.sendall(f"{cmd}\n".encode())
                    response = s.recv(1024)
                    print(f"  Telnet命令 {i+1} '{cmd}' 响应: {response.decode(errors='ignore')[:50]}...")
                    prompt = s.recv(1024)  # 获取下一个提示符
                    time.sleep(0.2)  # 命令间稍作停顿

                # 退出
                s.sendall(b"exit\n")
                exit_msg = s.recv(1024)
                print(f"  Telnet退出消息: {exit_msg.decode(errors='ignore')}")

                time.sleep(1)  # 会话间等待
        print("Telnet测试完成\n")
    except Exception as e:
        print(f"Telnet测试失败: {e}\n")

def test_ftp():
    """测试FTP服务"""
    print("测试FTP服务...")
    try:
        # 进行多次FTP会话测试
        for session in range(2):
            print(f"FTP会话 {session+1}:")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORTS["ftp"]))

                # 接收欢迎消息
                welcome = s.recv(1024)
                print(f"  FTP欢迎消息: {welcome.decode(errors='ignore')}")

                # 发送USER命令
                username = f"ftpuser{session}"
                s.sendall(f"USER {username}\n".encode())
                response = s.recv(1024)
                print(f"  FTP USER响应: {response.decode(errors='ignore')}")

                # 发送PASS命令
                password = f"ftppass{session}"
                s.sendall(f"PASS {password}\n".encode())
                response = s.recv(1024)
                print(f"  FTP PASS响应: {response.decode(errors='ignore')}")

                # 发送多个FTP命令
                ftp_commands = ["SYST", "PWD", "CWD /tmp", "PWD", "LIST", "HELP"]
                for i, cmd in enumerate(ftp_commands):
                    s.sendall(f"{cmd}\n".encode())
                    response = s.recv(1024)
                    print(f"  FTP命令 {i+1} '{cmd}' 响应: {response.decode(errors='ignore')[:50]}...")
                    time.sleep(0.2)  # 命令间稍作停顿

                # 发送QUIT命令
                s.sendall(b"QUIT\n")
                response = s.recv(1024)
                print(f"  FTP QUIT响应: {response.decode(errors='ignore')}")

                time.sleep(1)  # 会话间等待
        print("FTP测试完成\n")
    except Exception as e:
        print(f"FTP测试失败: {e}\n")

def check_logs():
    """检查日志文件是否记录了测试操作"""
    print("检查日志记录...")
    try:
        log_path = Path(LOG_FILE)
        if log_path.exists():
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                print(f"日志文件包含 {len(lines)} 条记录")

                # 统计各协议记录数量
                protocol_counts = {}
                for line in lines:
                    try:
                        entry = json.loads(line)
                        protocol = entry.get("protocol", "unknown")
                        protocol_counts[protocol] = protocol_counts.get(protocol, 0) + 1
                    except json.JSONDecodeError:
                        pass

                print("各协议记录数量:")
                for protocol, count in protocol_counts.items():
                    print(f"  {protocol}: {count} 条记录")

                # 显示最近几条记录的详细信息
                print("\n最近5条记录详情:")
                for i, line in enumerate(lines[-5:]):  # 显示最近5条
                    try:
                        entry = json.loads(line)
                        protocol = entry.get("protocol", "unknown")
                        session_id = entry.get("session_id", "N/A")
                        duration = entry.get("duration_seconds", "N/A")
                        remote_ip = entry.get("remote_ip", "N/A")
                        print(f"  记录 {len(lines)-4+i}: 协议={protocol}, "
                              f"会话ID={session_id[:8]}..., "
                              f"持续时间={duration}s, "
                              f"远程IP={remote_ip}")
                    except json.JSONDecodeError:
                        print(f"  记录 {len(lines)-4+i}: 无法解析的JSON")
        else:
            print("日志文件不存在")
    except Exception as e:
        print(f"检查日志失败: {e}")
    print("日志检查完成\n")

def run_all_tests():
    """运行所有测试"""
    print("开始测试多协议蜜罐...\n")

    # 创建线程分别运行各协议测试，避免阻塞
    tests = [
        ("TCP", test_tcp),
        ("HTTP", test_http),
        ("HTTPS", test_https),
        ("SSH", test_ssh),
        ("Telnet", test_telnet),
        ("FTP", test_ftp),
    ]

    threads = []
    for name, test_func in tests:
        print(f"启动{name}测试...")
        thread = threading.Thread(target=test_func, name=name)
        thread.start()
        threads.append(thread)
        time.sleep(1)  # 稍微间隔，避免同时连接过多

    # 等待所有测试完成
    for thread in threads:
        thread.join()

    # 等待一段时间让日志写入
    print("等待日志写入...")
    time.sleep(3)

    # 检查日志
    check_logs()

    print("所有测试完成!")

if __name__ == "__main__":
    run_all_tests()
