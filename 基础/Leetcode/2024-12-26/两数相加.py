# -*- coding: utf-8 -*-
# @Time    : 26 12月 2024 7:29 上午
# @Author  : codervibe
# @File    : 两数相加.py
# @Project : pythonBasics
"""
给你两个 非空 的链表，表示两个非负的整数。它们每位数字都是按照 逆序 的方式存储的，并且每个节点只能存储 一位 数字。
请你将两个数相加，并以相同形式返回一个表示和的链表。
你可以假设除了数字 0 之外，这两个数都不会以 0 开头。
"""
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    # l1 和 l2 为当前遍历的节点，carry 为进位
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode], carry=0) -> Optional[ListNode]:
        """
        递归地将两个链表 l1 和 l2 对应位置的节点值相加，并处理进位。

        参数:
        l1: 第一个链表的当前节点
        l2: 第二个链表的当前节点
        carry: 从低位进位的值，默认为0

        返回:
        返回相加后的链表的头节点
        """
        # 递归边界：l1 和 l2 都是空节点
        if l1 is None and l2 is None:
            # 如果进位了，就额外创建一个节点，否则返回None
            return ListNode(carry) if carry else None
        # 如果 l1 是空的，那么此时 l2 一定不是空节点
        if l1 is None:
            # 交换 l1 与 l2，保证 l1 非空，从而简化代码
            l1, l2 = l2, l1
        # 节点值和进位加在一起
        s = carry + l1.val + (l2.val if l2 else 0)
        # 每个节点保存一个数位（直接修改原链表）
        l1.val = s % 10
        # 递归处理下一对节点，并传递进位
        l1.next = self.addTwoNumbers(l1.next, l2.next if l2 else None, s // 10)
        # 返回相加后的链表的头节点
        return l1

