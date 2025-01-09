# -*- coding: utf-8 -*-
# @Time    : 09 1月 2025 6:40 下午
# @Author  : codervibe
# @File    : 二叉树展开为链表.py
# @Project : pythonBasics
"""
给你二叉树的根结点 root ，请你将它展开为一个单链表：

展开后的单链表应该同样使用 TreeNode ，其中 right 子指针指向链表中下一个结点，而左子指针始终为 null 。
展开后的单链表应该与二叉树 先序遍历 顺序相同。
"""
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    head = None
    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        不要返回任何东西，而是就地修改根。
        """
        if root is None:
            return
        self.flatten(root.right)
        self.flatten(root.left)
        root.left = None
        root.right = self.head
        self.head = root
