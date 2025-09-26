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

    BANNER = b"Welcome to MiniTelnet Service\r\nAuthorized access only.\r\n"
    PROMPT = b"mini-shell> "
    LOGIN_PROMPT = b"login: "
    PASS_PROMPT = b"password: "

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
            writer.write(self.BANNER)
            await writer.drain()

            writer.write(self.LOGIN_PROMPT)
            await writer.drain()
            login = await reader.readline()
            if not login:
                raise ConnectionResetError("登录为空")
            raw_buf.extend(login)
            login_text = login.decode(errors="ignore").strip()

            writer.write(self.PASS_PROMPT)
            await writer.drain()
            pwd = await reader.readline()
            if not pwd:
                raise ConnectionResetError("密码为空")
            raw_buf.extend(pwd)
            pwd_text = pwd.decode(errors="ignore").strip()

            # 接受任何凭据但不在日志中写入实际密码（掩码）
            writer.write(b"\r\nLogin successful.\r\n")
            writer.write(self.PROMPT)
            await writer.drain()

            while True:
                data = await reader.readline()
                if not data:
                    break
                raw_buf.extend(data)
                txt = data.decode(errors="ignore").rstrip("\r\n")
                inputs.append({"ts": datetime.now(timezone.utc).isoformat(), "input": txt})
                op_logger.debug("Telnet %s 输入: %s", session_id, txt)

                cmd = txt.strip().lower()
                if cmd in ("exit", "quit", "logout"):
                    writer.write(b"Goodbye.\r\n")
                    await writer.drain()
                    break
                elif cmd.startswith("get "):
                    writer.write(b"dummy-file.txt\r\n")
                elif cmd == "whoami":
                    writer.write((login_text + "\r\n").encode())
                else:
                    writer.write(b"Command received: " + data)
                writer.write(self.PROMPT)
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
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            op_logger.info("Telnet关闭会话 %s 来自 %s", session_id, peer)

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
            await self._send_line(writer, "220 mini-ftp Service ready")
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
                    await self._send_line(writer, "331 Username ok, need password")
                elif cmd == "PASS":
                    await self._send_line(writer, "230 Login successful")
                    authenticated = True
                elif cmd == "SYST":
                    await self._send_line(writer, "215 UNIX Type: L8")
                elif cmd == "PWD":
                    await self._send_line(writer, '257 "/" is current directory')
                elif cmd == "CWD":
                    await self._send_line(writer, "250 Directory changed")
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
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                raw_buf.extend(data)
                # 回显
                writer.write(data)
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

    RESPONSE_BODY = b"<html><body><h1>Fake HTTP Service</h1></body></html>"

    def __init__(self, host, port, log_file):
        """
        初始化HTTP处理器

        Args:
            host (str): 监听主机地址
            port (int): 监听端口
            log_file (str): 日志文件路径
        """
        super().__init__("http", host, port, log_file)

    async def start(self):
        """
        启动HTTP服务器
        """
        self._server = await asyncio.start_server(self._handle, host=self.host, port=self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
        op_logger.info("HTTP监听于 %s", addrs)
        asyncio.create_task(self._server.serve_forever())

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
            # 响应简单页面
            body = self.RESPONSE_BODY
            resp = b"HTTP/1.1 200 OK\r\nContent-Length: %d\r\nContent-Type: text/html; charset=utf-8\r\n\r\n%s" % (len(body), body)
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

    async def start(self):
        """
        启动HTTPS服务器
        """
        try:
            # 创建SSL上下文
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # 福建旧版本
            ctx.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
            self._server = await asyncio.start_server(self._handle, host=self.host, port=self.port, ssl=ctx)
            addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
            op_logger.info("HTTPS监听于 %s", addrs)
            asyncio.create_task(self._server.serve_forever())
        except FileNotFoundError:
            op_logger.error("找不到SSL证书文件: certfile=%s keyfile=%s", self.certfile, self.keyfile)
            op_logger.error("请使用--generate-cert参数自动生成证书，或手动提供证书文件")
        except Exception as e:
            op_logger.exception("HTTPS服务器启动失败: %s", e)


# ---------------------- SSH处理器（仅横幅） -------------------------
class SSHHandler(ProtocolHandler):
    """
    SSH协议处理器，模拟SSH服务端并捕获客户端连接信息
    """

    BANNER = b"SSH-2.0-OpenSSH_8.2p1 FakeHoneypot\r\n"

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
