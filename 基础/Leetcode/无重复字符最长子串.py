# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 9:36 上午
# @Author  : codervibe
# @File    : 无重复字符最长子串.py
# @Project : pythonBasics
"""
给定一个字符串 s ，请你找出其中不含有重复字符的 最长子串
"""
import collections

"""
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        dic, res, i = {}, 0, -1
        for j in range(len(s)):
            if s[j] in dic:
                i = max(dic[s[j]], i) # 更新左指针 i
            dic[s[j]] = j # 哈希表记录
            res = max(res, j - i) # 更新结果
        return res

"""


class Solution:
    @staticmethod
    def lengthOfLongestSubstring(s: str) -> int:
        """
        找出给定字符串中最长不重复字符子串的长度。

        :param s: 输入的字符串
        :return: 最长不重复字符子串的长度
        """
        n = len(s)
        # 如果字符串长度小于2，直接返回其长度，因为不存在重复字符的最长子串长度至少为1
        if n < 2:
            return n
        # 使用defaultdict来存储每个字符最后出现的位置
        dic = collections.defaultdict()
        # 初始化子串开始位置begin和最大长度max_len
        begin, max_len = 0, 1
        # 遍历字符串，获取每个字符及其索引
        for i, c in enumerate(s):
            # 如果字符已经在字典中且上次出现的位置大于等于当前子串的开始位置begin
            if c in dic and dic[c] >= begin:
                # 更新最大长度max_len为当前字符索引i与子串开始位置begin的差值
                max_len = max(max_len, i - begin)
                # 更新子串开始位置begin为当前重复字符上次出现位置的下一个位置
                begin = dic[c] + 1
            # 更新或添加当前字符的索引到字典中
            dic[c] = i
        # 最后检查并更新最大长度，防止遗漏最后一段不重复子串
        max_len = max(max_len, n - begin)
        return max_len


"""
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        n = len(s)
        if n < 2: return n
        dic = collections.defaultdict() # 存储key元素的最右边idex
        begin, max_len = 0, 1
        for i, c in enumerate(s):
            if c in dic and dic[c] >= begin: # 当前跟之前重复，先计算之前的最大长度
                max_len = max(max_len, i - begin)
                begin = dic[c] + 1
            dic[c] = i
        max_len = max(max_len, n - begin) # 统计最后不重复子串长度
        return max_len
"""
