# -*- coding: utf-8 -*-
"""
自定义加密类 —— 非对称加密实战版
RSA-2048 + OAEP + PSS + AES-GCM 混合加密（数字信封）

先回答两个关键问题:

    1) 密钥要怎么做?
       非对称的密钥不是双方"约定"出来的，而是接收方在本地"生成一对":
            generate_keypair()  ->  私钥(打死不外传) + 公钥(可以满世界发)
       私钥存成 name.vibe(可加口令)，公钥存成 name_pub.vibe。
       文件内容依然是标准的 PEM 文本，后缀只是我们自己套的"马甲"，
       不喜欢 .vibe 就改 KEY_SUFFIX 一行(比如 .bet / .key / .xyz)。

    2) 密钥要不要和密文加在一起?
       私钥: 绝对不。它连文件都不该离开本机。
       公钥: 可以，它本来就设计成公开的，带了也无妨。
       真正跟着密文走的，是"被对方公钥封装过的会话密钥"(数字信封)，
       只有对方的私钥能拆开 —— 泄露了也没用。这与对称加密
       "密钥随文 = 直接泄密"是完全不同的两件事。

为什么要用混合加密(不直接拿 RSA 加密正文):
    RSA-2048 配 OAEP 一次只能加密约 190 字节，所以正文交给 AES-GCM，
    RSA 只负责封装 32 字节的会话密钥。

    加密: 随机会话密钥 sk
          -> AES-GCM(sk) 加密正文            -> ct
          -> RSA-OAEP(对方公钥) 封装 sk       -> enc_sk
          -> PSS(自己私钥) 给密文签名          -> sig
          -> 打包成"单件" base64 串(最终加密结果)
    解密: 先验 PSS 签名(防篡改 + 证明是对方发的)
          -> 用自己的私钥解开 enc_sk 得到 sk
          -> AES-GCM 还原明文

一进一出(沿用本目录约定):
    encrypt(明文, 对方公钥)  -> 单件 base64 包
    decrypt(单件 base64 包, 自己私钥) -> 明文
"""

import base64
import json
import os
import sys
import tempfile

from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ---------------------------------------------------------------- 约定常量
# 不喜欢 .pem？改这一行即可，例如 ".bet"，文件内容不受影响(PEM 文本不变)
KEY_SUFFIX = ".vibe"
PUB_SUFFIX = "_pub" + KEY_SUFFIX         # 公钥: name_pub.vibe

# 脚本所在目录，密钥文件默认落在这里
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- 小工具
def b64(data: bytes) -> str:
    """字节 -> base64 字符串(便于在电报/聊天窗口里传)。"""
    return base64.b64encode(data).decode("ascii")


def ub64(text: str) -> bytes:
    """base64 字符串 -> 字节。"""
    return base64.b64decode(text)


def print_safe(label: str, text: str) -> None:
    """打印内容。控制台编不出某些字符(Windows GBK)时自动退回 repr。"""
    try:
        print(f"{label}: {text}")
    except UnicodeEncodeError:
        print(f"{label}: (当前控制台无法显示，改用安全表示)")
        print(f"{' ' * len(label)}  {text!r}")


def _oaep():
    """RSA-OAEP 填充参数(配 SHA256 + MGF1-SHA256)。"""
    return padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )


def _pss():
    """RSA-PSS 签名参数(配 SHA256 + MGF1-SHA256，盐长取最大)。"""
    return padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH,
    )


class AsymmetricRSA:
    """
    非对称加密: RSA 密钥对 + OAEP 封装会话密钥 + AES-GCM 加密正文 + PSS 签名。

    围绕"单件密文包"完成:
        encrypt(明文, 对方公钥[, 自己私钥])  -> 单件 base64 包
        decrypt(单件 base64 包, 自己私钥[, 对方公钥]) -> 明文
    """

    def __init__(self, key_size: int = 2048):
        self.key_size = key_size          # 2048 位，生产环境可用 3072

    # ================= 密钥生成 =================
    def generate_keypair(self):
        """本地生成一对密钥: (私钥, 公钥)。私钥永不外传，公钥随便发。"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
        )
        return private_key, private_key.public_key()

    # ================= 密钥文件(.vibe) =================
    def save_private_key(self, private_key, path: str, passphrase: str | None = None) -> str:
        """保存私钥。给了口令就用口令加密存储(推荐)，否则明文存储。"""
        enc = (serialization.BestAvailableEncryption(passphrase.encode("utf-8"))
               if passphrase else serialization.NoEncryption())
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=enc,
        )
        with open(path, "wb") as f:
            f.write(pem)
        return path

    def save_public_key(self, public_key, path: str) -> str:
        """保存公钥(本来就是公开的，不需要加密)。"""
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        with open(path, "wb") as f:
            f.write(pem)
        return path

    @staticmethod
    def load_private_key(path: str, passphrase: str | None = None):
        """载入私钥。文件若在生成时加了口令，这里必须给同样的口令。"""
        with open(path, "rb") as f:
            data = f.read()
        pwd = passphrase.encode("utf-8") if passphrase else None
        return serialization.load_pem_private_key(data, password=pwd)

    @staticmethod
    def load_public_key(path: str):
        """载入公钥。"""
        with open(path, "rb") as f:
            data = f.read()
        return serialization.load_pem_public_key(data)

    # ================= 加密(输出单件) =================
    def encrypt(self, plaintext: str, recipient_public_key,
                sender_private_key=None) -> str:
        """
        加密，返回最终加密结果 —— 单件 base64 密文包。

        recipient_public_key : 收件人的公钥(谁收信用谁的公钥)
        sender_private_key   : 可选。给了就对密文做 PSS 签名，收方先验签再解密
        """
        if not plaintext:
            raise ValueError("明文不能为空")

        sk = AESGCM.generate_key(bit_length=256)        # ① 随机会话密钥
        nonce = os.urandom(12)                          # ② GCM 的随机数
        ct = AESGCM(sk).encrypt(nonce, plaintext.encode("utf-8"), None)   # ③ 正文加密

        enc_sk = recipient_public_key.encrypt(sk, _oaep())                 # ④ 封装会话密钥

        sig_b64 = ""
        if sender_private_key is not None:
            sig = sender_private_key.sign(ct, _pss(), hashes.SHA256())     # ⑤ 给密文签名
            sig_b64 = b64(sig)

        bundle = {
            "v": 1,                 # 版本号
            "enc_sk": b64(enc_sk),  # 被对方公钥封装的会话密钥（数字信封）
            "nonce": b64(nonce),    # AES-GCM 随机数
            "ct": b64(ct),          # 正文密文（含 GCM 标签）
            "sig": sig_b64,         # 发送方对密文的 PSS 签名（可为空）
        }
        return b64(json.dumps(bundle, ensure_ascii=False).encode("utf-8"))

    # ================= 解密(入参就是那单件) =================
    def decrypt(self, artifact: str, recipient_private_key,
                sender_public_key=None) -> str:
        """
        解密，入参就是加密给出的那串 base64 密文包。

        顺序很重要: 先验签(确认是对方发的、没被改过) -> 再解会话密钥 -> 再还原正文。
        """
        if not artifact:
            raise ValueError("密文包不能为空")

        try:
            bundle = json.loads(ub64(artifact).decode("utf-8"))
            ct = ub64(bundle["ct"])
            nonce = ub64(bundle["nonce"])
            enc_sk = ub64(bundle["enc_sk"])
            sig_b64 = bundle.get("sig", "")
        except (ValueError, KeyError) as e:
            raise ValueError("密文包格式非法，应粘贴加密给出的那串 base64") from e

        if sig_b64:
            if sender_public_key is None:
                raise ValueError("该密文带有签名，但未提供发送方公钥，无法验签")
            try:
                sender_public_key.verify(ub64(sig_b64), ct, _pss(), hashes.SHA256())
            except InvalidSignature as e:
                raise ValueError("签名验证失败：密文被篡改，或不是对方所发") from e

        sk = recipient_private_key.decrypt(enc_sk, _oaep())
        try:
            return AESGCM(sk).decrypt(nonce, ct, None).decode("utf-8")
        except InvalidTag as e:
            raise ValueError("解密失败：密钥不匹配或密文已损坏") from e

    # ================= 独立签名 / 验签 =================
    @staticmethod
    def sign(data: bytes, private_key) -> str:
        """用自己的私钥签名，返回 base64 签名串。"""
        return b64(private_key.sign(data, _pss(), hashes.SHA256()))

    @staticmethod
    def verify(data: bytes, signature_b64: str, public_key) -> bool:
        """用对方的公钥验签。True = 内容确实来自对方且未被篡改。"""
        try:
            public_key.verify(ub64(signature_b64), data, _pss(), hashes.SHA256())
            return True
        except InvalidSignature:
            return False


def run_demo(hao: AsymmetricRSA, message: str) -> None:
    """演示一次完整流程: 生成密钥对 -> 加密成单件 -> 存/读 .vibe -> 验签解密。"""
    print("=" * 68)
    print_safe("明文", message)

    bob_priv, bob_pub = hao.generate_keypair()      # 发送方：私钥用来签名
    alice_priv, alice_pub = hao.generate_keypair()  # 接收方：公钥用来加密
    print(f"密钥对            : RSA-{hao.key_size} ×2 "
          f"(发送方私钥签名 / 接收方公钥加密)")

    artifact = hao.encrypt(message, alice_pub, sender_private_key=bob_priv)
    print(f"最终加密结果(单件): {artifact}")
    print(f"单件长度          : {len(artifact)} 字符 "
          f"(内含: 封装的会话密钥 + nonce + 密文 + 签名)")

    # 密钥文件(.vibe)存取：私钥带口令，公钥明文
    with tempfile.TemporaryDirectory() as tmp:
        priv_path = os.path.join(tmp, "alice" + KEY_SUFFIX)
        pub_path = os.path.join(tmp, "alice" + PUB_SUFFIX)
        hao.save_private_key(alice_priv, priv_path, passphrase="1234")
        hao.save_public_key(alice_pub, pub_path)
        reloaded_priv = hao.load_private_key(priv_path, passphrase="1234")
        reloaded_pub = hao.load_public_key(pub_path)
        print(f"密钥文件          : {os.path.basename(priv_path)} (带口令) / "
              f"{os.path.basename(pub_path)} (明文)")
        print_safe("用载入的密钥解密",
                   hao.decrypt(artifact, reloaded_priv, sender_public_key=bob_pub))

    # 篡改演示：只改密文内容、格式保持合法，看 PSS 验签能不能拦下
    try:
        raw = json.loads(ub64(artifact).decode("utf-8"))
        ct_bytes = bytearray(ub64(raw["ct"]))
        ct_bytes[0] ^= 0x01                       # 翻一个比特，模拟中途被改
        raw["ct"] = b64(bytes(ct_bytes))
        tampered = b64(json.dumps(raw, ensure_ascii=False).encode("utf-8"))
        hao.decrypt(tampered, alice_priv, sender_public_key=bob_pub)
        print("篡改演示          : 未检测到(不应出现)")
    except ValueError as e:
        print(f"篡改演示          : 已拒绝 -> {e}")


def main() -> None:
    hao = AsymmetricRSA()
    print(f"非对称加密: RSA-{hao.key_size} + OAEP(SHA256) + PSS + AES-GCM 混合加密")
    print(f"密钥文件: 私钥 name{KEY_SUFFIX} / 公钥 name{PUB_SUFFIX}  (不喜欢？改 KEY_SUFFIX 一行)")

    if "--demo" in sys.argv:
        run_demo(hao, "举头望明月，低头思故乡 —— 非对称加密测试")
        run_demo(hao, "Hello Asymmetric RSA!")
        print("=" * 68)
        print("私钥永不随文；随文的是被对方公钥封装的会话密钥(数字信封)。")
        return

    # 交互模式: 每次只做一件事，做完即结束
    print("-" * 68)
    print("请选择: 1=生成密钥对  2=加密  3=解密  4=签名  5=验签")
    choice = input("请输入序号: ").strip()

    if choice == "1":
        # 生成密钥对并存成 .vibe 文件
        name = input(f"密钥文件名(不含后缀，默认 mykey): ").strip() or "mykey"
        pwd = input("私钥口令(直接回车=不加口令): ").strip() or None
        priv, pub = hao.generate_keypair()
        p1 = hao.save_private_key(priv, os.path.join(BASE_DIR, name + KEY_SUFFIX), pwd)
        p2 = hao.save_public_key(pub, os.path.join(BASE_DIR, name + PUB_SUFFIX))
        print(f"已生成私钥: {p1}")
        print(f"已生成公钥: {p2}")
        print("提示: 公钥随便发，私钥(和口令)别离开本机；流程到此结束。")
        return

    if choice == "2":
        # 加密: 明文 + 对方公钥 -> 单件密文包
        plain = input("请输入要加密的内容: ").strip()
        if not plain:
            print("[失败] 明文不能为空")
            return
        pub_file = input(f"对方公钥文件名(默认 mykey{PUB_SUFFIX}): ").strip() \
            or ("mykey" + PUB_SUFFIX)
        pub_path = pub_file if os.path.isabs(pub_file) else os.path.join(BASE_DIR, pub_file)
        try:
            pub_key = hao.load_public_key(pub_path)
        except (OSError, ValueError) as e:
            print(f"[失败] 读取公钥失败: {e}")
            return

        sender_priv = None
        if input("是否用自己的私钥签名? (y/n): ").strip().lower() == "y":
            priv_file = input(f"自己的私钥文件名(默认 mykey{KEY_SUFFIX}): ").strip() \
                or ("mykey" + KEY_SUFFIX)
            priv_path = priv_file if os.path.isabs(priv_file) else os.path.join(BASE_DIR, priv_file)
            pwd = input("私钥口令(无口令直接回车): ").strip() or None
            try:
                sender_priv = hao.load_private_key(priv_path, pwd)
            except (OSError, ValueError, TypeError) as e:
                print(f"[失败] 读取私钥失败(口令错了？): {e}")
                return

        try:
            artifact = hao.encrypt(plain, pub_key, sender_private_key=sender_priv)
        except ValueError as e:
            print(f"[失败] {e}")
            return
        print(f"最终加密结果(单件): {artifact}")
        print("提示: 把这一整串发给收方即可；加密流程到此结束。")
        return

    if choice == "3":
        # 解密: 单件密文包 + 自己的私钥 -> 明文
        artifact = input("请输入加密给出的密文包(一整串 base64): ").strip()
        if not artifact:
            print("[失败] 密文包不能为空")
            return
        priv_file = input(f"自己的私钥文件名(默认 mykey{KEY_SUFFIX}): ").strip() \
            or ("mykey" + KEY_SUFFIX)
        priv_path = priv_file if os.path.isabs(priv_file) else os.path.join(BASE_DIR, priv_file)
        pwd = input("私钥口令(无口令直接回车): ").strip() or None
        try:
            priv_key = hao.load_private_key(priv_path, pwd)
        except (OSError, ValueError, TypeError) as e:
            print(f"[失败] 读取私钥失败(口令错了？): {e}")
            return

        sender_pub = None
        if input("密文带签名吗? 要验签吗? (y/n): ").strip().lower() == "y":
            pub_file = input(f"对方公钥文件名(默认 mykey{PUB_SUFFIX}): ").strip() \
                or ("mykey" + PUB_SUFFIX)
            pub_path = pub_file if os.path.isabs(pub_file) else os.path.join(BASE_DIR, pub_file)
            try:
                sender_pub = hao.load_public_key(pub_path)
            except (OSError, ValueError) as e:
                print(f"[失败] 读取公钥失败: {e}")
                return

        try:
            plaintext = hao.decrypt(artifact, priv_key, sender_public_key=sender_pub)
        except ValueError as e:
            print(f"[失败] {e}")
            return
        print_safe("解密还原", plaintext)
        print("提示: 解密流程到此结束。")
        return

    if choice == "4":
        # 签名: 自己的私钥
        text = input("请输入要签名的内容: ").strip()
        if not text:
            print("[失败] 内容不能为空")
            return
        priv_file = input(f"自己的私钥文件名(默认 mykey{KEY_SUFFIX}): ").strip() \
            or ("mykey" + KEY_SUFFIX)
        priv_path = priv_file if os.path.isabs(priv_file) else os.path.join(BASE_DIR, priv_file)
        pwd = input("私钥口令(无口令直接回车): ").strip() or None
        try:
            priv_key = hao.load_private_key(priv_path, pwd)
        except (OSError, ValueError, TypeError) as e:
            print(f"[失败] 读取私钥失败: {e}")
            return
        print(f"签名(base64): {hao.sign(text.encode('utf-8'), priv_key)}")
        print("提示: 把原文 + 这串签名一起发出去；签名流程到此结束。")
        return

    if choice == "5":
        # 验签: 对方的公钥
        text = input("请输入原文: ").strip()
        sig_b64 = input("请输入签名(base64): ").strip()
        pub_file = input(f"对方公钥文件名(默认 mykey{PUB_SUFFIX}): ").strip() \
            or ("mykey" + PUB_SUFFIX)
        pub_path = pub_file if os.path.isabs(pub_file) else os.path.join(BASE_DIR, pub_file)
        try:
            pub_key = hao.load_public_key(pub_path)
        except (OSError, ValueError) as e:
            print(f"[失败] 读取公钥失败: {e}")
            return
        ok = hao.verify(text.encode("utf-8"), sig_b64, pub_key)
        print(f"验签结果: {'通过 —— 内容确实来自对方且未被篡改' if ok else '不通过 —— 内容被改过或不是对方所签'}")
        print("提示: 验签流程到此结束。")
        return

    print("[失败] 未识别的操作序号，请输入 1~5")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Windows 控制台兼容
    except Exception:
        pass
    main()
