# -*- coding: utf-8 -*-
# @Time    : 28 12月 2024 8:42 上午
# @Author  : codervibe
# @File    : 图片隐写术信息检测提取.py
# @Project : pythonBasics

from PIL import Image
from PIL.ExifTags import TAGS
from stegano import lsb


def get_exif_data(image_path):
    """
    获取图片的EXIF数据
    :param image_path: 图片路径
    :return: EXIF数据字典或None
    """
    with Image.open(image_path) as img:
        exif_data = img._getexif()
        if exif_data:
            exif = {TAGS.get(tag): value for tag, value in exif_data.items()}
            return exif
        else:
            return None


def check_hidden_message(image_path):
    """
    检查图片中隐藏的消息
    :param image_path: 图片路径
    """
    try:
        secret_message = lsb.reveal(image_path)
        print("发现隐藏消息:", secret_message)
    except IndexError as e:
        print(f"Error: {e}. No hidden message detected.")


def analyze_binary_data(image_path):
    """
    分析图片的二进制数据
    :param image_path: 图片路径
    """
    with open(image_path, 'rb') as file:
        binary_data = file.read()

    # 打印前100个字节的十六进制表示
    print("前100个字节的十六进制表示:")
    print(binary_data[:100].hex())


# 图片路径
image_path = 'img/黑客海报.jpg'  # 替换为你的图片路径

# 检查EXIF数据
print("正在检查EXIF数据...")
exif = get_exif_data(image_path)
if exif:
    print("EXIF数据:")
    for key, value in exif.items():
        print(f"{key}: {value}")
else:
    print("未发现EXIF数据。")

# 使用stegano检查隐藏消息
print("\n正在使用stegano检查隐藏消息...")
check_hidden_message(image_path)

# 分析二进制数据
print("\n正在分析二进制数据...")
analyze_binary_data(image_path)
