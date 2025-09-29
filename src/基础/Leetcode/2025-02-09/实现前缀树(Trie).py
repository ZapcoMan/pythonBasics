# -*- coding: utf-8 -*-
# @Time    : 09 2月 2025 7:01 下午
# @Author  : codervibe
# @File    : 实现前缀树(Trie).py
# @Project : pythonBasics
"""
Trie（发音类似 "try"）或者说 前缀树 是一种树形数据结构，用于高效地存储和检索字符串数据集中的键。这一数据结构有相当多的应用情景，例如自动补全和拼写检查。

请你实现 Trie 类：

Trie() 初始化前缀树对象。
void insert(String word) 向前缀树中插入字符串 word 。
boolean search(String word) 如果字符串 word 在前缀树中，返回 true（即，在检索之前已经插入）；否则，返回 false 。
boolean startsWith(String prefix) 如果之前已经插入的字符串 word 的前缀之一为 prefix ，返回 true ；否则，返回 false 。

"""
class Trie:
    """
    Trie类初始化方法。
    """
    def __init__(self):
        self.root = {}

    """
    向前缀树中插入一个单词。
    
    参数:
    word: 需要插入的单词。
    """
    def insert(self, word: str) -> None:
        cur = self.root
        for c in word:
            if c not in cur:
                cur[c] = {}
            cur = cur[c]
        cur["isEnd"] = True  # value can be anything

    """
    在前缀树中搜索一个单词。
    
    参数:
    word: 需要搜索的单词。
    
    返回:
    如果单词存在于前缀树中，则返回True；否则返回False。
    """
    def search(self, word: str) -> bool:
        cur = self.root
        for c in word:
            if c not in cur:
                return False
            cur = cur[c]
        return "isEnd" in cur

    """
    检查前缀树中是否存在以给定前缀开头的单词。
    
    参数:
    prefix: 需要检查的前缀。
    
    返回:
    如果前缀树中存在以给定前缀开头的单词，则返回True；否则返回False。
    """
    def startsWith(self, prefix: str) -> bool:
        cur = self.root
        for c in prefix:
            if c not in cur:
                return False
            cur = cur[c]
        return True


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
