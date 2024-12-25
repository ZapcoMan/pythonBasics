# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 9:50 上午
# @Author  : codervibe
# @File    : 找出字符串中所有的字母异位词.py
# @Project : pythonBasics
"""
给定两个字符串 s 和 p，找到 s 中所有 p 的 异位词的子串，返回这些子串的起始索引。不考虑答案输出的顺序。
"""

# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 9:50 上午
# @Author  : codervibe
# @File    : 找出字符串中所有的字母异位词.py
# @Project : pythonBasics
"""
给定两个字符串 s 和 p，找到 s 中所有 p 的 异位词的子串，返回这些子串的起始索引。不考虑答案输出的顺序。
"""


class Solution:
    """
    本类提供了一个方法用于寻找字符串s中所有p的异位词的起始索引。
    异位词指的是由相同字母组成但排列方式不同的字符串。
    """

    def findAnagrams(self, s: str, p: str) -> List[int]:
        """
        寻找字符串s中所有p的异位词的起始索引。

        参数:
        s: 被搜索的字符串。
        p: 目标异位词原型字符串。

        返回:
        一个列表，包含了s中所有p的异位词的起始索引。
        """
        # 如果s的长度小于p，直接返回空列表，因为不可能存在异位词
        if len(s) < len(p):
            return []

        # 初始化检查列表，用于记录p中每个字符的出现次数
        check_list = {}
        for index in p:
            if index not in check_list.keys():
                check_list[index] = 0
            check_list[index] += 1

        # 初始化s中第一个与p长度相等的子串，更新check_list中字符的计数
        init_substring = s[0:len(p)]
        for index in init_substring:
            if index not in check_list.keys():
                check_list[index] = 0
            check_list[index] -= 1

        # 初始化结果列表，用于存放所有异位词的起始索引
        result = []

        def check_zero():
            """
            检查check_list中所有值是否为0，用于判断当前子串是否为p的异位词。

            返回:
            如果所有值均为0，表示当前子串是p的一个异位词，返回True；否则返回False。
            """
            for value in check_list.values():
                if value != 0:
                    return False
            return True

        # 检查初始子串是否为异位词，如果是，则将其起始索引0添加到结果列表中
        if check_zero():
            result.append(0)

        # 遍历s，寻找所有异位词的起始索引
        for index in range(1, len(s) - len(p) + 1):
            # 更新check_list，移除前一个字符，添加新字符
            pre_value = s[index - 1]
            next_value = s[index + len(p) - 1]

            if pre_value not in check_list.keys():
                check_list[pre_value] = 0
            check_list[pre_value] += 1
            if next_value not in check_list.keys():
                check_list[next_value] = 0
            check_list[next_value] -= 1

            # 检查当前子串是否为异位词，如果是，则将其起始索引添加到结果列表中
            if check_zero():
                result.append(index)

        return result
