# -*- coding: utf-8 -*-
# @Time    : 01 1月 2025 11:04 上午
# @Author  : codervibe
# @File    : 对称二叉树.py
# @Project : pythonBasics

"""
给你一个二叉树的根节点 root ， 检查它是否轴对称。
"""
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    # 如果是中序遍历 那么中序遍历后的逆序和自己本身是一样的
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        """
        判断给定的二叉树是否为对称二叉树。

        参数:
        root: Optional[TreeNode] - 二叉树的根节点。

        返回值:
        bool - 如果二叉树是对称的，则返回True；否则返回False。
        """
        # 初始化当前节点、结果列表和栈
        cur, res, stack = root, [], []
        # 遍历二叉树
        while stack or cur:
            # 尽可能地遍历左子树
            while cur:
                stack.append(cur)
                cur = cur.left
            # 回溯到上一个节点
            cur = stack.pop()
            # 将节点值添加到结果列表中
            res.append(cur.val)
            # 遍历右子树
            cur = cur.right
        # 生成结果列表的逆序列表
        ress = res[::-1]
        # 判断原列表和逆序列表是否相同，从而确定二叉树是否对称
        return res == ress
