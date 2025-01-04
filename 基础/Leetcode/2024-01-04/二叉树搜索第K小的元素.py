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
        """
        在二叉搜索树中查找第k小的元素。

        使用深度优先搜索（DFS）进行中序遍历，因为中序遍历二叉搜索树会得到一个升序的序列。
        在遍历过程中，记录当前是第几个最小的元素，并在找到第k个最小元素时返回。

        参数:
        root: TreeNode - 二叉搜索树的根节点
        k: int - 需要查找的第k小的元素的序号

        返回:
        int - 第k小的元素的值
        """
        def dfs(root):
            # 如果当前节点为空，则直接返回
            if not root:
                return
            # 先递归遍历左子树
            dfs(root.left)
            # if self.k == 0: return
            # 当前节点是第k小的元素时，将其值赋给self.res
            self.k -= 1
            if self.k == 0:
                self.res = root.val
            # 递归遍历右子树
            dfs(root.right)

        # 初始化k值
        self.k = k
        # 从根节点开始进行深度优先搜索
        dfs(root)
        # 返回第k小的元素的值
        return self.res
