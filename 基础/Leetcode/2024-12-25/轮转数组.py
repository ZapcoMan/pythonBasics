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
        """
        将给定数组向右轮转k步。

        参数:
        nums: List[int] - 要轮转的数组。
        k: int - 轮转的步数。

        返回值:
        None - 原地修改数组，不返回任何值。
        """

        def reverse(i: int, j: int) -> None:
            """
            反转数组中从索引i到j的部分。

            参数:
            i: int - 起始索引。
            j: int - 结束索引。

            返回值:
            None - 原地修改数组，不返回任何值。
            """
            while i < j:
                # 交换索引i和j处的元素
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1

        n = len(nums)
        # 轮转k次等于轮转k%n次，处理k大于数组长度的情况
        k %= n
        # 全局反转数组
        reverse(0, n - 1)
        # 反转前k个元素，以恢复这部分的原始顺序
        reverse(0, k - 1)
        # 反转剩余的元素，以恢复这部分的原始顺序
        reverse(k, n - 1)


