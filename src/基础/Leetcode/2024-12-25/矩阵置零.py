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
        将矩阵中某个元素为0所在的行和列都设置为0。

        参数:
        matrix: List[List[int]] - 二维整数数组

        不返回任何东西，而是就地修改矩阵。
        """
        # 用于记录需要置零的位置
        zero = []
        # 遍历矩阵，记录所有0的位置
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    zero.append((i, j))

        # 遍历记录的位置，将对应行和列的元素置零
        while len(zero) > 0:
            x, y = zero.pop()
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    if i == x or j == y:
                        matrix[i][j] = 0

        return

    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        将矩阵中某个元素为0所在的行和列都设置为0。

        参数:
        matrix: List[List[int]] - 二维整数数组

        不返回任何东西，而是就地修改矩阵。
        """
        # 初始化行标志和列标志
        row_flag = [0 for i in range(len(matrix))]
        col_flag = [0 for i in range(len(matrix[0]))]
        # 遍历矩阵，标记含有0的行和列
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 0:
                    row_flag[i] = 1
                    col_flag[j] = 1
        # 根据标志将对应的行和列的元素置零
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if row_flag[i] == 1 or col_flag[j] == 1:
                    matrix[i][j] = 0
