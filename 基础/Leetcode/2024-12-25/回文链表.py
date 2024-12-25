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


# 单链表的定义。
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next



class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        prev = None
        while slow:
            tmp = slow.next
            slow.next = prev
            prev = slow
            slow = tmp
        # 注意反转后 prev 为头结点
        while prev:  # Tips
            if prev.val != head.val:
                return False
            prev = prev.next
            head = head.next
        return True

from typing import Optional

from functorch.dim import stack


# 单链表的定义。
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next




    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        prev = None
        while slow:
            tmp = slow.next
            slow.next = prev
            prev = slow
            slow = tmp
        # 注意反转后 prev 为头结点
        while prev:  # Tips
            if prev.val != head.val:
                return False
            prev = prev.next
            head = head.next
        return True
