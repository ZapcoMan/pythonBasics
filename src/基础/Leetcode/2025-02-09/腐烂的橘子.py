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
from typing import List


class Solution:
    """
    解决腐烂橘子问题的类

    该类提供了一个方法来计算所有新鲜橘子变成腐烂橘子所需的最小分钟数
    """

    def orangesRotting(self, grid: List[List[int]]) -> int:
        """
        计算腐烂橘子 spread 到所有新鲜橘子所需的最小时间

        参数:
        grid: 二维列表，表示网格，其中 1 表示新鲜橘子，2 表示腐烂的橘子

        返回:
        最小分钟数，如果不可能腐烂所有橘子，则返回 -1
        """
        # 获取网格的行数和列数
        m, n = len(grid), len(grid[0])
        # 初始化新鲜橘子的数量为 0
        fresh = 0
        # 初始化一个空队列 q，用于存放腐烂橘子的位置
        q = []
        # 遍历网格，统计新鲜橘子的数量，并将腐烂橘子的位置加入队列
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x == 1:
                    fresh += 1  # 统计新鲜橘子个数
                elif x == 2:
                    q.append((i, j))  # 一开始就腐烂的橘子

        # 初始化经过的时间为 0
        ans = 0
        # 当队列不为空且存在新鲜橘子时，进行循环
        while q and fresh:
            # 时间经过一分钟
            ans += 1
            # 临时存储当前这一分钟内需要处理的腐烂橘子的位置
            tmp = q
            # 清空队列，为下一分钟做准备
            q = []
            # 遍历当前这一分钟内的腐烂橘子位置
            for x, y in tmp:
                # 检查四个方向的相邻单元格
                for i, j in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
                    # 如果相邻单元格内是新鲜橘子
                    if 0 <= i < m and 0 <= j < n and grid[i][j] == 1:
                        # 新鲜橘子数量减一
                        fresh -= 1
                        # 将新鲜橘子变为腐烂橘子
                        grid[i][j] = 2
                        # 将新腐烂的橘子位置加入队列
                        q.append((i, j))

        # 如果还有新鲜橘子，说明无法腐烂所有橘子，返回 -1；否则返回经过的时间
        return -1 if fresh else ans
