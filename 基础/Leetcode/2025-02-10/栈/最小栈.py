# -*- coding: utf-8 -*-
# @Time    : 10 2月 2025 11:08 下午
# @Author  : codervibe
# @File    : 最小栈.py
# @Project : pythonBasics
"""
设计一个支持 push ，pop ，top 操作，并能在常数时间内检索到最小元素的栈。

实现 MinStack 类:

MinStack() 初始化堆栈对象。
void push(int val) 将元素val推入堆栈。
void pop() 删除堆栈顶部的元素。
int top() 获取堆栈顶部的元素。
int getMin() 获取堆栈中的最小元素。
"""
class MinStack:
    def __init__(self):
        """
        初始化MinStack对象。
        """
        self.stack = []  # 主栈，用于存储所有元素
        self.min_stack = []  # 辅助栈，用于存储最小元素

    def push(self, x: int) -> None:
        """
        将元素x推入主栈。
        如果辅助栈为空或x小于等于辅助栈顶元素，也将x推入辅助栈。

        参数:
        x (int): 要推入栈的元素值。
        """
        self.stack.append(x)
        if not self.min_stack or x <= self.min_stack[-1]:
            self.min_stack.append(x)

    def pop(self) -> None:
        """
        删除主栈顶部的元素。
        如果删除的元素是最小元素，则也从辅助栈中删除。
        """
        if self.stack.pop() == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        """
        获取主栈顶部的元素。

        返回:
        int: 主栈顶部的元素值。
        """
        return self.stack[-1]

    def getMin(self) -> int:
        """
        获取主栈中的最小元素。

        返回:
        int: 主栈中的最小元素值。
        """
        return self.min_stack[-1]
