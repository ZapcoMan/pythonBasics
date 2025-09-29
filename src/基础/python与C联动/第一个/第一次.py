# -*- coding: utf-8 -*-
# @Time    : 17 2月 2025 9:54 上午
# @Author  : codervibe
# @File    : 第一次.py
# @Project : pythonBasics
from ctypes import cdll
c_function = cdll.LoadLibrary("./py_test_libc.so")
main_function = cdll.LoadLibrary("./main.so")

res = c_function.py_test(123)
main_function.main()

print(res)

