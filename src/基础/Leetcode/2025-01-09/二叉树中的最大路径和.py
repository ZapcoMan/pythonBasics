# -*- coding: utf-8 -*-
# @Time    : 09 1月 2025 7:34 下午
# @Author  : codervibe
# @File    : 二叉树中的最大路径和.py
# @Project : pythonBasics
"""
二叉树中的 路径 被定义为一条节点序列，序列中每对相邻节点之间都存在一条边。
同一个节点在一条路径序列中 至多出现一次 。该路径 至少包含一个 节点，且不一定经过根节点。

路径和 是路径中各节点值的总和。

给你一个二叉树的根节点 root ，返回其 最大路径和 。
"""
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        # 初始化最大路径和为负无穷
        self.maxsum = float('-inf')

        def dfs(root):
            # 如果节点为空，返回0
            if not root:
                return 0
            # 递归计算左子树的最大路径和
            left = dfs(root.left)
            # 递归计算右子树的最大路径和
            right = dfs(root.right)
            # 更新最大路径和，比较当前节点的值加上左子树和右子树的最大路径和与已有的最大路径和
            self.maxsum = max(self.maxsum, root.val + left + right)
            # 返回当前节点值与左子树或右子树最大路径和的较大值，且不小于0
            return max(0, max(left, right) + root.val)

        # 调用dfs函数，启动递归
        print(dfs(root))
        # 返回最大路径和
        return self.maxsum
