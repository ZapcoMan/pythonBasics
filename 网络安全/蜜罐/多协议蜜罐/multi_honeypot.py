#!/usr/bin/env python3
# multi_protocol_honeypot.py
# Multi-protocol honeypot (single-file)
# Protocols: TCP (echo), HTTP, HTTPS (TLS), SSH (banner-only), Telnet, FTP (control-channel minimal)
# Python 3.11+

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

# ---------------------- Operator logging & defaults ----------------------
OP_LOG_LEVEL = logging.INFO
logging.basicConfig(level=OP_LOG_LEVEL, format="%(asctime)s [%(levelname)s] %(message)s")
op_logger = logging.getLogger("honeypot_operator")

DEFAULT_LOG_FILE = "honeypot_sessions.jsonl"
# Default ports (non-privileged so you can run without root)
DEFAULTS = {
    "tcp": 9000,
    "http": 8080,
    "https": 8443,
    "ssh": 2222,
    "telnet": 2323,
    "ftp": 2121,
}
# ------------------------------------------------------------------------

# ---------------------- Utility: JSONL append (async-safe) ----------------
async def append_jsonl(entry: dict, path: str = DEFAULT_LOG_FILE):
    loop = asyncio.get_running_loop()
    s = json.dumps(entry, ensure_ascii=False)
    def _write():
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8") as f:
            f.write(s + "\n")
    await loop.run_in_executor(None, _write)

def now_iso():
    return datetime.now(timezone.utc).isoformat()

# ---------------------- Base ProtocolHandler ------------------------------
class ProtocolHandler:
    def __init__(self, name: str, host: str, port: int, log_file: str):
        self.name = name
        self.host = host
        self.port = port
        self.log_file = log_file
        self._server: Optional[asyncio.base_events.Server] = None

    async def start(self):
        raise NotImplementedError

    async def stop(self):
        if self._server:
            self._server.close()
            try:
                await self._server.wait_closed()
            except Exception:
                pass
        op_logger.info("%s handler stopped", self.name)

    async def persist(self, session_entry: dict):
        # enforce protocol field and write
        session_entry.setdefault("protocol", self.name)
        try:
            await append_jsonl(session_entry, path=self.log_file)
        except Exception:
            op_logger.exception("Persist failed for %s", self.name)

# ---------------------- Telnet Handler (interactive pseudo-shell) ----------
class TelnetHandler(ProtocolHandler):
    BANNER = b"Welcome to MiniTelnet Service\r\nAuthorized access only.\r\n"
    PROMPT = b"mini-shell> "
    LOGIN_PROMPT = b"login: "
    PASS_PROMPT = b"password: "

    def __init__(self, host, port, log_file):
        super().__init__("telnet", host, port, log_file)

    async def start(self):
        self._server = await asyncio.start_server(self._handle_client, host=self.host, port=self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
        op_logger.info("Telnet listening on %s", addrs)
        # run serve_forever in background
        asyncio.create_task(self._server.serve_forever())

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer = writer.get_extra_info("peername") or ("unknown", 0)
        session_id = str(uuid.uuid4())
        start_ts = datetime.now(timezone.utc)
        raw_buf = bytearray()
        inputs = []
        login_text = None
        pwd_text = None

        op_logger.info("Telnet new conn %s session=%s", peer, session_id)
        try:
            writer.write(self.BANNER)
            await writer.drain()

            writer.write(self.LOGIN_PROMPT)
            await writer.drain()
            login = await reader.readline()
            if not login:
                raise ConnectionResetError("login empty")
            raw_buf.extend(login)
            login_text = login.decode(errors="ignore").strip()

            writer.write(self.PASS_PROMPT)
            await writer.drain()
            pwd = await reader.readline()
            if not pwd:
                raise ConnectionResetError("password empty")
            raw_buf.extend(pwd)
            pwd_text = pwd.decode(errors="ignore").strip()

            # Accept any credentials but do not write actual password to log (mask)
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
                op_logger.debug("Telnet %s input: %s", session_id, txt)

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
            op_logger.info("Telnet session cancelled %s", session_id)
        except Exception as e:
            op_logger.exception("Telnet handler error %s: %s", session_id, e)
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
            op_logger.info("Telnet closed session %s from %s", session_id, peer)

# ---------------------- FTP Handler (control-channel minimal) -------------
class FTPHandler(ProtocolHandler):
    def __init__(self, host, port, log_file):
        super().__init__("ftp", host, port, log_file)

    async def start(self):
        self._server = await asyncio.start_server(self._handle_client, host=self.host, port=self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
        op_logger.info("FTP listening on %s", addrs)
        asyncio.create_task(self._server.serve_forever())

    async def _send_line(self, writer: asyncio.StreamWriter, line: str):
        writer.write((line + "\r\n").encode())
        await writer.drain()

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer = writer.get_extra_info("peername") or ("unknown", 0)
        session_id = str(uuid.uuid4())
        start_ts = datetime.now(timezone.utc)
        raw_buf = bytearray()
        inputs = []
        username = None
        authenticated = False

        op_logger.info("FTP new conn %s session=%s", peer, session_id)
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
                    text = "<non-decodable>"
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
                    # no data connection: send canned success
                    await self._send_line(writer, "150 Opening ASCII mode data connection for file list")
                    await self._send_line(writer, "226 Transfer complete")
                elif cmd in ("RETR", "STOR"):
                    # refuse actual transfer for safety
                    await self._send_line(writer, "550 Action not taken (simulated)")
                elif cmd == "QUIT":
                    await self._send_line(writer, "221 Goodbye.")
                    break
                else:
                    await self._send_line(writer, "502 Command not implemented")
        except asyncio.CancelledError:
            op_logger.info("FTP session cancelled %s", session_id)
        except Exception as e:
            op_logger.exception("FTP handler error %s: %s", session_id, e)
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
            op_logger.info("FTP closed session %s from %s", session_id, peer)

# ---------------------- TCP Echo Handler ---------------------------------
class TCPHandler(ProtocolHandler):
    def __init__(self, host, port, log_file):
        super().__init__("tcp", host, port, log_file)

    async def start(self):
        self._server = await asyncio.start_server(self._handle, host=self.host, port=self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
        op_logger.info("TCP listening on %s", addrs)
        asyncio.create_task(self._server.serve_forever())

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer = writer.get_extra_info("peername") or ("unknown", 0)
        session_id = str(uuid.uuid4())
        start_ts = datetime.now(timezone.utc)
        raw_buf = bytearray()

        op_logger.info("TCP new conn %s session=%s", peer, session_id)
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                raw_buf.extend(data)
                # echo back
                writer.write(data)
                await writer.drain()
        except asyncio.CancelledError:
            op_logger.info("TCP session cancelled %s", session_id)
        except Exception as e:
            op_logger.exception("TCP handler error %s: %s", session_id, e)
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
            op_logger.info("TCP closed session %s from %s", session_id, peer)

# ---------------------- HTTP Handler (minimal) ----------------------------
class HTTPHandler(ProtocolHandler):
    RESPONSE_BODY = b"<html><body><h1>Fake HTTP Service</h1></body></html>"

    def __init__(self, host, port, log_file):
        super().__init__("http", host, port, log_file)

    async def start(self):
        self._server = await asyncio.start_server(self._handle, host=self.host, port=self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
        op_logger.info("HTTP listening on %s", addrs)
        asyncio.create_task(self._server.serve_forever())

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer = writer.get_extra_info("peername") or ("unknown", 0)
        session_id = str(uuid.uuid4())
        start_ts = datetime.now(timezone.utc)
        try:
            raw = await reader.read(64 * 1024)  # read up to 64KB for headers+body
            text = raw.decode(errors="ignore")
            # respond with simple page
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
            op_logger.exception("HTTP handler error %s: %s", session_id, e)
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            op_logger.info("HTTP closed session %s from %s", session_id, peer)

# ---------------------- HTTPS Handler (wraps HTTP with ssl) ----------------
class HTTPSHandler(HTTPHandler):
    def __init__(self, host, port, log_file, certfile: str, keyfile: str):
        super().__init__(host, port, log_file)
        self.name = "https"
        self.certfile = certfile
        self.keyfile = keyfile

    async def start(self):
        # create SSL context
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # disable old
        ctx.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        self._server = await asyncio.start_server(self._handle, host=self.host, port=self.port, ssl=ctx)
        addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
        op_logger.info("HTTPS listening on %s", addrs)
        asyncio.create_task(self._server.serve_forever())

# ---------------------- SSH Handler (banner-only) -------------------------
class SSHHandler(ProtocolHandler):
    BANNER = b"SSH-2.0-OpenSSH_8.2p1 FakeHoneypot\r\n"

    def __init__(self, host, port, log_file):
        super().__init__("ssh", host, port, log_file)

    async def start(self):
        self._server = await asyncio.start_server(self._handle, host=self.host, port=self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
        op_logger.info("SSH listening on %s", addrs)
        asyncio.create_task(self._server.serve_forever())

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer = writer.get_extra_info("peername") or ("unknown", 0)
        session_id = str(uuid.uuid4())
        start_ts = datetime.now(timezone.utc)
        raw_buf = bytearray()
        op_logger.info("SSH new conn %s session=%s", peer, session_id)
        try:
            # send banner and read once to capture client banner or any early bytes
            writer.write(self.BANNER)
            await writer.drain()
            # attempt to read a small buffer; don't block long
            try:
                data = await asyncio.wait_for(reader.read(1024), timeout=5.0)
                if data:
                    raw_buf.extend(data)
            except asyncio.TimeoutError:
                pass
        except Exception as e:
            op_logger.exception("SSH handler exception %s: %s", session_id, e)
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
            op_logger.info("SSH closed session %s from %s", session_id, peer)

# ---------------------- Manager to orchestrate handlers -------------------
class HoneypotManager:
    def __init__(self, handlers):
        self.handlers = handlers

    async def start(self):
        op_logger.info("Starting HoneypotManager with %d handlers", len(self.handlers))
        # start handlers concurrently
        await asyncio.gather(*(h.start() for h in self.handlers))
        op_logger.info("All handlers started")

    async def stop(self):
        op_logger.info("Stopping HoneypotManager")
        await asyncio.gather(*(h.stop() for h in self.handlers), return_exceptions=True)

# ---------------------- Helper: generate self-signed cert via openssl -----
def ensure_self_signed(certfile: Path, keyfile: Path, common_name: str = "mini-honeypot.local"):
    """
    Try to generate a self-signed cert using openssl command if files missing.
    Requires openssl available in PATH.
    """
    if certfile.exists() and keyfile.exists():
        op_logger.info("Found existing cert/key: %s %s", certfile, keyfile)
        return True

    # attempt to run openssl
    cmd = [
        "openssl", "req", "-x509", "-nodes", "-days", "365",
        "-newkey", "rsa:2048",
        "-keyout", str(keyfile),
        "-out", str(certfile),
        "-subj", f"/CN={common_name}"
    ]
    try:
        op_logger.info("Generating self-signed cert via openssl...")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        op_logger.info("Generated cert/key at %s %s", certfile, keyfile)
        return True
    except Exception as e:
        op_logger.error("Failed to generate cert/key with openssl: %s", e)
        return False

# ---------------------- CLI / Entrypoint ---------------------------------
def parse_args():
    p = argparse.ArgumentParser(description="Multi-protocol honeypot (single-file)")
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--log", default=DEFAULT_LOG_FILE)
    p.add_argument("--tcp-port", type=int, default=DEFAULTS["tcp"])
    p.add_argument("--http-port", type=int, default=DEFAULTS["http"])
    p.add_argument("--https-port", type=int, default=DEFAULTS["https"])
    p.add_argument("--ssh-port", type=int, default=DEFAULTS["ssh"])
    p.add_argument("--telnet-port", type=int, default=DEFAULTS["telnet"])
    p.add_argument("--ftp-port", type=int, default=DEFAULTS["ftp"])
    p.add_argument("--certfile", default="cert.pem", help="HTTPS cert (PEM)")
    p.add_argument("--keyfile", default="key.pem", help="HTTPS key (PEM)")
    p.add_argument("--generate-cert", action="store_true", help="Try to auto-generate self-signed cert with openssl if missing")
    return p.parse_args()

async def main_async():
    args = parse_args()
    # ensure certs if requested
    certfile = Path(args.certfile)
    keyfile = Path(args.keyfile)
    if args.generate_cert:
        ok = ensure_self_signed(certfile, keyfile)
        if not ok:
            op_logger.warning("HTTPS will fail without valid cert/key. Continue anyway.")

    # instantiate handlers
    handlers = []
    handlers.append(TCPHandler(host=args.host, port=args.tcp_port, log_file=args.log))
    handlers.append(HTTPHandler(host=args.host, port=args.http_port, log_file=args.log))
    handlers.append(HTTPSHandler(host=args.host, port=args.https_port, log_file=args.log, certfile=str(certfile), keyfile=str(keyfile)))
    handlers.append(SSHHandler(host=args.host, port=args.ssh_port, log_file=args.log))
    handlers.append(TelnetHandler(host=args.host, port=args.telnet_port, log_file=args.log))
    handlers.append(FTPHandler(host=args.host, port=args.ftp_port, log_file=args.log))

    manager = HoneypotManager(handlers)
    await manager.start()

    # run until interrupted
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        op_logger.info("Keyboard interrupt received; shutting down")
    finally:
        await manager.stop()

def main():
    try:
        asyncio.run(main_async())
    except Exception as e:
        op_logger.exception("Fatal error: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
