#!/usr/bin/env python3
# telnet_honeypot_standalone.py
# 简单的基于asyncio的TelnetService （单协议版本）
# 将会话元数据和所有输入记录到JSONL文件中。

import argparse
import asyncio
import logging
import json
import uuid
import base64
from datetime import datetime, timezone
import random
import re

# ---------- 配置 ----------
# 更真实的Telnet服务Banner，模仿真实设备
BANNER = b"\r\n\r\nWelcome to Telnet Server\r\n" + \
         b"Login authentication\r\n\r\n"

# 更真实的提示符，模仿网络设备
PROMPT = b"Router> "
ENABLE_PROMPT = b"Router# "
LOGIN_PROMPT = b"Username: "
PASS_PROMPT = b"Password: "

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

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 2323  # 如果你控制基础设施，使用23；2323避免需要root权限

LOG_FILE = "honeypot_sessions.jsonl"
# ---------- 配置结束 ----------

# 设置Python日志记录用于操作员日志（不是会话日志）
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("honeypot")


# ---------- TelnetSession 类 ----------
class TelnetSession:
    """
    Telnet会话类，用于处理单个Telnet连接的生命周期
    """

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, remote):
        """
        初始化Telnet会话

        Args:
            reader (asyncio.StreamReader): 用于从连接中读取数据的流读取器
            writer (asyncio.StreamWriter): 用于向连接写入数据的流写入器
            remote (tuple): 远程地址信息 (ip, port)
        """
        self.reader = reader
        self.writer = writer
        self.remote = remote  # (ip, port)
        self.id = str(uuid.uuid4())
        self.start_time = datetime.now(timezone.utc)
        self.inputs = []  # 文本命令列表（字符串）
        self.raw_bytes = bytearray()
        self.closed = False
        self.login = None
        self.password = None

    async def send(self, data: bytes):
        """
        向客户端发送数据

        Args:
            data (bytes): 要发送的字节数据
        """
        try:
            self.writer.write(data)
            await self.writer.drain()
        except Exception as e:
            logger.debug("发送错误: %s", e)

    async def close(self):
        """
        关闭会话连接
        """
        if not self.closed:
            self.closed = True
            try:
                self.writer.close()
                await asyncio.wait_for(self.writer.wait_closed(), timeout=3)
            except Exception:
                pass

    def record_raw(self, data: bytes):
        """
        记录原始字节数据

        Args:
            data (bytes): 接收到的原始字节数据
        """
        # 保存原始字节
        self.raw_bytes.extend(data)

    def record_input(self, text: str):
        """
        记录用户输入的文本命令

        Args:
            text (str): 用户输入的命令文本
        """
        # 存储输入以供后续分析
        self.inputs.append({"ts": datetime.now(timezone.utc).isoformat(), "input": text})

    async def persist(self):
        """
        将会话数据持久化到日志文件中
        """
        # 打包会话详情
        end_time = datetime.now(timezone.utc)
        entry = {
            "session_id": self.id,
            "start_time": self.start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": (end_time - self.start_time).total_seconds(),
            "remote_ip": self.remote[0],
            "remote_port": self.remote[1],
            "login": self.login,
            "password": None if self.password is None else "<captured>",
            "inputs": self.inputs,
            "raw_base64": base64.b64encode(bytes(self.raw_bytes)).decode("ascii"),
        }
        # 持久化到JSONL
        await self.append_session_log(entry)

    # 辅助函数：安全地追加JSON行
    async def append_session_log(self, entry: dict, path=LOG_FILE):
        """
        将会话日志条目以JSON行格式追加到日志文件中

        Args:
            entry (dict): 包含会话信息的字典
            path (str): 日志文件路径
        """
        loop = asyncio.get_running_loop()
        data = json.dumps(entry, ensure_ascii=False)
        # 在线程中写入以避免长时间文件I/O阻塞事件循环
        await loop.run_in_executor(None, lambda: open(path, "a", encoding="utf-8").write(data + "\n"))


# ---------- 工具函数 ----------
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


# ---------- 主要处理函数 ----------
async def handle_telnet(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """
    处理Telnet连接的主要逻辑函数

    Args:
        reader (asyncio.StreamReader): 用于从连接中读取数据的流读取器
        writer (asyncio.StreamWriter): 用于向连接写入数据的流写入器
    """
    peer = writer.get_extra_info("peername") or ("unknown", 0)
    # 获取连接的精确时间（包含毫秒）
    connection_time = datetime.now()
    connection_time_iso = connection_time.isoformat()

    session = TelnetSession(reader, writer, peer)
    logger.info("新连接 %s 会话=%s 连接时间=%s", peer, session.id, connection_time_iso)

    try:
        # 发送系统Banner，模拟真实设备的延迟
        await asyncio.sleep(random.uniform(0.1, 0.5))
        await session.send(BANNER)

        # 检查是否有初始数据（可能是扫描工具）
        try:
            # 设置较短的超时时间来检测快速扫描
            initial_data = await asyncio.wait_for(reader.readline(), timeout=1.0)
            if initial_data:
                session.record_raw(initial_data)

                # 检查是否为扫描工具
                if is_automated_scan(initial_data):
                    logger.info("检测到自动化扫描工具，会话=%s", session.id)
                    # 对扫描工具做出适当响应
                    if b'GET /' in initial_data or b'HEAD /' in initial_data:
                        # HTTP请求响应
                        await session.send(b"HTTP/1.1 400 Bad Request\r\n")
                        await session.send(b"Content-Type: text/html\r\n")
                        await session.send(b"Connection: close\r\n")
                        await session.send(b"\r\n")
                        await session.send(b"<html><body><h1>400 Bad Request</h1></body></html>\r\n")
                        await session.close()
                        return
                    elif b'script' in initial_data.lower() or b'nmap' in initial_data.lower():
                        # Nmap脚本扫描响应，模拟SSH服务
                        await session.send(b"SSH-2.0-OpenSSH_7.9p1 Debian-10+deb10u2\r\n")
                        await asyncio.sleep(random.uniform(0.1, 0.5))
                        await session.close()
                        return
                    elif b'OPTIONS *' in initial_data:
                        # WebDAV探测
                        await session.send(b"HTTP/1.1 405 Method Not Allowed\r\n")
                        await session.send(b"Allow: GET, HEAD, POST\r\n")
                        await session.send(b"\r\n")
                        await session.close()
                        return
        except asyncio.TimeoutError:
            # 没有初始数据，继续正常流程
            pass

        # 基本的假登录序列
        await session.send(LOGIN_PROMPT)
        login_bytes = await reader.readline()
        if not login_bytes:
            await session.close()
            return
        session.record_raw(login_bytes)
        login = login_bytes.decode(errors="ignore").strip()
        session.login = login
        logger.info("会话 %s 登录=%s", session.id, login)

        await session.send(PASS_PROMPT)
        # 读取密码原始数据（我们将其视为一行）
        password_bytes = await reader.readline()
        if not password_bytes:
            await session.close()
            return
        session.record_raw(password_bytes)
        session.password = password_bytes.decode(errors="ignore").strip()

        # 模拟登录延迟和验证
        await asyncio.sleep(random.uniform(1.0, 3.0))

        # 模拟登录失败重试机制
        login_attempts = 1
        while login_attempts < 3 and (not login or not session.password):
            if login_attempts > 1:
                await session.send(b"\r\n% Login invalid\r\n\r\n")
                # 模拟真实系统在多次失败后的延迟增加
                await asyncio.sleep(random.uniform(1.0, 2.0) * login_attempts)
                await session.send(LOGIN_PROMPT)
                login_bytes = await reader.readline()
                if not login_bytes:
                    await session.close()
                    return
                session.record_raw(login_bytes)
                login = login_bytes.decode(errors="ignore").strip()
                session.login = login

                await session.send(PASS_PROMPT)
                password_bytes = await reader.readline()
                if not password_bytes:
                    await session.close()
                    return
                session.record_raw(password_bytes)
                session.password = password_bytes.decode(errors="ignore").strip()

            login_attempts += 1

        # 三次登录失败后断开连接
        if login_attempts >= 3 and (not login or not session.password):
            await session.send(b"\r\n% Login invalid\r\n")
            await session.send(b"% Login timed out after 3 minutes\r\n")
            await session.close()
            return

        # 接受任何凭据（模拟弱密码策略）
        await session.send(b"\r\nUser Access Verification\r\n\r\n")

        # 显示设备信息
        await session.send(f"{DEVICE_INFO['hostname']}>".encode())

        # 进入命令模式
        mode = "user"  # user or enable
        prompt = PROMPT

        # 交互循环：读取行，回显预设响应但记录所有内容
        while True:
            data = await reader.readline()
            if not data:
                break
            session.record_raw(data)
            # 尽力解码用于日志记录
            text = data.decode(errors="ignore").rstrip("\r\n")
            session.record_input(text)
            logger.info("会话 %s 输入: %s", session.id, text)

            # 简单命令处理（网络设备命令）
            lowered = text.strip().lower()
            original_text = text.strip()

            if lowered in ("exit", "quit"):
                await session.send(b"\r\n% Connection closed by foreign host.\r\n")
                break
            elif lowered == "logout":
                await session.send(b"\r\n% Logout successful.\r\n")
                break
            elif lowered == "enable":
                # 进入特权模式
                mode = "enable"
                prompt = ENABLE_PROMPT
                await session.send(prompt)
                continue
            elif lowered.startswith("disable"):
                # 退出特权模式
                mode = "user"
                prompt = PROMPT
                await session.send(prompt)
                continue
            elif lowered == "show version" or lowered == "sh ver":
                await simulate_command_execution(0.5, 1.5)
                await session.send(f"\r\nCisco IOS Software, {DEVICE_INFO['hardware']} Software (C2800NM-ADVENTERPRISEK9-M), Version {DEVICE_INFO['version']}, RELEASE SOFTWARE (fc1)\r\n".encode())
                await session.send(b"Technical Support: http://www.cisco.com/techsupport\r\n")
                await session.send(b"Copyright (c) 1986-2010 by Cisco Systems, Inc.\r\n")
                await session.send(b"Compiled Thu 09-Sep-10 13:53 by prod_rel_team\r\n\r\n")
                await session.send(f"ROM: System Bootstrap, Version 12.4(13r)T11, RELEASE SOFTWARE (fc1)\r\n\r\n".encode())
                await session.send(f"{DEVICE_INFO['hostname']} uptime is {DEVICE_INFO['uptime']}\r\n".encode())
                await session.send(b"System returned to ROM by power-on\r\n")
                await session.send(b"System image file is \"flash:c2800nm-adventerprisek9-mz.124-25b.bin\"\r\n\r\n")
                await session.send(b"This product contains cryptographic features and is subject to United\r\n")
                await session.send(b"States and local country laws governing import, export, transfer and\r\n")
                await session.send(b"use. Delivery of Cisco cryptographic products does not imply\r\n")
                await session.send(b"third-party authority to import, export, distribute or use encryption.\r\n")
                await session.send(b"Importers, exporters, distributors and users are responsible for\r\n")
                await session.send(b"compliance with U.S. and local country laws. By using this product you\r\n")
                await session.send(b"agree to comply with applicable laws and regulations. If you are unable\r\n")
                await session.send(b"to comply with U.S. and local laws, return this product immediately.\r\n\r\n")
                await session.send(b"A summary of U.S. laws governing Cisco cryptographic products may be found at:\r\n")
                await session.send(b"http://www.cisco.com/wwl/export/crypto/tool/stqrg.html\r\n\r\n")
                await session.send(b"If you require further assistance please contact us by sending email to\r\n")
                await session.send(b"export@cisco.com.\r\n\r\n")
                await session.send(b"cisco {DEVICE_INFO['hardware']} (revision 2.0) with 503808K/24576K bytes of memory.\r\n".encode())
                await session.send(b"Processor board ID FTX1043A0K8\r\n")
                await session.send(b"2 FastEthernet interfaces\r\n")
                await session.send(b"1 Serial interface\r\n")
                await session.send(b"1 Virtual Private Network (VPN) Module\r\n")
                await session.send(b"4 Network Processing Engine(s)\r\n")
                await session.send(b"DRAM configuration is 64 bits wide with parity enabled.\r\n")
                await session.send(b"255K bytes of non-volatile configuration memory.\r\n")
                await session.send(b"62464K bytes of ATA CompactFlash (Read/Write)\r\n\r\n")
                await session.send(b"Configuration register is 0x2102\r\n")
            elif lowered == "show ip interface brief" or lowered == "sh ip int br":
                await simulate_command_execution(0.5, 1.2)
                await session.send(b"\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\n")
                await session.send(b"FastEthernet0/0            192.168.1.1     YES NVRAM  up                    up      \r\n")
                await session.send(b"FastEthernet0/1            10.0.0.1        YES NVRAM  administratively down down    \r\n")
                await session.send(b"Serial0/0/0                unassigned      YES NVRAM  up                    up      \r\n")
            elif lowered == "show interfaces" or lowered == "sh int":
                await simulate_command_execution(1.0, 2.5)
                for interface in DEVICE_INFO["interfaces"]:
                    await session.send(f"\r\n{interface} is up, line protocol is up\r\n".encode())
                    await session.send(b"  Hardware is CNFGT, address is 0000.0000.0000 (bia 0000.0000.0000)\r\n")
                    await session.send(b"  MTU 1500 bytes, BW 100000 Kbit, DLY 100 usec,\r\n")
                    await session.send(b"     reliability 255/255, txload 1/255, rxload 1/255\r\n")
                    await session.send(b"  Encapsulation ARPA, loopback not set\r\n")
                    await session.send(b"  Keepalive set (10 sec)\r\n")
                    await session.send(b"  Full-duplex, 100Mb/s, 100BaseTX/FX\r\n")
                    await session.send(b"  ARP type: ARPA, ARP Timeout 04:00:00\r\n")
                    rx_pkts = random.randint(10000, 999999)
                    tx_pkts = random.randint(10000, 999999)
                    await session.send(f"  Last input 00:00:02, output 00:00:01, output hang never\r\n".encode())
                    await session.send(f"  Last clearing of \"show interface\" counters never\r\n".encode())
                    await session.send(f"  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0\r\n".encode())
                    await session.send(f"  Queueing strategy: fifo\r\n".encode())
                    await session.send(f"  Output queue: 0/40 (size/max)\r\n".encode())
                    await session.send(f"  5 minute input rate 0 bits/sec, 0 packets/sec\r\n".encode())
                    await session.send(f"  5 minute output rate 0 bits/sec, 0 packets/sec\r\n".encode())
                    await session.send(f"     {rx_pkts} packets input, {rx_pkts*random.randint(64, 1500)} bytes\r\n".encode())
                    await session.send(f"     Received {random.randint(0, 10)} broadcasts (0 IP multicasts)\r\n".encode())
                    await session.send(f"     0 runts, 0 giants, 0 throttles\r\n".encode())
                    await session.send(f"     {random.randint(0, 5)} input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored\r\n".encode())
                    await session.send(f"     0 watchdog, 0 multicast, 0 pause input\r\n".encode())
                    await session.send(f"     {tx_pkts} packets output, {tx_pkts*random.randint(64, 1500)} bytes, 0 underruns\r\n".encode())
                    await session.send(f"     0 output errors, 0 collisions, 1 interface resets\r\n".encode())
                    await session.send(f"     0 babbles, 0 late collision, 0 deferred\r\n".encode())
                    await session.send(f"     0 lost carrier, 0 no carrier, 0 PAUSE output\r\n".encode())
                    await session.send(f"     0 output buffer failures, 0 output buffers swapped out\r\n".encode())
            elif lowered == "show running-config" or lowered == "sh run":
                await simulate_command_execution(1.5, 3.0)
                await session.send(b"\r\nBuilding configuration...\r\n\r\n")
                await session.send(b"Current configuration : 2048 bytes\r\n")
                await session.send(b"!\r\n")
                await session.send(b"version 12.4\r\n")
                await session.send(b"no service pad\r\n")
                await session.send(b"service timestamps debug datetime msec\r\n")
                await session.send(b"service timestamps log datetime msec\r\n")
                await session.send(b"no service password-encryption\r\n")
                await session.send(b"!\r\n")
                await session.send(f"hostname {DEVICE_INFO['hostname']}\r\n".encode())
                await session.send(b"!\r\n")
                await session.send(b"boot-start-marker\r\n")
                await session.send(b"boot-end-marker\r\n")
                await session.send(b"!\r\n")
                await session.send(b"enable secret 5 $1$1234$abcdefghijklmnopqrstuvwx\r\n")
                await session.send(b"!\r\n")
                await session.send(b"username admin privilege 15 password 0 admin\r\n")
                await session.send(b"username user password 0 password\r\n")
                await session.send(b"!\r\n")
                await session.send(b"interface FastEthernet0/0\r\n")
                await session.send(b" ip address 192.168.1.1 255.255.255.0\r\n")
                await session.send(b" ip nat inside\r\n")
                await session.send(b" ip virtual-reassembly\r\n")
                await session.send(b" duplex auto\r\n")
                await session.send(b" speed auto\r\n")
                await session.send(b"!\r\n")
                await session.send(b"interface FastEthernet0/1\r\n")
                await session.send(b" no ip address\r\n")
                await session.send(b" shutdown\r\n")
                await session.send(b" duplex auto\r\n")
                await session.send(b" speed auto\r\n")
                await session.send(b"!\r\n")
                await session.send(b"interface Serial0/0/0\r\n")
                await session.send(b" no ip address\r\n")
                await session.send(b"!\r\n")
                await session.send(b"ip route 0.0.0.0 0.0.0.0 Serial0/0/0\r\n")
                await session.send(b"!\r\n")
                await session.send(b"ip http server\r\n")
                await session.send(b"no ip http secure-server\r\n")
                await session.send(b"!\r\n")
                await session.send(b"control-plane\r\n")
                await session.send(b"!\r\n")
                await session.send(b"line con 0\r\n")
                await session.send(b" exec-timeout 0 0\r\n")
                await session.send(b" privilege level 15\r\n")
                await session.send(b" logging synchronous\r\n")
                await session.send(b"line aux 0\r\n")
                await session.send(b"line vty 0 4\r\n")
                await session.send(b" login local\r\n")
                await session.send(b" transport input telnet\r\n")
                await session.send(b"!\r\n")
                await session.send(b"end\r\n")
            elif lowered == "show startup-config" or lowered == "sh start":
                await simulate_command_execution(0.8, 1.8)
                await session.send(b"\r\nstartup-config is not set\r\n")
            elif lowered == "show users" or lowered == "sh users":
                await simulate_command_execution(0.3, 0.8)
                await session.send(b"\r\n    Line       User       Host(s)              Idle       Location\r\n")
                await session.send(f"   0 con 0                {peer[0]}               00:00:00   \r\n".encode())
                await session.send(b"*  1 vty 0     admin      192.168.1.100        00:00:02   \r\n")
                await session.send(b"   2 vty 1                idle                 01:23:45   \r\n")
            elif lowered == "show processes" or lowered == "sh proc":
                await simulate_command_execution(0.8, 2.0)
                await session.send(b"\r\nCPU utilization for five seconds: 1%/0%; one minute: 2%; five minutes: 1%\r\n")
                await session.send(b" PID Runtime(ms)     Invoked      uSecs   5Sec   1Min   5Min TTY Process\r\n")
                await session.send(b"   1          12        1605          7  0.00%  0.00%  0.00%   0 Chunk Manager\r\n")
                await session.send(b"   2           4         542          7  0.00%  0.00%  0.00%   0 Load Meter\r\n")
                await session.send(b"   3         100        1500         66  0.00%  0.00%  0.00%   0 DHCPD Timer\r\n")
                await session.send(b"   4        2000       12000        166  0.00%  0.00%  0.00%   0 IP SNMP\r\n")
                await session.send(b"   5         150        1200        125  0.00%  0.00%  0.00%   0 TCP Timer\r\n")
            elif lowered == "help":
                await session.send(b"\r\nCisco CLI Help System\r\n\r\n")
                await session.send(b"show version                - System hardware and software status\r\n")
                await session.send(b"show interfaces             - Interface status and configuration\r\n")
                await session.send(b"show ip interface brief     - Brief IP interface status\r\n")
                await session.send(b"show running-config         - Current system configuration\r\n")
                await session.send(b"show startup-config         - Startup configuration\r\n")
                await session.send(b"show users                  - Display information about terminal lines\r\n")
                await session.send(b"show processes              - CPU usage statistics\r\n")
                await session.send(b"enable                      - Turn on privileged commands\r\n")
                await session.send(b"disable                     - Turn off privileged commands\r\n")
                await session.send(b"exit                        - Exit from the EXEC\r\n")
                await session.send(b"logout                      - Exit from the EXEC\r\n")
            elif lowered.startswith("ping "):
                await simulate_command_execution(1.0, 2.0)
                target = original_text[5:].strip()
                if target:
                    await session.send(f"\r\nType escape sequence to abort.\r\n".encode())
                    await session.send(f"Sending 5, 100-byte ICMP Echos to {target}, timeout is 2 seconds:\r\n".encode())
                    await session.send(b"!!!!!\r\n")
                    await session.send(b"Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/1 ms\r\n")
                else:
                    await session.send(b"\r\nUsage: ping <target>\r\n")
            elif lowered.startswith("traceroute "):
                await simulate_command_execution(1.5, 3.0)
                target = original_text[11:].strip()
                if target:
                    await session.send(f"\r\nType escape sequence to abort.\r\n".encode())
                    await session.send(f"Tracing the route to {target}\r\n\r\n".encode())
                    await session.send(b"  1 192.168.1.1 0 msec 0 msec 4 msec\r\n")
                    await session.send(b"  2 10.0.0.1 4 msec 4 msec 4 msec\r\n")
                    await session.send(b"  3 8.8.8.8 8 msec *  8 msec\r\n")
                else:
                    await session.send(b"\r\nUsage: traceroute <target>\r\n")
            elif lowered == "reload":
                await session.send(b"\r\nProceed with reload? [confirm]\r\n")
                # 等待确认
                confirm = await reader.readline()
                session.record_raw(confirm)
                confirm_text = confirm.decode(errors="ignore").rstrip("\r\n")
                session.record_input(confirm_text)
                if confirm_text.lower() in ["y", "yes", ""]:
                    await session.send(b"\r\nSystem configuration has been modified. Save? [yes/no]:\r\n")
                    save_confirm = await reader.readline()
                    session.record_raw(save_confirm)
                    save_text = save_confirm.decode(errors="ignore").rstrip("\r\n")
                    session.record_input(save_text)
                    await session.send(b"\r\nBuilding configuration...\r\n")
                    await session.send(b"[OK]\r\n")
                    await session.send(b"Reloading...\r\n")
                    await asyncio.sleep(2)
                    await session.send(b"\r\n% Connection closed by foreign host.\r\n")
                    break
                else:
                    await session.send(b"\r\nReload cancelled.\r\n")
            else:
                # 通用错误消息，模拟真实网络设备
                if mode == "user" and lowered.startswith("show"):
                    await session.send(b"\r\n% Incomplete command.\r\n\r\n")
                else:
                    await session.send(b"\r\n% Ambiguous command:  \"" + original_text.encode() + b"\"\r\n\r\n")

            await session.send(prompt)

    except Exception as exc:
        logger.exception("会话 %s 异常: %s", session.id, exc)
    finally:
        try:
            # 在会话持久化之前添加连接时间信息
            await session.persist()
        except Exception as e:
            logger.exception("持久化错误: %s", e)
        await session.close()
        logger.info("关闭会话 %s 来自 %s", session.id, peer)


async def start_server(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """
    启动TelnetService 服务器

    Args:
        host (str): 监听的主机地址
        port (int): 监听的端口号
    """
    server = await asyncio.start_server(handle_telnet, host, port)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    logger.info("TelnetService 监听于 %s", addrs)
    async with server:
        await server.serve_forever()


def parse_args():
    """
    解析命令行参数

    Returns:
        argparse.Namespace: 解析后的命令行参数
    """
    p = argparse.ArgumentParser(description="Standalone Telnet Honeypot Service")
    p.add_argument("--host", default=DEFAULT_HOST)
    p.add_argument("--port", default=DEFAULT_PORT, type=int)
    p.add_argument("--log", default=LOG_FILE)
    return p.parse_args()


def main():
    """
    程序主入口函数
    """
    args = parse_args()
    global LOG_FILE
    LOG_FILE = args.log
    logger.info("启动Service  (主机=%s 端口=%d) 日志=%s", args.host, args.port, LOG_FILE)
    try:
        asyncio.run(start_server(args.host, args.port))
    except KeyboardInterrupt:
        logger.info("正在关闭。")
    except Exception as exc:
        logger.exception("致命错误: %s", exc)


if __name__ == "__main__":
    main()
