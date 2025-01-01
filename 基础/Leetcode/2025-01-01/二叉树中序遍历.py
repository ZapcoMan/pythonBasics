# -*- coding: utf-8 -*-
# @Time    : 01 1月 2025 9:42 上午
# @Author  : codervibe
# @File    : 二叉树中序遍历.py
# @Project : pythonBasics
"""
给定一个二叉树的根节点 root ，返回 它的 中序 遍历 。
"""

from typing import Optional, List


# 二叉树节点的定义。
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    # 递归遍历
    # 方法一：递归遍历
    # 我们先递归左子树，再访问根节点，接着递归右子树。
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(root):
            if root is None:
                return
            dfs(root.left)
            nonlocal ans
            ans.append(root.val)
            dfs(root.right)

        ans = []
        dfs(root)
        return ans
