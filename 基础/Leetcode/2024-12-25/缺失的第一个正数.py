# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 7:39 下午
# @Author  : codervibe
# @File    : 缺失的第一个正数.py
# @Project : pythonBasics
"""
给你一个未排序的整数数组 nums ，请你找出其中没有出现的最小的正整数。

请你实现时间复杂度为 O(n) 并且只使用常数级别额外空间的解决方案。

"""
from typing import List


class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        """
        寻找缺失的最小正整数。

        Args:
            nums: 一个整数列表。

        Returns:
            返回缺失的最小正整数。
        """
        # 计算列表长度
        n = len(nums)
        # 哈希表的大小为n+1，因为可能的答案范围是1到n+1
        hash_size = n + 1
        # 可能的答案为1, 2, ..., n + 1
        # 处理掉取值范围外的数
        for i in range(n):
            if nums[i] <= 0 or nums[i] >= hash_size:
                nums[i] = 0
        # 第二次遍历，将出现的数通过哈希表标记
        for i in range(n):
            if nums[i] % hash_size != 0:
                pos = (nums[i] % hash_size) - 1
                # 先取余再加，防止数字过大
                nums[pos] = (nums[pos] % hash_size) + hash_size
        # 第三次遍历，找到第一个没有被标记的位置，即为缺失的最小正整数
        for i in range(n):
            if nums[i] < hash_size:
                return i + 1
        # 如果所有位置都被标记，那么缺失的最小正整数是n+1
        return hash_size


    def firstMissingPositive(self, nums: List[int]) -> int:
        """
        使用集合寻找缺失的最小正整数。

        Args:
            nums: 一个整数列表。

        Returns:
            返回缺失的最小正整数。
        """
        # 创建一个集合，用于快速查找
        s = set(nums)
        # 从1开始遍历到列表长度加1，寻找第一个不在集合中的数
        for i in range(1, len(nums) + 1):
            if i not in s:
                return i
        # 如果所有数都在集合中，那么缺失的最小正整数是列表长度加1
        return len(nums) + 1
