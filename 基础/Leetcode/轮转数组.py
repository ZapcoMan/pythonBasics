# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 7:25 下午
# @Author  : codervibe
# @File    : 轮转数组.py
# @Project : pythonBasics
"""
给定一个整数数组 nums，将数组中的元素向右轮转 k 个位置，其中 k 是非负数。
"""
from typing import List


class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        def reverse(i: int, j: int) -> None:
            while i < j:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1

        n = len(nums)
        k %= n  # 轮转 k 次等于轮转 k%n 次
        reverse(0, n - 1)
        reverse(0, k - 1)
        reverse(k, n - 1)

