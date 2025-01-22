# -*- coding: utf-8 -*-
# @Time    : 22 1月 2025 1:24 下午
# @Author  : codervibe
# @File    : 动态规划-爬楼梯.py
# @Project : pythonBasics
"""
假设你正在爬楼梯。需要 n 阶你才能到达楼顶。

每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？


"""


class Solution:
    def climbStairs(self, n: int) -> int:
        a, b = 1, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b
