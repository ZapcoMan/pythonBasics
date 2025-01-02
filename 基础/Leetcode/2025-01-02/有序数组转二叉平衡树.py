# -*- coding: utf-8 -*-
# @Time    : 02 1月 2025 8:06 下午
# @Author  : codervibe
# @File    : 有序数组转二叉平衡树.py
# @Project : pythonBasics
"""
给你一个整数数组 nums ，其中元素已经按 升序 排列，请你将其转换为一棵
平衡二叉搜索树。
"""
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        def buildTree(left: int, right: int) -> Optional[TreeNode]:
            if left >= right: return None  # 范围为空，即没有元素可以构造节点，返回空
            mid = left + ((right - left) >> 1)  # 获取范围中点
            return TreeNode(nums[mid], buildTree(left, mid), buildTree(mid + 1, right))  # 创建根节点并递归生成子树

        return buildTree(0, len(nums))  # 对整个数组范围的元素生成树
