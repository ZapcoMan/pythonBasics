# -*- coding: utf-8 -*-
# @Time    : 01 1月 2025 10:24 上午
# @Author  : codervibe
# @File    : 二叉树的最大深度.py
# @Project : pythonBasics
"""
给定一个二叉树 root ，返回其最大深度。

二叉树的 最大深度 是指从根节点到最远叶子节点的最长路径上的节点数。
"""
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    """定义二叉树节点类"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """提供解决方案的类"""

    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """
        计算二叉树的最大深度

        采用递归方法，如果当前节点不为空，则计算其左右子树的最大深度，并返回较大值加1；
        如果当前节点为空，说明到达叶子节点，返回0

        :param root: 二叉树的根节点
        :return: 最大深度
        """
        print(f"{root}")
        if root is not None:
            return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1
        return 0

