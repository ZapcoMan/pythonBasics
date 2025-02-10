# -*- coding: utf-8 -*-
# @Time    : 10 2月 2025 11:04 下午
# @Author  : codervibe
# @File    : 有效的括号.py
# @Project : pythonBasics
"""
给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s ，判断字符串是否有效。

有效字符串需满足：

左括号必须用相同类型的右括号闭合。
左括号必须以正确的顺序闭合。
每个右括号都有一个对应的相同类型的左括号
"""
class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) % 2:  # s 长度必须是偶数
            return False
        mp = {')': '(', ']': '[', '}': '{'}
        st = []
        for c in s:
            if c not in mp:  # c 是左括号
                st.append(c)  # 入栈
            elif not st or st.pop() != mp[c]:  # c 是右括号
                return False  # 没有左括号，或者左括号类型不对
        return not st  # 所有左括号必须匹配完毕

