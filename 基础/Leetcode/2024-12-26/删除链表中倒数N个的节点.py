# -*- coding: utf-8 -*-
# @Time    : 26 12月 2024 7:36 上午
# @Author  : codervibe
# @File    : 删除链表中倒数N个的节点.py
# @Project : pythonBasics
"""
给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。
"""
from typing import Optional

# 定义链表节点类
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 定义解决方案类
class Solution:
    # 从链表的倒数第n个节点开始删除
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # 初始化两个指针，left和right，dummy是一个虚拟节点，简化边界情况处理
        left = right = dummy = ListNode(next=head)
        # right指针向前移动n步，目的是使left和right之间保持n的距离
        for _ in range(n):
            right = right.next
        # 移动left和right，直到right到达链表末尾，此时left指向倒数第n个节点的前一个节点
        while right.next:
            left = left.next
            right = right.next
        # 跳过le
