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
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORTS["tcp"]))
            s.sendall(b"Hello TCP Honeypot!")
            data = s.recv(1024)
            print(f"TCP回显数据: {data.decode()}")
        print("TCP测试完成\n")
    except Exception as e:
        print(f"TCP测试失败: {e}\n")

def test_http():
    """测试HTTP服务"""
    print("测试HTTP服务...")
    try:
        response = requests.get(f"http://{HOST}:{PORTS['http']}/", timeout=5)
        print(f"HTTP状态码: {response.status_code}")
        print(f"HTTP响应头: {dict(response.headers)}")
        print("HTTP测试完成\n")
    except Exception as e:
        print(f"HTTP测试失败: {e}\n")

def test_https():
    """测试HTTPS服务"""
    print("测试HTTPS服务...")
    try:
        # 禁用SSL验证，因为使用的是自签名证书
        response = requests.get(f"https://{HOST}:{PORTS['https']}/", timeout=5, verify=False)
        print(f"HTTPS状态码: {response.status_code}")
        print(f"HTTPS响应头: {dict(response.headers)}")
        print("HTTPS测试完成\n")
    except Exception as e:
        print(f"HTTPS测试失败: {e}\n")

def test_ssh():
    """测试SSH服务（仅测试连接和横幅获取）"""
    print("测试SSH服务...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORTS["ssh"]))
            # 接收SSH横幅
            banner = s.recv(1024)
            print(f"SSH横幅: {banner.decode(errors='ignore')}")
        print("SSH测试完成\n")
    except Exception as e:
        print(f"SSH测试失败: {e}\n")

def test_telnet():
    """测试Telnet服务"""
    print("测试Telnet服务...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORTS["telnet"]))

            # 接收欢迎横幅
            banner = s.recv(1024)
            print(f"Telnet横幅: {banner.decode(errors='ignore')}")

            # 发送用户名
            s.sendall(b"testuser\n")

            # 接收密码提示
            prompt = s.recv(1024)
            print(f"Telnet密码提示: {prompt.decode(errors='ignore')}")

            # 发送密码
            s.sendall(b"testpass\n")

            # 接收登录成功消息和提示符
            success = s.recv(1024)
            print(f"Telnet登录响应: {success.decode(errors='ignore')}")

            prompt = s.recv(1024)
            print(f"Telnet命令提示符: {prompt.decode(errors='ignore')}")

            # 发送测试命令
            s.sendall(b"whoami\n")
            response = s.recv(1024)
            print(f"Telnet命令响应: {response.decode(errors='ignore')}")

            prompt = s.recv(1024)
            print(f"Telnet新提示符: {prompt.decode(errors='ignore')}")

            # 退出
            s.sendall(b"exit\n")
            exit_msg = s.recv(1024)
            print(f"Telnet退出消息: {exit_msg.decode(errors='ignore')}")

        print("Telnet测试完成\n")
    except Exception as e:
        print(f"Telnet测试失败: {e}\n")

def test_ftp():
    """测试FTP服务"""
    print("测试FTP服务...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORTS["ftp"]))

            # 接收欢迎消息
            welcome = s.recv(1024)
            print(f"FTP欢迎消息: {welcome.decode(errors='ignore')}")

            # 发送USER命令
            s.sendall(b"USER testuser\n")
            response = s.recv(1024)
            print(f"FTP USER响应: {response.decode(errors='ignore')}")

            # 发送PASS命令
            s.sendall(b"PASS testpass\n")
            response = s.recv(1024)
            print(f"FTP PASS响应: {response.decode(errors='ignore')}")

            # 发送SYST命令
            s.sendall(b"SYST\n")
            response = s.recv(1024)
            print(f"FTP SYST响应: {response.decode(errors='ignore')}")

            # 发送PWD命令
            s.sendall(b"PWD\n")
            response = s.recv(1024)
            print(f"FTP PWD响应: {response.decode(errors='ignore')}")

            # 发送QUIT命令
            s.sendall(b"QUIT\n")
            response = s.recv(1024)
            print(f"FTP QUIT响应: {response.decode(errors='ignore')}")

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

                # 显示最近几条记录的协议类型
                for i, line in enumerate(lines[-5:]):  # 显示最近5条
                    try:
                        entry = json.loads(line)
                        protocol = entry.get("protocol", "unknown")
                        print(f"  记录 {len(lines)-4+i}: 协议={protocol}, "
                              f"会话ID={entry.get('session_id', 'N/A')}")
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
        time.sleep(0.5)  # 稍微间隔，避免同时连接过多

    # 等待所有测试完成
    for thread in threads:
        thread.join()

    # 等待一段时间让日志写入
    print("等待日志写入...")
    time.sleep(2)

    # 检查日志
    check_logs()

    print("所有测试完成!")

if __name__ == "__main__":
    run_all_tests()
