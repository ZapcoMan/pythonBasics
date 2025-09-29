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
    """定义二叉树节点类"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    head = None  # 初始化链表头节点为空

    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        将二叉树就地展开为链表，不需要返回任何东西，而是就地修改根。
        展开后的链表顺序与二叉树的先序遍历顺序相同。

        参数:
        root (Optional[TreeNode]): 二叉树的根节点
        """
        if root is None:
            return  # 如果节点为空，则直接返回
        self.flatten(root.right)  # 递归处理右子树
        self.flatten(root.left)  # 递归处理左子树
        root.left = None  # 将当前节点的左子节点设为空
        root.right = self.head  # 将当前节点的右子节点设为链表的头节点
        self.head = root  # 更新链表的头节点为当前节点
