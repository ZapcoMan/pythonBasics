#!/usr/bin/env python3
# multi_protocol_honeypot.py
# 多协议蜜罐（单文件）
# 支持协议：TCP（回显）、HTTP、HTTPS（TLS）、SSH（仅横幅）、Telnet、FTP（控制通道最小实现）
# 需要 Python 3.11+

import argparse
import asyncio
import base64
import json
import logging
import ssl
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import random
import re

# ---------------------- 操作员日志记录和默认值 ----------------------
OP_LOG_LEVEL = logging.INFO
logging.basicConfig(level=OP_LOG_LEVEL, format="%(asctime)s [%(levelname)s] %(message)s")
op_logger = logging.getLogger("honeypot_operator")

DEFAULT_LOG_FILE = "honeypot_sessions.jsonl"
# 默认端口（非特权端口，因此无需root权限即可运行）
DEFAULTS = {
    "tcp": 9000,
    "http": 8080,
    "https": 8443,
    "ssh": 2222,
    "telnet": 2323,
    "ftp": 2121,
}

# Telnet配置
TELNET_BANNER = b"\r\n\r\nWelcome to Telnet Server\r\n" + \
         b"Login authentication\r\n\r\n"

TELNET_PROMPT = b"Router> "
TELNET_ENABLE_PROMPT = b"Router# "
TELNET_LOGIN_PROMPT = b"Username: "
TELNET_PASS_PROMPT = b"Password: "

# 模拟网络设备信息
DEVICE_INFO = {
    "hostname": "Router",
    "model": "Cisco IOS Router",
    "version": "12.4(25b)",
    "hardware": "CISCO2811",
    "uptime": "3 days, 14 hours, 25 minutes",
    "interfaces": [
        "FastEthernet0/0", "FastEthernet0/1", "Serial0/0/0"
    ]
}
# ------------------------------------------------------------------------

# ---------------------- 工具函数：JSONL追加（异步安全） ----------------
async def append_jsonl(entry: dict, path: str = DEFAULT_LOG_FILE):
    """
    将条目以JSONL格式异步追加到文件中

    Args:
        entry (dict): 要写入的条目字典
        path (str): 日志文件路径
    """
    loop = asyncio.get_running_loop()
    s = json.dumps(entry, ensure_ascii=False)
    def _write():
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8") as f:
            f.write(s + "\n")
    await loop.run_in_executor(None, _write)

def now_iso():
    """
    获取当前UTC时间的ISO格式字符串

    Returns:
        str: ISO格式的时间字符串
    """
    return datetime.now(timezone.utc).isoformat()

# ---------------------- 工具函数 --------------------------
# 模拟命令执行时间
async def simulate_command_execution(min_time=0.1, max_time=1.5):
    # 模拟命令执行的延迟
    await asyncio.sleep(random.uniform(min_time, max_time))

# 检测是否为自动化扫描工具
def is_automated_scan(data_bytes):
    # 检测常见的nmap探测模式
    data_str = data_bytes.decode('utf-8', errors='ignore')

    # Nmap探测特征
    nmap_patterns = [
        'Nmap', 'script', 'vuln', 'banner', 'ssh', 'telnet',
        '<?xml', 'GET /', 'HEAD /', 'OPTIONS *', 'PUT /', 'POST /'
    ]

    # 检查是否包含任何nmap特征
    for pattern in nmap_patterns:
        if pattern in data_str:
            return True

    return False

# ---------------------- 基础协议处理器 ------------------------------
class ProtocolHandler:
    """
    协议处理器基类，定义所有协议处理器的通用接口和功能
    """

    def __init__(self, name: str, host: str, port: int, log_file: str):
        """
        初始化协议处理器

        Args:
            name (str): 协议名称
            host (str): 监听主机地址
            port (int): 监听端口
            log_file (str): 日志文件路径
        """
        self.name = name
        self.host = host
        self.port = port
        self.log_file = log_file
        self._server: Optional[asyncio.base_events.Server] = None

    async def start(self):
        """
        启动协议处理器
        """
        raise NotImplementedError

    async def stop(self):
        """
        停止协议处理器
        """
        if self._server:
            self._server.close()
            try:
                await self._server.wait_closed()
            except Exception:
                pass
        op_logger.info("%s 处理器已停止", self.name)

    async def persist(self, session_entry: dict):
        """
        持久化会话条目到日志文件

        Args:
            session_entry (dict): 会话条目数据
        """
        # 强制添加协议字段并写入
        session_entry.setdefault("protocol", self.name)
        try:
            await append_jsonl(session_entry, path=self.log_file)
        except Exception:
            op_logger.exception("持久化失败 %s", self.name)

# ---------------------- Telnet处理器（交互式伪shell） ----------
class TelnetHandler(ProtocolHandler):
    """
    Telnet协议处理器，模拟Telnet服务端并记录客户端交互
    """

    def __init__(self, host, port, log_file):
        """
        初始化Telnet处理器

        Args:
            host (str): 监听主机地址
            port (int): 监听端口
            log_file (str): 日志文件路径
        """
        super().__init__("telnet", host, port, log_file)

    async def start(self):
        """
        启动Telnet服务器
        """
        self._server = await asyncio.start_server(self._handle_client, host=self.host, port=self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
        op_logger.info("Telnet监听于 %s", addrs)
        # 在后台运行serve_forever
        asyncio.create_task(self._server.serve_forever())

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        处理Telnet客户端连接

        Args:
            reader (asyncio.StreamReader): 用于从连接中读取数据的流读取器
            writer (asyncio.StreamWriter): 用于向连接写入数据的流写入器
        """
        peer = writer.get_extra_info("peername") or ("unknown", 0)
        session_id = str(uuid.uuid4())
        start_ts = datetime.now(timezone.utc)
        raw_buf = bytearray()
        inputs = []
        login_text = None
        pwd_text = None

        op_logger.info("Telnet新连接 %s 会话=%s", peer, session_id)
        try:
            # 发送系统Banner，模拟真实设备的延迟
            await asyncio.sleep(random.uniform(0.1, 0.5))
            writer.write(TELNET_BANNER)
            await writer.drain()

            # 检查是否有初始数据（可能是扫描工具）
            try:
                # 设置较短的超时时间来检测快速扫描
                initial_data = await asyncio.wait_for(reader.readline(), timeout=1.0)
                if initial_data:
                    raw_buf.extend(initial_data)

                    # 检查是否为扫描工具
                    if is_automated_scan(initial_data):
                        op_logger.info("检测到自动化扫描工具，会话=%s", session_id)
                        # 对扫描工具做出适当响应
                        if b'GET /' in initial_data or b'HEAD /' in initial_data:
                            # HTTP请求响应
                            writer.write(b"HTTP/1.1 400 Bad Request\r\n")
                            writer.write(b"Content-Type: text/html\r\n")
                            writer.write(b"Connection: close\r\n")
                            writer.write(b"\r\n")
                            writer.write(b"<html><body><h1>400 Bad Request</h1></body></html>\r\n")
                            await writer.drain()
                            await self._close_writer(writer)
                            return
                        elif b'script' in initial_data.lower() or b'nmap' in initial_data.lower():
                            # Nmap脚本扫描响应，模拟SSH服务
                            writer.write(b"SSH-2.0-OpenSSH_7.9p1 Debian-10+deb10u2\r\n")
                            await asyncio.sleep(random.uniform(0.1, 0.5))
                            await self._close_writer(writer)
                            return
                        elif b'OPTIONS *' in initial_data:
                            # WebDAV探测
                            writer.write(b"HTTP/1.1 405 Method Not Allowed\r\n")
                            writer.write(b"Allow: GET, HEAD, POST\r\n")
                            writer.write(b"\r\n")
                            await writer.drain()
                            await self._close_writer(writer)
                            return
            except asyncio.TimeoutError:
                # 没有初始数据，继续正常流程
                pass

            # 基本的假登录序列
            writer.write(TELNET_LOGIN_PROMPT)
            await writer.drain()
            login = await reader.readline()
            if not login:
                await self._close_writer(writer)
                return
            raw_buf.extend(login)
            login_text = login.decode(errors="ignore").strip()
            op_logger.info("会话 %s 登录=%s", session_id, login_text)

            writer.write(TELNET_PASS_PROMPT)
            await writer.drain()
            # 读取密码原始数据（我们将其视为一行）
            password = await reader.readline()
            if not password:
                await self._close_writer(writer)
                return
            raw_buf.extend(password)
            pwd_text = password.decode(errors="ignore").strip()

            # 模拟登录延迟和验证
            await asyncio.sleep(random.uniform(1.0, 3.0))

            # 模拟登录失败重试机制
            login_attempts = 1
            while login_attempts < 3 and (not login_text or not pwd_text):
                if login_attempts > 1:
                    writer.write(b"\r\n% Login invalid\r\n\r\n")
                    # 模拟真实系统在多次失败后的延迟增加
                    await asyncio.sleep(random.uniform(1.0, 2.0) * login_attempts)
                    writer.write(TELNET_LOGIN_PROMPT)
                    await writer.drain()
                    login = await reader.readline()
                    if not login:
                        await self._close_writer(writer)
                        return
                    raw_buf.extend(login)
                    login_text = login.decode(errors="ignore").strip()

                    writer.write(TELNET_PASS_PROMPT)
                    await writer.drain()
                    password = await reader.readline()
                    if not password:
                        await self._close_writer(writer)
                        return
                    raw_buf.extend(password)
                    pwd_text = password.decode(errors="ignore").strip()

                login_attempts += 1

            # 三次登录失败后断开连接
            if login_attempts >= 3 and (not login_text or not pwd_text):
                writer.write(b"\r\n% Login invalid\r\n")
                writer.write(b"% Login timed out after 3 minutes\r\n")
                await writer.drain()
                await self._close_writer(writer)
                return

            # 接受任何凭据（模拟弱密码策略）
            writer.write(b"\r\nUser Access Verification\r\n\r\n")
            await writer.drain()

            # 显示设备信息
            writer.write(f"{DEVICE_INFO['hostname']}>".encode())
            await writer.drain()

            # 进入命令模式
            mode = "user"  # user or enable
            prompt = TELNET_PROMPT

            # 交互循环：读取行，回显预设响应但记录所有内容
            while True:
                data = await reader.readline()
                if not data:
                    break
                raw_buf.extend(data)
                # 尽力解码用于日志记录
                text = data.decode(errors="ignore").rstrip("\r\n")
                inputs.append({"ts": datetime.now(timezone.utc).isoformat(), "input": text})
                op_logger.debug("Telnet %s 输入: %s", session_id, text)

                # 简单命令处理（网络设备命令）
                lowered = text.strip().lower()
                original_text = text.strip()

                if lowered in ("exit", "quit"):
                    writer.write(b"\r\n% Connection closed by foreign host.\r\n")
                    await writer.drain()
                    break
                elif lowered == "logout":
                    writer.write(b"\r\n% Logout successful.\r\n")
                    await writer.drain()
                    break
                elif lowered == "enable":
                    # 进入特权模式
                    mode = "enable"
                    prompt = TELNET_ENABLE_PROMPT
                    writer.write(prompt)
                    await writer.drain()
                    continue
                elif lowered.startswith("disable"):
                    # 退出特权模式
                    mode = "user"
                    prompt = TELNET_PROMPT
                    writer.write(prompt)
                    await writer.drain()
                    continue
                elif lowered == "show version" or lowered == "sh ver":
                    await simulate_command_execution(0.5, 1.5)
                    writer.write(f"\r\nCisco IOS Software, {DEVICE_INFO['hardware']} Software (C2800NM-ADVENTERPRISEK9-M), Version {DEVICE_INFO['version']}, RELEASE SOFTWARE (fc1)\r\n".encode())
                    writer.write(b"Technical Support: http://www.cisco.com/techsupport\r\n")
                    writer.write(b"Copyright (c) 1986-2010 by Cisco Systems, Inc.\r\n")
                    writer.write(b"Compiled Thu 09-Sep-10 13:53 by prod_rel_team\r\n\r\n")
                    writer.write(f"ROM: System Bootstrap, Version 12.4(13r)T11, RELEASE SOFTWARE (fc1)\r\n\r\n".encode())
                    writer.write(f"{DEVICE_INFO['hostname']} uptime is {DEVICE_INFO['uptime']}\r\n".encode())
                    writer.write(b"System returned to ROM by power-on\r\n")
                    writer.write(b"System image file is \"flash:c2800nm-adventerprisek9-mz.124-25b.bin\"\r\n\r\n")
                    writer.write(b"This product contains cryptographic features and is subject to United\r\n")
                    writer.write(b"States and local country laws governing import, export, transfer and\r\n")
                    writer.write(b"use. Delivery of Cisco cryptographic products does not imply\r\n")
                    writer.write(b"third-party authority to import, export, distribute or use encryption.\r\n")
                    writer.write(b"Importers, exporters, distributors and users are responsible for\r\n")
                    writer.write(b"compliance with U.S. and local country laws. By using this product you\r\n")
                    writer.write(b"agree to comply with applicable laws and regulations. If you are unable\r\n")
                    writer.write(b"to comply with U.S. and local laws, return this product immediately.\r\n\r\n")
                    writer.write(b"A summary of U.S. laws governing Cisco cryptographic products may be found at:\r\n")
                    writer.write(b"http://www.cisco.com/wwl/export/crypto/tool/stqrg.html\r\n\r\n")
                    writer.write(b"If you require further assistance please contact us by sending email to\r\n")
                    writer.write(b"export@cisco.com.\r\n\r\n")
                    writer.write(b"cisco {DEVICE_INFO['hardware']} (revision 2.0) with 503808K/24576K bytes of memory.\r\n".encode())
                    writer.write(b"Processor board ID FTX1043A0K8\r\n")
                    writer.write(b"2 FastEthernet interfaces\r\n")
                    writer.write(b"1 Serial interface\r\n")
                    writer.write(b"1 Virtual Private Network (VPN) Module\r\n")
                    writer.write(b"4 Network Processing Engine(s)\r\n")
                    writer.write(b"DRAM configuration is 64 bits wide with parity enabled.\r\n")
                    writer.write(b"255K bytes of non-volatile configuration memory.\r\n")
                    writer.write(b"62464K bytes of ATA CompactFlash (Read/Write)\r\n\r\n")
                    writer.write(b"Configuration register is 0x2102\r\n")
                    await writer.drain()
                elif lowered == "show ip interface brief" or lowered == "sh ip int br":
                    await simulate_command_execution(0.5, 1.2)
                    writer.write(b"\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\n")
                    writer.write(b"FastEthernet0/0            192.168.1.1     YES NVRAM  up                    up      \r\n")
                    writer.write(b"FastEthernet0/1            10.0.0.1        YES NVRAM  administratively down down    \r\n")
                    writer.write(b"Serial0/0/0                unassigned      YES NVRAM  up                    up      \r\n")
                    await writer.drain()
                elif lowered == "show interfaces" or lowered == "sh int":
                    await simulate_command_execution(1.0, 2.5)
                    for interface in DEVICE_INFO["interfaces"]:
                        writer.write(f"\r\n{interface} is up, line protocol is up\r\n".encode())
                        writer.write(b"  Hardware is CNFGT, address is 0000.0000.0000 (bia 0000.0000.0000)\r\n")
                        writer.write(b"  MTU 1500 bytes, BW 100000 Kbit, DLY 100 usec,\r\n")
                        writer.write(b"     reliability 255/255, txload 1/255, rxload 1/255\r\n")
                        writer.write(b"  Encapsulation ARPA, loopback not set\r\n")
                        writer.write(b"  Keepalive set (10 sec)\r\n")
                        writer.write(b"  Full-duplex, 100Mb/s, 100BaseTX/FX\r\n")
                        writer.write(b"  ARP type: ARPA, ARP Timeout 04:00:00\r\n")
                        rx_pkts = random.randint(10000, 999999)
                        tx_pkts = random.randint(10000, 999999)
                        writer.write(f"  Last input 00:00:02, output 00:00:01, output hang never\r\n".encode())
                        writer.write(f"  Last clearing of \"show interface\" counters never\r\n".encode())
                        writer.write(f"  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0\r\n".encode())
                        writer.write(f"  Queueing strategy: fifo\r\n".encode())
                        writer.write(f"  Output queue: 0/40 (size/max)\r\n".encode())
                        writer.write(f"  5 minute input rate 0 bits/sec, 0 packets/sec\r\n".encode())
                        writer.write(f"  5 minute output rate 0 bits/sec, 0 packets/sec\r\n".encode())
                        writer.write(f"     {rx_pkts} packets input, {rx_pkts*random.randint(64, 1500)} bytes\r\n".encode())
                        writer.write(f"     Received {random.randint(0, 10)} broadcasts (0 IP multicasts)\r\n".encode())
                        writer.write(f"     0 runts, 0 giants, 0 throttles\r\n".encode())
                        writer.write(f"     {random.randint(0, 5)} input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored\r\n".encode())
                        writer.write(f"     0 watchdog, 0 multicast, 0 pause input\r\n".encode())
                        writer.write(f"     {tx_pkts} packets output, {tx_pkts*random.randint(64, 1500)} bytes, 0 underruns\r\n".encode())
                        writer.write(f"     0 output errors, 0 collisions, 1 interface resets\r\n".encode())
                        writer.write(f"     0 babbles, 0 late collision, 0 deferred\r\n".encode())
                        writer.write(f"     0 lost carrier, 0 no carrier, 0 PAUSE output\r\n".encode())
                        writer.write(f"     0 output buffer failures, 0 output buffers swapped out\r\n".encode())
                    await writer.drain()
                elif lowered == "show running-config" or lowered == "sh run":
                    await simulate_command_execution(1.5, 3.0)
                    writer.write(b"\r\nBuilding configuration...\r\n\r\n")
                    writer.write(b"Current configuration : 2048 bytes\r\n")
                    writer.write(b"!\r\n")
                    writer.write(b"version 12.4\r\n")
                    writer.write(b"no service pad\r\n")
                    writer.write(b"service timestamps debug datetime msec\r\n")
                    writer.write(b"service timestamps log datetime msec\r\n")
                    writer.write(b"no service password-encryption\r\n")
                    writer.write(b"!\r\n")
                    writer.write(f"hostname {DEVICE_INFO['hostname']}\r\n".encode())
                    writer.write(b"!\r\n")
                    writer.write(b"boot-start-marker\r\n")
                    writer.write(b"boot-end-marker\r\n")
                    writer.write(b"!\r\n")
                    writer.write(b"enable secret 5 $1$1234$abcdefghijklmnopqrstuvwx\r\n")
                    writer.write(b"!\r\n")
                    writer.write(b"username admin privilege 15 password 0 admin\r\n")
                    writer.write(b"username user password 0 password\r\n")
                    writer.write(b"!\r\n")
                    writer.write(b"interface FastEthernet0/0\r\n")
                    writer.write(b" ip address 192.168.1.1 255.255.255.0\r\n")
                    writer.write(b" ip nat inside\r\n")
                    writer.write(b" ip virtual-reassembly\r\n")
                    writer.write(b" duplex auto\r\n")
                    writer.write(b" speed auto\r\n")
                    writer.write(b"!\r\n")
                    writer.write(b"interface FastEthernet0/1\r\n")
                    writer.write(b" no ip address\r\n")
                    writer.write(b" shutdown\r\n")
                    writer.write(b" duplex auto\r\n")
                    writer.write(b" speed auto\r\n")
                    writer.write(b"!\r\n")
                    writer.write(b"interface Serial0/0/0\r\n")
                    writer.write(b" no ip address\r\n")
                    writer.write(b"!\r\n")
                    writer.write(b"ip route 0.0.0.0 0.0.0.0 Serial0/0/0\r\n")
                    writer.write(b"!\r\n")
                    writer.write(b"ip http server\r\n")
                    writer.write(b"no ip http secure-server\r\n")
                    writer.write(b"!\r\n")
                    writer.write(b"control-plane\r\n")
                    writer.write(b"!\r\n")
                    writer.write(b"line con 0\r\n")
                    writer.write(b" exec-timeout 0 0\r\n")
                    writer.write(b" privilege level 15\r\n")
                    writer.write(b" logging synchronous\r\n")
                    writer.write(b"line aux 0\r\n")
                    writer.write(b"line vty 0 4\r\n")
                    writer.write(b" login local\r\n")
                    writer.write(b" transport input telnet\r\n")
                    writer.write(b"!\r\n")
                    writer.write(b"end\r\n")
                    await writer.drain()
                elif lowered == "show startup-config" or lowered == "sh start":
                    await simulate_command_execution(0.8, 1.8)
                    writer.write(b"\r\nstartup-config is not set\r\n")
                    await writer.drain()
                elif lowered == "show users" or lowered == "sh users":
                    await simulate_command_execution(0.3, 0.8)
                    writer.write(b"\r\n    Line       User       Host(s)              Idle       Location\r\n")
                    writer.write(f"   0 con 0                {peer[0]}               00:00:00   \r\n".encode())
                    writer.write(b"*  1 vty 0     admin      192.168.1.100        00:00:02   \r\n")
                    writer.write(b"   2 vty 1                idle                 01:23:45   \r\n")
                    await writer.drain()
                elif lowered == "show processes" or lowered == "sh proc":
                    await simulate_command_execution(0.8, 2.0)
                    writer.write(b"\r\nCPU utilization for five seconds: 1%/0%; one minute: 2%; five minutes: 1%\r\n")
                    writer.write(b" PID Runtime(ms)     Invoked      uSecs   5Sec   1Min   5Min TTY Process\r\n")
                    writer.write(b"   1          12        1605          7  0.00%  0.00%  0.00%   0 Chunk Manager\r\n")
                    writer.write(b"   2           4         542          7  0.00%  0.00%  0.00%   0 Load Meter\r\n")
                    writer.write(b"   3         100        1500         66  0.00%  0.00%  0.00%   0 DHCPD Timer\r\n")
                    writer.write(b"   4        2000       12000        166  0.00%  0.00%  0.00%   0 IP SNMP\r\n")
                    writer.write(b"   5         150        1200        125  0.00%  0.00%  0.00%   0 TCP Timer\r\n")
                    await writer.drain()
                elif lowered == "help":
                    writer.write(b"\r\nCisco CLI Help System\r\n\r\n")
                    writer.write(b"show version                - System hardware and software status\r\n")
                    writer.write(b"show interfaces             - Interface status and configuration\r\n")
                    writer.write(b"show ip interface brief     - Brief IP interface status\r\n")
                    writer.write(b"show running-config         - Current system configuration\r\n")
                    writer.write(b"show startup-config         - Startup configuration\r\n")
                    writer.write(b"show users                  - Display information about terminal lines\r\n")
                    writer.write(b"show processes              - CPU usage statistics\r\n")
                    writer.write(b"enable                      - Turn on privileged commands\r\n")
                    writer.write(b"disable                     - Turn off privileged commands\r\n")
                    writer.write(b"exit                        - Exit from the EXEC\r\n")
                    writer.write(b"logout                      - Exit from the EXEC\r\n")
                    await writer.drain()
                elif lowered.startswith("ping "):
                    await simulate_command_execution(1.0, 2.0)
                    target = original_text[5:].strip()
                    if target:
                        writer.write(f"\r\nType escape sequence to abort.\r\n".encode())
                        writer.write(f"Sending 5, 100-byte ICMP Echos to {target}, timeout is 2 seconds:\r\n".encode())
                        writer.write(b"!!!!!\r\n")
                        writer.write(b"Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/1 ms\r\n")
                    else:
                        writer.write(b"\r\nUsage: ping <target>\r\n")
                    await writer.drain()
                elif lowered.startswith("traceroute "):
                    await simulate_command_execution(1.5, 3.0)
                    target = original_text[11:].strip()
                    if target:
                        writer.write(f"\r\nType escape sequence to abort.\r\n".encode())
                        writer.write(f"Tracing the route to {target}\r\n\r\n".encode())
                        writer.write(b"  1 192.168.1.1 0 msec 0 msec 4 msec\r\n")
                        writer.write(b"  2 10.0.0.1 4 msec 4 msec 4 msec\r\n")
                        writer.write(b"  3 8.8.8.8 8 msec *  8 msec\r\n")
                    else:
                        writer.write(b"\r\nUsage: traceroute <target>\r\n")
                    await writer.drain()
                elif lowered == "reload":
                    writer.write(b"\r\nProceed with reload? [confirm]\r\n")
                    await writer.drain()
                    # 等待确认
                    confirm = await reader.readline()
                    raw_buf.extend(confirm)
                    confirm_text = confirm.decode(errors="ignore").rstrip("\r\n")
                    inputs.append({"ts": datetime.now(timezone.utc).isoformat(), "input": confirm_text})
                    if confirm_text.lower() in ["y", "yes", ""]:
                        writer.write(b"\r\nSystem configuration has been modified. Save? [yes/no]:\r\n")
                        await writer.drain()
                        save_confirm = await reader.readline()
                        raw_buf.extend(save_confirm)
                        save_text = save_confirm.decode(errors="ignore").rstrip("\r\n")
                        inputs.append({"ts": datetime.now(timezone.utc).isoformat(), "input": save_text})
                        writer.write(b"\r\nBuilding configuration...\r\n")
                        writer.write(b"[OK]\r\n")
                        writer.write(b"Reloading...\r\n")
                        await writer.drain()
                        await asyncio.sleep(2)
                        writer.write(b"\r\n% Connection closed by foreign host.\r\n")
                        await writer.drain()
                        break
                    else:
                        writer.write(b"\r\nReload cancelled.\r\n")
                        await writer.drain()
                else:
                    # 通用错误消息，模拟真实网络设备
                    if mode == "user" and lowered.startswith("show"):
                        writer.write(b"\r\n% Incomplete command.\r\n\r\n")
                    else:
                        writer.write(b"\r\n% Ambiguous command:  \"" + original_text.encode() + b"\"\r\n\r\n")
                    await writer.drain()

                writer.write(prompt)
                await writer.drain()

        except asyncio.CancelledError:
            op_logger.info("Telnet会话已取消 %s", session_id)
        except Exception as e:
            op_logger.exception("Telnet处理器错误 %s: %s", session_id, e)
        finally:
            entry = {
                "session_id": session_id,
                "start_time": start_ts.isoformat(),
                "end_time": datetime.now(timezone.utc).isoformat(),
                "duration_seconds": (datetime.now(timezone.utc) - start_ts).total_seconds(),
                "remote_ip": peer[0],
                "remote_port": peer[1],
                "login": login_text,
                "password": "<captured>" if pwd_text else None,
                "inputs": inputs,
                "raw_base64": base64.b64encode(bytes(raw_buf)).decode("ascii"),
            }
            await self.persist(entry)
            await self._close_writer(writer)
            op_logger.info("Telnet关闭会话 %s 来自 %s", session_id, peer)

    async def _close_writer(self, writer):
        """
        安全关闭writer
        """
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

# ---------------------- FTP处理器（控制通道最小实现） -------------
class FTPHandler(ProtocolHandler):
    """
    FTP协议处理器，模拟FTP控制通道并记录客户端交互
    """

    def __init__(self, host, port, log_file):
        """
        初始化FTP处理器

        Args:
            host (str): 监听主机地址
            port (int): 监听端口
            log_file (str): 日志文件路径
        """
        super().__init__("ftp", host, port, log_file)

    async def start(self):
        """
        启动FTP服务器
        """
        self._server = await asyncio.start_server(self._handle_client, host=self.host, port=self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
        op_logger.info("FTP监听于 %s", addrs)
        asyncio.create_task(self._server.serve_forever())

    async def _send_line(self, writer: asyncio.StreamWriter, line: str):
        """
        向客户端发送一行FTP响应

        Args:
            writer (asyncio.StreamWriter): 用于向连接写入数据的流写入器
            line (str): 要发送的响应行
        """
        writer.write((line + "\r\n").encode())
        await writer.drain()

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        处理FTP客户端连接

        Args:
            reader (asyncio.StreamReader): 用于从连接中读取数据的流读取器
            writer (asyncio.StreamWriter): 用于向连接写入数据的流写入器
        """
        peer = writer.get_extra_info("peername") or ("unknown", 0)
        session_id = str(uuid.uuid4())
        start_ts = datetime.now(timezone.utc)
        raw_buf = bytearray()
        inputs = []
        username = None
        authenticated = False

        op_logger.info("FTP新连接 %s 会话=%s", peer, session_id)
        try:
            await self._send_line(writer, "220 Microsoft FTP Service")
            while True:
                line = await reader.readline()
                if not line:
                    break
                raw_buf.extend(line)
                try:
                    text = line.decode(errors="ignore").rstrip("\r\n")
                except Exception:
                    text = "<无法解码>"
                inputs.append({"ts": datetime.now(timezone.utc).isoformat(), "input": text})
                op_logger.debug("FTP %s: %s", session_id, text)

                parts = text.split(" ", 1)
                cmd = parts[0].upper()
                arg = parts[1] if len(parts) > 1 else ""

                if cmd == "USER":
                    username = arg
                    await self._send_line(writer, "331 Password required for " + username)
                elif cmd == "PASS":
                    await self._send_line(writer, "230 User " + username + " logged in")
                    authenticated = True
                elif cmd == "SYST":
                    await self._send_line(writer, "215 UNIX Type: L8")
                elif cmd == "PWD":
                    await self._send_line(writer, '257 "/" is current directory')
                elif cmd == "CWD":
                    await self._send_line(writer, "250 CWD command successful")
                elif cmd == "LIST":
                    # 无数据连接：发送预设的成功消息
                    await self._send_line(writer, "150 Opening ASCII mode data connection for file list")
                    await self._send_line(writer, "226 Transfer complete")
                elif cmd in ("RETR", "STOR"):
                    # 出于安全原因拒绝实际传输
                    await self._send_line(writer, "550 Action not taken (simulated)")
                elif cmd == "QUIT":
                    await self._send_line(writer, "221 Goodbye.")
                    break
                else:
                    await self._send_line(writer, "502 Command not implemented")
        except asyncio.CancelledError:
            op_logger.info("FTP会话已取消 %s", session_id)
        except Exception as e:
            op_logger.exception("FTP处理器错误 %s: %s", session_id, e)
        finally:
            entry = {
                "session_id": session_id,
                "start_time": start_ts.isoformat(),
                "end_time": datetime.now(timezone.utc).isoformat(),
                "duration_seconds": (datetime.now(timezone.utc) - start_ts).total_seconds(),
                "remote_ip": peer[0],
                "remote_port": peer[1],
                "username": username,
                "authenticated": authenticated,
                "inputs": inputs,
                "raw_base64": base64.b64encode(bytes(raw_buf)).decode("ascii"),
            }
            await self.persist(entry)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            op_logger.info("FTP关闭会话 %s 来自 %s", session_id, peer)

# ---------------------- TCP回显处理器 ---------------------------------
class TCPHandler(ProtocolHandler):
    """
    TCP协议处理器，实现简单的TCP回显服务
    """

    def __init__(self, host, port, log_file):
        """
        初始化TCP处理器

        Args:
            host (str): 监听主机地址
            port (int): 监听端口
            log_file (str): 日志文件路径
        """
        super().__init__("tcp", host, port, log_file)

    async def start(self):
        """
        启动TCP服务器
        """
        self._server = await asyncio.start_server(self._handle, host=self.host, port=self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
        op_logger.info("TCP监听于 %s", addrs)
        asyncio.create_task(self._server.serve_forever())

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        处理TCP客户端连接，实现回显功能

        Args:
            reader (asyncio.StreamReader): 用于从连接中读取数据的流读取器
            writer (asyncio.StreamWriter): 用于向连接写入数据的流写入器
        """
        peer = writer.get_extra_info("peername") or ("unknown", 0)
        session_id = str(uuid.uuid4())
        start_ts = datetime.now(timezone.utc)
        raw_buf = bytearray()

        op_logger.info("TCP新连接 %s 会话=%s", peer, session_id)
        try:
            writer.write(b"Microsoft Windows [Version 10.0.19041.1]\n(c) 2020 Microsoft Corporation. All rights reserved.\n\nC:\\Users\\Administrator>")
            await writer.drain()
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                raw_buf.extend(data)
                # 回显
                writer.write(data)
                await writer.drain()

                # 如果收到命令，模拟Windows命令行响应
                try:
                    text = data.decode(errors="ignore").strip()
                    if text.lower() == "ipconfig":
                        response = b"\nWindows IP Configuration\n\nEthernet adapter Ethernet:\n   Connection-specific DNS Suffix  . : localdomain\n   IPv4 Address. . . . . . . . . . . : 192.168.1.100\n   Subnet Mask . . . . . . . . . . . : 255.255.255.0\n   Default Gateway . . . . . . . . . : 192.168.1.1\n\n"
                        writer.write(response)
                    elif text.lower() == "ver":
                        writer.write(b"\nMicrosoft Windows [Version 10.0.19041.1]\n")
                except:
                    pass

                writer.write(b"\nC:\\Users\\Administrator>")
                await writer.drain()
        except asyncio.CancelledError:
            op_logger.info("TCP会话已取消 %s", session_id)
        except Exception as e:
            op_logger.exception("TCP处理器错误 %s: %s", session_id, e)
        finally:
            entry = {
                "session_id": session_id,
                "start_time": start_ts.isoformat(),
                "end_time": datetime.now(timezone.utc).isoformat(),
                "duration_seconds": (datetime.now(timezone.utc) - start_ts).total_seconds(),
                "remote_ip": peer[0],
                "remote_port": peer[1],
                "raw_base64": base64.b64encode(bytes(raw_buf)).decode("ascii"),
            }
            await self.persist(entry)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            op_logger.info("TCP关闭会话 %s 来自 %s", session_id, peer)

# ---------------------- HTTP处理器（最小实现） ----------------------------
class HTTPHandler(ProtocolHandler):
    """
    HTTP协议处理器，模拟简单的HTTP服务端
    """

    # 多个响应页面内容，增加随机性
    RESPONSE_BODIES = [
        b"<!DOCTYPE html>\n<html>\n<head>\n<title>Welcome to nginx!</title>\n<style>\n    body {\n        width: 35em;\n        margin: 0 auto;\n        font-family: Tahoma, Verdana, Arial, sans-serif;\n    }\n</style>\n</head>\n<body>\n<h1>Welcome to nginx!</h1>\n<p>If you see this page, the nginx web server is successfully installed and\nworking. Further configuration is required.</p>\n\n<p>For online documentation and support please refer to\n<a href=\"http://nginx.org/\">nginx.org</a>.<br/>\nCommercial support is available at\n<a href=\"http://nginx.com/\">nginx.com</a>.</p>\n\n<p><em>Thank you for using nginx.</em></p>\n</body>\n</html>\n",
        b"<!DOCTYPE html>\n<html>\n<head>\n<title>Test Page for nginx</title>\n<style>\n    body {\n        width: 35em;\n        margin: 0 auto;\n        font-family: Tahoma, Verdana, Arial, sans-serif;\n    }\n</style>\n</head>\n<body>\n<h1>Welcome to nginx!</h1>\n<p>This is a test page used to test the correct operation of the nginx.</p>\n</body>\n</html>\n",
        b"<!DOCTYPE html>\n<html>\n<head>\n<title>Default Web Page</title>\n<style>\n    body {\n        width: 35em;\n        margin: 0 auto;\n        font-family: Tahoma, Verdana, Arial, sans-serif;\n    }\n</style>\n</head>\n<body>\n<h1>Default Web Page</h1>\n<p>This is the default web page for this server.</p>\n<p>The web server software is running but no content has been added, yet.</p>\n</body>\n</html>\n"
    ]

    # 真实的nginx版本号
    NGINX_VERSIONS = [
        "nginx/1.18.0",
        "nginx/1.20.1",
        "nginx/1.21.6",
        "nginx/1.22.1",
        "nginx/1.23.3",
        "nginx/1.24.0"
    ]

    # 登录页面模板
    LOGIN_PAGE = b"""<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; }
        .login-container { width: 300px; margin: 100px auto; padding: 20px; background-color: white; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #333; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 3px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #007cba; color: white; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background-color: #005a87; }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Admin Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>"""

    # 登录API的JSON响应
    LOGIN_JSON_RESPONSES = [
        b'{"success": false, "message": "Invalid credentials"}',
        b'{"success": false, "message": "Authentication failed"}',
        b'{"error": {"code": "INVALID_CREDENTIALS", "message": "The provided credentials are incorrect"}}',
        b'{"error": "Unauthorized", "message": "Login failed. Please check your username and password."}'
    ]

    # phpMyAdmin页面模板
    PHPMYADMIN_PAGE = b"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>phpMyAdmin</title>
    <meta charset="utf-8">
    <style>
        body { font-family: sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; }
        .container { max-width: 500px; margin: 100px auto; background: white; padding: 30px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #666; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; }
        input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 3px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #ffd600; color: black; border: none; border-radius: 3px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #e6c000; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to phpMyAdmin</h1>
        <form method="post" action="index.php">
            <div class="form-group">
                <label for="server">Server:</label>
                <input type="text" id="server" name="server" value="localhost" readonly>
            </div>
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Go</button>
        </form>
    </div>
</body>
</html>"""

    # Admin面板页面模板
    ADMIN_PAGE = b"""<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f1f1f1; }
        .header { background-color: #333; color: white; padding: 15px; }
        .login-form { width: 300px; margin: 100px auto; background: white; padding: 30px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 3px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Admin Panel</h2>
    </div>
    <div class="login-form">
        <h3>Login</h3>
        <form method="POST">
            <div class="form-group">
                <label>Username:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Password:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>"""

    # API数据示例
    API_DATA = [
        b'{"users": [{"id": 1, "name": "John Doe", "email": "john@example.com"}, {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}], "total": 2}',
        b'{"products": [{"id": 1, "name": "Product 1", "price": 29.99}, {"id": 2, "name": "Product 2", "price": 39.99}], "total": 2}',
        b'{"orders": [{"id": 1001, "customer": "John Doe", "amount": 99.99, "status": "shipped"}, {"id": 1002, "customer": "Jane Smith", "amount": 149.99, "status": "pending"}], "total": 2}'
    ]

    # 静态资源内容
    STATIC_CONTENTS = {
        "/favicon.ico": (b"\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00", "image/x-icon"),
        "/robots.txt": (b"User-agent: *\nDisallow: /admin/\nDisallow: /private/\n", "text/plain"),
        "/sitemap.xml": (b"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n<url>\n<loc>http://localhost/</loc>\n</url>\n</urlset>", "application/xml"),
    }

    def __init__(self, host, port, log_file):
        """
        初始化HTTP处理器

        Args:
            host (str): 监听主机地址
            port (int): 监听端口
            log_file (str): 日志文件路径
        """
        super().__init__("http", host, port, log_file)
        # 生成带hash的动态路径
        self.dynamic_paths = self._generate_dynamic_paths()

    def _generate_dynamic_paths(self):
        """生成带hash的动态路径"""
        paths = {}
        # 生成多个带hash的JS和CSS文件路径
        for i in range(5):
            hash_val = ''.join(random.choices('0123456789abcdef', k=5))
            paths[f"/static/js/app.{hash_val}.js"] = (b"console.log('App loaded');", "application/javascript")
            paths[f"/css/style.{hash_val}.css"] = (b"body { margin: 0; padding: 0; }", "text/css")
        return paths

    async def start(self):
        """
        启动HTTP服务器
        """
        self._server = await asyncio.start_server(self._handle, host=self.host, port=self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
        op_logger.info("HTTP监听于 %s", addrs)
        asyncio.create_task(self._server.serve_forever())

    def _generate_session_id(self):
        """生成随机会话ID"""
        return ''.join(random.choices('0123456789abcdef', k=32))

    def _generate_etag(self):
        """生成ETag"""
        return '"' + ''.join(random.choices('0123456789abcdef', k=16)) + '"'

    async def _simulate_network_delay(self, writer, content_length):
        """模拟网络延迟和带宽限制"""
        # 模拟网络延迟 (50ms - 300ms)
        delay = random.uniform(0.05, 0.3)
        await asyncio.sleep(delay)

        # 模拟带宽限制 (10KB/s - 100KB/s)
        bandwidth = random.uniform(10 * 1024, 100 * 1024)  # bytes per second
        transmission_time = content_length / bandwidth
        if transmission_time > 0:
            await asyncio.sleep(transmission_time)

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamReader):
        """
        处理HTTP客户端请求

        Args:
            reader (asyncio.StreamReader): 用于从连接中读取数据的流读取器
            writer (asyncio.StreamWriter): 用于向连接写入数据的流写入器
        """
        peer = writer.get_extra_info("peername") or ("unknown", 0)
        session_id = str(uuid.uuid4())
        start_ts = datetime.now(timezone.utc)
        try:
            raw = await reader.read(64 * 1024)  # 读取最多64KB的头部和内容
            text = raw.decode(errors="ignore")

            # 解析请求
            request_lines = text.split('\n')
            if not request_lines:
                writer.close()
                return

            request_line = request_lines[0].strip()
            headers = {}
            for line in request_lines[1:]:
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip().lower()] = value.strip()

            parts = request_line.split()
            if len(parts) < 3:
                writer.close()
                return

            method, path, version = parts[0], parts[1], parts[2]

            # 检查是否为可疑路径
            if any(pattern in path.lower() for pattern in ['manager', 'python', '.env', 'flask', 'django']):
                body = b'<!DOCTYPE html>\n<html>\n<head>\n<title>404 Not Found</title>\n</head>\n<body>\n<center><h1>404 Not Found</h1></center>\n<hr><center>nginx</center>\n</body>\n</html>\n'
                server_header = random.choice(self.NGINX_VERSIONS)
                resp = b"HTTP/1.1 404 Not Found\r\nServer: %s\r\nDate: %s\r\nContent-Type: text/html\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                    server_header.encode(),
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                    len(body),
                    body
                )
                writer.write(resp)
                await writer.drain()
                return

            # 处理phpMyAdmin页面请求
            if path.startswith("/phpmyadmin"):
                if path == "/phpmyadmin" or path == "/phpmyadmin/":
                    if method == "GET":
                        body = self.PHPMYADMIN_PAGE
                        content_type = "text/html"
                    elif method == "POST":
                        # 记录登录尝试
                        post_data = f"<PHPMyAdmin login attempt with {headers.get('content-length', 'unknown')} bytes of data>"
                        op_logger.info("phpMyAdmin login attempt from %s: %s", peer[0], post_data)

                        # 返回登录失败页面
                        body = b"""<!DOCTYPE html>
<html>
<head>
    <title>phpMyAdmin</title>
    <style>
        body { font-family: sans-serif; background-color: #f5f5f5; }
        .error { width: 500px; margin: 100px auto; background: white; padding: 30px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); border-left: 5px solid #f44336; }
        .error h2 { color: #f44336; }
        .back-link { display: block; text-align: center; margin-top: 20px; color: #2196F3; text-decoration: none; }
    </style>
</head>
<body>
    <div class="error">
        <h2>Login failed</h2>
        <p>Invalid credentials. Please try again.</p>
        <a href="index.php" class="back-link">Back to login</a>
    </div>
</body>
</html>"""
                        content_type = "text/html"
                    else:
                        body = b'{"error": "Method not allowed"}'
                        content_type = "application/json"

                    server_header = random.choice(self.NGINX_VERSIONS)
                    resp = b"HTTP/1.1 200 OK\r\nServer: %s\r\nDate: %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                        server_header.encode(),
                        datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                        content_type.encode(),
                        len(body),
                        body
                    )
                    await self._simulate_network_delay(writer, len(body))
                    writer.write(resp)
                    await writer.drain()
                    return
                else:
                    # phpMyAdmin子路径返回404
                    body = b'<!DOCTYPE html>\n<html>\n<head>\n<title>404 Not Found</title>\n</head>\n<body>\n<center><h1>404 Not Found</h1></center>\n<hr><center>nginx</center>\n</body>\n</html>\n'
                    server_header = random.choice(self.NGINX_VERSIONS)
                    resp = b"HTTP/1.1 404 Not Found\r\nServer: %s\r\nDate: %s\r\nContent-Type: text/html\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                        server_header.encode(),
                        datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                        len(body),
                        body
                    )
                    writer.write(resp)
                    await writer.drain()
                    return

            # 处理Admin面板请求
            if path.startswith("/admin"):
                if path == "/admin" or path == "/admin/":
                    if method == "GET":
                        body = self.ADMIN_PAGE
                        content_type = "text/html"
                    elif method == "POST":
                        # 记录登录尝试
                        post_data = f"<Admin panel login attempt with {headers.get('content-length', 'unknown')} bytes of data>"
                        op_logger.info("Admin panel login attempt from %s: %s", peer[0], post_data)

                        # 返回登录失败页面
                        body = b"""<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f1f1f1; }
        .header { background-color: #333; color: white; padding: 15px; }
        .error { width: 300px; margin: 100px auto; background: white; padding: 30px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); border-left: 5px solid #f44336; }
        .error h3 { color: #f44336; margin-top: 0; }
        .back-link { display: block; text-align: center; margin-top: 20px; color: #2196F3; text-decoration: none; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Admin Panel</h2>
    </div>
    <div class="error">
        <h3>Login Failed</h3>
        <p>Invalid username or password.</p>
        <a href="/" class="back-link">Back to login</a>
    </div>
</body>
</html>"""
                        content_type = "text/html"
                    else:
                        body = b'{"error": "Method not allowed"}'
                        content_type = "application/json"

                    server_header = random.choice(self.NGINX_VERSIONS)
                    resp = b"HTTP/1.1 200 OK\r\nServer: %s\r\nDate: %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                        server_header.encode(),
                        datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                        content_type.encode(),
                        len(body),
                        body
                    )
                    await self._simulate_network_delay(writer, len(body))
                    writer.write(resp)
                    await writer.drain()
                    return
                else:
                    # Admin子路径返回404
                    body = b'<!DOCTYPE html>\n<html>\n<head>\n<title>404 Not Found</title>\n</head>\n<body>\n<center><h1>404 Not Found</h1></center>\n<hr><center>nginx</center>\n</body>\n</html>\n'
                    server_header = random.choice(self.NGINX_VERSIONS)
                    resp = b"HTTP/1.1 404 Not Found\r\nServer: %s\r\nDate: %s\r\nContent-Type: text/html\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                        server_header.encode(),
                        datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                        len(body),
                        body
                    )
                    writer.write(resp)
                    await writer.drain()
                    return

            # 处理API请求
            if path.startswith("/api/"):
                if method == "GET":
                    body = random.choice(self.API_DATA)
                    content_type = "application/json"
                else:
                    body = b'{"error": "Method not allowed"}'
                    content_type = "application/json"

                server_header = random.choice(self.NGINX_VERSIONS)
                resp = b"HTTP/1.1 200 OK\r\nServer: %s\r\nDate: %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                    server_header.encode(),
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                    content_type.encode(),
                    len(body),
                    body
                )
                await self._simulate_network_delay(writer, len(body))
                writer.write(resp)
                await writer.drain()
                return

            # 处理登录页面请求
            if path == "/login" and method == "GET":
                # 检查Accept头以决定返回HTML还是JSON
                accept_header = headers.get('accept', '')
                if 'application/json' in accept_header and 'text/html' not in accept_header:
                    # 返回JSON格式的登录页面信息
                    body = b'{"login_url": "/login", "method": "POST", "fields": ["username", "password"]}'
                    content_type = "application/json"
                else:
                    # 返回HTML登录页面
                    body = self.LOGIN_PAGE
                    content_type = "text/html"

                server_header = random.choice(self.NGINX_VERSIONS)
                resp = b"HTTP/1.1 200 OK\r\nServer: %s\r\nDate: %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                    server_header.encode(),
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                    content_type.encode(),
                    len(body),
                    body
                )
                await self._simulate_network_delay(writer, len(body))
                writer.write(resp)
                await writer.drain()
                return

            # 处理登录表单提交
            if path == "/login" and method == "POST":
                # 检查Content-Type以决定如何处理请求
                content_type_header = headers.get('content-type', '').lower()

                # 记录提交的登录凭据
                post_data = b""
                content_length = 0
                if "content-length" in headers:
                    try:
                        content_length = int(headers["content-length"])
                    except ValueError:
                        pass

                # 简化处理，实际应该读取body内容
                post_data = f"<{content_length} bytes of POST data>".encode()

                # 根据请求的Accept头决定返回什么类型的数据
                accept_header = headers.get('accept', '')
                if 'application/json' in accept_header and 'text/html' not in accept_header:
                    # 返回JSON格式的错误响应
                    body = random.choice(self.LOGIN_JSON_RESPONSES)
                    content_type = "application/json"
                    status_line = "HTTP/1.1 401 Unauthorized"
                else:
                    # 返回HTML格式的错误响应
                    body = b'<!DOCTYPE html>\n<html>\n<head>\n<title>Login Failed</title>\n</head>\n<body>\n<center><h1>Login Failed</h1></center>\n<hr><center>nginx</center>\n</body>\n</html>\n'
                    content_type = "text/html"
                    status_line = "HTTP/1.1 401 Unauthorized"

                server_header = random.choice(self.NGINX_VERSIONS)
                resp = b"%s\r\nServer: %s\r\nDate: %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                    status_line.encode(),
                    server_header.encode(),
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                    content_type.encode(),
                    len(body),
                    body
                )
                writer.write(resp)
                await writer.drain()

                # 记录登录尝试
                op_logger.info("Login attempt from %s: %s", peer[0], post_data.decode(errors="ignore"))
                return

            # 处理静态资源请求
            all_static_contents = {**self.STATIC_CONTENTS, **self.dynamic_paths}
            if path in all_static_contents:
                content, content_type = all_static_contents[path]
                server_header = random.choice(self.NGINX_VERSIONS)
                resp = b"HTTP/1.1 200 OK\r\nServer: %s\r\nDate: %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nETag: %s\r\nCache-Control: max-age=3600\r\nConnection: close\r\n\r\n%s" % (
                    server_header.encode(),
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                    content_type.encode(),
                    len(content),
                    self._generate_etag().encode(),
                    content
                )
                await self._simulate_network_delay(writer, len(content))
                writer.write(resp)
                await writer.drain()
                return

            # 处理/favicon.ico特殊请求
            if path == "/favicon.ico":
                content = b"\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00"
                server_header = random.choice(self.NGINX_VERSIONS)
                resp = b"HTTP/1.1 200 OK\r\nServer: %s\r\nDate: %s\r\nContent-Type: image/x-icon\r\nContent-Length: %d\r\nETag: %s\r\nCache-Control: max-age=86400\r\nConnection: close\r\n\r\n%s" % (
                    server_header.encode(),
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                    len(content),
                    self._generate_etag().encode(),
                    content
                )
                await self._simulate_network_delay(writer, len(content))
                writer.write(resp)
                await writer.drain()
                return

            # 检查是否需要返回304
            if 'if-none-match' in headers:
                server_header = random.choice(self.NGINX_VERSIONS)
                resp = b"HTTP/1.1 304 Not Modified\r\nServer: %s\r\nDate: %s\r\nETag: %s\r\nConnection: close\r\n\r\n" % (
                    server_header.encode(),
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                    self._generate_etag().encode()
                )
                writer.write(resp)
                await writer.drain()
                return

            # 生成Cookie
            has_cookie = 'cookie' in headers
            session_cookie = ""
            if not has_cookie:
                session_cookie = "Set-Cookie: sessionid=%s; Path=/; HttpOnly\r\n" % self._generate_session_id()

            # 随机选择响应页面
            body = random.choice(self.RESPONSE_BODIES)

            # 随机选择nginx版本
            server_header = random.choice(self.NGINX_VERSIONS)

            # 构建响应
            resp_headers = [
                "HTTP/1.1 200 OK",
                "Server: %s" % server_header,
                "Date: %s" % datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT'),
                "Content-Type: text/html",
                "Content-Length: %d" % len(body),
                "ETag: %s" % self._generate_etag(),
                "Cache-Control: no-cache",
                "Connection: close"
            ]

            if not has_cookie:
                resp_headers.append(session_cookie.rstrip())

            resp = ("\r\n".join(resp_headers) + "\r\n\r\n").encode() + body
            await self._simulate_network_delay(writer, len(body))
            writer.write(resp)
            await writer.drain()

            entry = {
                "session_id": session_id,
                "start_time": start_ts.isoformat(),
                "end_time": datetime.now(timezone.utc).isoformat(),
                "duration_seconds": (datetime.now(timezone.utc) - start_ts).total_seconds(),
                "remote_ip": peer[0],
                "remote_port": peer[1],
                "inputs": [text],
                "raw_base64": base64.b64encode(raw).decode("ascii"),
            }
            await self.persist(entry)
        except Exception as e:
            op_logger.exception("HTTP处理器错误 %s: %s", session_id, e)
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            op_logger.info("HTTP关闭会话 %s 来自 %s", session_id, peer)

# ---------------------- HTTPS处理器（使用ssl包装HTTP） ----------------
class HTTPSHandler(HTTPHandler):
    """
    HTTPS协议处理器，通过SSL包装HTTP处理器实现HTTPS服务
    """

    # 多个响应页面内容，增加随机性
    RESPONSE_BODIES = [
        b"<!DOCTYPE html>\n<html>\n<head>\n<title>Welcome to nginx!</title>\n<style>\n    body {\n        width: 35em;\n        margin: 0 auto;\n        font-family: Tahoma, Verdana, Arial, sans-serif;\n    }\n</style>\n</head>\n<body>\n<h1>Welcome to nginx!</h1>\n<p>If you see this page, the nginx web server is successfully installed and\nworking. Further configuration is required.</p>\n\n<p>For online documentation and support please refer to\n<a href=\"http://nginx.org/\">nginx.org</a>.<br/>\nCommercial support is available at\n<a href=\"http://nginx.com/\">nginx.com</a>.</p>\n\n<p><em>Thank you for using nginx.</em></p>\n</body>\n</html>\n",
        b"<!DOCTYPE html>\n<html>\n<head>\n<title>Test Page for nginx</title>\n<style>\n    body {\n        width: 35em;\n        margin: 0 auto;\n        font-family: Tahoma, Verdana, Arial, sans-serif;\n    }\n</style>\n</head>\n<body>\n<h1>Welcome to nginx!</h1>\n<p>This is a test page used to test the correct operation of the nginx.</p>\n</body>\n</html>\n",
        b"<!DOCTYPE html>\n<html>\n<head>\n<title>Default Web Page</title>\n<style>\n    body {\n        width: 35em;\n        margin: 0 auto;\n        font-family: Tahoma, Verdana, Arial, sans-serif;\n    }\n</style>\n</head>\n<body>\n<h1>Default Web Page</h1>\n<p>This is the default web page for this server.</p>\n<p>The web server software is running but no content has been added, yet.</p>\n</body>\n</html>\n"
    ]

    # 真实的nginx版本号
    NGINX_VERSIONS = [
        "nginx/1.18.0",
        "nginx/1.20.1",
        "nginx/1.21.6",
        "nginx/1.22.1",
        "nginx/1.23.3",
        "nginx/1.24.0"
    ]

    # 登录页面模板
    LOGIN_PAGE = b"""<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; }
        .login-container { width: 300px; margin: 100px auto; padding: 20px; background-color: white; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #333; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 3px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #007cba; color: white; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background-color: #005a87; }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Admin Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>"""

    # 登录API的JSON响应
    LOGIN_JSON_RESPONSES = [
        b'{"success": false, "message": "Invalid credentials"}',
        b'{"success": false, "message": "Authentication failed"}',
        b'{"error": {"code": "INVALID_CREDENTIALS", "message": "The provided credentials are incorrect"}}',
        b'{"error": "Unauthorized", "message": "Login failed. Please check your username and password."}'
    ]

    # phpMyAdmin页面模板
    PHPMYADMIN_PAGE = b"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>phpMyAdmin</title>
    <meta charset="utf-8">
    <style>
        body { font-family: sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; }
        .container { max-width: 500px; margin: 100px auto; background: white; padding: 30px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #666; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; }
        input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 3px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #ffd600; color: black; border: none; border-radius: 3px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #e6c000; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to phpMyAdmin</h1>
        <form method="post" action="index.php">
            <div class="form-group">
                <label for="server">Server:</label>
                <input type="text" id="server" name="server" value="localhost" readonly>
            </div>
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Go</button>
        </form>
    </div>
</body>
</html>"""

    # Admin面板页面模板
    ADMIN_PAGE = b"""<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f1f1f1; }
        .header { background-color: #333; color: white; padding: 15px; }
        .login-form { width: 300px; margin: 100px auto; background: white; padding: 30px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 3px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Admin Panel</h2>
    </div>
    <div class="login-form">
        <h3>Login</h3>
        <form method="POST">
            <div class="form-group">
                <label>Username:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Password:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>"""

    # API数据示例
    API_DATA = [
        b'{"users": [{"id": 1, "name": "John Doe", "email": "john@example.com"}, {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}], "total": 2}',
        b'{"products": [{"id": 1, "name": "Product 1", "price": 29.99}, {"id": 2, "name": "Product 2", "price": 39.99}], "total": 2}',
        b'{"orders": [{"id": 1001, "customer": "John Doe", "amount": 99.99, "status": "shipped"}, {"id": 1002, "customer": "Jane Smith", "amount": 149.99, "status": "pending"}], "total": 2}'
    ]

    # 静态资源内容
    STATIC_CONTENTS = {
        "/favicon.ico": (b"\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00", "image/x-icon"),
        "/robots.txt": (b"User-agent: *\nDisallow: /admin/\nDisallow: /private/\n", "text/plain"),
        "/sitemap.xml": (b"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n<url>\n<loc>http://localhost/</loc>\n</url>\n</urlset>", "application/xml"),
    }

    def __init__(self, host, port, log_file, certfile: str, keyfile: str):
        """
        初始化HTTPS处理器

        Args:
            host (str): 监听主机地址
            port (int): 监听端口
            log_file (str): 日志文件路径
            certfile (str): SSL证书文件路径
            keyfile (str): SSL密钥文件路径
        """
        super().__init__(host, port, log_file)
        self.name = "https"
        self.certfile = certfile
        self.keyfile = keyfile
        # 生成带hash的动态路径
        self.dynamic_paths = self._generate_dynamic_paths()

    async def start(self):
        """
        启动HTTPS服务器
        """
        try:
            # 创建SSL上下文
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # 禁用旧版本
            ctx.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
            # 添加更强的SSL配置
            ctx.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS')
            self._server = await asyncio.start_server(self._handle, host=self.host, port=self.port, ssl=ctx)
            addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
            op_logger.info("HTTPS监听于 %s", addrs)
            asyncio.create_task(self._server.serve_forever())
        except FileNotFoundError:
            op_logger.error("找不到SSL证书文件: certfile=%s keyfile=%s", self.certfile, self.keyfile)
            op_logger.error("请使用--generate-cert参数自动生成证书，或手动提供证书文件")
        except Exception as e:
            op_logger.exception("HTTPS服务器启动失败: %s", e)

    def _generate_session_id(self):
        """生成随机会话ID"""
        return ''.join(random.choices('0123456789abcdef', k=32))

    def _generate_etag(self):
        """生成ETag"""
        return '"' + ''.join(random.choices('0123456789abcdef', k=16)) + '"'

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        处理HTTP客户端请求

        Args:
            reader (asyncio.StreamReader): 用于从连接中读取数据的流读取器
            writer (asyncio.StreamWriter): 用于向连接写入数据的流写入器
        """
        peer = writer.get_extra_info("peername") or ("unknown", 0)
        session_id = str(uuid.uuid4())
        start_ts = datetime.now(timezone.utc)
        try:
            raw = await reader.read(64 * 1024)  # 读取最多64KB的头部和内容
            text = raw.decode(errors="ignore")

            # 解析请求
            request_lines = text.split('\n')
            if not request_lines:
                writer.close()
                return

            request_line = request_lines[0].strip()
            headers = {}
            for line in request_lines[1:]:
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip().lower()] = value.strip()

            parts = request_line.split()
            if len(parts) < 3:
                writer.close()
                return

            method, path, version = parts[0], parts[1], parts[2]

            # 检查是否为可疑路径
            if any(pattern in path.lower() for pattern in ['manager', 'python', '.env', 'flask', 'django']):
                body = b'<!DOCTYPE html>\n<html>\n<head>\n<title>404 Not Found</title>\n</head>\n<body>\n<center><h1>404 Not Found</h1></center>\n<hr><center>nginx</center>\n</body>\n</html>\n'
                server_header = random.choice(self.NGINX_VERSIONS)
                resp = b"HTTP/1.1 404 Not Found\r\nServer: %s\r\nDate: %s\r\nContent-Type: text/html\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                    server_header.encode(),
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                    len(body),
                    body
                )
                writer.write(resp)
                await writer.drain()
                return

            # 处理phpMyAdmin页面请求
            if path.startswith("/phpmyadmin"):
                if path == "/phpmyadmin" or path == "/phpmyadmin/":
                    if method == "GET":
                        body = self.PHPMYADMIN_PAGE
                        content_type = "text/html"
                    elif method == "POST":
                        # 记录登录尝试
                        post_data = f"<PHPMyAdmin login attempt with {headers.get('content-length', 'unknown')} bytes of data>"
                        op_logger.info("phpMyAdmin login attempt from %s: %s", peer[0], post_data)

                        # 返回登录失败页面
                        body = b"""<!DOCTYPE html>
<html>
<head>
    <title>phpMyAdmin</title>
    <style>
        body { font-family: sans-serif; background-color: #f5f5f5; }
        .error { width: 500px; margin: 100px auto; background: white; padding: 30px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); border-left: 5px solid #f44336; }
        .error h2 { color: #f44336; }
        .back-link { display: block; text-align: center; margin-top: 20px; color: #2196F3; text-decoration: none; }
    </style>
</head>
<body>
    <div class="error">
        <h2>Login failed</h2>
        <p>Invalid credentials. Please try again.</p>
        <a href="index.php" class="back-link">Back to login</a>
    </div>
</body>
</html>"""
                        content_type = "text/html"
                    else:
                        body = b'{"error": "Method not allowed"}'
                        content_type = "application/json"

                    server_header = random.choice(self.NGINX_VERSIONS)
                    resp = b"HTTP/1.1 200 OK\r\nServer: %s\r\nDate: %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                        server_header.encode(),
                        datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                        content_type.encode(),
                        len(body),
                        body
                    )
                    await self._simulate_network_delay(writer, len(body))
                    writer.write(resp)
                    await writer.drain()
                    return
                else:
                    # phpMyAdmin子路径返回404
                    body = b'<!DOCTYPE html>\n<html>\n<head>\n<title>404 Not Found</title>\n</head>\n<body>\n<center><h1>404 Not Found</h1></center>\n<hr><center>nginx</center>\n</body>\n</html>\n'
                    server_header = random.choice(self.NGINX_VERSIONS)
                    resp = b"HTTP/1.1 404 Not Found\r\nServer: %s\r\nDate: %s\r\nContent-Type: text/html\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                        server_header.encode(),
                        datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                        len(body),
                        body
                    )
                    writer.write(resp)
                    await writer.drain()
                    return

            # 处理Admin面板请求
            if path.startswith("/admin"):
                if path == "/admin" or path == "/admin/":
                    if method == "GET":
                        body = self.ADMIN_PAGE
                        content_type = "text/html"
                    elif method == "POST":
                        # 记录登录尝试
                        post_data = f"<Admin panel login attempt with {headers.get('content-length', 'unknown')} bytes of data>"
                        op_logger.info("Admin panel login attempt from %s: %s", peer[0], post_data)

                        # 返回登录失败页面
                        body = b"""<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f1f1f1; }
        .header { background-color: #333; color: white; padding: 15px; }
        .error { width: 300px; margin: 100px auto; background: white; padding: 30px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); border-left: 5px solid #f44336; }
        .error h3 { color: #f44336; margin-top: 0; }
        .back-link { display: block; text-align: center; margin-top: 20px; color: #2196F3; text-decoration: none; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Admin Panel</h2>
    </div>
    <div class="error">
        <h3>Login Failed</h3>
        <p>Invalid username or password.</p>
        <a href="/" class="back-link">Back to login</a>
    </div>
</body>
</html>"""
                        content_type = "text/html"
                    else:
                        body = b'{"error": "Method not allowed"}'
                        content_type = "application/json"

                    server_header = random.choice(self.NGINX_VERSIONS)
                    resp = b"HTTP/1.1 200 OK\r\nServer: %s\r\nDate: %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                        server_header.encode(),
                        datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                        content_type.encode(),
                        len(body),
                        body
                    )
                    await self._simulate_network_delay(writer, len(body))
                    writer.write(resp)
                    await writer.drain()
                    return
                else:
                    # Admin子路径返回404
                    body = b'<!DOCTYPE html>\n<html>\n<head>\n<title>404 Not Found</title>\n</head>\n<body>\n<center><h1>404 Not Found</h1></center>\n<hr><center>nginx</center>\n</body>\n</html>\n'
                    server_header = random.choice(self.NGINX_VERSIONS)
                    resp = b"HTTP/1.1 404 Not Found\r\nServer: %s\r\nDate: %s\r\nContent-Type: text/html\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                        server_header.encode(),
                        datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                        len(body),
                        body
                    )
                    writer.write(resp)
                    await writer.drain()
                    return

            # 处理API请求
            if path.startswith("/api/"):
                if method == "GET":
                    body = random.choice(self.API_DATA)
                    content_type = "application/json"
                else:
                    body = b'{"error": "Method not allowed"}'
                    content_type = "application/json"

                server_header = random.choice(self.NGINX_VERSIONS)
                resp = b"HTTP/1.1 200 OK\r\nServer: %s\r\nDate: %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                    server_header.encode(),
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                    content_type.encode(),
                    len(body),
                    body
                )
                await self._simulate_network_delay(writer, len(body))
                writer.write(resp)
                await writer.drain()
                return

            # 处理登录页面请求
            if path == "/login" and method == "GET":
                # 检查Accept头以决定返回HTML还是JSON
                accept_header = headers.get('accept', '')
                if 'application/json' in accept_header and 'text/html' not in accept_header:
                    # 返回JSON格式的登录页面信息
                    body = b'{"login_url": "/login", "method": "POST", "fields": ["username", "password"]}'
                    content_type = "application/json"
                else:
                    # 返回HTML登录页面
                    body = self.LOGIN_PAGE
                    content_type = "text/html"

                server_header = random.choice(self.NGINX_VERSIONS)
                resp = b"HTTP/1.1 200 OK\r\nServer: %s\r\nDate: %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                    server_header.encode(),
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                    content_type.encode(),
                    len(body),
                    body
                )
                await self._simulate_network_delay(writer, len(body))
                writer.write(resp)
                await writer.drain()
                return

            # 处理登录表单提交
            if path == "/login" and method == "POST":
                # 检查Content-Type以决定如何处理请求
                content_type_header = headers.get('content-type', '').lower()

                # 记录提交的登录凭据
                post_data = b""
                content_length = 0
                if "content-length" in headers:
                    try:
                        content_length = int(headers["content-length"])
                    except ValueError:
                        pass

                # 简化处理，实际应该读取body内容
                post_data = f"<{content_length} bytes of POST data>".encode()

                # 根据请求的Accept头决定返回什么类型的数据
                accept_header = headers.get('accept', '')
                if 'application/json' in accept_header and 'text/html' not in accept_header:
                    # 返回JSON格式的错误响应
                    body = random.choice(self.LOGIN_JSON_RESPONSES)
                    content_type = "application/json"
                    status_line = "HTTP/1.1 401 Unauthorized"
                else:
                    # 返回HTML格式的错误响应
                    body = b'<!DOCTYPE html>\n<html>\n<head>\n<title>Login Failed</title>\n</head>\n<body>\n<center><h1>Login Failed</h1></center>\n<hr><center>nginx</center>\n</body>\n</html>\n'
                    content_type = "text/html"
                    status_line = "HTTP/1.1 401 Unauthorized"

                server_header = random.choice(self.NGINX_VERSIONS)
                resp = b"%s\r\nServer: %s\r\nDate: %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" % (
                    status_line.encode(),
                    server_header.encode(),
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                    content_type.encode(),
                    len(body),
                    body
                )
                writer.write(resp)
                await writer.drain()

                # 记录登录尝试
                op_logger.info("Login attempt from %s: %s", peer[0], post_data.decode(errors="ignore"))
                return

            # 处理静态资源请求
            all_static_contents = {**self.STATIC_CONTENTS, **self.dynamic_paths}
            if path in all_static_contents:
                content, content_type = all_static_contents[path]
                server_header = random.choice(self.NGINX_VERSIONS)
                resp = b"HTTP/1.1 200 OK\r\nServer: %s\r\nDate: %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nETag: %s\r\nCache-Control: max-age=3600\r\nConnection: close\r\n\r\n%s" % (
                    server_header.encode(),
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                    content_type.encode(),
                    len(content),
                    self._generate_etag().encode(),
                    content
                )
                await self._simulate_network_delay(writer, len(content))
                writer.write(resp)
                await writer.drain()
                return

            # 处理/favicon.ico特殊请求
            if path == "/favicon.ico":
                content = b"\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00"
                server_header = random.choice(self.NGINX_VERSIONS)
                resp = b"HTTP/1.1 200 OK\r\nServer: %s\r\nDate: %s\r\nContent-Type: image/x-icon\r\nContent-Length: %d\r\nETag: %s\r\nCache-Control: max-age=86400\r\nConnection: close\r\n\r\n%s" % (
                    server_header.encode(),
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                    len(content),
                    self._generate_etag().encode(),
                    content
                )
                await self._simulate_network_delay(writer, len(content))
                writer.write(resp)
                await writer.drain()
                return

            # 检查是否需要返回304
            if 'if-none-match' in headers:
                server_header = random.choice(self.NGINX_VERSIONS)
                resp = b"HTTP/1.1 304 Not Modified\r\nServer: %s\r\nDate: %s\r\nETag: %s\r\nConnection: close\r\n\r\n" % (
                    server_header.encode(),
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT').encode(),
                    self._generate_etag().encode()
                )
                writer.write(resp)
                await writer.drain()
                return

            # 生成Cookie
            has_cookie = 'cookie' in headers
            session_cookie = ""
            if not has_cookie:
                session_cookie = "Set-Cookie: sessionid=%s; Path=/; HttpOnly; Secure\r\n" % self._generate_session_id()

            # 随机选择响应页面
            body = random.choice(self.RESPONSE_BODIES)

            # 随机选择nginx版本
            server_header = random.choice(self.NGINX_VERSIONS)

            # 构建响应
            resp_headers = [
                "HTTP/1.1 200 OK",
                "Server: %s" % server_header,
                "Date: %s" % datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT'),
                "Content-Type: text/html",
                "Content-Length: %d" % len(body),
                "ETag: %s" % self._generate_etag(),
                "Cache-Control: no-cache",
                "Connection: close"
            ]

            if not has_cookie:
                resp_headers.append(session_cookie.rstrip())

            resp = ("\r\n".join(resp_headers) + "\r\n\r\n").encode() + body
            await self._simulate_network_delay(writer, len(body))
            writer.write(resp)
            await writer.drain()

            entry = {
                "session_id": session_id,
                "start_time": start_ts.isoformat(),
                "end_time": datetime.now(timezone.utc).isoformat(),
                "duration_seconds": (datetime.now(timezone.utc) - start_ts).total_seconds(),
                "remote_ip": peer[0],
                "remote_port": peer[1],
                "inputs": [text],
                "raw_base64": base64.b64encode(raw).decode("ascii"),
            }
            await self.persist(entry)
        except Exception as e:
            op_logger.exception("HTTPS处理器错误 %s: %s", session_id, e)
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            op_logger.info("HTTPS关闭会话 %s 来自 %s", session_id, peer)


# ---------------------- SSH处理器（仅横幅） -------------------------
class SSHHandler(ProtocolHandler):
    """
    SSH协议处理器，模拟SSH服务端并捕获客户端连接信息
    """

    BANNER = b"SSH-2.0-OpenSSH_7.9\r\n"

    def __init__(self, host, port, log_file):
        """
        初始化SSH处理器

        Args:
            host (str): 监听主机地址
            port (int): 监听端口
            log_file (str): 日志文件路径
        """
        super().__init__("ssh", host, port, log_file)

    async def start(self):
        """
        启动SSH服务器
        """
        self._server = await asyncio.start_server(self._handle, host=self.host, port=self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
        op_logger.info("SSH监听于 %s", addrs)
        asyncio.create_task(self._server.serve_forever())

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        处理SSH客户端连接，捕获客户端横幅信息

        Args:
            reader (asyncio.StreamReader): 用于从连接中读取数据的流读取器
            writer (asyncio.StreamWriter): 用于向连接写入数据的流写入器
        """
        peer = writer.get_extra_info("peername") or ("unknown", 0)
        session_id = str(uuid.uuid4())
        start_ts = datetime.now(timezone.utc)
        raw_buf = bytearray()
        op_logger.info("SSH新连接 %s 会话=%s", peer, session_id)
        try:
            # 发送横幅并读取一次以捕获客户端横幅或任何早期字节
            writer.write(self.BANNER)
            await writer.drain()
            # 尝试读取小缓冲区；不长时间阻塞
            try:
                data = await asyncio.wait_for(reader.read(1024), timeout=5.0)
                if data:
                    raw_buf.extend(data)
            except asyncio.TimeoutError:
                pass
        except Exception as e:
            op_logger.exception("SSH处理器异常 %s: %s", session_id, e)
        finally:
            entry = {
                "session_id": session_id,
                "start_time": start_ts.isoformat(),
                "end_time": datetime.now(timezone.utc).isoformat(),
                "duration_seconds": (datetime.now(timezone.utc) - start_ts).total_seconds(),
                "remote_ip": peer[0],
                "remote_port": peer[1],
                "raw_base64": base64.b64encode(bytes(raw_buf)).decode("ascii"),
            }
            await self.persist(entry)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            op_logger.info("SSH关闭会话 %s 来自 %s", session_id, peer)

# ---------------------- 管理器协调处理器 -------------------
class HoneypotManager:
    """
    蜜罐管理器，用于协调和管理所有协议处理器
    """

    def __init__(self, handlers):
        """
        初始化蜜罐管理器

        Args:
            handlers (list): 协议处理器列表
        """
        self.handlers = handlers

    async def start(self):
        """
        启动所有协议处理器
        """
        op_logger.info("启动蜜罐管理器，包含 %d 个处理器", len(self.handlers))
        # 并发启动处理器
        await asyncio.gather(*(h.start() for h in self.handlers))
        op_logger.info("所有处理器已启动")

    async def stop(self):
        """
        停止所有协议处理器
        """
        op_logger.info("停止蜜罐管理器")
        await asyncio.gather(*(h.stop() for h in self.handlers), return_exceptions=True)

# ---------------------- 工具函数：通过openssl生成自签名证书 -----
def ensure_self_signed(certfile: Path, keyfile: Path, common_name: str = "mini-honeypot.local"):
    """
    如果文件缺失，尝试使用openssl命令生成自签名证书。
    需要在PATH中有openssl可用。

    Args:
        certfile (Path): 证书文件路径
        keyfile (Path): 密钥文件路径
        common_name (str): 证书通用名称

    Returns:
        bool: 生成成功返回True，否则返回False
    """
    if certfile.exists() and keyfile.exists():
        op_logger.info("找到现有证书/密钥: %s %s", certfile, keyfile)
        return True

    # 尝试运行openssl
    cmd = [
        "openssl", "req", "-x509", "-nodes", "-days", "365",
        "-newkey", "rsa:2048",
        "-keyout", str(keyfile),
        "-out", str(certfile),
        "-subj", f"/CN={common_name}"
    ]
    try:
        op_logger.info("通过openssl生成自签名证书...")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        op_logger.info("生成证书/密钥于 %s %s", certfile, keyfile)
        return True
    except Exception as e:
        op_logger.error("使用openssl生成证书/密钥失败: %s", e)
        return False

# ---------------------- 命令行界面 / 入口点 ---------------------------------
def parse_args():
    """
    解析命令行参数

    Returns:
        argparse.Namespace: 解析后的命令行参数
    """
    p = argparse.ArgumentParser(description="多协议蜜罐（单文件）")
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--log", default=DEFAULT_LOG_FILE)
    p.add_argument("--tcp-port", type=int, default=DEFAULTS["tcp"])
    p.add_argument("--http-port", type=int, default=DEFAULTS["http"])
    p.add_argument("--https-port", type=int, default=DEFAULTS["https"])
    p.add_argument("--ssh-port", type=int, default=DEFAULTS["ssh"])
    p.add_argument("--telnet-port", type=int, default=DEFAULTS["telnet"])
    p.add_argument("--ftp-port", type=int, default=DEFAULTS["ftp"])
    p.add_argument("--certfile", default="cert.pem", help="HTTPS证书（PEM格式）")
    p.add_argument("--keyfile", default="key.pem", help="HTTPS密钥（PEM格式）")
    p.add_argument("--generate-cert", action="store_true", help="如果缺失，尝试使用openssl自动创建自签名证书")
    return p.parse_args()

async def main_async():
    """
    异步主函数，负责初始化和运行蜜罐
    """
    args = parse_args()
    # 如果需要，确保证书存在
    certfile = Path(args.certfile)
    keyfile = Path(args.keyfile)
    if args.generate_cert:
        ok = ensure_self_signed(certfile, keyfile)
        if not ok:
            op_logger.warning("没有有效的证书/密钥，HTTPS将失败。继续运行。")

    # 实例化处理器
    handlers = []
    handlers.append(TCPHandler(host=args.host, port=args.tcp_port, log_file=args.log))
    handlers.append(HTTPHandler(host=args.host, port=args.http_port, log_file=args.log))
    handlers.append(HTTPSHandler(host=args.host, port=args.https_port, log_file=args.log, certfile=str(certfile), keyfile=str(keyfile)))
    handlers.append(SSHHandler(host=args.host, port=args.ssh_port, log_file=args.log))
    handlers.append(TelnetHandler(host=args.host, port=args.telnet_port, log_file=args.log))
    handlers.append(FTPHandler(host=args.host, port=args.ftp_port, log_file=args.log))

    manager = HoneypotManager(handlers)
    await manager.start()

    # 运行直到被中断
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        op_logger.info("收到键盘中断；正在关闭")
    finally:
        await manager.stop()

def main():
    """
    程序主入口函数
    """
    try:
        asyncio.run(main_async())
    except Exception as e:
        op_logger.exception("致命错误: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
