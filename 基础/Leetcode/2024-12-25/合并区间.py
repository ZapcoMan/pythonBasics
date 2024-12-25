# -*- coding: utf-8 -*-
# @Time    : 25 12月 2024 7:21 下午
# @Author  : codervibe
# @File    : 合并区间.py
# @Project : pythonBasics
"""
以数组 intervals 表示若干个区间的集合，其中单个区间为 intervals[i] = [starti, endi] 。
请你合并所有重叠的区间，并返回 一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间 。

"""
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        合并所有重叠的区间，并返回一个不重叠的区间数组。

        参数:
        intervals: List[List[int]] - 一个二维列表，其中每个子列表代表一个区间的左右端点。

        返回值:
        List[List[int]] - 合并重叠区间后，返回的不重叠区间列表。
        """
        # 按照区间的左端点进行排序，以便后续合并处理
        intervals.sort(key=lambda p: p[0])
        ans = []
        for p in intervals:
            # 判断当前区间是否与上一个区间重叠
            if ans and p[0] <= ans[-1][1]:
                # 如果重叠，更新最后一个区间的右端点为两个区间右端点的最大值
                ans[-1][1] = max(ans[-1][1], p[1])
            else:
                # 如果不重叠，将当前区间作为新的合并区间加入结果列表
                ans.append(p)
        return ans

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        合并所有重叠的区间，并返回一个不重叠的区间数组。

        参数:
        intervals: List[List[int]] - 一个二维列表，其中每个子列表代表一个区间的左右端点。

        返回值:
        List[List[int]] - 合并重叠区间后，返回的不重叠区间列表。
        """
        # 按照区间的左端点进行排序，以便后续合并处理
        intervals.sort(key=lambda x: x[0])
        merge = []

        for interval in intervals:
            # 判断当前区间是否与上一个区间重叠
            if not merge or merge[-1][1] < interval[0]:
                # 如果不重叠，将当前区间加入合并列表
                merge.append(interval)
            else:
                # 如果重叠，更新最后一个区间的右端点为两个区间右端点的最大值
                merge[-1][1] = max(merge[-1][1], interval[1])
        return merge
