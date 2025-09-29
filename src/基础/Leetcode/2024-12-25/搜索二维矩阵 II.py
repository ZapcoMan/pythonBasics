# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 8:40 下午
# @Author  : codervibe
# @File    : 搜索二维矩阵 II.py
# @Project : pythonBasics
"""
编写一个高效的算法来搜索 m x n 矩阵 matrix 中的一个目标值 target 。该矩阵具有以下特性：

每行的元素从左到右升序排列。
每列的元素从上到下升序排列。
"""
from typing import List

# 官方题解
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """
        在二维矩阵中搜索目标值。

        第一个方法是简单的暴力搜索方法，遍历矩阵中的每个元素，直到找到目标值或遍历完所有元素。
        这种方法没有利用矩阵行和列的排序特性。

        参数:
        matrix (List[List[int]]): 二维矩阵，每一行的元素从左到右按升序排列，每一列的元素从上到下按升序排列。
        target (int): 要搜索的目标值。

        返回:
        bool: 如果找到目标值则返回True，否则返回False。
        """
        for row in matrix:
            for element in row:
                if element == target:
                    return True
        return False

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """
        在二维矩阵中搜索目标值。

        第二个方法是利用矩阵行和列的排序特性的搜索方法，从矩阵的右上角开始搜索。
        如果当前元素等于目标值，则返回True；如果当前元素小于目标值，则排除这一行；如果当前元素大于目标值，则排除这一列。
        这种方法有效地减少了需要搜索的元素数量。

        参数:
        matrix (List[List[int]]): 二维矩阵，每一行的元素从左到右按升序排列，每一列的元素从上到下按升序排列。
        target (int): 要搜索的目标值。

        返回:
        bool: 如果找到目标值则返回True，否则返回False。
        """
        m, n = len(matrix), len(matrix[0])
        i, j = 0, n - 1  # 从右上角开始
        while i < m and j >= 0:  # 还有剩余元素
            if matrix[i][j] == target:
                return True  # 找到 target
            if matrix[i][j] < target:
                i += 1  # 这一行剩余元素全部小于 target，排除
            else:
                j -= 1  # 这一列剩余元素全部大于 target，排除
        return False
