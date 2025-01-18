# -*- coding: utf-8 -*-
# @Time    : 18 1月 2025 11:34 下午
# @Author  : codervibe
# @File    : dictsociety.py
# @Project : pythonBasics
import itertools
import string

dictFile = open("dict.txt", "w", encoding="utf-8")

def ReadInfoList():
    infoList = []
    try:
        info = open("info.txt", "r", encoding="utf-8")
        lines = info.readlines()
        for line in lines:
            infoList.append(line.strip().split(":")[1])
        info.close()
    except Exception as e:
        print(e)
    return infoList


def createNumberList():
    numbersList = []
    words = string.digits
    itertoolsNumberList = itertools.product(words, repeat=3)
    for number in itertoolsNumberList:
        numbersList.append("".join(number))
    return numbersList


def creatSpecalList():
    specalList = []
    specalWords = string.punctuation
    for i in specalWords:
        specalList.append("".join(i))
    return specalList


def Combination():
    password_length = 4
    infolist = ReadInfoList()
    infolen = len(infolist)
    specal_list = creatSpecalList()
    for a in range(infolen):
        # 把个人信息大于八位的输出到文件
        if len(infolist[a]) >= password_length:
            print(infolist[a])
        else:
            needWords = password_length - len(infolist[a])
            for b in itertools.permutations(string.digits, needWords):
                dictFile.write(infolist[a] + "".join(b) + '\n')
        for c in range(0, infolen):
            if len(infolist[a] + infolist[c]) >= password_length:
                dictFile.write(infolist[a] + infolist[c] + '\n')
        for d in range(0, infolen):
            for e in range(0, len(specal_list)):
                if len(infolist[a] + infolist[d] + specal_list[e]) >= password_length:
                    # 特殊字符加尾部 加中间 加前面
                    dictFile.write(infolist[a] + infolist[d] + specal_list[e] + '\n')
                    dictFile.write(specal_list[e] + infolist[d] + infolist[a] + '\n')
                    dictFile.write(infolist[a] + specal_list[e] + infolist[d] + '\n')



if __name__ == '__main__':
    Combination()
    # ReadInfoList()
