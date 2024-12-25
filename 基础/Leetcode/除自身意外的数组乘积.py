# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 7:29 下午
# @Author  : codervibe
# @File    : 除自身意外的数组的乘积.py
# @Project : pythonBasics
"""
给你一个整数数组 nums，返回 数组 answer ，其中 answer[i] 等于 nums 中除 nums[i] 之外其余各元素的乘积 。

题目数据 保证 数组 nums之中任意元素的全部前缀元素和后缀的乘积都在  32 位 整数范围内。

请 不要使用除法，且在 O(n) 时间复杂度内完成此题。
"""
from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        计算数组中每个元素对应的除自身以外所有元素的乘积。

        Args:
        nums: List[int] - 输入的整数列表。

        Returns:
        List[int] - 每个元素为除自身以外所有元素乘积的结果列表。
        """
        n = len(nums)
        # 初始化前缀乘积数组，初始值为1
        pre = [1] * n
        # 计算每个位置的前缀乘积（不包括当前位置的元素）
        for i in range(1, n):
            pre[i] = pre[i - 1] * nums[i - 1]

        # 初始化后缀乘积数组，初始值为1
        suf = [1] * n
        # 计算每个位置的后缀乘积（不包括当前位置的元素）
        for i in range(n - 2, -1, -1):
            suf[i] = suf[i + 1] * nums[i + 1]

        # 返回前缀乘积和后缀乘积的乘积结果
        return [p * s for p, s in zip(pre, suf)]



    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        计算数组中每个元素对应的除自身以外所有元素的乘积，优化处理包含0的情况。

        Args:
        nums: List[int] - 输入的整数列表。

        Returns:
        List[int] - 每个元素为除自身以外所有元素乘积的结果列表。
        """
        zero_cnt = 0
        p = 1
        # 统计数组中0的数量，并计算非零元素的乘积
        for x in nums:
            if x == 0:
                zero_cnt += 1
            else:
                p *= x

        n = len(nums)
        ans = [0] * n
        # 如果没有0，直接用总乘积除以当前元素
        if zero_cnt == 0:
            for i, x in enumerate(nums):
                ans[i] = p // x
        # 如果有且仅有一个0，只有该位置的结果为非零元素的乘积
        elif zero_cnt == 1:
            for i, x in enumerate(nums):
                if x == 0:
                    ans[i] = p
        return ans



