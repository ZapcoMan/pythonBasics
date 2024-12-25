# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 7:53 下午
# @Author  : codervibe
# @File    : 矩阵置零.py
# @Project : pythonBasics
"""
给定一个 m x n 的矩阵，如果一个元素为 0 ，则将其所在行和列的所有元素都设为 0 。请使用 原地 算法。
"""
from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        不返回任何东西，而是就地修改矩阵。
        """
        zero = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    zero.append((i, j))

        while len(zero) > 0:
            x, y = zero.pop()
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    if i == x or j == y:
                        matrix[i][j] = 0

        return

