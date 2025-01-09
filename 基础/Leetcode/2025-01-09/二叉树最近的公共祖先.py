# -*- coding: utf-8 -*-
# @Time    : 09 1月 2025 7:11 下午
# @Author  : codervibe
# @File    : 二叉树最近的公共祖先.py
# @Project : pythonBasics
"""
给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。

百度百科中最近公共祖先的定义为：“对于有根树 T 的两个节点 p、q，最近公共祖先表示为一个节点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。”


"""

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        """
        找到二叉树中两个指定节点的最近公共祖先。

        :param root: 二叉树的根节点。
        :param p: 第一个要查找的节点。
        :param q: 第二个要查找的节点。
        :return: 最近公共祖先节点。

        递归地在左右子树中查找节点 p 和 q 的最近公共祖先，如果当前节点是 p 或 q 或为空，则返回当前节点。
        如果 p 和 q 分别在当前节点的左右子树中，则当前节点是它们的最近公共祖先。
        如果 p 和 q 都在当前节点的同一侧子树中，则继续在该侧子树中查找。
        """
        # 如果当前节点为空或为 p 或 q，返回当前节点
        if not root or root == p or root == q:
            return root
        # 在左子树中查找 p 和 q 的最近公共祖先
        left = self.lowestCommonAncestor(root.left, p, q)
        # 在右子树中查找 p 和 q 的最近公共祖先
        right = self.lowestCommonAncestor(root.right, p, q)
        # 如果左子树中未找到，则返回右子树中的结果
        if not left:
            return right
        # 如果右子树中未找到，则返回左子树中的结果
        if not right:
            return left
        # 如果 p 和 q 分别在左右子树中，返回当前节点作为最近公共祖先
        return root
