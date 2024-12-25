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
        """
        查找给定整数数组中连续子数组的最大和。

        该方法使用动态规划，将每个元素更新为以该位置结尾的子数组的最大和。

        参数:
        nums (List[int]): 整数列表

        返回值:
        int: 连续子数组的最大和
        """
        for i in range(1, len(nums)):
            # 将当前元素与以之前位置结尾的子数组最大和（如果为正）累加
            nums[i] += max(nums[i - 1], 0)
        # 返回累加后的最大值，即为最大子数组和
        return max(nums)

    def maxSubArray(self, nums: List[int]) -> int:
        """
        查找给定整数数组中连续子数组的最大和。

        该方法使用一个变量跟踪当前子数组的和，并更新迄今为止找到的最大子数组和。
        当当前子数组和变为负数时，将其重置为0。

        参数:
        nums (List[int]): 整数列表

        返回值:
        int: 连续子数组的最大和
        """
        # 将最大子数组和初始化为数组的第一个元素
        ans = nums[0]
        # 将当前子数组和初始化为0
        i = 0
        for n in nums:
            # 将当前元素添加到当前子数组和中
            i += n
            # 如果当前子数组和大于已知最大值，则更新最大值
            if i > ans:
                ans = i
            # 如果当前子数组和为负数，则重置为0
            if i < 0:
                i = 0
        # 返回找到的最大子数组和
        return ans
