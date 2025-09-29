# -*- coding: utf-8 -*-
# @Time    : 02 1月 2025 7:51 下午
# @Author  : codervibe
# @File    : 二叉树的直径.py
# @Project : pythonBasics
"""
给你一棵二叉树的根节点，返回该树的 直径 。

二叉树的 直径 是指树中任意两个节点之间最长路径的 长度 。这条路径可能经过也可能不经过根节点 root 。

两节点之间路径的 长度 由它们之间边数表示。
"""
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        """
        计算二叉树的直径

        :param root: 二叉树的根节点
        :return: 返回二叉树的直径
        """
        # 初始化直径为1，因为至少有一个节点时，直径为1
        self.ans = 1

        def depth(root):
            """
            深度优先搜索函数，用于计算每个节点的深度并更新最大直径

            :param root: 当前节点
            :return: 返回当前节点的深度
            """
            # 如果当前节点为空，返回深度0
            if not root: return 0
            # 递归计算左子树的深度
            L = depth(root.left)
            # 递归计算右子树的深度
            R = depth(root.right)
            # 更新最大直径，直径为左子树深度加右子树深度加1
            self.ans = max(self.ans, L + R + 1)
            # 返回当前节点的深度，取左右子树深度的最大值加1
            return max(L, R) + 1

        # 调用深度优先搜索函数
        depth(root)
        # 返回最大直径减1，因为题目要求的是路径长度，即边数
        return self.ans - 1
