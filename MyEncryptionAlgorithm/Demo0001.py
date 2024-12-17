# 设计一个属于自己的 加密算法只有我自己能解开
import base64
from typing import List


def firstLayerEncryption(text):
    # 创建一个数组用于 接收 text 转换为十六进制 的结果
    result: list[str] = []
    # 将 text 以字符分割 并将每个 字符 转换为 十六进制
    for i in text:
        result.append(hex(ord(i)))
    print(result)
    for i in result:
        # 输出此时 i 的类型
        print(type(i))
        # 将 i 转换成bytes类型的对象
        i = i.encode('utf-8')
        i = bytes(i)
        result.append(base64.b64encode(i))
    print(result)


def secondLayerEncryption(text):


    print(result)







if __name__ == '__main__':
    # 输入要加密的字符
    text = input('请输入要加密的字符:')
    result = firstLayerEncryption(text)
    secondLayerEncryption(result)
