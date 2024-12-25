# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 8:16 下午
# @Author  : codervibe
# @File    : 旋转图像.py
# @Project : pythonBasics
"""
给定一个 n × n 的二维矩阵 matrix 表示一个图像。请你将图像顺时针旋转 90 度。

你必须在 原地 旋转图像，这意味着你需要直接修改输入的二维矩阵。请不要 使用另一个矩阵来旋转图像。
"""
from typing import List


#
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        将给定的二维矩阵顺时针旋转90度。
        不返回任何东西，而是就地修改矩阵。

        参数:
        matrix: List[List[int]] - 二维整数数组，表示待旋转的矩阵。
        """
        # 获取矩阵的大小，用于后续的遍历
        size = len(matrix)

        # 第一步：沿对角线翻转矩阵
        for r in range(size):
            for c in range(r, size):
                # 交换对角线两侧的元素
                matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]

        # 第二步：翻转每一行，完成整个旋转操作
        for r in range(size):
            left, right = 0, size - 1
            while left < right:
                # 交换左右两侧的元素
                matrix[r][left], matrix[r][right] = matrix[r][right], matrix[r][left]
                left += 1
                right -= 1

        # 旋转完成后，不返回任何值
        return

    # 添加最优解
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        不返回任何东西，而是就地修改矩阵。
        """

        def next_position(i, j, di, dj, steps):
            """
            计算下一个位置。
            """
            while steps:
                if not (left <= i + di <= right and top <= j + dj <= bottom):
                    di, dj = dj, -di
                steps, i, j = steps - 1, i + di, j + dj
            return i, j, di, dj

        def move_4_points(i, j, steps):
            """
            移动四个点的位置。
            """
            to_be_moved, di, dj = matrix[i][j], 0, 1
            for _ in range(4):
                next_i, next_j, di, dj = next_position(i, j, di, dj, steps)
                matrix[next_i][next_j], to_be_moved, i, j = to_be_moved, matrix[next_i][next_j], next_i, next_j

        left, right, top, bottom = 0, len(matrix) - 1, 0, len(matrix) - 1
        while left < right:
            for j in range(left, right):
                move_4_points(top, j, right - left)
            left, right, top, bottom = left + 1, right - 1, top + 1, bottom - 1

if __name__ == '__main__':
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    Solution().rotate(matrix)
    print(matrix)
