# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 7:10 下午
# @Author  : codervibe
# @File    : 最小覆盖子串.py
# @Project : pythonBasics
"""
给你一个字符串 s 、一个字符串 t 。返回 s 中涵盖 t 所有字符的最小子串。如果 s 中不存在涵盖 t 所有字符的子串，则返回空字符串 "" 。

注意：

对于 t 中重复字符，我们寻找的子字符串中该字符数量必须不少于 t 中该字符数量。
如果 s 中存在这样的子串，我们保证它是唯一的答案。

"""
from collections import Counter, defaultdict


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Find the minimum window substring in string s which encompasses all characters of string t.

        Parameters:
        s (str): The source string
        t (str): The target string, whose characters need to be encompassed by the substring of s

        Returns:
        str: The minimum window substring; returns an empty string if it does not exist
        """
        # Initialize the left and right boundaries of the minimum window substring
        ans_left, ans_right = -1, len(s)
        # Initialize Counters for string s and t
        cnt_s = Counter()  # s 子串字母的出现次数
        cnt_t = Counter(t)  # t 中字母的出现次数

        left = 0
        # Start enumerating through string s to find the minimum window substring
        for right, c in enumerate(s):  # 移动子串右端点
            cnt_s[c] += 1  # Add the character at the right end point to the substring
            # When the substring encompasses all characters of t
            while cnt_s >= cnt_t:
                # If a shorter substring is found
                if right - left < ans_right - ans_left:
                    ans_left, ans_right = left, right  # Update the minimum window substring's boundaries
                cnt_s[s[left]] -= 1  # Remove the character at the left end point from the substring
                left += 1  # Move the left boundary of the substring to the right
        # If ans_left is -1, it means no valid substring was found, return an empty string; otherwise, return the minimum window substring
        return "" if ans_left < 0 else s[ans_left: ans_right + 1]

    def minWindow(self, s: str, t: str) -> str:
        ans_left, ans_right = -1, len(s)
        cnt = defaultdict(int)  # 比 Counter 更快
        for c in t:
            cnt[c] += 1
        less = len(cnt)  # 有 less 种字母的出现次数 < t 中的字母出现次数

        left = 0
        for right, c in enumerate(s):  # 移动子串右端点
            cnt[c] -= 1  # 右端点字母移入子串
            if cnt[c] == 0:
                # 原来窗口内 c 的出现次数比 t 的少，现在一样多
                less -= 1
            while less == 0:  # 涵盖：所有字母的出现次数都是 >=
                if right - left < ans_right - ans_left:  # 找到更短的子串
                    ans_left, ans_right = left, right  # 记录此时的左右端点
                x = s[left]  # 左端点字母
                if cnt[x] == 0:
                    # x 移出窗口之前，检查出现次数，
                    # 如果窗口内 x 的出现次数和 t 一样，
                    # 那么 x 移出窗口后，窗口内 x 的出现次数比 t 的少
                    less += 1
                cnt[x] += 1  # 左端点字母移出子串
                left += 1
        return "" if ans_left < 0 else s[ans_left: ans_right + 1]
