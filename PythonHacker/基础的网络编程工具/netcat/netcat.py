# -*- coding: utf-8 -*-
# @Time    : 19 2月 2025 10:28下午
# @Author  : codervibe
# @File    : netcat.py
# @Project : pythonBasics
import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading



def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()




