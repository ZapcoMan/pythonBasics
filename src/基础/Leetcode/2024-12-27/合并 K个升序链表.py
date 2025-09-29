# -*- coding: utf-8 -*-
# @Time    : 27 12月 2024 3:22 下午
# @Author  : codervibe
# @File    : 合并 K个升序链表.py
# @Project : pythonBasics
"""
给你一个链表数组，每个链表都已经按升序排列。
请你将所有链表合并到一个升序链表中，返回合并后的链表。
"""
from typing import Optional, List


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        """
        合并两个有序链表。

        参数:
        list1: 第一个有序链表。
        list2: 第二个有序链表。

        返回:
        合并后的有序链表。
        """
        cur = dummy = ListNode()  # 用哨兵节点简化代码逻辑
        while list1 and list2:
            if list1.val < list2.val:
                cur.next = list1  # 把 list1 加到新链表中
                list1 = list1.next
            else:  # 注：相等的情况加哪个节点都是可以的
                cur.next = list2  # 把 list2 加到新链表中
                list2 = list2.next
            cur = cur.next
        cur.next = list1 if list1 else list2  # 拼接剩余链表
        return dummy.next

    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        合并K个有序链表。

        参数:
        lists: 包含K个有序链表的列表。

        返回:
        合并后的有序链表。
        """
        m = len(lists)
        if m == 0: return None  # 注意输入的 lists 可能是空的
        if m == 1: return lists[0]  # 无需合并，直接返回
        left = self.mergeKLists(lists[:m // 2])  # 合并左半部分
        right = self.mergeKLists(lists[m // 2:])  # 合并右半部分
        return self.mergeTwoLists(left, right)  # 最后把左半和右半合并
