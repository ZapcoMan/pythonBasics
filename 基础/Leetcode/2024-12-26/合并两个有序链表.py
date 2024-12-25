# -*- coding: utf-8 -*-
# @Time    : 26 12月 2024 6:13 上午
# @Author  : codervibe
# @File    : 合并两个有序链表.py
# @Project : pythonBasics
"""
将两个升序链表合并为一个新的 升序 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。
"""
from typing import Optional


# 定义单链表的节点结构
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val  # 节点的值
        self.next = next  # 指向下一个节点的指针

# 定义解决方案类，用于合并两个有序链表
class Solution:
    # 合并两个有序链表的主要函数
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # 如果list1为空，则直接返回list2
        if not list1: return list2  # 终止条件，直到两个链表都空
        # 如果list2为空，则直接返回list1
        if not list2: return list1
        # 如果list1的值小于等于list2的值，将list1的下一个节点设为剩余节点的合并结果
        if list1.val <= list2.val:  # 递归调用
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        # 如果list2的值小于list1的值，将list2的下一个节点设为剩余节点的合并结果
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2
