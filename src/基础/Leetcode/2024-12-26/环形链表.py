# -*- coding: utf-8 -*-
# @Time    : 26 12月 2024 5:55 上午
# @Author  : codervibe
# @File    : 环形链表.py
# @Project : pythonBasics
"""
给你一个链表的头节点 head ，判断链表中是否有环。
如果链表中有某个节点，可以通过连续跟踪 next 指针再次到达，则链表中存在环。
为了表示给定链表中的环，评测系统内部使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）
。注意：pos 不作为参数进行传递 。仅仅是为了标识链表的实际情况。
如果链表中存在环 ，则返回 true 。 否则，返回 false 。
"""
from typing import Optional

# 定义单链表节点类
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

# 定义解决方案类
class Solution:
    # 检测链表中是否有环
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        # 初始化慢指针和快指针都指向链表头
        slow = fast = head
        # 当快指针及其下一个节点存在时，执行循环
        while fast and fast.next:
            # 慢指针向前移动一步
            slow = slow.next
            # 快指针向前移动两步
            fast = fast.next.next
            # 如果快慢指针相遇，说明链表中有环
            if slow == fast:
                return True
        # 如果快指针到达链表尾部，说明链表中无环
        return False

    # 重复定义检测链表中是否有环的方法，实现在功能上与上一个方法相同
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        # 初始化慢指针和快指针都指向链表头
        slow, fast = head, head
        # 当快指针及其下一个节点存在时，执行循环
        while fast and fast.next:
            # 慢指针向前移动一步
            slow = slow.next
            # 快指针向前移动两步
            fast = fast.next.next
            # 如果快慢指针相遇，说明链表中有环
            if slow == fast:
                return True
        # 如果快指针到达链表尾部，说明链表中无环
        return False
