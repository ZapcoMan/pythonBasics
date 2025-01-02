# -*- coding: utf-8 -*-
# @Time    : 02 1月 2025 8:21 下午
# @Author  : codervibe
# @File    : 验证二叉搜索树.py
# @Project : pythonBasics
"""
给你一个二叉树的根节点 root ，判断其是否是一个有效的二叉搜索树。
有效 二叉搜索树定义如下：
节点的左子树只包含 小于 当前节点的数。
节点的右子树只包含 大于 当前节点的数。
所有左子树和右子树自身必须也是二叉搜索树。
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        return self.dg(root, -(2 ** 32), 2 ** 32)  #这里我直接粗暴地将最小值和最大值设置为一个足够小（大）的数，你可以设置你认为的最优解

    def dg(self, root, min_v, max_v):
        # 参数：root：当前节点，min_v：允许最小值（下界），max_v：允许最大值（上界）

        if root == None:  # 如果当前节点为空，证明已经递归到叶子节点，返回True
            return True

        if root.val < max_v and root.val > min_v:  # 如果当前节点值符合规定，继续进行之后的递归
            pass
        else:  # 如果不符合规定，之间返回 False
            return False

        if self.dg(root.left, min_v, root.val) == False:  # 对左子树进行递归，此时最大值应该为当前节点值
            return False
        if self.dg(root.right, root.val, max_v) == False:  # 对右子树进行递归，此时最小值应该为当前节点值
            return False

        return True  # 如果成功避开所有坑，恭喜，这个当前节点下的子树是一个二叉搜索树
