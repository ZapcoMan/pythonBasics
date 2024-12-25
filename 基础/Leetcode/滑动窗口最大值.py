# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 7:04 下午
# @Author  : codervibe
# @File    : 滑动窗口最大值.py
# @Project : pythonBasics
"""
题目描述：给你一个整数数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 k 个数字。滑动窗口每次只向右移动一位。

返回 滑动窗口中的最大值
"""
import collections
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        deque = collections.deque()
        res, n = [], len(nums)
        for i, j in zip(range(1 - k, n + 1 - k), range(n)):
            # 删除 deque 中对应的 nums[i-1]
            if i > 0 and deque[0] == nums[i - 1]:
                deque.popleft()
            # 保持 deque 递减
            while deque and deque[-1] < nums[j]:
                deque.pop()
            deque.append(nums[j])
            # 记录窗口最大值
            if i >= 0:
                res.append(deque[0])
        return res

    def maxSlidingWindow(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        if not nums:
            return []

        if k == 0:
            return []

        if len(nums) <= k:
            return [max(nums)]

        first = max(nums[:k])
        idx = nums.index(first)
        res = [first]
        for i in range(k, len(nums)):
            if i - k <= idx and nums[i] >= first:
                first = nums[i]
                idx = i
            elif i - k + 1 > idx:
                first = max(nums[idx + 1:i + 1])
                idx = i - k + nums[idx + 1:i + 1].index(first) + 1
            res.append(first)
        return res
