# -*- coding: utf-8 -*-
# @Time    : 27 12月 2024 3:07 下午
# @Author  : codervibe
# @File    : 排序链表.py
# @Project : pythonBasics
"""
给你链表的头结点 head ，请将其按 升序 排列并返回 排序后的链表。
"""


# 单链表的定义。
class ListNode:
    def __init__(self, val=0, next=None):
        """
        初始化单链表节点。

        参数:
        val (int): 节点的值，默认为0。
        next (ListNode): 下一个节点，默认为None。
        """
        self.val = val
        self.next = next


class Solution:
    def sortList(self, head: ListNode) -> ListNode:
        """
        使用归并排序对链表进行升序排序。

        参数:
        head (ListNode): 链表的头节点。

        返回:
        ListNode: 排序后链表的头节点。
        """
        # 如果链表为空或只有一个节点，直接返回链表（已排序）
        if not head or not head.next:
            return head

        # 使用快慢指针找到链表的中间节点，并将链表从中点分割成两部分
        slow, fast = head, head.next
        while fast and fast.next:
            fast, slow = fast.next.next, slow.next
        mid, slow.next = slow.next, None  # 保存中点并切断链表

        # 递归地对左右两部分链表进行排序
        left, right = self.sortList(head), self.sortList(mid)

        # 合并两个有序链表
        h = res = ListNode(0)
        while left and right:
            if left.val < right.val:
                h.next, left = left, left.next
            else:
                h.next, right = right, right.next
            h = h.next
        h.next = left if left else right

        return res.next


def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
    """
    对链表进行升序排序。

    将链表转换为节点列表，根据节点的值对列表进行排序，然后重新连接节点以形成排序后的链表。

    参数:
    head (Optional[ListNode]): 需要排序的链表的头节点。

    返回:
    Optional[ListNode]: 返回排序后链表的新头节点。如果输入链表为空，则返回 None。
    """

    # 将链表节点逐个拆解并存入列表中
    cur = head
    nodeList = []
    while cur:
        tmp = cur.next
        cur.next = None
        nodeList.append(cur)
        cur = tmp

    # 对节点列表按照节点值进行排序
    nodeList.sort(key=lambda x: x.val)

    # 重新连接排序后的节点
    for i in range(len(nodeList) - 1):
        nodeList[i].next = nodeList[i + 1]

    # 返回排序后链表的新头节点，如果原链表为空则返回 None
    return nodeList[0] if head else None
