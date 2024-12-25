# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 8:54 下午
# @Author  : codervibe
# @File    : 回文链表.py
# @Project : pythonBasics
"""
给你一个单链表的头节点 head ，请你判断该链表是否为
回文链表
。如果是，返回 true ；否则，返回 false
"""
from typing import Optional

from functorch.dim import stack


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        # 给你一个单链表的头节点 head ，请你判断该链表是否为
        # 回文链表
        if not head:
            return True
        while head:
            if head.val != stack.pop():
                return False
            head = head.next
            return True

        def reverseList(head: ListNode) -> ListNode:
            pre = None
            cur = head
            while cur:
                tmp = cur.next
                cur.next = pre
                pre = cur
                cur = tmp
            return pre

        while head:
            if head.val != stack.pop():
                return False
            head = head.next
            return True
