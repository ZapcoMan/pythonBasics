# -*- coding: utf-8 -*-
# @Time    : 02 1月 2025 8:21 下午
# @Author  : codervibe
# @File    : 验证二叉搜索树.py
# @Project : pythonBasics
"""
给你一个二叉树的根节点 root ，判断其是否是一个有效的二叉搜索树。
有效 二叉搜索树定义如下：
节点的左子树只包含 小于 当前节点的数。
节点的右子树只包含 大于 当前节点的数。
所有左子树和右子树自身必须也是二叉搜索树。
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        """
        初始化二叉树节点。

        参数:
        val (int): 节点的值，默认为0。
        left (TreeNode): 左子节点，默认为None。
        right (TreeNode): 右子节点，默认为None。
        """
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        """
        判断给定的二叉树是否为有效的二叉搜索树。

        参数:
        root (TreeNode): 二叉树的根节点。

        返回:
        bool: 如果是有效的二叉搜索树返回True，否则返回False。
        """
        # 初始化递归函数，设置初始最小值和最大值
        return self.dg(root, -(2 ** 32), 2 ** 32)

    def dg(self, root, min_v, max_v):
        """
        辅助递归函数，用于验证当前子树是否为有效的二叉搜索树。

        参数:
        root (TreeNode): 当前子树的根节点。
        min_v (int): 当前子树中允许的最小值（下界）。
        max_v (int): 当前子树中允许的最大值（上界）。

        返回:
        bool: 如果当前子树是有效的二叉搜索树返回True，否则返回False。
        """
        if root is None:
            # 如果当前节点为空，证明已经递归到叶子节点，返回True
            return True

        # 检查当前节点值是否在允许的范围内
        if not (min_v < root.val < max_v):
            # 如果当前节点值不符合规定，直接返回 False
            return False

        # 递归检查左子树和右子树
        # 对左子树进行递归，此时最大值应该为当前节点值
        if not self.dg(root.left, min_v, root.val):
            return False
        # 对右子树进行递归，此时最小值应该为当前节点值
        if not self.dg(root.right, root.val, max_v):
            return False

        # 如果成功避开所有坑，恭喜，这个当前节点下的子树是一个二叉搜索树
        return True
