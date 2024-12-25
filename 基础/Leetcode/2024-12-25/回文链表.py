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


# 解决方案类，用于检测链表是否为回文。
class Solution:
    # 使用快慢指针和链表反转的方法检测回文。
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        # 初始化快慢指针。
        slow = fast = head
        # 使用快慢指针找到链表的中点。
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # 反转中点之后的链表。
        prev = None
        while slow:
            tmp = slow.next
            slow.next = prev
            prev = slow
            slow = tmp
        # 注意反转后 prev 为头结点
        # 比较前半部分和反转后的后半部分链表是否相同。
        while prev:  # Tips
            if prev.val != head.val:
                return False
            prev = prev.next
            head = head.next
        return True

    # 优化代码，使用列表存储链表值后判断是否回文。

    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        current_node = head
        res = []
        try:
            # 遍历链表，将值存入列表。
            while current_node is not None:
                res.append(current_node.val)
                current_node = current_node.next
        except AttributeError as e:
            print(f"AttributeError: {e}")
            return False
        # 检查列表是否对称。
        return res == res[::-1]



if __name__ == '__main__':
    # 实例化
    solution = Solution()
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(2)
    head.next.next.next = ListNode(1)
    print(solution.isPalindrome(head))
