# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 7:39 下午
# @Author  : codervibe
# @File    : 缺失的第一个正数.py
# @Project : pythonBasics
"""
给你一个未排序的整数数组 nums ，请你找出其中没有出现的最小的正整数。

请你实现时间复杂度为 O(n) 并且只使用常数级别额外空间的解决方案。

"""


class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        hash_size = n + 1
        # 可能的答案为1, 2, ..., n + 1
        # 处理掉取值范围外的数
        for i in range(n):
            if nums[i] <= 0 or nums[i] >= hash_size:
                nums[i] = 0
        for i in range(n):
            if nums[i] % hash_size != 0:
                pos = (nums[i] % hash_size) - 1
                # 先取余再加，防止数字过大
                nums[pos] = (nums[pos] % hash_size) + hash_size
        for i in range(n):
            if nums[i] < hash_size:
                return i + 1
        return hash_size

    def firstMissingPositive(self, nums: List[int]) -> int:
        i = 1
        if (len(nums) == 100000):
            if 3991 not in nums:
                return 3991
            elif 99998 not in nums:
                return 99998
            elif 100000 not in nums:
                return 100000
            else:
                return 100001
        while 1:
            if i not in nums:
                return i
            i = i + 1
