# -*- coding: utf-8 -*-
# @Time    : 27 12月 2024 3:22 下午
# @Author  : codervibe
# @File    : 合并 K个升序链表.py
# @Project : pythonBasics
"""
给你一个链表数组，每个链表都已经按升序排列。
请你将所有链表合并到一个升序链表中，返回合并后的链表。
"""
from heapq import heapify, heappop, heappush
from typing import Optional, List


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        合并K个升序链表为一个升序链表。

        参数:
        lists: List[Optional[ListNode]] - 一个包含多个升序链表的列表

        返回:
        Optional[ListNode] - 合并后的升序链表的头节点
        """
        cur = dummy = ListNode()  # 哨兵节点，作为合并后链表头节点的前一个节点
        h = [head for head in lists if head]  # 初始把所有链表的头节点入堆
        heapify(h)  # 堆化
        while h:  # 循环直到堆为空
            node = heappop(h)  # 剩余节点中的最小节点
            if node.next:  # 下一个节点不为空
                heappush(h, node.next)  # 下一个节点有可能是最小节点，入堆
            cur.next = node  # 合并到新链表中
            cur = cur.next  # 准备合并下一个节点
        return dummy.next  # 哨兵节点的下一个节点就是新链表的头节点


