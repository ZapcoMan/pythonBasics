#!/usr/bin/env python3
# telnet_honeypot.py
# 简单的基于asyncio的TelnetService （单协议版本）
# 将会话元数据和所有输入记录到JSONL文件中。

import argparse
import asyncio
import logging
import random
import datetime

from 网络安全.蜜罐.单协议Telnet蜜罐.TelnetSession import TelnetSession

# ---------- 配置 ----------
# 更真实的系统Banner
BANNER = b"Debian GNU/Linux 11\r\n" + \
         b"server01 login: "

# 更真实的提示符
PROMPT = b"root@server01:~# "
LOGIN_PROMPT = b"login: "
PASS_PROMPT = b"Password: "

# 模拟系统信息
SYSTEM_INFO = {
    "hostname": "server01",
    "os": "Debian GNU/Linux 11",
    "kernel": "5.10.0-11-amd64",
    "users": ["root", "admin", "user", "guest"],
    "processes": [
        "systemd", "sshd", "apache2", "mysql", "cron",
        "rsyslog", "networkd", "supervisord"
    ],
    "filesystems": [
        ("/dev/sda1", "ext4", "20G", "8.2G", "11G", "43%", "/"),
        ("/dev/sda2", "ext4", "50G", "15G", "33G", "32%", "/home"),
        ("tmpfs", "tmpfs", "2.0G", "0", "2.0G", "0%", "/run")
    ]
}

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
        # 发送系统Banner
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

        # 模拟登录延迟和验证
        await asyncio.sleep(random.uniform(0.5, 2.0))

        # 接受任何凭据（模拟弱密码策略）
        await session.send(b"\r\nLinux server01 5.10.0-11-amd64 #1 SMP Debian 5.10.92-1 (2022-01-18) x86_64\r\n")
        await session.send(b"\r\nThe programs included with the Debian GNU/Linux system are free software;\r\n")
        await session.send(b"the exact distribution terms for each program are described in the\r\n")
        await session.send(b"individual files in /usr/share/doc/*/copyright.\r\n")
        await session.send(b"\r\nDebian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent\r\n")
        await session.send(b"permitted by applicable law.\r\n")

        # 显示上次登录信息
        last_login_time = datetime.datetime.now() - datetime.timedelta(
            minutes=random.randint(10, 1000))
        await session.send(f"\r\nLast login: {last_login_time.strftime('%a %b %d %H:%M')} from 192.168.1.105\r\n".encode())

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
                await session.send(b"logout\r\n")
                break
            elif lowered.startswith("get "):
                # 假装显示文件列表
                await session.send(b"dummy-file.txt\r\n")
            elif lowered == "whoami":
                await session.send(f"{session.login}\r\n".encode())
            elif lowered == "id":
                await session.send(f"uid=0({session.login}) gid=0(root) groups=0(root)\r\n".encode())
            elif lowered == "uname -a":
                await session.send(f"Linux {SYSTEM_INFO['hostname']} {SYSTEM_INFO['kernel']} #1 SMP Debian 5.10.92-1 (2022-01-18) x86_64 GNU/Linux\r\n".encode())
            elif lowered == "ls":
                await session.send(b"Desktop  Documents  Downloads  Pictures  Public  Templates  Videos\r\n")
            elif lowered == "ls -la":
                await session.send(b"total 48\r\n"
                                   b"drwx------ 10 root root 4096 Feb 15 10:22 .\r\n"
                                   b"drwxr-xr-x 19 root root 4096 Feb 10 09:15 ..\r\n"
                                   b"-rw-------  1 root root  234 Feb 15 10:22 .bash_history\r\n"
                                   b"-rw-r--r--  1 root root  220 Feb 10 09:15 .bash_logout\r\n"
                                   b"-rw-r--r--  1 root root 3771 Feb 10 09:15 .bashrc\r\n"
                                   b"drwx------  3 root root 4096 Feb 10 09:18 .cache\r\n"
                                   b"drwxr-xr-x  3 root root 4096 Feb 10 09:18 .local\r\n"
                                   b"-rw-r--r--  1 root root  807 Feb 10 09:15 .profile\r\n"
                                   b"drwx------  2 root root 4096 Feb 15 10:22 .ssh\r\n"
                                   b"drwxr-xr-x  2 root root 4096 Feb 10 09:20 Desktop\r\n"
                                   b"drwxr-xr-x  2 root root 4096 Feb 10 09:20 Documents\r\n"
                                   b"drwxr-xr-x  2 root root 4096 Feb 10 09:20 Downloads\r\n"
                                   b"drwxr-xr-x  2 root root 4096 Feb 10 09:20 Pictures\r\n")
            elif lowered == "pwd":
                await session.send(b"/root\r\n")
            elif lowered == "cat /etc/passwd":
                passwd_content = "\r\n".join([
                    "root:x:0:0:root:/root:/bin/bash",
                    "daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin",
                    "bin:x:2:2:bin:/bin:/usr/sbin/nologin",
                    "sys:x:3:3:sys:/dev:/usr/sbin/nologin",
                    "sync:x:4:65534:sync:/bin:/bin/sync",
                    "games:x:5:60:games:/usr/games:/usr/sbin/nologin",
                    "man:x:6:12:man:/var/cache/man:/usr/sbin/nologin",
                    "admin:x:1001:1001:Admin User,,,:/home/admin:/bin/bash",
                    "user:x:1002:1002:Regular User,,,:/home/user:/bin/bash"
                ]) + "\r\n"
                await session.send(passwd_content.encode())
            elif lowered == "ps aux":
                ps_header = b"USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\r\n"
                ps_lines = []
                for i, proc in enumerate(SYSTEM_INFO["processes"]):
                    ps_lines.append(f"root      {1000+i:5}  0.0  0.1  {random.randint(10000, 99999):6}  {random.randint(1000, 9999):4}  ?        Ss   Feb10   0:{random.randint(10, 59):02} {proc}".encode())
                await session.send(ps_header + b"\r\n".join(ps_lines) + b"\r\n")
            elif lowered == "df -h":
                df_header = b"Filesystem      Size  Used Avail Use% Mounted on\r\n"
                df_lines = []
                for fs in SYSTEM_INFO["filesystems"]:
                    df_lines.append(f"{fs[0]:15} {fs[2]:>4} {fs[3]:>4} {fs[4]:>4} {fs[5]:>3} {fs[6]}".encode())
                await session.send(df_header + b"\r\n".join(df_lines) + b"\r\n")
            elif lowered == "help":
                await session.send(b"Supported commands: ls, ls -la, cat, ps aux, df -h, whoami, id, uname -a, pwd, help, exit, quit, logout\r\n")
            elif lowered.startswith("cat "):
                filename = lowered[4:].strip()
                if filename in ["/etc/issue", "/etc/motd"]:
                    await session.send(b"Debian GNU/Linux 11 \\n \\l\r\n")
                elif filename == "/proc/version":
                    await session.send(f"Linux version {SYSTEM_INFO['kernel']} (debian-kernel@lists.debian.org) (gcc-10 (Debian 10.2.1-6) 10.2.1 20210110, GNU ld (GNU Binutils for Debian) 2.35.2) #1 SMP Debian 5.10.92-1 (2022-01-18)\r\n".encode())
                else:
                    await session.send(f"cat: {filename}: No such file or directory\r\n".encode())
            elif lowered.startswith("echo "):
                message = text[5:]  # Skip "echo "
                await session.send(f"{message}\r\n".encode())
            else:
                # 通用回显
                await session.send(b"bash: " + text.encode() + b": command not found\r\n")
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
