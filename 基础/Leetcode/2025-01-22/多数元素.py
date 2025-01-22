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
        votes = 0
        for num in nums:
            if votes == 0: x = num
            votes ==1 if num==x else -1
        return  x
