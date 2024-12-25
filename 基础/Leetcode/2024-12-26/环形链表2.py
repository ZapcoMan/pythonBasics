# -*- coding: utf-8 -*-
# @Time    : 26 12月 2024 6:04 上午
# @Author  : codervibe
# @File    : 环形链表2.py
# @Project : pythonBasics
"""
给定一个链表的头节点  head ，返回链表开始入环的第一个节点。 如果链表无环，则返回 null。
如果链表中有某个节点，可以通过连续跟踪 next 指针再次到达，则链表中存在环。
为了表示给定链表中的环，评测系统内部使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。
如果 pos 是 -1，则在该链表中没有环。注意：pos 不作为参数进行传递，仅仅是为了标识链表的实际情况
不允许修改 链表。
"""
from typing import Optional

# 定义链表节点类
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

# 解决链表中环检测问题的解决方案类
class Solution:
    # 检测链表中环的起始节点
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 初始化快慢指针，都指向链表头部
        fast = slow = head
        # 遍历链表，寻找快慢指针相遇的节点
        while True:
            # 如果快指针到达链表末尾，则无环，返回None
            if not (fast and fast.next): return
            # 快指针每次移动两步，慢指针每次移动一步
            fast, slow = fast.next.next, slow.next
            # 如果快慢指针相遇，则表示有环，跳出循环
            if fast == slow: break
        # 重新将快指针指向链表头部
        fast = head
        # 快慢指针再次同时移动，每次一步，直到相遇
        while fast != slow:
            fast, slow = fast.next, slow.next
        # 相遇的节点即为环的起始节点
        return fast

    # 另一种实现方式检测链表中的环
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 初始化快慢指针，指向链表头部
        slow = head
        fast = head
        # 遍历链表，寻找环
        while fast:
            # 慢指针移动一步
            slow = slow.next
            # 如果快指针到达链表末尾，则无环，返回None
            if not fast.next:
                return None
            else:
                # 快指针移动两步
                fast = fast.next.next
            # 如果快慢指针相遇，则表示有环
            if fast == slow:
                # 初始化一个新的指针，指向链表头部
                new = head
                # 新指针和慢指针同时移动，直到相遇
                while new != slow:
                    new = new.next
                    slow = slow.next
                # 相遇的节点即为环的起始节点
                return new
