#!/usr/bin/env python3
# TelnetSession.py
# Telnet会话类，用于处理单个Telnet连接的生命周期

import asyncio
import logging
import json
import uuid
import base64
from datetime import datetime, timezone

# 设置Python日志记录用于操作员日志（不是会话日志）
logger = logging.getLogger("honeypot")

# ---------- 配置 ----------
LOG_FILE = "honeypot_sessions.jsonl"
# ---------- 配置结束 ----------

# 辅助函数：安全地追加JSON行
async def append_session_log(entry: dict, path=LOG_FILE):
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
        await append_session_log(entry)
