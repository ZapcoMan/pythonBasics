# -*- coding: utf-8 -*-
# @Time    : 02 1月 2025 7:58 下午
# @Author  : codervibe
# @File    : 二叉树的层序遍历.py
# @Project : pythonBasics
"""
给你二叉树的根节点 root ，返回其节点值的 层序遍历 。 （即逐层地，从左到右访问所有节点）。
"""
import collections
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:return []
        res,queue = [],collections.deque()
        queue.append(root)
        while queue:
            tmp = []
            for i in range(len(queue)):
                node = queue.popleft()
                tmp.append(node.val)
                if node.left:queue.append(node.left)
                if node.right:queue.append(node.right)
            res.append(tmp)
        return res
