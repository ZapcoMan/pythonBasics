# -*- coding: utf-8 -*-
"""
自定义加密类 —— 豪密风格改良版
底本 = ASCII/UTF-8 编码   旋转 = ROT13 旋转十三    混淆 = 佩兰(Perrin)数列
最终结果 = 乱码(加密的产物就是解密的输入，两边是同一份内容)

    机制 1【公开底本 = 阿斯克码 + UTF-8】
        明文 -> UTF-8 字节流。ASCII 字符占 1 字节、中文等占 3 字节，
        每个字节就是"底本位置码"(取值 0~255，模数 M = 256)。
        因为是公开编码标准，双方无需再共约一本实体书。

    机制 2【旋转十三 = ROT13】
        每个字节在 0~255 上整体旋转 13 位(经典 ROT13 只作用于字母 A<->N，
        这里推广到整个字节空间，中文等多字节数据同样被旋转)，
        解密时反向旋转 13 位即可还原。

    机制 3【混淆 = 佩兰数列】
        佩兰数列: P0=3, P1=0, P2=2, Pn = P(n-2) + P(n-3)
        (3, 0, 2, 3, 5, 5, 7, 10, 12, 17, 22, 29, ...)
        把每一位的佩兰数模 256 掺进模加运算，破坏明文字节与密文字节的
        线性对应，使频率统计更难发挥作用。

    机制 4【模加之后输出乱码】
        加密: 乱码字节 = (ROT13(底本字节) + 佩兰) mod 256  -> 渲染成乱码字符串
        解密: 底本字节 = ROT13逆(乱码字节 - 佩兰 mod 256)  -> UTF-8 还原

    一进一出(关键点):
        encrypt(明文) 给出的"乱码"就是最终加密结果；
        decrypt(乱码) 要的就是这份乱码 —— 不再有"密文 + 密钥"两份东西。

说明: 本版是确定性对称加密(没有随机乱码页)，因此不具备一次一密的
      理论安全性，仅用于演示"底本取码 + 旋转 + 数列混淆"的组合方式。
      真·一次一密(乱码页)版本见同目录 HaoMi.py。
"""

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
def rot13(data: bytes) -> bytes:
    """旋转十三: 每个字节在 0~255 上整体旋转 13 位。

    经典 ROT13 只处理字母(A<->N)，这里推广到整个字节空间，
    这样中文等多字节 UTF-8 数据同样会被旋转。
    """
    return bytes((b + 13) % 256 for b in data)


def rot13_inv(data: bytes) -> bytes:
    """旋转十三的逆运算: 每个字节反向旋转 13 位。"""
    return bytes((b - 13) % 256 for b in data)


class HaoMiRot13Perrin:
    """
    豪密改良版: ASCII/UTF-8 底本 + ROT13 旋转十三 + 佩兰混淆 + 模256加算。

    加解密围绕"一份乱码"完成:
        encrypt(明文)  -> 乱码(最终加密结果)
        decrypt(乱码)  -> 明文
    """

    def __init__(self, modulus: int = 256):
        self.modulus = modulus          # 字节取值空间(ASCII 0~127, UTF-8 0~255)

    # ---------------- 加密 ----------------
    def encrypt(self, plaintext: str) -> str:
        """
        加密，返回最终加密结果 —— 乱码字符串。

        流程:
            p_bytes = plaintext.encode('utf-8')      # 机制1 底本取码
            rotated = rot13(p_bytes)                 # 机制2 旋转十三
            per     = perrin_stream(len)             # 机制3 佩兰混淆
            cipher  = (rotated + per) % 256          # 机制4 模加
            return  cipher.decode('latin-1')         # 输出乱码
        """
        if not plaintext:
            raise ValueError("明文不能为空")

        p_bytes = plaintext.encode("utf-8")                 # 底本取码
        rotated = rot13(p_bytes)                            # ROT13 旋转十三
        per = perrin_stream(len(rotated), self.modulus)     # 佩兰混淆序列
        cipher = bytes(
            (rotated[i] + per[i]) % self.modulus
            for i in range(len(rotated))
        )
        # latin-1 与 0~255 字节一一对应，保证乱码内容可以原样送回解密
        return cipher.decode("latin-1")

    # ---------------- 解密 ----------------
    def decrypt(self, cipher_text: str) -> str:
        """
        解密，入参就是加密给出的那份乱码。

        流程:
            cipher  = cipher_text.encode('latin-1')  # 收方拿到的乱码
            rotated = (cipher - per) % 256           # 去掉佩兰混淆
            p_bytes = rot13_inv(rotated)             # 反向旋转十三
            return  p_bytes.decode('utf-8')          # 还原明文
        """
        if not cipher_text:
            raise ValueError("乱码内容不能为空")

        cipher = cipher_text.encode("latin-1")
        per = perrin_stream(len(cipher), self.modulus)
        rotated = bytes(
            (cipher[i] - per[i]) % self.modulus
            for i in range(len(cipher))
        )
        p_bytes = rot13_inv(rotated)
        try:
            return p_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError("乱码内容不匹配或已被篡改，无法按 UTF-8 还原") from e

    # ---------------- 辅助: 控制台复制粘贴用 ----------------
    @staticmethod
    def to_hex(cipher_text: str) -> str:
        """乱码字符串 -> HEX(乱码里可能有不可见字符，复制不便时用这个)。"""
        return cipher_text.encode("latin-1").hex().upper()

    @staticmethod
    def from_hex(hex_text: str) -> str:
        """HEX -> 乱码字符串(收到 HEX 时先转回乱码再解密)。"""
        try:
            return bytes.fromhex(hex_text).decode("latin-1")
        except ValueError as e:
            raise ValueError("HEX 格式非法，应为偶数个 0-9/A-F 字符") from e


def print_cipher(label: str, cipher_text: str) -> None:
    """打印乱码结果。乱码里可能出现控制台编不出的字符，此时自动退回 HEX。"""
    try:
        print(f"{label}: {cipher_text}")
    except UnicodeEncodeError:
        print(f"{label}: (当前控制台无法显示该乱码，请改用下面的 HEX)")
        print(f"{' ' * len(label)}  HEX -> {HaoMiRot13Perrin.to_hex(cipher_text)}")


def run_demo(hao: HaoMiRot13Perrin, message: str) -> None:
    """打印一次完整流程: 取码 -> 旋转十三 -> 佩兰加算 -> 乱码 -> 还原。"""
    print("=" * 68)
    p_bytes = message.encode("utf-8")
    print(f"明文              : {message}")
    print(f"UTF-8 字节(底本)  : {list(p_bytes)}")
    print(f"ROT13 旋转后      : {list(rot13(p_bytes))}")
    print(f"佩兰混淆序列      : {perrin_stream(len(p_bytes), hao.modulus)}")

    cipher = hao.encrypt(message)                 # 最终加密结果 = 乱码
    print_cipher("最终加密结果(乱码)", cipher)
    print(f"复制用HEX         : {hao.to_hex(cipher)}")

    print(f"解密还原          : {hao.decrypt(cipher)}")   # 入参就是上面那份乱码


def main() -> None:
    hao = HaoMiRot13Perrin()
    print(f"底本方案: 公开的 ASCII + UTF-8 字节编码，运算模数 M = {hao.modulus}")

    if "--demo" in sys.argv:
        run_demo(hao, "举头望明月低头思故乡")
        run_demo(hao, "Hello ROT13 Perrin!")
        print("=" * 68)
        print("加密的产出是「乱码」，解密的入参就是这份乱码，两者是同一份内容。")
        return

    # 交互模式: 加密与解密严格分成两条独立流程，选一项、执行一次、随即结束
    print("-" * 68)
    print("请选择操作: 1 = 加密    2 = 解密")
    choice = input("请输入序号: ").strip()

    if choice == "1":
        # 加密流程: 给出乱码(最终结果)后即结束
        plain = input("请输入要加密的内容: ").strip()
        if not plain:
            print("[失败] 明文不能为空")
            return
        try:
            cipher = hao.encrypt(plain)
        except ValueError as e:
            print(f"[失败] {e}")
            return
        print_cipher("最终加密结果(乱码)", cipher)
        print(f"复制用HEX         : {hao.to_hex(cipher)}")
        print("提示: 把这串乱码交给收方即可；加密流程到此结束。")
        return

    if choice == "2":
        # 解密流程: 只收加密给出的那份乱码
        cipher = input("请输入加密给出的乱码内容(不便粘贴时留空改用HEX): ")
        if not cipher:
            hex_text = input("请输入乱码的HEX: ").strip().upper()
            try:
                cipher = hao.from_hex(hex_text)
            except ValueError as e:
                print(f"[失败] {e}")
                return
        try:
            plaintext = hao.decrypt(cipher)
        except ValueError as e:
            print(f"[失败] {e}")
            return
        print(f"解密还原          : {plaintext}")
        print("提示: 解密流程到此结束。")
        return

    print("[失败] 未识别的操作序号，请输入 1 或 2")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Windows 控制台兼容
    except Exception:
        pass
    main()
