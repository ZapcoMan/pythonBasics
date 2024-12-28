# -*- coding: utf-8 -*-
# @Time    : 28 12月 2024 8:42 上午
# @Author  : codervibe
# @File    : 图片隐写术信息检测提取.py
# @Project : pythonBasics

from PIL import Image
from PIL.ExifTags import TAGS
from stegano import lsb


def get_exif_data(image_path):
    with Image.open(image_path) as img:
        exif_data = img._getexif()
        if exif_data:
            exif = {TAGS.get(tag): value for tag, value in exif_data.items()}
            return exif
        else:
            return None


def check_hidden_message(image_path):
    secret_message = lsb.reveal(image_path)
    if secret_message:
        print("Hidden message found:", secret_message)
    else:
        print("No hidden message found.")


def analyze_binary_data(image_path):
    with open(image_path, 'rb') as file:
        binary_data = file.read()

    # 打印前100个字节的十六进制表示
    print("First 100 bytes in hexadecimal:")
    print(binary_data[:100].hex())


# 打开图片文件并读取二进制数据
image_path = './img/0c4870b556898d046c170e15345ac1fd3546576408546044.jpg'

# 检查 EXIF 数据
print("Checking EXIF data...")
exif = get_exif_data(image_path)
if exif:
    print("EXIF Data:")
    for key, value in exif.items():
        print(f"{key}: {value}")
else:
    print("No EXIF data found.")

# 检测隐藏信息
print("\nChecking for hidden messages using stegano...")
check_hidden_message(image_path)

# 分析二进制数据
print("\nAnalyzing binary data...")
analyze_binary_data(image_path)
