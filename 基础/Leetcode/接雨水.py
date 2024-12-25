# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 8:58 上午
# @Author  : codervibe
# @File    : 接雨水.py
# @Project : pythonBasics
"""
困难：给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。
"""
from typing import List

"""
此方法未使用，故已注释
class Solution:
    def trap(self, height: List[int]) -> int:
        ans = 0
        h1 = 0
        h2 = 0
        for i in range(len(height)):
            h1 = max(h1, height[i])
            h2 = max(h2, height[-i - 1])
            ans = ans + h1 + h2 - height[i]
        return ans - len(height) * h1
"""

"""
最优解
"""
class Solution:
    @staticmethod
    def trap(height: List[int]) -> int:
        """
        计算给定高度图能接的雨水量。

        参数:
        height (List[int]): 一个非负整数列表表示每个柱子的高度。

        返回:
        int: 下雨后能接的雨水总量。
        """
        if not height:
            return 0

        left, right = 0, len(height) - 1
        left_max, right_max = height[left], height[right]
        water_trapped = 0

        while left < right:
            # 移动指针以找到可以接水的区域
            if height[left] < height[right]:
                # 更新左侧最高点或累加可以接的雨水量
                if height[left] >= left_max:
                    left_max = height[left]
                else:
                    water_trapped += left_max - height[left]
                left += 1
            else:
                # 更新右侧最高点或累加可以接的雨水量
                if height[right] >= right_max:
                    right_max = height[right]
                else:
                    water_trapped += right_max - height[right]
                right -= 1

        return water_trapped
