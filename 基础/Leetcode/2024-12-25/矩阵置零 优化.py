# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 7:58 下午
# @Author  : codervibe
# @File    : 矩阵置零 优化.py
# @Project : pythonBasics
from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        将矩阵中某个元素为0所在的行和列都设置为0。

        参数:
        matrix: List[List[int]] - 二维整数数组

        不返回任何东西，而是就地修改矩阵。
        """
        if not matrix or not matrix[0]:
            return

        # 获取矩阵的行数和列数
        rows = len(matrix)
        cols = len(matrix[0])

        # 标记第一行和第一列是否需要置零
        first_row_has_zero = any(matrix[0][j] == 0 for j in range(cols))
        first_col_has_zero = any(matrix[i][0] == 0 for i in range(rows))

        # 使用第一行和第一列来标记需要置零的行和列
        for i in range(1, rows):
            for j in range(1, cols):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        # 根据第一行和第一列的标记将对应的行和列置零
        for i in range(1, rows):
            for j in range(1, cols):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        # 如果第一行有0，将第一行全部置零
        if first_row_has_zero:
            for j in range(cols):
                matrix[0][j] = 0

        # 如果第一列有0，将第一列全部置零
        if first_col_has_zero:
            for i in range(rows):
                matrix[i][0] = 0


if __name__ == '__main__':
    matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    Solution().setZeroes(matrix)

