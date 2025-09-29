# -*- coding: utf-8 -*-
# @Time    : 09 1月 2025 6:45 下午
# @Author  : codervibe
# @File    : 从前序与中序遍历序列构造二叉树.py
# @Project : pythonBasics
"""
给定两个整数数组 preorder 和 inorder ，其中 preorder 是二叉树的先序遍历， inorder 是同一棵树的中序遍历，请构造二叉树并返回其根节点。
"""
from typing import List, Optional

class TreeNode:
    """
    二叉树节点定义。
    """
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        """
        根据前序遍历和中序遍历构造二叉树。

        参数:
        preorder (List[int]): 二叉树的前序遍历列表。
        inorder (List[int]): 二叉树的中序遍历列表。

        返回:
        Optional[TreeNode]: 构造的二叉树的根节点。
        """
        # 创建一个字典来存储中序遍历中每个节点的位置，以便快速查找。
        dic = {}
        # 初始化前序遍历的索引。
        preorder = preorder

        def recur(root, left, right):
            """
            递归地构造二叉树。

            参数:
            root (int): 当前子树根节点在前序遍历中的索引。
            left (int): 当前子树在中序遍历中的左边界。
            right (int): 当前子树在中序遍历中的右边界。

            返回:
            TreeNode: 构造的子树的根节点。
            """
            # 如果左边界大于右边界，说明没有元素可以构造子树，返回None。
            if left > right:
                return None

            # 选择前序遍历中当前索引的元素作为根节点。
            node = TreeNode(preorder[root])
            # 在中序遍历中找到根节点的位置。
            i = dic[preorder[root]]
            # 递归构造左子树。
            node.left = recur(root + 1, left, i - 1)
            # 递归构造右子树。
            node.right = recur(i - left + root + 1, i + 1, right)
            return node

        # 构建中序遍历中每个节点的位置字典。
        for i in range(len(inorder)):
            dic[inorder[i]] = i
        # 从前序遍历的第一个元素开始，递归构造整棵树。
        return recur(0, 0, len(inorder) - 1)
