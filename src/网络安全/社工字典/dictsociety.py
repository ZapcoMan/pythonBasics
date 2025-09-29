# -*- coding: utf-8 -*-
# @Time    : 18 1月 2025 11:34 下午
# @Author  : codervibe
# @File    : dictsociety.py
# @Project : pythonBasics
import itertools
import string
import logging
import os
import argparse

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_info_list(info_file="info.txt"):
    """
    读取个人信息文件info.txt，并提取所有个人信息字段
    :param info_file: 个人信息文件路径，默认为 "info.txt"
    :return: 包含所有个人信息字段的列表
    """
    info_list = []
    if not os.path.exists(info_file):
        logging.error(f"文件 {info_file} 不存在")
        return info_list

    try:
        with open(info_file, "r", encoding="utf-8") as info:
            lines = info.readlines()
            for line in lines:
                # 提取每行信息的字段值，并添加到列表中
                parts = line.strip().split(":")
                if len(parts) == 2:
                    info_list.append(parts[1])
                else:
                    logging.warning(f"格式错误的行: {line.strip()}")
    except Exception as e:
        logging.error(f"读取个人信息文件时发生错误: {e}")
    return info_list


def create_number_list():
    """
    生成所有可能的三位数字组合
    :return: 包含所有三位数字组合的列表
    """
    numbers_list = [''.join(p) for p in itertools.product(string.digits, repeat=3)]
    return numbers_list


def create_special_list():
    """
    生成所有特殊字符的列表
    :return: 包含所有特殊字符的列表
    """
    return list(string.punctuation)


def generate_password_combinations(infolist, specal_list, password_length):
    """
    生成密码的所有可能组合
    :param infolist: 个人信息列表
    :param specal_list: 特殊字符列表
    :param password_length: 密码长度
    :return: 包含所有可能密码组合的集合
    """
    combinations = set()

    for a in infolist:
        if len(a) >= password_length:
            combinations.add(a)
        else:
            need_words = password_length - len(a)
            for b in itertools.permutations(string.digits, need_words):
                combinations.add(a + ''.join(b))

    for a in infolist:
        for c in infolist:
            combined = a + c
            if len(combined) >= password_length:
                combinations.add(combined)

    for a in infolist:
        for d in infolist:
            for e in specal_list:
                combined1 = a + d + e
                combined2 = e + d + a
                combined3 = a + e + d
                if len(combined1) >= password_length:
                    combinations.add(combined1)
                if len(combined2) >= password_length:
                    combinations.add(combined2)
                if len(combined3) >= password_length:
                    combinations.add(combined3)

    return combinations


def combination(dict_file="dict.txt", info_file="info.txt", password_length=4):
    """
    生成密码的所有可能组合，并将它们写入文件
    :param dict_file: 密码字典文件路径，默认为 "dict.txt"
    :param info_file: 个人信息文件路径，默认为 "info.txt"
    :param password_length: 密码长度，默认为 4
    """
    infolist = read_info_list(info_file)
    specal_list = create_special_list()

    if not infolist:
        logging.warning("个人信息列表为空，无法生成密码组合")
        return

    combinations = generate_password_combinations(infolist, specal_list, password_length)

    with open(dict_file, "w", encoding="utf-8") as df:
        for password in combinations:
            df.write(password + '\n')

    logging.info(f"生成的密码组合已写入文件 {dict_file}")


# 设置命令行参数解析
parser = argparse.ArgumentParser(description="生成密码字典")
parser.add_argument("--dict_file", type=str, default="dict.txt", help="密码字典文件路径，默认为 dict.txt")
parser.add_argument("--info_file", type=str, default="info.txt", help="个人信息文件路径，默认为 info.txt")
parser.add_argument("--password_length", type=int, default=4, help="密码长度，默认为 4")

args = parser.parse_args()

# 执行密码生成函数
combination(dict_file=args.dict_file, info_file=args.info_file, password_length=args.password_length)
# 也可以选择执行read_info_list()来仅读取和打印个人信息
print(read_info_list())
