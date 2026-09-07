# -*- coding: utf-8 -*-
"""
自定义加密类 —— 豪密风格改良版
底本 = ASCII/UTF-8 编码   密钥 = ROT13 旋转十三    混淆 = 佩兰(Perrin)数列

设计动机: 学习"豪密"的"底本取码 + 随机密钥 + 双重加算"框架，
但把三块零件换成更容易跑通的计算机版本:

    机制 1【公开底本 = 阿斯克码 + UTF-8】
        明文 -> UTF-8 字节流。ASCII 字符占 1 字节、中文等占 3 字节，
        每个字节就是"底本位置码"(取值 0~255，模数 M = 256)。
        因为是公开编码标准，双方无需再共约一本实体书。

    机制 2【随机密钥 = ROT13 旋转十三】
        每次取码随机生成一页 26 个大写字母的"乱码页"(一电一密)，
        分发给对方前先做 ROT13 旋转: A<->N, B<->O ... 收方反旋即还原，
        即使密钥中途被看到，也不是明文密钥(旋转加密是它的自逆)。

    机制 3【混淆 = 佩兰数列】
        佩兰数列: P0=3, P1=0, P2=2, Pn = P(n-2) + P(n-3)
        (3, 0, 2, 3, 5, 5, 7, 10, 12, 17, 22, 29, ...)
        把每一位的佩兰数模 256 掺进模加运算，破坏明文字节与密文字节的
        线性对应，使频率统计更难发挥作用。

    机制 4【双重加算】
        加密: 密文 = (底本字节 + 密钥字节 + 佩兰混淆) mod 256
        解密: 底本字节 = (密文 - 密钥字节 - 佩兰混淆) mod 256

说明: 若密钥为真随机、绝不重用且安全分发，则该结构具备一次一密特性，
      ROT13/佩兰只是教学上的"混淆与伪装"，本身不增加理论安全性。
"""

import secrets
import sys

# ---------- 佩兰数列 ----------
def perrin_stream(length: int, modulus: int = 256):
    """返回佩兰数列前 length 项，每项已取模(0 ~ modulus-1)。

    P0=3, P1=0, P2=2, Pn = P(n-2) + P(n-3)
    """
    if length <= 0:
        return []
    seq = [3 % modulus, 0, 2 % modulus]
    while len(seq) < length:
        seq.append((seq[-2] + seq[-3]) % modulus)
    return seq[:length]


# ---------- ROT13 旋转十三 ----------
def rot13_byte(b: int) -> int:
    """对单个 ASCII 字母字节做 ROT13(A<->N)，非字母字节保持不变。"""
    if ord('A') <= b <= ord('Z'):
        return ord('A') + (b - ord('A') + 13) % 26
    if ord('a') <= b <= ord('z'):
        return ord('a') + (b - ord('a') + 13) % 26
    return b


def rot13(data: bytes) -> bytes:
    """字节流 ROT13。ROT13 是自逆的: rot13(rot13(x)) == x。"""
    return bytes(rot13_byte(b) for b in data)


class HaoMiRot13Perrin:
    """
    豪密改良版: ASCII/UTF-8 底本 + ROT13 随机密钥 + 佩兰混淆 + 模256双重加算。
    所有运算都在"字节(0~255)"上完成，因此天然支持中英文混排。
    """

    def __init__(self, modulus: int = 256):
        self.modulus = modulus          # 字节取值空间(ASCII 0~127, UTF-8 0~255)

    # ---------------- 加密 ----------------
    def encrypt(self, plaintext: str):
        """
        加密并返回 (密文HEX, 已ROT13的密钥HEX)。

        内部流程:
            p_bytes = plaintext.encode('utf-8')          # 机制1 底本取码
            key     = 随机生成 len(p_bytes) 个大写字母      # 机制2 乱码页
            key_rot = rot13(key)                          # ROT13 后再分发
            per     = perrin_stream(len)                  # 机制3 佩兰混淆
            cipher  = (p_bytes + key + per) % 256         # 机制4 双重加算
        """
        if not plaintext:
            raise ValueError("明文不能为空")

        p_bytes = plaintext.encode("utf-8")               # 底本: 字符 -> 字节码
        n = len(p_bytes)
        per = perrin_stream(n, self.modulus)              # 佩兰混淆序列

        # 随机乱码页: 一页大写字母，长度=消息字节数(一电一密，用完即焚)
        key = bytes(secrets.choice(range(ord('A'), ord('Z') + 1)) for _ in range(n))
        key_rot = rot13(key)                              # 分发前先做 ROT13

        cipher = bytes(
            (p_bytes[i] + key[i] + per[i]) % self.modulus
            for i in range(n)
        )
        return cipher.hex().upper(), key_rot.hex().upper()

    # ---------------- 解密 ----------------
    def decrypt(self, cipher_hex: str, key_hex: str) -> str:
        """
        用"已 ROT13 的密钥"还原明文:
            1. key = rot13(收方收到的密钥字节)              # 反旋回原乱码页
            2. p_bytes = (密文 - key - 佩兰) mod 256
            3. plaintext = p_bytes.decode('utf-8')
        """
        cipher = bytes.fromhex(cipher_hex)
        key_rot = bytes.fromhex(key_hex)
        if len(cipher) != len(key_rot):
            raise ValueError("密文与乱码页长度不一致，无法解密")

        key = rot13(key_rot)                              # 自逆旋转，还原真密钥
        per = perrin_stream(len(cipher), self.modulus)
        p_bytes = bytes(
            (cipher[i] - key[i] - per[i]) % self.modulus
            for i in range(len(cipher))
        )
        try:
            return p_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError("密钥错误或电文被篡改，无法按 UTF-8 还原") from e


def run_demo(hao: HaoMiRot13Perrin, message: str) -> None:
    """打印一次完整流程: 取码 -> 生成乱码页 -> ROT13 -> 佩兰加算 -> 还原。"""
    print("=" * 68)
    p_bytes = message.encode("utf-8")
    print(f"明文            : {message}")
    print(f"UTF-8 字节(底本): {list(p_bytes)}")
    print(f"ASCII 可见部分  : {p_bytes.decode('latin-1')!r}")

    cipher_hex, key_hex = hao.encrypt(message)
    key_rot = bytes.fromhex(key_hex)
    per = perrin_stream(len(p_bytes), hao.modulus)

    print(f"乱码页(真密钥)  : {rot13(key_rot).decode('ascii')}")
    print(f"ROT13 后分发    : {key_rot.decode('ascii')}   <- 对方反旋即还原")
    print(f"佩兰混淆序列    : {per[:len(p_bytes)]}")
    print(f"密文(HEX)       : {cipher_hex}")
    print(f"解密还原        : {hao.decrypt(cipher_hex, key_hex)}")
    # 用后即焚: 密钥变量用完即丢弃，绝不重复使用
    del key_hex


def main() -> None:
    hao = HaoMiRot13Perrin()
    print(f"底本方案: 公开的 ASCII + UTF-8 字节编码，运算模数 M = {hao.modulus}")

    if "--demo" in sys.argv:
        # 演示一电一密: 同一句明文发两次，密文完全不同
        run_demo(hao, "举头望明月低头思故乡")
        run_demo(hao, "举头望明月低头思故乡")
        print("=" * 68)
        print("两次密文完全不同 => 同一明文 + 不同乱码页 = 不同密文，")
        print("敌方即使截获多份电文也无法通过比对寻找规律。")
        return

    # 交互模式
    while True:
        plain = input("请输入要加密的内容(直接回车退出): ").strip()
        if not plain:
            break
        try:
            cipher_hex, key_hex = hao.encrypt(plain)
            print(f"密文(HEX)      : {cipher_hex}")
            print(f"乱码页(ROT13后): {key_hex}   <- 安全分发，收方反旋 ROT13 后使用")
            check = input("是否立即用这页乱码解密验证? (y/n): ").strip().lower()
            if check == "y":
                print(f"解密还原        : {hao.decrypt(cipher_hex, key_hex)}")
        except ValueError as e:
            print(f"[失败] {e}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Windows 控制台兼容
    except Exception:
        pass
    main()
