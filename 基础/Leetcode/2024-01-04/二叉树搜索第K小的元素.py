# -*- coding: utf-8 -*-
# @Time    : 04 1月 2025 2:43 下午
# @Author  : codervibe
# @File    : 二叉树搜索第K小的元素.py
# @Project : pythonBasics
"""
给定一个二叉搜索树的根节点 root ，和一个整数 k ，请你设计一个算法查找其中第 k 小的元素（从 1 开始计数）。
"""
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        def dfs(root):
            if not root:
                return
            dfs(root.left)
            # if self.k == 0: return
            self.k -= 1
            if self.k == 0:
                self.res = root.val
            dfs(root.right)

        self.k = k
        dfs(root)
        return self.res
