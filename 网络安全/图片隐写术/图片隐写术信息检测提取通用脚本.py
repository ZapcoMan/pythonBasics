# -*- coding: utf-8 -*-
# @Time    : 29 12月 2024 9:46 上午
# @Author  : codervibe
# @File    : 图片隐写术信息检测提取通用脚本.py
# @Project : pythonBasics
import os


def get_file_type_by_hex(file_path):
    """
    根据文件的十六进制开头判断文件类型，并检查文件结尾后面是否有多余的文件十六进制开头或文本。
    如果有多余的信息，尝试判断这些信息是否是一个文件，并根据多余信息的十六进制开头另存为另一个文件并设置成对应的扩展名。
    如果多余的信息不是文件，则将其打印出来。

    参数:
    file_path (str): 文件的路径。

    返回:
    str: 文件类型描述，如果无法识别则返回 "未知"。
    """
    # 常见文件类型的魔数和结尾
    magic_numbers = {
        b'\x89PNG\r\n\x1a\n': ('PNG', b'IEND\xaeB`\x82'),
        b'\xff\xd8\xff': ('JPEG', b'\xff\xd9'),
        b'GIF87a': ('GIF', b'\x3b'),
        b'GIF89a': ('GIF', b'\x3b'),
        b'\x42\x4d': ('BMP', None),
        b'\x25\x50\x44\x46': ('PDF', b'%%EOF'),
        b'\x1f\x8b': ('GZIP', None),
        b'\x50\x4b\x03\x04': ('ZIP', b'\x50\x4b\x05\x06'),  # End of central directory record
        b'\x7fELF': ('ELF', None),
        b'\xca\xfe\xba\xbe': ('JAVA CLASS', None),
        b'\x00\x00\x01\x00': ('ICO', None),
        b'\x23\x21\x2f\x62\x69\x6e\x2f\x73\x68': ('SHELL SCRIPT', None),
        b'\x77\x4f\x46\x46': ('WOFF', None),
        b'\x77\x4f\x46\x32': ('WOFF2', None),
        b'\x52\x61\x72\x21\x1a\x07\x00': ('RAR', b'\x52\x61\x72\x21\x1a\x07\x00'),
    }

    # 读取文件的前几个字节
    with open(file_path, 'rb') as file:
        file_header = file.read(8)
        file.seek(0, 2)  # 移动到文件末尾
        file_size = file.tell()
        file.seek(-1024, 2)  # 从末尾读取1024字节
        file_footer = file.read(1024)

    # 判断文件类型
    for magic, (file_type, footer_magic) in magic_numbers.items():
        if file_header.startswith(magic):
            if footer_magic:
                # 查找文件结尾
                footer_index = file_footer.find(footer_magic)
                if footer_index != -1:
                    extra_content = file_footer[footer_index + len(footer_magic):]
                    if extra_content:
                        # 检查多余的内容是否是一个文件
                        for extra_magic, (extra_file_type, _) in magic_numbers.items():
                            if extra_content.startswith(extra_magic):
                                # 提取多余的内容并保存为另一个文件
                                extra_file_path = f"{os.path.splitext(file_path)[0]}_extra.{extra_file_type.lower()}"
                                with open(extra_file_path, 'wb') as extra_file:
                                    extra_file.write(extra_content)
                                print(f"多余内容是文件：{extra_file_path}")
                                return file_type
                        # 如果多余的内容不是文件，则打印出来
                        print(f"多余内容不是已知文件：{extra_content.hex()}")
                else:
                    print("未找到文件结尾。")
            return file_type

    return "未知"


# 示例用法
file_path = 'example.png'
file_type = get_file_type_by_hex(file_path)
print(f"文件 {file_path} 的类型是：{file_type}")
