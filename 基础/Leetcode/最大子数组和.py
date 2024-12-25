# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 7:17 下午
# @Author  : codervibe
# @File    : 最大子数组和.py
# @Project : pythonBasics
"""
给你一个整数数组 nums ，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

子数组
是数组中的一个连续部分。
"""
from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        for i in range(1, len(nums)):
            nums[i] += max(nums[i - 1], 0)
        return max(nums)

    def maxSubArray(self, nums: List[int]) -> int:
        ans = nums[0]
        i = 0
        for n in nums:
            i += n
            if i > ans:
                ans = i
            if i < 0:
                i = 0
        return ans
