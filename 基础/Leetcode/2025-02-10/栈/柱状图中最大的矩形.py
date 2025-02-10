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
        # 单调递增栈，遇到一个较小的，可以算出前一个面积。宽需再次获取栈顶元素
        heights = [0] + heights + [0]

        stack = []
        ans = 0

        for i, h in enumerate(heights):
            while stack and h < heights[stack[-1]]:
                # 对于重复元素，会多次求面积，最后会算到最大面积
                # [9,8,7,7,7,7,6]. 6这里会分别与前面四个7算出最大面积
                dh = heights[stack.pop()]
                dw = i - stack[-1] - 1
                ans = max(ans, dh * dw)

            stack.append(i)

        return ans