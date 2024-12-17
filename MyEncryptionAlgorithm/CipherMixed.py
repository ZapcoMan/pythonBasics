def caesar_cipher(text, shift, mode='encrypt'):
    """
    实现凯撒密码的加密或解密。

    参数:
    text : str
        需要加密或解密的文本。
    shift : int
        字符移动的位置数。
    mode : str, 可选
        操作模式，'encrypt' 为加密，'decrypt' 为解密，默认为 'encrypt'。

    返回:
    str
        加密或解密后的文本。
    """
    result = ""
    # 根据模式调整偏移量
    if mode == 'decrypt':
        shift = -shift
    for char in text:
        # 处理字母字符
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            offset = (ord(char) - start + shift) % 26
            result += chr(start + offset)
        else:
            # 非字母字符直接添加
            result += char
    return result

def atbash_cipher(text):
    """
    实现Atbash密码的加密和解密。

    参数:
    text : str
        需要加密或解密的文本。

    返回:
    str
        加密或解密后的文本。
    """
    result = ""
    for char in text:
        if char.isalpha():
            # 判断字母大小写并进行转换
            start = ord('a') if char.islower() else ord('A')
            # 使用25 - (ord(char) - start)实现Atbash密码逻辑
            result += chr(start + (25 - (ord(char) - start)))
        else:
            # 非字母字符直接添加
            result += char
    return result

# 字符串反转函数，直接使用切片实现
def reverse_string(text):
    return text[::-1]

# 主程序部分
# 输入需要加密的文本
text = input()
# 输入偏移量
shift = int(input())
# 使用凯撒密码加密后，再使用Atbash密码加密，并将结果反转
print("加密:"+atbash_cipher(reverse_string(caesar_cipher(text, shift))))
# 对加密后的密文进行解密，过程与加密相反
加密之后的密文 = atbash_cipher(reverse_string(caesar_cipher(text, shift)))
print("解密:"+atbash_cipher(reverse_string(caesar_cipher(加密之后的密文, shift, mode='decrypt'))))
