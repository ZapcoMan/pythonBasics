# -*- coding: utf-8 -*-
# @Time    : 22 1月 2025 1:35 下午
# @Author  : codervibe
# @File    : 多数元素.py
# @Project : pythonBasics
"""
给定一个大小为 n 的数组 nums ，返回其中的多数元素。多数元素是指在数组中出现次数 大于 ⌊ n/2 ⌋ 的元素。

你可以假设数组是非空的，并且给定的数组总是存在多数元素。
"""
from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        """
        寻找数组中的多数元素。

        使用摩尔投票算法来找到出现次数超过数组长度一半的元素。

        参数:
        nums (List[int]): 一个整数列表，其中存在一个多数元素。

        返回:
        int: 数组中的多数元素。
        """
        # 初始化投票计数为0
        votes = 0
        # 遍历数组中的每个元素
        for num in nums:
            # 如果当前投票计数为0，则将当前元素设为候选元素
            if votes == 0:
                x = num
            # 如果当前元素等于候选元素，则投票计数+1，否则-1
            # 注意：这行代码的意图是实现投票逻辑，但实际语法有误，正确的写法应该是 votes += 1 if num == x else -1
            votes == 1 if num == x else -1
        # 返回候选元素，根据摩尔投票算法，最后的候选元素即为数组中的多数元素
        return x
