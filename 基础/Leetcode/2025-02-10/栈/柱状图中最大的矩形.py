# -*- coding: utf-8 -*-
# @Time    : 10 2月 2025 11:21 下午
# @Author  : codervibe
# @File    : 柱状图中最大的矩形.py
# @Project : pythonBasics
"""
给定 n 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1 。

求在该柱状图中，能够勾勒出来的矩形的最大面积。
"""


class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        """
        使用单调递增栈来解决柱状图中最大矩形面积问题。
        通过维护一个单调递增的栈，我们可以有效地计算出每个柱子能够构成的最大矩形的面积。

        参数:
        heights (List[int]): 表示柱状图中各个柱子的高度列表。

        返回:
        int: 返回柱状图中能够勾勒出来的最大矩形面积。
        """
        # 在高度列表的前后各添加一个高度为0的柱子，方便边界处理
        heights = [0] + heights + [0]

        # 初始化一个栈，用于存放柱子的索引
        stack = []
        # 初始化最大面积变量
        ans = 0

        # 遍历每个柱子，计算能够构成的最大矩形面积
        for i, h in enumerate(heights):
            # 当栈不为空且当前柱子的高度小于栈顶柱子的高度时，进行面积计算
            while stack and h < heights[stack[-1]]:
                # 弹出栈顶柱子，计算以它为高的矩形的面积
                dh = heights[stack.pop()]
                # 计算宽度，宽度为当前柱子的索引减去栈顶柱子的索引再减1
                dw = i - stack[-1] - 1
                # 更新最大面积
                ans = max(ans, dh * dw)

            # 将当前柱子的索引压入栈中
            stack.append(i)

        # 返回最大面积
        return ans
