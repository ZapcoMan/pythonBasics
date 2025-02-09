# -*- coding: utf-8 -*-
# @Time    : 09 2月 2025 6:56 下午
# @Author  : codervibe
# @File    : 课程表.py
# @Project : pythonBasics
"""
你这个学期必须选修 numCourses 门课程，记为 0 到 numCourses - 1 。

在选修某些课程之前需要一些先修课程。 先修课程按数组 prerequisites 给出，其中 prerequisites[i] = [ai, bi] ，表示如果要学习课程 ai 则 必须 先学习课程  bi 。

例如，先修课程对 [0, 1] 表示：想要学习课程 0 ，你需要先完成课程 1 。
请你判断是否可能完成所有课程的学习？如果可以，返回 true ；否则，返回 false 。
"""
from collections import defaultdict, deque
from typing import List

class Solution:
    """
    解决课程表问题，判断是否可能完成所有课程的学习。
    使用Kahn算法进行拓扑排序，以判断课程安排图中是否存在环。

    属性:
    - numCourses: int, 课程总数
    - prerequisites: List[List[int]], 先修课程对列表

    返回:
    - bool, 是否可以完成所有课程的学习
    """

    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # 构建图的邻接表和入度数组
        g = defaultdict(list)
        indeg = [0] * numCourses

        # 遍历先修课程对，填充邻接表和入度数组
        for a, b in prerequisites:
            g[b].append(a)  # b是a的先修课程
            indeg[a] += 1  # a的入度加1

        # 初始化计数器和队列，队列中包含所有入度为0的课程
        cnt = 0
        q = deque(i for i, x in enumerate(indeg) if x == 0)

        # 使用Kahn算法进行拓扑排序
        while q:
            i = q.popleft()  # 从队列中取出一门课程
            cnt += 1  # 计数器加1，表示已完成一门课程
            # 遍历该课程的后续课程，减少它们的入度
            for j in g[i]:
                indeg[j] -= 1
                # 如果后续课程的入度变为0，则加入队列
                if indeg[j] == 0:
                    q.append(j)

        # 如果计数器的值等于课程总数，说明所有课程都可以完成
        return cnt == numCourses
