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
        """
        对二叉树进行层序遍历

        参数:
        root: Optional[TreeNode] - 二叉树的根节点

        返回值:
        List[List[int]] - 层序遍历的结果列表，每个元素为每一层的节点值列表
        """
        # 如果根节点为空，直接返回空列表
        if not root:
            return []

        # 初始化结果列表和队列，将根节点加入队列
        res, queue = [], collections.deque()
        queue.append(root)

        # 当队列不为空时，进行层序遍历
        while queue:
            tmp = []
            # 遍历当前层的所有节点
            for i in range(len(queue)):
                node = queue.popleft()
                # 将当前节点的值加入临时列表
                tmp.append(node.val)
                # 如果当前节点有左子节点，将左子节点加入队列
                if node.left:
                    queue.append(node.left)
                # 如果当前节点有右子节点，将右子节点加入队列
                if node.right:
                    queue.append(node.right)
            # 将临时列表加入结果列表
            res.append(tmp)

        # 返回结果列表
        return res
