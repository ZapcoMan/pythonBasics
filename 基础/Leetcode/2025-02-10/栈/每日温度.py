# -*- coding: utf-8 -*-
# @Time    : 10 2月 2025 11:17 下午
# @Author  : codervibe
# @File    : 每日温度.py
# @Project : pythonBasics
"""
给定一个整数数组 temperatures ，表示每天的温度，返回一个数组 answer ，其中 answer[i] 是指对于第 i 天，下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 0 来代替。
"""
from collections import deque


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        answer = [0] * len(temperatures)
        st = deque()    # 单调栈，栈底到栈顶依次递减，存储未找到结果的索引

        for i, t in enumerate(temperatures):
            # 将栈内索引j对应的温度小于当前温度t的索引都弹出，t就是它们的下一个更高温度
            while st and temperatures[st[-1]] < t:
                j = st.pop()
                answer[j] = i - j   # 间隔的天数等于下标差
            st.append(i)            # 将当前索引入栈
        return answer
