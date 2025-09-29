# -*- coding: utf-8 -*-
# @Time    : 10 2月 2025 11:11 下午
# @Author  : codervibe
# @File    : 字符串解码.py
# @Project : pythonBasics
"""
给定一个经过编码的字符串，返回它解码后的字符串。

编码规则为: k[encoded_string]，表示其中方括号内部的 encoded_string 正好重复 k 次。注意 k 保证为正整数。

你可以认为输入字符串总是有效的；输入字符串中没有额外的空格，且输入的方括号总是符合格式要求的。

此外，你可以认为原始数据不包含数字，所有的数字只表示重复的次数 k ，例如不会出现像 3a 或 2[4] 的输入。


"""
class Solution:
    """
    解码字符串类
    """
    def decodeString(self, s: str) -> str:
        """
        解码字符串主函数

        递归地解析字符串，将数字代表的重复次数与中括号内的字符串相乘，并累加到结果字符串中。

        :param s: 编码后的字符串
        :return: 解码后的字符串
        """
        def dfs(s, i):
            """
            深度优先搜索函数，用于解码字符串

            :param s: 待解码的字符串
            :param i: 当前处理到的字符串索引
            :return: 解码后的字符串和下一个要处理的索引位置
            """
            res, multi = "", 0
            while i < len(s):
                if '0' <= s[i] <= '9':
                    # 处理数字，计算重复次数
                    multi = multi * 10 + int(s[i])
                elif s[i] == '[':
                    # 遇到左括号，递归处理括号内的字符串
                    i, tmp = dfs(s, i + 1)
                    res += multi * tmp
                    multi = 0
                elif s[i] == ']':
                    # 遇到右括号，结束当前层次的递归
                    return i, res
                else:
                    # 处理字母，直接累加到结果字符串
                    res += s[i]
                i += 1
            return res
        return dfs(s,0)
