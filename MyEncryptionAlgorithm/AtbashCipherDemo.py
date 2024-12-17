# 完成 Atbash Cipher

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


# 输入原文
text = input("Enter the text: ")
# 输入要执行的操作 输入 1 执行加密 输入2 执行解密
choice = int(input("Enter 1 for encryption or 2 for decryption: "))
if choice == 1:
    # 执行加密操作
    encrypted_text = atbash_cipher(text)
    print("Encrypted:", encrypted_text)
elif choice == 2:
    # 再次执行Atbash密码将加密文本转换回原文
    decrypted_text = atbash_cipher(text)
    print("Decrypted:", decrypted_text)
else:
    print("Invalid choice. Exiting.")
    exit()






