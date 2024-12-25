# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 9:50 上午
# @Author  : codervibe
# @File    : 找出字符串中所有的字母异位词.py
# @Project : pythonBasics
"""
给定两个字符串 s 和 p，找到 s 中所有 p 的 异位词的子串，返回这些子串的起始索引。不考虑答案输出的顺序。
"""
from typing import List

# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 9:50 上午
# @Author  : codervibe
# @File    : 找出字符串中所有的字母异位词.py
# @Project : pythonBasics
"""
给定两个字符串 s 和 p，找到 s 中所有 p 的 异位词的子串，返回这些子串的起始索引。不考虑答案输出的顺序。
"""

from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        if len(s) < len(p):
            return []

        check_list = {}
        for index in p:
            if index not in check_list.keys():
                check_list[index] = 0
            check_list[index] += 1

        init_substring = s[0:len(p)]
        for index in init_substring:
            if index not in check_list.keys():
                check_list[index] = 0
            check_list[index] -= 1

        result = []

        def check_zero():
            for value in check_list.values():
                if value != 0:
                    return False
            return True

        if check_zero():
            result.append(0)

        for index in range(1, len(s) - len(p) + 1):
            pre_value = s[index - 1]
            next_value = s[index + len(p) - 1]

            if pre_value not in check_list.keys():
                check_list[pre_value] = 0
            check_list[pre_value] += 1
            if next_value not in check_list.keys():
                check_list[next_value] = 0
            check_list[next_value] -= 1

            if check_zero():
                result.append(index)

        return result


if __name__ == '__main__':
    print(Solution().findAnagrams("cbaebabacd", "abc"))
    print(Solution().findAnagrams("abab", "ab"))