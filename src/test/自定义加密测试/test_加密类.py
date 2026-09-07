# -*- coding: utf-8 -*-
"""
只测试"完全自研"的两个加密类（不依赖任何第三方加密库）:

    HaoMi            —— 豪密 OTP: 公开底本 + 真随机乱码页 + 一电一密
    HaoMiRot13Perrin —— UTF-8 + ROT13 旋转十三 + 佩兰数列混淆

这两个类的加密数学 100% 是本仓库自己实现的(只用标准库 secrets 和纯算术)，
没有调用 cryptography 之类的加密库，所以它们才是"你自己的算法"。

不在此文件测试:
    AsymmetricRSA / RSAUtils —— 底层用的是 cryptography 库的 RSA / AES-GCM，
    属于"用现成零件组装"，要测请单独建文件。

运行(需 pytest):
    pytest test_加密类.py -v
"""

import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))    # .../src/test/自定义加密测试
SRC = os.path.dirname(os.path.dirname(HERE))         # .../src
CRYPTO_DIR = os.path.join(SRC, "网络安全", "自定义加密类")
sys.path.insert(0, CRYPTO_DIR)

# 下面两个 import 由运行时 sys.path 解析，IDE 静态分析会误报"没有该模块"
# noinspection PyUnresolvedReferences
import HaoMi
import HaoMiRot13Perrin

# 自制底本（可以换成任何一本公开书籍的正文）
MY_BOOK = "床前明月光疑是地上霜举头望明月低头思故乡春眠不觉晓处处闻啼鸟"


# ============================================================ fixtures
@pytest.fixture(scope="session")
def haomi():
    """豪密 OTP（默认底本：内置唐诗）。"""
    return HaoMi.HaoMi()


@pytest.fixture(scope="session")
def rot13():
    """ROT13 旋转十三 + 佩兰数列。"""
    return HaoMiRot13Perrin.HaoMiRot13Perrin()


@pytest.fixture
def my_haomi():
    """用自制底本造一个豪密实例。"""
    return HaoMi.HaoMi(MY_BOOK)


# ============================================================ 证明: 底层确实是自研的
def test_custom_classes_use_no_crypto_library():
    """这两个类没有引入任何第三方加密库 —— 底层就是你自己的代码。"""
    for mod in (HaoMi, HaoMiRot13Perrin):
        source = open(mod.__file__, encoding="utf-8").read()
        for banned in ("cryptography", "AESGCM", "nacl", "Crypto.Cipher"):
            assert banned not in source, f"{mod.__name__} 引入了 {banned}"
    assert "cryptography" not in sys.modules


# ============================================================ 豪密 OTP
def test_haomi_roundtrip(haomi):
    cipher, key = haomi.encrypt("低头思故乡")
    assert haomi.decrypt(cipher, key) == "低头思故乡"


def test_haomi_one_time_pad_changes_cipher(haomi):
    """一电一密: 同一明文两次加密，密文必须不同。"""
    a, _ = haomi.encrypt("低头思故乡")
    b, _ = haomi.encrypt("低头思故乡")
    assert a != b


def test_haomi_wrong_key_cannot_decrypt(haomi):
    """乱码错了就还原不回来。"""
    cipher, key = haomi.encrypt("低头思故乡")
    bad_key = " ".join(str((int(x) + 1) % haomi.space) for x in key.split())
    assert haomi.decrypt(cipher, bad_key) != "低头思故乡"


def test_haomi_char_not_in_book_raises(haomi):
    """底本里没有的字符必须报错，不能静默出错。"""
    with pytest.raises(ValueError):
        haomi.encrypt("Hello")


def test_haomi_empty_plaintext_raises(haomi):
    with pytest.raises(ValueError):
        haomi.encrypt("")


def test_haomi_custom_book(my_haomi):
    """换成自制底本同样能加解密。"""
    cipher, key = my_haomi.encrypt("处处闻啼鸟")
    assert my_haomi.decrypt(cipher, key) == "处处闻啼鸟"


def test_haomi_space_matches_book(my_haomi):
    """位置码空间 = 底本中非空白字符的数量。"""
    expected = len([c for c in MY_BOOK if not c.isspace()])
    assert my_haomi.space == expected


def test_haomi_cipher_are_numbers_within_space(haomi):
    """密文是一串落在 [0, space) 内的数字。"""
    cipher, _ = haomi.encrypt("低头思故乡")
    nums = [int(x) for x in cipher.split()]
    assert len(nums) == 5
    assert all(0 <= n < haomi.space for n in nums)


# ============================================================ ROT13 + 佩兰
@pytest.mark.parametrize("msg", [
    "Hello",
    "abc 123",
    "中文 English 混排 !@#",
    "举头望明月低头思故乡",
    "床前明月光疑是地上霜",
])
def test_rot13_roundtrip(rot13, msg):
    """参数化: 多种文本各跑一遍往返。"""
    assert rot13.decrypt(rot13.encrypt(msg)) == msg


def test_rot13_known_value(rot13):
    """固定值测试: 手算验证流水线(明文 -> +13 旋转 -> +佩兰)。

    'A' 的 UTF-8 字节 = 65
    旋转十三            : (65 + 13) % 256 = 78
    加佩兰第 0 项(3)    : (78 + 3)  % 256 = 81 -> 字符 'Q'
    """
    assert rot13.encrypt("A") == "Q"


def test_rot13_no_key_means_deterministic(rot13):
    """没有密钥 -> 每次结果都一样(所以它只是混淆，不是加密)。"""
    assert rot13.encrypt("测试内容") == rot13.encrypt("测试内容")


def test_rot13_hex_roundtrip(rot13):
    cipher = rot13.encrypt("举头望明月")
    assert rot13.decrypt(rot13.from_hex(rot13.to_hex(cipher))) == "举头望明月"


def test_rot13_empty_plaintext_raises(rot13):
    with pytest.raises(ValueError):
        rot13.encrypt("")


def test_rot13_tampered_cipher_is_detected(rot13):
    """乱码被改 -> 要么解不出来报错，要么还原出的不是原文。"""
    cipher = rot13.encrypt("举头望明月")
    tampered = "\x80" + cipher[1:]
    try:
        out = rot13.decrypt(tampered)
    except ValueError:
        return                      # 解不出来，也算检测到了
    assert out != "举头望明月"


def test_rot13_perrin_sequence_values():
    """佩兰数列前几项必须是 3, 0, 2, 3, 2, 5, 5, 7 ..."""
    seq = HaoMiRot13Perrin.perrin_stream(8)
    assert seq == [3, 0, 2, 3, 2, 5, 5, 7]


# ============================================================ 手动输入
@pytest.mark.skipif(not sys.stdin.isatty(), reason="需要交互式终端，非交互环境自动跳过")
def test_manual_input(rot13):
    """手动输入一段内容，用自研的两个类各跑一遍。"""
    msg = input("\n请输入要加密的内容: ").strip()
    if not msg:
        pytest.skip("未输入内容")
    assert rot13.decrypt(rot13.encrypt(msg)) == msg


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
