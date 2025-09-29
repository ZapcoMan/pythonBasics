# -*- coding: utf-8 -*-
# @Time    : 09 1月 2025 6:58 下午
# @Author  : codervibe
# @File    : 路径总和 3.py
# @Project : pythonBasics
"""
给定一个二叉树的根节点 root ，和一个整数 targetSum ，求该二叉树里节点值之和等于 targetSum 的 路径 的数目。

路径 不需要从根节点开始，也不需要在叶子节点结束，但是路径方向必须是向下的（只能从父节点到子节点）。
"""
from collections import defaultdict
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        # 初始化路径总数为0
        ans = 0
        # 使用字典记录从根节点到当前节点的路径和出现的次数
        cnt = defaultdict(int)
        # 初始情况下，路径和为0出现了一次
        cnt[0] = 1

        def dfs(node: Optional[TreeNode], s: int) -> None:
            # 如果当前节点为空，则直接返回
            if node is None:
                return
            # 更新当前路径和
            s += node.val
            # 如果存在路径和与目标值的差，说明找到了符合条件的路径
            ans += cnt[s - targetSum]
            # 将当前路径和加入字典，为后续计算路径和做准备
            cnt[s] += 1
            # 递归处理左子树
            dfs(node.left, s)
            # 递归处理右子树
            dfs(node.right, s)
            # 回溯，移除当前路径和，避免影响其他分支的计算
            cnt[s] -= 1

        # 从根节点开始深度优先搜索
        dfs(root, 0)
        # 返回路径总数
        return ans
