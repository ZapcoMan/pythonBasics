#!/usr/bin/env python3
# telnet_honeypot.py
# 简单的基于asyncio的TelnetService （单协议版本）
# 将会话元数据和所有输入记录到JSONL文件中。

import argparse
import asyncio
import logging

from 网络安全.蜜罐.单协议Telnet蜜罐.TelnetSession import TelnetSession

# ---------- 配置 ----------
BANNER = b"Welcome to MiniTelnet Service\r\n" 
PROMPT = b"shell> "
LOGIN_PROMPT = b"login: "
PASS_PROMPT = b"password: "

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 2323  # 如果你控制基础设施，使用23；2323避免需要root权限

LOG_FILE = "honeypot_sessions.jsonl"
# 你可以在这里更改编码/原始数据保存策略
# ---------- 配置结束 ----------

# 设置Python日志记录用于操作员日志（不是会话日志）
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("honeypot")


async def handle_telnet(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """
    处理Telnet连接的主要逻辑函数

    Args:
        reader (asyncio.StreamReader): 用于从连接中读取数据的流读取器
        writer (asyncio.StreamWriter): 用于向连接写入数据的流写入器
    """
    peer = writer.get_extra_info("peername") or ("unknown", 0)
    session = TelnetSession(reader, writer, peer)
    logger.info("新连接 %s 会话=%s", peer, session.id)

    try:
        # 横幅
        await session.send(BANNER)

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

        # 接受任何凭据
        await session.send(b"\r\nLogin successful.\r\n")
        await session.send(PROMPT)

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

            # 简单命令处理（非详尽）
            lowered = text.strip().lower()
            if lowered in ("exit", "quit", "logout"):
                await session.send(b"Goodbye.\r\n")
                break
            elif lowered.startswith("get "):
                # 假装显示文件列表
                await session.send(b"dummy-file.txt\r\n")
            elif lowered == "whoami":
                await session.send(f"{session.login}\r\n".encode())
            else:
                # 通用回显
                await session.send(b"Command received: " + data)
            await session.send(PROMPT)

    except Exception as exc:
        logger.exception("会话 %s 异常: %s", session.id, exc)
    finally:
        try:
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
    p = argparse.ArgumentParser(description="Mini TelnetService  (asyncio)")
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
