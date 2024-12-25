# -*- coding: utf-8 -*-
# @Time    : 26 12月 2024 7:48 上午
# @Author  : codervibe
# @File    : 两两交换链表中的节点.py
# @Project : pythonBasics
"""
给你一个链表，两两交换其中相邻的节点，并返回交换后链表的头节点。你必须在不修改节点内部的值的情况下完成本题（即，只能进行节点交换）。
"""
from typing import Optional


class ListNode:
    """链表节点类"""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    """解决方案类"""
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        两两交换链表中的节点。

        不修改节点值，只通过改变节点间的指针来完成交换。

        参数:
        head: Optional[ListNode] - 输入链表的头节点。

        返回:
        Optional[ListNode] - 交换后链表的头节点。
        """
        # 使用哨兵节点简化边界处理
        node0 = dummy = ListNode(next=head)
        node1 = head
        # 遍历链表，两两交换节点
        while node1 and node1.next:
            # 定义当前节点的下一个节点
            node2 = node1.next
            # 保存下一个节点的下一个节点
            node3 = node2.next

            # 交换节点
            node0.next = node2  # 0 -> 2
            node2.next = node1  # 2 -> 1
            node1.next = node3  # 1 -> 3

            # 更新指针，为下一次交换做准备
            node0 = node1  # 下一轮交换，0 是 1
            node1 = node3  # 下一轮交换，1 是 3
        # 返回新链表的头节点
        return dummy.next
