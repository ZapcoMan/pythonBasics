# -*- coding: utf-8 -*-
# @Time    : 09 2月 2025 6:52 下午
# @Author  : codervibe
# @File    : 腐烂的橘子.py
# @Project : pythonBasics

"""
在给定的 m x n 网格 grid 中，每个单元格可以有以下三个值之一：

值 0 代表空单元格；
值 1 代表新鲜橘子；
值 2 代表腐烂的橘子。
每分钟，腐烂的橘子 周围 4 个方向上相邻 的新鲜橘子都会腐烂。

返回 直到单元格中没有新鲜橘子为止所必须经过的最小分钟数。如果不可能，返回 -1 。
"""
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        fresh = 0
        q = []
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x == 1:
                    fresh += 1  # 统计新鲜橘子个数
                elif x == 2:
                    q.append((i, j))  # 一开始就腐烂的橘子

        ans = 0
        while q and fresh:
            ans += 1  # 经过一分钟
            tmp = q
            q = []
            for x, y in tmp:  # 已经腐烂的橘子
                for i, j in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):  # 四方向
                    if 0 <= i < m and 0 <= j < n and grid[i][j] == 1:  # 新鲜橘子
                        fresh -= 1
                        grid[i][j] = 2  # 变成腐烂橘子
                        q.append((i, j))

        return -1 if fresh else ans
