#!/usr/bin/env python3
# telnet_honeypot.py
# 简单的基于asyncio的TelnetService （单协议版本）
# 将会话元数据和所有输入记录到JSONL文件中。

import argparse
import asyncio
import logging
import random
import datetime
import re

from 网络安全.蜜罐.单协议Telnet蜜罐.TelnetSession import TelnetSession

# ---------- 配置 ----------
# 更真实的系统Banner
BANNER = b"\r\n\r\nDebian GNU/Linux 11\r\n" + \
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
    ],
    "network": [
        ("lo", "127.0.0.1", "255.0.0.0"),
        ("eth0", "192.168.1.101", "255.255.255.0")
    ],
    "memory": {
        "total": "2048000",  # KB
        "free": "819000",
        "buffers": "123000",
        "cached": "456000"
    }
}

# 模拟文件系统内容
FILESYSTEM = {
    "/": ["bin", "boot", "dev", "etc", "home", "lib", "lib64", "media", "mnt", "opt", "proc", "root", "run", "sbin", "srv", "sys", "tmp", "usr", "var"],
    "/etc": ["passwd", "group", "hosts", "hostname", "resolv.conf", "motd", "issue", "network", "apache2", "mysql"],
    "/var/log": ["syslog", "auth.log", "kern.log", "mail.log", "daemon.log"],
    "/home": ["admin", "user"],
    "/home/admin": [".bashrc", ".profile", "readme.txt"],
    "/home/user": [".bashrc", ".profile"],
    "/tmp": ["test.tmp", "tempfile.log"],
    "/var/www": ["html"],
    "/var/www/html": ["index.html", "test.php"]
}

# 模拟文件内容
FILE_CONTENTS = {
    "/etc/hosts": "127.0.0.1\tlocalhost\n192.168.1.101\tserver01\n::1\tlocalhost ip6-localhost ip6-loopback\n",
    "/etc/hostname": "server01\n",
    "/etc/resolv.conf": "nameserver 8.8.8.8\nnameserver 8.8.4.4\n",
    "/proc/meminfo": "\n".join([
        "MemTotal:        2048000 kB",
        "MemFree:          819000 kB",
        "MemAvailable:    1200000 kB",
        "Buffers:          123000 kB",
        "Cached:           456000 kB",
        "SwapTotal:       1024000 kB",
        "SwapFree:        1024000 kB"
    ]) + "\n",
    "/proc/cpuinfo": "\n".join([
        "processor\t: 0",
        "vendor_id\t: GenuineIntel",
        "cpu family\t: 6",
        "model\t\t: 142",
        "model name\t: Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz",
        "stepping\t: 10",
        "cpu MHz\t\t: 1992.000",
        "cache size\t: 8192 KB"
    ]) + "\n",
    "/home/admin/readme.txt": "This is a readme file for admin user.\nContains some basic information.\n",
    "/var/www/html/index.html": "<html>\n<head><title>Welcome to server01</title></head>\n<body>\n<h1>Welcome to server01</h1>\n<p>This is a default web page.</p>\n</body>\n</html>\n",
    "/var/www/html/test.php": "<?php\n// Test PHP file\necho 'Hello World';\n?>\n"
}

# 模拟环境变量
ENV_VARS = {
    "HOME": "/root",
    "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "SHELL": "/bin/bash",
    "USER": "root",
    "LOGNAME": "root",
    "PWD": "/root",
    "LANG": "en_US.UTF-8"
}

# 模拟命令历史
COMMAND_HISTORY = [
    "ls -la",
    "cat /etc/passwd",
    "ps aux",
    "df -h",
    "free -h",
    "uname -a"
]

# 模拟服务列表
SERVICES = [
    ("ssh", "sshd", "listening on 0.0.0.0:22"),
    ("http", "apache2", "listening on 0.0.0.0:80"),
    ("mysql", "mysqld", "listening on 127.0.0.1:3306")
]

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 2323  # 如果你控制基础设施，使用23；2323避免需要root权限

LOG_FILE = "honeypot_sessions.jsonl"
# 你可以在这里更改编码/原始数据保存策略
# ---------- 配置结束 ----------

# 设置Python日志记录用于操作员日志（不是会话日志）
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("honeypot")


# 辅助函数：生成随机MAC地址
def generate_mac():
    return ":".join(["%02x" % random.randint(0, 255) for _ in range(6)])


# 辅助函数：获取目录内容
def get_directory_contents(path):
    if path in FILESYSTEM:
        return FILESYSTEM[path]
    # 处理子目录情况
    for key in FILESYSTEM:
        if path.startswith(key) and len(path) > len(key) and path[len(key)] == '/':
            return FILESYSTEM.get(key, [])
    return []


# 辅助函数：获取文件内容
def get_file_content(filepath):
    if filepath in FILE_CONTENTS:
        return FILE_CONTENTS[filepath]
    for key in FILE_CONTENTS:
        if filepath.startswith(key):
            return FILE_CONTENTS[key]
    return None


# 模拟命令执行时间
async def simulate_command_execution():
    # 模拟命令执行的延迟
    await asyncio.sleep(random.uniform(0.1, 1.0))


async def handle_telnet(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """
    处理Telnet连接的主要逻辑函数

    Args:
        reader (asyncio.StreamReader): 用于从连接中读取数据的流读取器
        writer (asyncio.StreamWriter): 用于向连接写入数据的流写入器
    """
    peer = writer.get_extra_info("peername") or ("unknown", 0)
    # 获取连接的精确时间（包含毫秒）
    connection_time = datetime.datetime.now()
    connection_time_iso = connection_time.isoformat()

    session = TelnetSession(reader, writer, peer)
    logger.info("新连接 %s 会话=%s 连接时间=%s", peer, session.id, connection_time_iso)

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

        # 模拟登录失败重试机制
        login_attempts = 1
        while login_attempts < 3 and (not login or not session.password):
            if login_attempts > 1:
                await session.send(b"\r\nLogin incorrect\r\n")
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
            await session.send(b"\r\nLogin incorrect\r\n")
            await session.send(b"Login timed out after 3 minutes\r\n")
            await session.close()
            return

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

        # 显示系统消息
        await session.send(b"No mail.\r\n")

        current_path = "/root"
        command_history = COMMAND_HISTORY.copy()
        env_vars = ENV_VARS.copy()

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
            original_text = text.strip()

            # 处理cd命令和路径
            if lowered.startswith("cd "):
                new_path = lowered[3:].strip()
                if new_path == "" or new_path == "~":
                    current_path = "/root"
                elif new_path == "..":
                    if current_path != "/":
                        parts = current_path.split("/")
                        current_path = "/".join(parts[:-1]) if len(parts) > 2 else "/"
                elif new_path.startswith("/"):
                    current_path = new_path
                else:
                    current_path = current_path.rstrip("/") + "/" + new_path
                env_vars["PWD"] = current_path
                await session.send(PROMPT)
                continue

            # 根据当前路径更新提示符
            prompt = f"{session.login}@{SYSTEM_INFO['hostname']}:{current_path}# ".encode() if current_path != "/root" else PROMPT

            if lowered in ("exit", "quit", "logout"):
                await session.send(b"logout\r\n")
                break
            elif lowered.startswith("get "):
                # 假装显示文件列表
                await session.send(b"dummy-file.txt\r\n")
            elif lowered == "whoami":
                await simulate_command_execution()
                await session.send(f"{session.login}\r\n".encode())
            elif lowered == "id":
                await simulate_command_execution()
                await session.send(f"uid=0({session.login}) gid=0(root) groups=0(root)\r\n".encode())
            elif lowered == "uname -a":
                await simulate_command_execution()
                await session.send(f"Linux {SYSTEM_INFO['hostname']} {SYSTEM_INFO['kernel']} #1 SMP Debian 5.10.92-1 (2022-01-18) x86_64 GNU/Linux\r\n".encode())
            elif lowered == "ls":
                await simulate_command_execution()
                contents = get_directory_contents(current_path)
                if contents:
                    await session.send("  ".join(contents).encode() + b"\r\n")
                else:
                    await session.send(b"\r\n")
            elif lowered == "ls -l" or lowered == "ls -la":
                await simulate_command_execution()
                contents = get_directory_contents(current_path)
                if contents:
                    # 生成类似 ls -l 的输出
                    output_lines = [f"total {len(contents)}"]
                    dir_count = 0
                    for item in contents:
                        is_dir = item in [d.lstrip("/") for d in FILESYSTEM.keys() if d.startswith(current_path)]
                        perms = "drwxr-xr-x" if is_dir else "-rw-r--r--"
                        size = random.randint(1000, 10000) if not is_dir else 4096
                        date = "Feb 10 09:15" if not is_dir else "Feb 10 09:15"
                        output_lines.append(f"{perms} 1 root root {size:6} {date} {item}")
                        dir_count += 1
                    await session.send("\r\n".join(output_lines).encode() + b"\r\n")
                else:
                    await session.send(b"\r\n")
            elif lowered == "pwd":
                await simulate_command_execution()
                await session.send(f"{current_path}\r\n".encode())
            elif lowered == "cat /etc/passwd":
                await simulate_command_execution()
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
                await simulate_command_execution()
                ps_header = b"USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\r\n"
                ps_lines = []
                for i, proc in enumerate(SYSTEM_INFO["processes"]):
                    ps_lines.append(f"root      {1000+i:5}  0.0  0.1  {random.randint(10000, 99999):6}  {random.randint(1000, 9999):4}  ?        Ss   Feb10   0:{random.randint(10, 59):02} {proc}".encode())
                await session.send(ps_header + b"\r\n".join(ps_lines) + b"\r\n")
            elif lowered == "df -h":
                await simulate_command_execution()
                df_header = b"Filesystem      Size  Used Avail Use% Mounted on\r\n"
                df_lines = []
                for fs in SYSTEM_INFO["filesystems"]:
                    df_lines.append(f"{fs[0]:15} {fs[2]:>4} {fs[3]:>4} {fs[4]:>4} {fs[5]:>3} {fs[6]}".encode())
                await session.send(df_header + b"\r\n".join(df_lines) + b"\r\n")
            elif lowered == "free -h":
                await simulate_command_execution()
                mem_info = SYSTEM_INFO["memory"]
                await session.send(b"               total        used        free      shared  buff/cache   available\r\n")
                await session.send(f"Mem:           2.0G        1.2G        800M         50M        579M        1.1G\r\n".encode())
                await session.send(f"Swap:          1.0G          0B        1.0G\r\n".encode())
            elif lowered == "ifconfig" or lowered == "ip addr":
                await simulate_command_execution()
                ifconfig_lines = []
                for i, (iface, ip, mask) in enumerate(SYSTEM_INFO["network"]):
                    ifconfig_lines.append(f"{iface}: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500")
                    ifconfig_lines.append(f"        inet {ip}  netmask {mask}  broadcast {ip.split('.')[0]}.{ip.split('.')[1]}.{ip.split('.')[2]}.255")
                    ifconfig_lines.append(f"        inet6 ::1  prefixlen 128  scopeid 0x10<host>")
                    ifconfig_lines.append(f"        ether {generate_mac()}  txqueuelen 1000  (Ethernet)")
                    ifconfig_lines.append(f"        RX packets 123456  bytes 789012345 (752.1 MiB)")
                    ifconfig_lines.append(f"        TX packets 98765  bytes 456789012 (435.2 MiB)")
                    ifconfig_lines.append("")
                await session.send("\r\n".join(ifconfig_lines).encode())
            elif lowered == "help":
                await session.send(b"Supported commands: ls, ls -l, ls -la, cd, cat, ps aux, df -h, free -h, ifconfig, ip addr, whoami, id, uname -a, pwd, env, export, history, service, systemctl, help, exit, quit, logout\r\n")
            elif lowered.startswith("cat "):
                await simulate_command_execution()
                filename = original_text[4:].strip()  # 保留原始大小写
                # 处理相对路径和绝对路径
                if filename.startswith("/"):
                    filepath = filename
                else:
                    filepath = current_path.rstrip("/") + "/" + filename

                content = get_file_content(filepath)
                if content is not None:
                    await session.send(content.encode())
                elif filepath in ["/etc/issue", "/etc/motd"]:
                    await session.send(b"Debian GNU/Linux 11 \\n \\l\r\n")
                elif filepath == "/proc/version":
                    await session.send(f"Linux version {SYSTEM_INFO['kernel']} (debian-kernel@lists.debian.org) (gcc-10 (Debian 10.2.1-6) 10.2.1 20210110, GNU ld (GNU Binutils for Debian) 2.35.2) #1 SMP Debian 5.10.92-1 (2022-01-18)\r\n".encode())
                elif filepath == "/proc/meminfo":
                    await session.send(FILE_CONTENTS["/proc/meminfo"].encode())
                elif filepath == "/proc/cpuinfo":
                    await session.send(FILE_CONTENTS["/proc/cpuinfo"].encode())
                else:
                    await session.send(f"cat: {filename}: No such file or directory\r\n".encode())
            elif lowered.startswith("echo "):
                await simulate_command_execution()
                message = original_text[5:]  # Skip "echo "，保留原始大小写
                await session.send(f"{message}\r\n".encode())
            elif lowered == "date":
                await simulate_command_execution()
                await session.send(f"{datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Z %Y')}\r\n".encode())
            elif lowered == "uptime":
                await simulate_command_execution()
                uptime_minutes = random.randint(60, 10000)
                days = uptime_minutes // (60 * 24)
                hours = (uptime_minutes % (60 * 24)) // 60
                mins = uptime_minutes % 60
                await session.send(f" {datetime.datetime.now().strftime('%H:%M:%S')} up {days} days, {hours}:{mins:02d},  1 user,  load average: 0.00, 0.01, 0.05\r\n".encode())
            elif lowered == "w" or lowered == "who":
                await simulate_command_execution()
                await session.send(b"USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT\r\n")
                await session.send(f"{session.login:<8} pts/0    192.168.1.105    {datetime.datetime.now().strftime('%H:%M')}   0.00s  0.04s  0.01s w\r\n".encode())
            elif lowered == "history":
                await simulate_command_execution()
                for i, cmd in enumerate(command_history, 1):
                    await session.send(f"{i:5}  {cmd}\r\n".encode())
            elif lowered.startswith("grep "):
                await simulate_command_execution()
                # 简单的grep模拟
                parts = original_text.split()
                if len(parts) >= 3:
                    pattern = parts[1]
                    filename = parts[2]
                    if filename.startswith("/"):
                        filepath = filename
                    else:
                        filepath = current_path.rstrip("/") + "/" + filename

                    content = get_file_content(filepath)
                    if content is not None:
                        lines = content.split('\n')
                        for line in lines:
                            if pattern in line:
                                await session.send(f"{line}\r\n".encode())
                    else:
                        await session.send(f"grep: {filename}: No such file or directory\r\n".encode())
                else:
                    await session.send(b"Usage: grep pattern file\r\n")
            elif lowered.startswith("mkdir "):
                await simulate_command_execution()
                await session.send(prompt)
                continue
            elif lowered.startswith("rm "):
                await simulate_command_execution()
                await session.send(prompt)
                continue
            elif lowered.startswith("touch "):
                await simulate_command_execution()
                await session.send(prompt)
                continue
            elif lowered == "env":
                await simulate_command_execution()
                for key, value in env_vars.items():
                    await session.send(f"{key}={value}\r\n".encode())
            elif lowered.startswith("export "):
                await simulate_command_execution()
                # 简单处理环境变量设置
                var_def = original_text[7:].strip()  # Skip "export "
                if "=" in var_def:
                    key, value = var_def.split("=", 1)
                    env_vars[key] = value
                await session.send(prompt)
                continue
            elif lowered.startswith("which "):
                await simulate_command_execution()
                command = original_text[6:].strip()
                if command in ["ls", "cat", "ps", "df", "free", "grep", "echo", "uname", "id", "whoami"]:
                    await session.send(f"/usr/bin/{command}\r\n".encode())
                else:
                    await session.send(f"which: no {command} in ({env_vars['PATH']})\r\n".encode())
            elif lowered == "printenv":
                await simulate_command_execution()
                for key, value in env_vars.items():
                    await session.send(f"{key}={value}\r\n".encode())
            elif lowered.startswith("tail "):
                await simulate_command_execution()
                parts = original_text.split()
                if len(parts) >= 2:
                    filename = parts[-1]
                    if filename.startswith("/"):
                        filepath = filename
                    else:
                        filepath = current_path.rstrip("/") + "/" + filename

                    content = get_file_content(filepath)
                    if content is not None:
                        lines = content.split('\n')
                        # 默认显示最后10行
                        tail_lines = lines[-10:] if len(lines) > 10 else lines
                        for line in tail_lines:
                            await session.send(f"{line}\r\n".encode())
                    else:
                        await session.send(f"tail: cannot open '{filename}' for reading: No such file or directory\r\n".encode())
                else:
                    await session.send(b"Usage: tail [file]\r\n")
            elif lowered.startswith("head "):
                await simulate_command_execution()
                parts = original_text.split()
                if len(parts) >= 2:
                    filename = parts[-1]
                    if filename.startswith("/"):
                        filepath = filename
                    else:
                        filepath = current_path.rstrip("/") + "/" + filename

                    content = get_file_content(filepath)
                    if content is not None:
                        lines = content.split('\n')
                        # 默认显示前10行
                        head_lines = lines[:10]
                        for line in head_lines:
                            await session.send(f"{line}\r\n".encode())
                    else:
                        await session.send(f"head: cannot open '{filename}' for reading: No such file or directory\r\n".encode())
                else:
                    await session.send(b"Usage: head [file]\r\n")
            elif lowered == "top":
                await simulate_command_execution()
                await session.send(b"top - 10:00:00 up 1 day,  1:00,  1 user,  load average: 0.00, 0.01, 0.05\r\n")
                await session.send(b"Tasks: 100 total,   1 running,  99 sleeping,   0 stopped,   0 zombie\r\n")
                await session.send(b"%Cpu(s):  0.3 us,  0.2 sy,  0.0 ni, 99.5 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st\r\n")
                await session.send(b"MiB Mem :   2048.0 total,    800.0 free,   1200.0 used,    579.0 buff/cache\r\n")
                await session.send(b"MiB Swap:   1024.0 total,   1024.0 free,      0.0 used.   1100.0 avail Mem\r\n")
                await session.send(b"\r\n")
                await session.send(b"  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND\r\n")
                await session.send(b"    1 root      20   0  167348   8768   4564 S   0.0   0.4   0:01.23 systemd\r\n")
                await session.send(b"  289 root      20   0   56784   6540   4092 S   0.0   0.3   0:00.23 systemd-journal\r\n")
                await session.send(b"  312 root      20   0   23456   4321   2014 S   0.0   0.2   0:00.10 systemd-udevd\r\n")
            elif lowered == "netstat":
                await simulate_command_execution()
                await session.send(b"Active Internet connections (w/o servers)\r\n")
                await session.send(b"Proto Recv-Q Send-Q Local Address           Foreign Address         State\r\n")
                await session.send(b"tcp        0      0 server01:ssh            192.168.1.105:54321     ESTABLISHED\r\n")
                await session.send(b"tcp        0      0 server01:23             192.168.1.105:54322     ESTABLISHED\r\n")
                await session.send(b"Active UNIX domain sockets (w/o servers)\r\n")
                await session.send(b"Proto RefCnt Flags       Type       State         I-Node   Path\r\n")
                await session.send(b"unix  2      [ ]         DGRAM                    12345    /run/systemd/notify\r\n")
            elif lowered.startswith("./"):
                await simulate_command_execution()
                # 模拟执行本地脚本
                script_name = original_text[2:]
                await session.send(f"bash: ./{script_name}: Permission denied\r\n".encode())
            elif lowered == "clear":
                # 发送清屏字符
                await session.send(b"\x1b[2J\x1b[H")
            elif lowered == "service --status-all":
                await simulate_command_execution()
                for service in ["apache2", "mysql", "ssh", "cron"]:
                    status = "[ + ]" if random.choice([True, False]) else "[ - ]"
                    await session.send(f"{status}  {service}\r\n".encode())
            elif lowered.startswith("systemctl status "):
                await simulate_command_execution()
                service = original_text[17:].strip()
                if service:
                    await session.send(f"● {service}.service - {service.capitalize()} Service\r\n".encode())
                    await session.send(b"   Loaded: loaded (/lib/systemd/system/" + service.encode() + b".service; enabled; vendor preset: enabled)\r\n")
                    await session.send(b"   Active: active (running) since Mon 2022-02-10 09:15:22 UTC; 3 days ago\r\n")
                    await session.send(b"  Process: 1234 ExecStart=/usr/sbin/" + service.encode() + b" (code=exited, status=0/SUCCESS)\r\n")
                    await session.send(b" Main PID: 1235 (" + service.encode() + b")\r\n")
                    await session.send(b"    Tasks: 10 (limit: 4915)\r\n")
                    await session.send(b"   Memory: 5.2M\r\n")
                    await session.send(b"   CGroup: /system.slice/" + service.encode() + b".service\r\n")
                else:
                    await session.send(b"systemctl status: no service specified\r\n")
            elif lowered == "systemctl list-units --type=service":
                await simulate_command_execution()
                await session.send(b"UNIT                    LOAD   ACTIVE SUB     DESCRIPTION\r\n")
                services = ["apache2.service", "mysql.service", "ssh.service", "cron.service", "rsyslog.service"]
                for svc in services:
                    active = "active" if random.choice([True, False, True]) else "inactive"  # 更多机会是active
                    await session.send(f"{svc:<23} loaded {active:<6} running {svc[:-8].capitalize()} Service\r\n".encode())
                await session.send(b"\r\nLOAD   = Reflects whether the unit definition was properly loaded.\r\n")
                await session.send(b"ACTIVE = The high-level unit activation state, i.e. generalization of SUB.\r\n")
                await session.send(b"SUB    = The low-level unit activation state, values depend on unit type.\r\n")
            elif lowered.startswith("find "):
                await simulate_command_execution()
                parts = original_text.split()
                if len(parts) >= 2:
                    path = parts[1]
                    await session.send(f"{path}/file1.txt\r\n".encode())
                    await session.send(f"{path}/file2.log\r\n".encode())
                    await session.send(f"{path}/subdir/\r\n".encode())
                else:
                    await session.send(b"Usage: find path\r\n")
            elif lowered.startswith("du -h"):
                await simulate_command_execution()
                await session.send(b"4.0K\t./.ssh\r\n")
                await session.send(b"8.0K\t./Documents\r\n")
                await session.send(b"12K\t.\r\n")
            elif lowered.startswith("chmod "):
                await simulate_command_execution()
                await session.send(prompt)
                continue
            elif lowered.startswith("chown "):
                await simulate_command_execution()
                await session.send(prompt)
                continue
            else:
                # 通用回显
                await session.send(b"bash: " + original_text.encode() + b": command not found\r\n")

            # 将命令添加到历史记录中
            if original_text and not original_text.startswith("history"):
                command_history.append(original_text)
                # 保持历史记录在合理范围内
                if len(command_history) > 50:
                    command_history.pop(0)

            await session.send(prompt)

    except Exception as exc:
        logger.exception("会话 %s 异常: %s", session.id, exc)
    finally:
        try:
            # 在会话持久化之前添加连接时间信息
            # 注意：这需要修改TelnetSession类以支持额外的连接时间字段
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
