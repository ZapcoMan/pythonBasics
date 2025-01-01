# -*- coding: utf-8 -*-
# @Time    : 01 1月 2025 10:49 上午
# @Author  : codervibe
# @File    : 翻转二叉树.py
# @Project : pythonBasics
"""
给你一棵二叉树的根节点 root ，翻转这棵二叉树，并返回其根节点。
"""
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # print(f"{root}")
        if root:
            root.left,root.right = self.invertTree(root.right),self.invertTree(root.left)
            return root
        return root