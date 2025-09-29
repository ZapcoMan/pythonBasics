# -*- coding: utf-8 -*-
# @Time    : 01 1月 2025 9:42 上午
# @Author  : codervibe
# @File    : 二叉树中序遍历.py
# @Project : pythonBasics
"""
给定一个二叉树的根节点 root ，返回 它的 中序 遍历 。
"""

from typing import Optional, List


# 二叉树节点的定义。
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        """
        初始化二叉树节点。

        参数:
        val (int): 节点的值，默认为0。
        left (Optional[TreeNode]): 左子节点，默认为None。
        right (Optional[TreeNode]): 右子节点，默认为None。
        """
        self.val = val  # 节点的值
        self.left = left  # 左子节点
        self.right = right  # 右子节点


class Solution:
    # 方法一：递归遍历
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """
        使用递归实现二叉树的中序遍历。
        中序遍历的顺序是：左子树 -> 根节点 -> 右子树。

        参数:
        root (Optional[TreeNode]): 二叉树的根节点

        返回:
        List[int]: 中序遍历的结果列表
        """
        def dfs(root):
            """
            深度优先搜索函数，用于递归遍历二叉树。

            参数:
            root (Optional[TreeNode]): 当前遍历的节点

            返回:
            None: 该函数不返回任何值，通过非局部变量 ans 记录遍历结果
            """
            if root is None:
                return  # 如果当前节点为空，直接返回
            dfs(root.left)  # 递归遍历左子树
            nonlocal ans  # 使用外部函数的变量 ans
            ans.append(root.val)  # 访问根节点并将其值添加到结果列表中
            dfs(root.right)  # 递归遍历右子树

        ans = []  # 初始化结果列表
        dfs(root)  # 开始递归遍历
        return ans  # 返回结果列表

    # 方法二：栈实现非递归遍历
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """
        使用栈实现二叉树的中序遍历（非递归方式）。
        中序遍历的顺序是：左子树 -> 根节点 -> 右子树。
        使用栈来模拟递归调用的过程，先将左子节点依次入栈，直到左子节点为空，
        然后弹出栈顶元素并访问，再处理右子节点。

        参数:
        root (Optional[TreeNode]): 二叉树的根节点

        返回:
        List[int]: 中序遍历的结果列表
        """
        ans = []  # 初始化结果列表
        stk = []  # 初始化栈
        while root or stk:  # 当前节点不为空或栈不为空时继续循环
            if root:  # 如果当前节点不为空
                stk.append(root)  # 将当前节点压入栈
                root = root.left  # 移动到左子节点
            else:  # 如果当前节点为空
                root = stk.pop()  # 弹出栈顶元素
                ans.append(root.val)  # 访问该节点并将其值添加到结果列表中
                root = root.right  # 移动到右子节点
        return ans  # 返回结果列表

    # 方法三：Morris 遍历
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """
        使用 Morris 遍历实现二叉树的中序遍历。
        Morris 遍历是一种空间复杂度为 O(1) 的遍历方法，通过建立和断开临时链接来实现中序遍历。
        中序遍历的顺序是：左子树 -> 根节点 -> 右子树。

        参数:
        root (Optional[TreeNode]): 二叉树的根节点

        返回:
        List[int]: 中序遍历的结果列表
        """
        ans = []  # 初始化结果列表
        while root:  # 当前节点不为空时继续循环
            if root.left is None:  # 如果当前节点没有左子树
                ans.append(root.val)  # 直接访问当前节点并将其值添加到结果列表中
                root = root.right  # 移动到右子节点
            else:  # 如果当前节点有左子树
                prev = root.left  # 找到当前节点左子树的最右节点
                while prev.right and prev.right != root:  # 如果最右节点的右子节点不是当前节点
                    prev = prev.right  # 继续向右移动
                if prev.right is None:  # 如果最右节点的右子节点为空
                    prev.right = root  # 建立临时链接指向当前节点
                    root = root.left  # 移动到左子节点
                else:  # 如果最右节点的右子节点是当前节点
                    ans.append(root.val)  # 访问当前节点并将其值添加到结果列表中
                    prev.right = None  # 断开临时链接
                    root = root.right  # 移动到右子节点
        return ans  # 返回结果列表
