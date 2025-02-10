# -*- coding: utf-8 -*-
# @Time    : 10 2月 2025 11:17 下午
# @Author  : codervibe
# @File    : 每日温度.py
# @Project : pythonBasics
"""
给定一个整数数组 temperatures ，表示每天的温度，返回一个数组 answer ，其中 answer[i] 是指对于第 i 天，下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 0 来代替。
"""
from typing import List
from collections import deque


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        # 初始化结果数组，长度与输入温度数组相同，初始值全为0
        answer = [0] * len(temperatures)
        # 初始化一个单调栈，用于存储未找到更高温度的索引
        st = deque()

        # 遍历温度数组，i为索引，t为对应的温度
        for i, t in enumerate(temperatures):
            # 当栈不为空且栈顶索引对应的温度小于当前温度t时，执行循环
            while st and temperatures[st[-1]] < t:
                # 弹出栈顶索引
                j = st.pop()
                # 计算当前索引与弹出索引的差值，即找到更高温度的天数间隔
                answer[j] = i - j
            # 将当前索引入栈
            st.append(i)
        # 返回结果数组
        return answer
