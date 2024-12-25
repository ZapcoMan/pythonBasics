# -*- coding: utf-8 -*-
# @Time    : 26 12月 2024 7:36 上午
# @Author  : codervibe
# @File    : 删除链表中倒数N个的节点.py
# @Project : pythonBasics
"""
给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。
"""
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        left = right = dummy = ListNode(next=head)
        for _ in range(n):
            right = right.next
        while right.next:
            left = left.next
            right = right.next
        left.next = left.next.next
        return dummy.next
