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
        cur, res, stack = root, [], []
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            res.append(cur.val)
            cur = cur.right
        ress = res[::-1]
        return res == ress