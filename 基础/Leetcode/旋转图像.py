# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 8:16 下午
# @Author  : codervibe
# @File    : 旋转图像.py
# @Project : pythonBasics
"""
给定一个 n × n 的二维矩阵 matrix 表示一个图像。请你将图像顺时针旋转 90 度。

你必须在 原地 旋转图像，这意味着你需要直接修改输入的二维矩阵。请不要 使用另一个矩阵来旋转图像。
"""
# 
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        不返回任何东西，而是就地修改矩阵。
        """
        size = len(matrix)
        for r in range(size):
            for c in range(r, size):
                matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
        for r in range(size):
            left, right = 0, size - 1
            while left < right:
                matrix[r][left], matrix[r][right] = matrix[r][right], matrix[r][left]
                left += 1
                right -= 1
        return

