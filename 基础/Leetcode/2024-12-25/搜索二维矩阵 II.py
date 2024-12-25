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
        for row in matrix:
            for element in row:
                if element == target:
                    return True
        return False

