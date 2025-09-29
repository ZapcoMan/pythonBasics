# -*- coding: utf-8 -*-
# @Time    : 10 2月 2025 10:59 下午
# @Author  : codervibe
# @File    : 猫和老鼠.py
# @Project : pythonBasics
"""
两位玩家分别扮演猫和老鼠，在一张 无向 图上进行游戏，两人轮流行动。

图的形式是：graph[a] 是一个列表，由满足 ab 是图中的一条边的所有节点 b 组成。

老鼠从节点 1 开始，第一个出发；猫从节点 2 开始，第二个出发。在节点 0 处有一个洞。

在每个玩家的行动中，他们 必须 沿着图中与所在当前位置连通的一条边移动。例如，如果老鼠在节点 1 ，那么它必须移动到 graph[1] 中的任一节点。

此外，猫无法移动到洞中（节点 0）。

然后，游戏在出现以下三种情形之一时结束：

如果猫和老鼠出现在同一个节点，猫获胜。
如果老鼠到达洞中，老鼠获胜。
如果某一位置重复出现（即，玩家的位置和移动顺序都与上一次行动相同），游戏平局。
给你一张图 graph ，并假设两位玩家都都以最佳状态参与游戏：

如果老鼠获胜，则返回 1；
如果猫获胜，则返回 2；
如果平局，则返回 0 。
"""
# 定义游戏中的洞、老鼠起始位置、猫起始位置
HOLE, MOUSE_START, CAT_START = 0, 1, 2
# 定义老鼠回合和猫回合
MOUSE_TURN, CAT_TURN = 0, 1
# 定义老鼠胜利、猫胜利和平局的结果
MOUSE_WIN, CAT_WIN, TIE = 1, 2, 0


class Solution:
    def catMouseGame(self, graph: List[List[int]]) -> int:
        """
        解决猫和老鼠游戏的问题，判断最终胜利者。

        :param graph: 游戏地图，由节点和其相邻节点列表组成
        :return: 返回游戏结果，1代表老鼠胜利，2代表猫胜利，0代表平局
        """
        def get_prev_states(state):
            """
            获取当前状态的前一个状态。

            :param state: 当前状态，包括老鼠位置、猫位置和当前回合
            :return: 返回前一个状态的列表
            """
            m, c, t = state
            pt = t ^ 1  # 上一个回合
            pre = []
            if pt == CAT_TURN:
                # 如果是猫回合，遍历猫的前一个可能位置
                for pc in graph[c]:
                    if pc != HOLE:
                        pre.append((m, pc, pt))
            else:
                # 如果是老鼠回合，遍历老鼠的前一个可能位置
                for pm in graph[m]:
                    pre.append((pm, c, pt))
            return pre

        n = len(graph)
        # 初始化游戏结果数组
        ans = [[[0, 0] for _ in range(n)] for _ in range(n)]
        # 初始化每个状态的度数
        degree = [[[0, 0] for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(1, n):
                degree[i][j][MOUSE_TURN] = len(graph[i])
                degree[i][j][CAT_TURN] = len(graph[j])
            for j in graph[HOLE]:
                degree[i][j][CAT_TURN] -= 1
        # 初始化队列，用于广度优先搜索
        q = deque()
        # 初始化已知结果的状态
        for j in range(1, n):
            ans[0][j][MOUSE_TURN] = ans[0][j][CAT_TURN] = MOUSE_WIN
            q.append((0, j, MOUSE_TURN))
            q.append((0, j, CAT_TURN))
        for i in range(1, n):
            ans[i][i][MOUSE_TURN] = ans[i][i][CAT_TURN] = CAT_WIN
            q.append((i, i, MOUSE_TURN))
            q.append((i, i, CAT_TURN))
        # 广度优先搜索，更新所有状态的结果
        while q:
            state = q.popleft()
            t = ans[state[0]][state[1]][state[2]]
            for prev_state in get_prev_states(state):
                pm, pc, pt = prev_state
                if ans[pm][pc][pt] == TIE:
                    win = (t == MOUSE_WIN and pt == MOUSE_TURN) or (
                            t == CAT_WIN and pt == CAT_TURN
                    )
                    if win:
                        ans[pm][pc][pt] = t
                        q.append(prev_state)
                    else:
                        degree[pm][pc][pt] -= 1
                        if degree[pm][pc][pt] == 0:
                            ans[pm][pc][pt] = t
                            q.append(prev_state)
        # 返回老鼠和猫起始位置的结果
        return ans[MOUSE_START][CAT_START][MOUSE_TURN]
