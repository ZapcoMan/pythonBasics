#!/usr/bin/env python3
# multi_honeypot.py
# Multi-protocol honeypot framework: each protocol is implemented as a class.
# Telnet and FTP minimal handlers included.

import asyncio
import argparse
import logging
import json
import uuid
import base64
from datetime import datetime, timezone
from typing import Tuple, Optional, List, Dict, Any

# ---------- Global Configuration (can be externalized) ----------
DEFAULT_LOG_FILE = "honeypot_multi_sessions.jsonl"
OPERATOR_LOG_LEVEL = logging.INFO
# ---------------------------------------------------------------

# Operator logger (for running state)
logging.basicConfig(level=OPERATOR_LOG_LEVEL, format="%(asctime)s [%(levelname)s] %(message)s")
op_logger = logging.getLogger("honeypot_operator")

# Helper: async-safe append to JSONL
async def append_jsonl(entry: dict, path: str = DEFAULT_LOG_FILE):
    loop = asyncio.get_running_loop()
    s = json.dumps(entry, ensure_ascii=False)
    def _write():
        with open(path, "a", encoding="utf-8") as f:
            f.write(s + "\n")
    await loop.run_in_executor(None, _write)

# ---------- ProtocolHandler base class ----------
class ProtocolHandler:
    """
    Abstract base for protocol handlers.
    Subclasses must implement:
      - get_listen() -> (host, port)
      - serve_forever() -> coroutine that runs the server (shouldn't block)
    """
    def __init__(self, name: str, *, log_file: str = DEFAULT_LOG_FILE):
        self.name = name
        self.log_file = log_file
        self._server = None  # asyncio.Server
        self._tasks: List[asyncio.Task] = []

    def get_listen(self) -> Tuple[str, int]:
        raise NotImplementedError

    async def start(self):
        raise NotImplementedError

    async def stop(self):
        # Cancel running tasks and close server
        for t in list(self._tasks):
            t.cancel()
        if self._server:
            self._server.close()
            try:
                await self._server.wait_closed()
            except Exception:
                pass
        op_logger.info("%s handler stopped", self.name)

    # Utility for session persist: unified schema
    async def persist_session(self, session_entry: dict):
        # enforce protocol name
        session_entry.setdefault("protocol", self.name)
        await append_jsonl(session_entry, path=self.log_file)

# ---------- Telnet Handler ----------
class TelnetHandler(ProtocolHandler):
    BANNER = b"Welcome to MiniTelnet Service\r\nAuthorized access only.\r\n"
    PROMPT = b"mini-shell> "
    LOGIN_PROMPT = b"login: "
    PASS_PROMPT = b"password: "

    def __init__(self, host="0.0.0.0", port=2323, **kwargs):
        super().__init__("telnet", **kwargs)
        self.host = host
        self.port = port

    def get_listen(self):
        return (self.host, self.port)

    async def start(self):
        self._server = await asyncio.start_server(self._handle_client, self.host, self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
        op_logger.info("Telnet listening on %s", addrs)
        # run serve_forever in background so manager can await it
        self._tasks.append(asyncio.create_task(self._server.serve_forever()))

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer = writer.get_extra_info("peername") or ("unknown", 0)
        session_id = str(uuid.uuid4())
        start_ts = datetime.now(timezone.utc)
        raw_buf = bytearray()
        inputs = []

        op_logger.info("Telnet new conn %s session=%s", peer, session_id)
        async def record_raw(b: bytes):
            raw_buf.extend(b)

        async def record_input(txt: str):
            inputs.append({"ts": datetime.now(timezone.utc).isoformat(), "input": txt})

        try:
            # banner / login
            writer.write(self.BANNER)
            await writer.drain()

            writer.write(self.LOGIN_PROMPT)
            await writer.drain()
            login = await reader.readline()
            if not login:
                raise ConnectionResetError("empty login")
            await record_raw(login)
            login_text = login.decode(errors="ignore").strip()

            writer.write(self.PASS_PROMPT)
            await writer.drain()
            pwd = await reader.readline()
            if not pwd:
                raise ConnectionResetError("empty password")
            await record_raw(pwd)
            pwd_text = pwd.decode(errors="ignore").strip()

            writer.write(b"\r\nLogin successful.\r\n")
            writer.write(self.PROMPT)
            await writer.drain()

            # main loop
            while True:
                data = await reader.readline()
                if not data:
                    break
                await record_raw(data)
                txt = data.decode(errors="ignore").rstrip("\r\n")
                await record_input(txt)
                op_logger.debug("Telnet %s: %s", session_id, txt)

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
            # persist
            entry = {
                "session_id": session_id,
                "start_time": start_ts.isoformat(),
                "end_time": datetime.now(timezone.utc).isoformat(),
                "duration_seconds": (datetime.now(timezone.utc) - start_ts).total_seconds(),
                "remote_ip": peer[0],
                "remote_port": peer[1],
                "login": login_text if 'login_text' in locals() else None,
                "password": "<captured>" if 'pwd_text' in locals() and pwd_text else None,
                "inputs": inputs,
                "raw_base64": base64.b64encode(bytes(raw_buf)).decode("ascii"),
            }
            try:
                await self.persist_session(entry)
            except Exception:
                op_logger.exception("Telnet persist failed %s", session_id)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            op_logger.info("Telnet closed session %s from %s", session_id, peer)

# ---------- FTP Handler (control-channel minimal implementation) ----------
class FTPHandler(ProtocolHandler):
    """
    Minimal FTP control-channel honeypot.
    Does NOT open data connections. Parses USER/PASS and several commands.
    """
    def __init__(self, host="0.0.0.0", port=2121, **kwargs):
        super().__init__("ftp", **kwargs)
        self.host = host
        self.port = port

    def get_listen(self):
        return (self.host, self.port)

    async def start(self):
        self._server = await asyncio.start_server(self._handle_client, self.host, self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in self._server.sockets)
        op_logger.info("FTP listening on %s", addrs)
        self._tasks.append(asyncio.create_task(self._server.serve_forever()))

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
                    # accept any password but don't execute
                    await self._send_line(writer, "230 Login successful")
                    authenticated = True
                elif cmd == "SYST":
                    await self._send_line(writer, "215 UNIX Type: L8")
                elif cmd == "PWD":
                    await self._send_line(writer, '257 "/" is current directory')
                elif cmd == "CWD":
                    await self._send_line(writer, "250 Directory changed")
                elif cmd == "LIST":
                    # we do NOT open a data connection; return empty list via canned reply
                    await self._send_line(writer, "150 Opening ASCII mode data connection for file list")
                    await self._send_line(writer, "226 Transfer complete")
                elif cmd in ("RETR", "STOR"):
                    # record intent but refuse actual transfer
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
            try:
                await self.persist_session(entry)
            except Exception:
                op_logger.exception("FTP persist failed %s", session_id)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            op_logger.info("FTP closed session %s from %s", session_id, peer)

# ---------- Honeypot Manager ----------
class HoneypotManager:
    def __init__(self, handlers: List[ProtocolHandler]):
        self.handlers = handlers

    async def start(self):
        op_logger.info("Starting HoneypotManager with %d handlers", len(self.handlers))
        # start all handlers
        await asyncio.gather(*(h.start() for h in self.handlers))
        op_logger.info("All handlers started")

    async def stop(self):
        op_logger.info("Stopping HoneypotManager")
        await asyncio.gather(*(h.stop() for h in self.handlers), return_exceptions=True)

# ---------- CLI / Entrypoint ----------
def parse_args():
    p = argparse.ArgumentParser(description="Multi-protocol honeypot (Telnet + FTP minimal).")
    p.add_argument("--telnet-port", type=int, default=2323)
    p.add_argument("--ftp-port", type=int, default=2121)
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--log", default=DEFAULT_LOG_FILE)
    return p.parse_args()

async def main_async():
    args = parse_args()
    # instantiate handlers with shared log file
    telnet = TelnetHandler(host=args.host, port=args.telnet_port, log_file=args.log)
    ftp = FTPHandler(host=args.host, port=args.ftp_port, log_file=args.log)
    manager = HoneypotManager([telnet, ftp])

    await manager.start()
    # run until cancelled
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass
    finally:
        await manager.stop()

def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        op_logger.info("Keyboard interrupt; shutting down")

if __name__ == "__main__":
    main()
