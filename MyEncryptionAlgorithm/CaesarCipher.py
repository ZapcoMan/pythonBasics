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


# 输入原文
text = input("")
# 输入偏移量
shift = int(input(""))

# 执行加密操作
encrypted_text = caesar_cipher(text, shift)
print("Encrypted:", encrypted_text)

# 执行解密操作
decrypted_text = caesar_cipher(encrypted_text, shift, mode='decrypt')
print("Decrypted:", decrypted_text)

