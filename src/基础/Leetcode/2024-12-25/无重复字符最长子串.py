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


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # 寻找最长无重复字符的子串长度。
        # 
        # 通过维护一个滑动窗口，使用字典记录每个字符最后出现的位置，来实现。
        # 
        # 参数:
        # s: 输入的字符串。
        # 
        # 返回:
        # 最长无重复字符子串的长度。
        n = len(s)
        # 如果字符串长度小于2，直接返回其长度，因为不存在重复字符的子串
        if n < 2: return n
        # 使用defaultdict来存储字符的索引，方便快速查找字符是否已经出现过
        dic = collections.defaultdict() # 存储key元素的最右边idex
        begin, max_len = 0, 1
        # 遍历字符串，使用enumerate同时获取索引和字符
        for i, c in enumerate(s):
            # 如果字符已经在字典中，并且上次出现的位置在当前窗口内
            if c in dic and dic[c] >= begin: 
                # 更新最大长度为当前索引到窗口开始位置的距离
                max_len = max(max_len, i - begin)
                # 移动窗口的开始位置到重复字符的下一个位置
                begin = dic[c] + 1
            # 更新或添加当前字符的索引到字典中
            dic[c] = i
        # 最后，确保检查从最后一个重复字符到字符串末尾的距离是否为最大长度
        max_len = max(max_len, n - begin) # 统计最后不重复子串长度
        return max_len

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



