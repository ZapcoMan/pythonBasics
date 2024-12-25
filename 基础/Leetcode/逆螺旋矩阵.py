# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 8:14 下午
# @Author  : codervibe
# @File    : 逆螺旋矩阵.py
# @Project : pythonBasics

"""
给你一个 m 行 n 列的矩阵 matrix ，请按照 顺时针螺旋顺序 ，返回矩阵中的所有元素。
"""
# 给你一个 m 行 n 列的矩阵 matrix ，请按照逆时针螺旋顺序 ，返回矩阵中的所有元素。
from typing import List
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix:
            return []
        m, n = len(matrix), len(matrix[0])
        res = []
        left, right, top, bottom = 0, n - 1, 0, m - 1
        while left <= right and top <= bottom:
            for i in range(left, right + 1):
                res.append(matrix[top][i])
            for i in range(top + 1, bottom + 1):
                res.append(matrix[i][right])










if __name__ == '__main__':
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(Solution().spiralOrder(matrix))
