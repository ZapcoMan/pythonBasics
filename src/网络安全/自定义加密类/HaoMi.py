# -*- coding: utf-8 -*-
"""
豪密(HaoMi) —— 一次一密风格的自定义加密类

"豪密"是周恩来同志在 1931 年前后主持设计的中共第一套高级密码，
其核心思想在本文件中被还原为一个可运行的加密类，对应四大机制：

    机制 1【公开底本】   __init__ + char_to_code / code_to_char
                         用公开书籍(唐诗三百首 / 词典 / 小说)建立
                         "字符 <-> 位置码" 对照表，位置码即历史上的"页码 + 字数"编号。
    机制 2【随机乱码本】  random_key()
                         用 secrets(操作系统级真随机源)生成乱码数字，
                         不遵循任何语法 / 数学规律，从源头杜绝频率分析法。
    机制 3【一次一密】    encrypt() / decrypt() 的密钥现场生成、用后即焚，
                         一电一密，截获再多电文也无法比对出规律。
    机制 4【双重加密】    encrypt(): 密文 = (位置码 + 乱码) mod 底本容量
                         decrypt(): 位置码 = (密文 - 乱码) mod 底本容量

说明: OTP 的安全性依赖"真随机 + 密钥长度不小于明文 + 绝不重用 + 密钥安全分发"，
      本类为教学演示实现，不是实际意义上的保密通信工具。
"""

import secrets
import sys
from typing import List, Tuple

# 默认底本: 公开易得的《唐诗三百首》节选(可以换成任何一本普通书籍的正文)
DEFAULT_BOOK = """
床前明月光疑是地上霜举头望明月低头思故乡
春眠不觉晓处处闻啼鸟夜来风雨声花落知多少
白日依山尽黄河入海流欲穷千里目更上一层楼
锄禾日当午汗滴禾下土谁知盘中餐粒粒皆辛苦
慈母手中线游子身上衣临行密密缝意恐迟迟归
鹅鹅鹅曲项向天歌白毛浮绿水红掌拨清波
"""


class HaoMi:
    """豪密风格加密类: 公开底本 + 随机乱码本 + 一次一密 + 模数加算。"""

    def __init__(self, book_text: str = DEFAULT_BOOK):
        # 机制1: 去空白后，底本正文中"每个字符占一个位置码"(页码+字数的抽象)
        self._chars = [ch for ch in book_text if not ch.isspace()]
        if not self._chars:
            raise ValueError("底本为空，无法建立字符对照表")
        self.space = len(self._chars)      # 位置码的取值空间(模数 M)
        self._char_codes: dict = {}        # 字符 -> 该字符在底本中出现过的全部位置码
        for idx, ch in enumerate(self._chars):
            self._char_codes.setdefault(ch, []).append(idx)

    # ================= 机制 1: 公开底本 =================
    def char_to_code(self, ch: str) -> int:
        """把明文字符翻译成底本位置码(对应历史上约定的"页码+字数")。"""
        codes = self._char_codes.get(ch)
        if not codes:
            raise ValueError(f"底本中没有字符 {ch!r}，请换一种说法或更换底本")
        # 同一个字在底本中多次出现时，随机选其中一处，进一步增加敌方的分析难度
        return secrets.choice(codes)

    def code_to_char(self, code: int) -> str:
        """把底本位置码反查成字符。"""
        return self._chars[code % self.space]

    # ================= 机制 2: 随机乱码本 =================
    @staticmethod
    def random_key(length: int, space: int) -> List[int]:
        """生成一页"乱码": length 个取值在 [0, space) 的真随机数。"""
        return [secrets.randbelow(space) for _ in range(length)]

    # ============ 机制 3 + 4: 一次一密 与 模数加算 ============
    def encrypt(self, plaintext: str) -> Tuple[str, str]:
        """加密并返回 (密文数字串, 一次性乱码串)。

        流程:
            明文逐字查底本得到位置码 p
            取一个真随机乱码 k
            密文 = (p + k) mod space
        乱码只服务于本次电文，解密完成即可焚毁(本类不保存它，天然"用后即焚")。
        """
        if not plaintext:
            raise ValueError("明文不能为空")
        codes = [self.char_to_code(c) for c in plaintext]
        key = self.random_key(len(codes), self.space)
        cipher = [(p + k) % self.space for p, k in zip(codes, key)]
        return self._fmt(cipher), self._fmt(key)

    def decrypt(self, cipher_text: str, key_text: str) -> str:
        """用同一页乱码反向加算: 位置码 = (密文 - 乱码) mod space，再还原成明文。"""
        cipher = self._parse(cipher_text)
        key = self._parse(key_text)
        if len(cipher) != len(key):
            raise ValueError("密文与乱码长度不一致，无法解密")
        codes = [(c - k) % self.space for c, k in zip(cipher, key)]
        return "".join(self.code_to_char(p) for p in codes)

    # ================= 序列化工具 =================
    @staticmethod
    def _fmt(nums: List[int]) -> str:
        return " ".join(str(n) for n in nums)

    @staticmethod
    def _parse(text: str) -> List[int]:
        return [int(x) for x in text.split()]


def run_demo(hao: HaoMi, message: str) -> None:
    """打印一次完整的"底本取码 -> 加乱码 -> 发密文 -> 减乱码还原"流程。"""
    print("=" * 66)
    print(f"明文            : {message}")
    # 展示用: 重新取一次位置码(每次可能不同，这正是"同字随机选位置"的效果)
    codes_demo = [hao.char_to_code(c) for c in message]
    print(f"底本位置码(演示): {codes_demo}")
    cipher, key = hao.encrypt(message)
    print(f"乱码本(一次性)  : {key}")
    print(f"密文(模数加算)  : {cipher}")
    print(f"解密还原        : {hao.decrypt(cipher, key)}")
    # 用后即焚: 变量随即被丢弃，代码层不落盘、不可复用
    del key
    print(f"(密钥已焚毁，本电文密钥不再可用)")


def main() -> None:
    # 命令行参数: python HaoMi.py --demo             -> 直接跑示例
    #             python HaoMi.py 某书.txt           -> 以指定文件作为底本
    book_text = DEFAULT_BOOK
    if len(sys.argv) > 1 and sys.argv[1] != "--demo":
        with open(sys.argv[1], encoding="utf-8") as f:
            book_text = f.read()

    hao = HaoMi(book_text)
    print(f"底本容量(位置码空间 M = {hao.space})")

    if "--demo" in sys.argv:
        # 演示一电一密: 同一句明文发两次，密文完全不同
        run_demo(hao, "举头望明月低头思故乡")
        run_demo(hao, "举头望明月低头思故乡")
        print("=" * 66)
        print("两次密文完全不同，说明: 同一明文 + 不同乱码 = 不同密文，")
        print("敌方即使截获多份电文也无法通过比对寻找规律。")
        return

    # 交互模式
    while True:
        plain = input("请输入要加密的内容(直接回车退出): ").strip()
        if not plain:
            break
        try:
            cipher, key = hao.encrypt(plain)
            print(f"密文(数字串): {cipher}")
            print(f"密钥(乱码页): {key}  <- 请通过安全渠道单独分发给接收方，用后即焚")
            check = input("是否立即用这页乱码解密验证? (y/n): ").strip().lower()
            if check == "y":
                print(f"解密还原    : {hao.decrypt(cipher, key)}")
        except ValueError as e:
            print(f"[失败] {e}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Windows 控制台兼容
    except Exception:
        pass
    main()
