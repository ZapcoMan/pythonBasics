# -*- coding: utf-8 -*-
# @Time    : 09 2月 2025 6:45 下午
# @Author  : codervibe
# @File    : 岛屿数量.py
# @Project : pythonBasics
"""
给你一个由 '1'（陆地）和 '0'（水）组成的的二维网格，请你计算网格中岛屿的数量。

岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。

此外，你可以假设该网格的四条边均被水包围。
"""
from typing import List


class Solution:
    """
    解决方案类，用于计算二维网格中的岛屿数量。
    """

    def numIslands(self, grid: List[List[str]]) -> int:
        """
        计算给定网格中的岛屿数量。

        :param grid: 二维网格，其中 '1' 表示陆地，'0' 表示水
        :return: 网格中岛屿的数量
        """
        # 初始化岛屿数量
        ans = 0
        # 获取网格的行数和列数
        m, n = len(grid), len(grid[0])

        def dfs(i: int, j: int) -> None:
            """
            深度优先搜索函数，用于遍历岛屿。

            :param i: 当前行索引
            :param j: 当前列索引
            """
            # 如果当前位置超出网格边界或为水，则返回
            if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == '0':
                return
            # 将当前位置标记为已访问（即将其设置为 '0'）
            grid[i][j] = '0'
            # 递归遍历上下左右四个相邻位置
            dfs(i + 1, j)
            dfs(i - 1, j)
            dfs(i, j + 1)
            dfs(i, j - 1)

        # 遍历网格中的每个位置
        for i in range(m):
            for j in range(n):
                # 如果当前位置是陆地
                if grid[i][j] == '1':
                    # 岛屿数量加一
                    ans += 1
                    # 使用深度优先搜索遍历整个岛屿
                    dfs(i, j)
        # 返回岛屿数量
        return ans
