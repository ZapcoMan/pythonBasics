# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 9:57 上午
# @Author  : codervibe
# @File    : 和为K 的子数组.py
# @Project : pythonBasics
"""
给你一个整数数组 nums 和一个整数 k ，请你统计并返回 该数组中和为 k 的子数组的个数 。

注意 ：子数组是数组中元素的连续非空序列
"""
from typing import List

"""
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # 统计并返回数组中和为 k 的子数组的个数。
        # 
        # 参数:
        # nums: 整数数组。
        # k: 目标子数组的和。
        # 
        # 返回:
        # 和为 k 的子数组的个数。
        # 创建一个字典，用于存储前缀和及其对应的次数
        prefix_sum_count = {0: 1}
        prefix_sum = 0
        count = 0

        # 遍历数组，计算前缀和
        for num in nums:
            prefix_sum += num

            # 计算当前前缀和与目标值的差值
            difference = prefix_sum - k
            if difference in prefix_sum_count:
                count += prefix_sum_count[difference]
            
            # 更新前缀和计数器
            if prefix_sum in prefix_sum_count:
                prefix_sum_count[prefix_sum] += 1
            else:
                prefix_sum_count[prefix_sum] = 1

        return count
"""


class Solution:
    """
    该类提供了一个方法，用于计算数组中和为 k 的连续子数组的数量。
    """

    @staticmethod
    def subarraySum(nums: List[int], k: int) -> int:
        """
        计算数组中和为 k 的连续子数组的数量。

        参数:
        nums: 整数数组。
        k: 目标和。

        返回:
        满足条件的子数组数量。
        """
        # 初始化满足条件的子数组数量为 0
        ans = 0
        # 使用字典记录每个前缀和出现的次数，初始化时前缀和 0 出现一次
        dic = {0: 1}
        # 初始化前缀和为 0
        s = 0
        # 遍历数组中的每个元素
        for v in nums:
            # 将当前元素加到前缀和中
            s += v
            # 如果当前前缀和减去目标和 k 的值在字典中存在，则将其出现次数加到 ans 中
            ans += dic.get(s - k, 0)
            # 更新字典，将当前前缀和的出现次数加 1
            dic[s] = dic.get(s, 0) + 1
        # 返回满足条件的子数组数量
        return ans


def subarraySum(nums: List[int], k: int, strList: List[str]) -> int:
    """
    重写方法
    :param nums:
    :param k:
    :param strList:
    """
    for num in nums:
        print(num)
    for s in strList:
        print(s)
