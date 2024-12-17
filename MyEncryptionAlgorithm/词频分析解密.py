from collections import Counter
import re

def analyze_character_frequency(text):
    """
    分析给定文本中字符的频率。

    参数:
    text : str
        需要分析的文本内容。

    返回:
    dict
        包含每个字符及其出现频率的字典。
    """
    # 清洗文本，移除非字母字符并将所有字符转为小写
    cleaned_text = re.sub(r'[^a-zA-Z]', '', text).lower()

    # 使用Counter统计每个字符出现的次数
    char_count = Counter(cleaned_text)

    return dict(char_count)

def calculate_similarity(char_freq, english_freq):
    """
    计算字符频率的相似度。

    参数:
    char_freq : dict
        输入文本的字符频率。
    english_freq : dict
        英语常见字符频率。

    返回:
    float
        相似度得分。
    """
    total_similarity = sum(char_freq.get(char, 0) for char in english_freq)
    return total_similarity / sum(char_freq.values())

def guess_caesar_cipher(text):
    """
    通过字符频率分析来猜测凯撒密码的偏移量。

    参数:
    text : str
        需要分析的加密文本。

    返回:
    str
        猜测的加密方式和偏移量。
    """
    # 英语中最常见的字符频率分布
    english_char_freq = {
        'e': 0.12702,
        't': 0.09056,
        'a': 0.08167,
        'o': 0.07507,
        'i': 0.06966,
        'n': 0.06749,
        's': 0.06327,
        'h': 0.06094,
        'r': 0.05987,
        'd': 0.04253,
        'l': 0.04025,
        'c': 0.02782,
        'u': 0.02758,
        'm': 0.02406,
        'w': 0.02360,
        'f': 0.02228,
        'g': 0.02015,
        'y': 0.01974,
        'p': 0.01929,
        'b': 0.01492,
        'v': 0.00978,
        'k': 0.00772,
        'j': 0.00153,
        'x': 0.00150,
        'q': 0.00095,
        'z': 0.00074
    }

    # 分析字符频率
    char_freq = analyze_character_frequency(text)

    # 计算每个偏移量下的相似度
    similarities = {}
    for shift in range(26):
        shifted_freq = {}
        for char, count in char_freq.items():
            shifted_char = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            shifted_freq[shifted_char] = count

        similarity = calculate_similarity(shifted_freq, english_freq)
        similarities[shift] = similarity

    # 找到最相似的偏移量
    best_shift = max(similarities, key=similarities.get)

    if best_shift != 0:
        return f"Caesar Cipher with shift {best_shift}"
    else:
        return "Unknown Encryption"

def guess_vigenere_cipher(text):
    """
    通过字符频率分析来猜测维吉尼亚密码。

    参数:
    text : str
        需要分析的加密文本。

    返回:
    str
        猜测的加密方式。
    """
    # 进行更复杂的分析，例如使用频率分析法
    # 这里仅作为示例，实际应用中需要更详细的算法
    return "Vigenere Cipher (Complex Analysis Required)"

# 示例文本
encrypted_text = "SYOIRYBE"

# 调用函数进行加密方式猜测
encryption_guess = guess_caesar_cipher(encrypted_text)

# 输出结果
print(f"Guessed Encryption Method: {encryption_guess}")

# 如果需要进一步分析维吉尼亚密码
# encryption_guess = guess_vigenere_cipher(encrypted_text)
# print(f"Guessed Encryption Method: {encryption_guess}")
