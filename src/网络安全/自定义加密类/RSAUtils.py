# -*- coding: utf-8 -*-
"""
非对称加密工具类 —— RSAUtils（开箱即用，不用先手动造密钥）

与 AsymmetricRSA.py 的区别:
    AsymmetricRSA.py : 带交互菜单的"演示脚本"，密钥要自己先生成。
    RSAUtils.py      : 纯工具类，只管给别的代码 import 用。
                       调用 encrypt() 时如果没给公钥，它会自动帮你:
                           生成 RSA 密钥对 -> 落到 keys/ 目录 -> 拿公钥加密
                       私钥只留在本机，密文包里只带一个"钥匙名字"(kid)。

自动生成的私钥放哪:
    默认 keys/ 目录下(脚本同级)，文件名形如 auto_20260907_153012_1a2b3c:
        auto_xxx.vibe       私钥(可加口令，打死不外传)
        auto_xxx_pub.vibe   公钥(可以发给任何人)
    解密时不用管文件在哪，decrypt() 会按密文包里的 kid 自己去找。

单次加解密流程(和上一个是同一套算法):
    AES-256-GCM 加密正文 -> RSA-OAEP(收方公钥) 封装会话密钥
    -> PSS(发方私钥) 给密文签名 -> 打包成单件 base64 串

典型用法(三行搞定):
    tool   = RSAUtils()
    packet = tool.encrypt("机密内容")          # 没给公钥 -> 自动生成密钥对
    plain  = tool.decrypt(packet)              # 按 kid 自动找私钥
"""

import base64
import json
import os
import time
import uuid

from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ---------------------------------------------------------------- 约定常量
KEY_SUFFIX = ".vibe"                                   # 私钥文件后缀
PUB_SUFFIX = "_pub" + KEY_SUFFIX                        # 公钥文件后缀
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_DIR = os.path.join(BASE_DIR, "keys")               # 自动生成的密钥默认放这里


# ---------------------------------------------------------------- 小工具
def b64(data: bytes) -> str:
    """字节 -> base64 字符串。"""
    return base64.b64encode(data).decode("ascii")


def ub64(text: str) -> bytes:
    """base64 字符串 -> 字节。"""
    return base64.b64decode(text)


def _oaep():
    """RSA-OAEP 填充(SHA256 + MGF1-SHA256)。"""
    return padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )


def _pss():
    """RSA-PSS 签名(SHA256 + MGF1-SHA256，盐长最大)。"""
    return padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH,
    )


class RSAUtils:
    """
    非对称加密工具类: 自动生成密钥 + OAEP 封装会话密钥 + AES-GCM 加密 + PSS 签名。

    三个最常用方法:
        encrypt(明文)                     -> 单件 base64 密文包(密钥自动造)
        decrypt(密文包)                   -> 明文(私钥自动找)
        sign(数据) / verify(数据, 签名, 公钥)  -> 只签名不加密时用
    """

    def __init__(self, key_dir: str | None = None,
                 key_size: int = 2048,
                 passphrase: str | None = None):
        self.key_dir = key_dir or KEY_DIR     # 密钥存放目录(不存在会自动建)
        self.key_size = key_size              # RSA 位数，生产可用 3072
        self.passphrase = passphrase          # 自动生成的私钥要不要加口令
        self.last_generated: dict | None = None   # 最近一次自动生成的密钥信息
        os.makedirs(self.key_dir, exist_ok=True)

    # ================= 路径 =================
    def private_path(self, name: str) -> str:
        """某个名字对应的私钥文件路径。"""
        return os.path.join(self.key_dir, name + KEY_SUFFIX)

    def public_path(self, name: str) -> str:
        """某个名字对应的公钥文件路径。"""
        return os.path.join(self.key_dir, name + PUB_SUFFIX)

    def list_keys(self) -> list[str]:
        """列出本机已有的私钥名字(不含后缀)。"""
        names = []
        for f in os.listdir(self.key_dir):
            if f.endswith(KEY_SUFFIX) and not f.endswith(PUB_SUFFIX):
                names.append(f[: -len(KEY_SUFFIX)])
        return sorted(names)

    # ================= 密钥生成 / 存取 =================
    def generate_keypair(self):
        """本地生成一对密钥: (私钥, 公钥)。"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
        )
        return private_key, private_key.public_key()

    def save_private_key(self, private_key, path: str,
                         passphrase: str | None = None) -> str:
        """保存私钥(给了口令就加密存储)。"""
        enc = (serialization.BestAvailableEncryption(passphrase.encode("utf-8"))
               if passphrase else serialization.NoEncryption())
        with open(path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=enc,
            ))
        return path

    def save_public_key(self, public_key, path: str) -> str:
        """保存公钥(公开的，不加密)。"""
        with open(path, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ))
        return path

    def load_private_key(self, path: str, passphrase: str | None = None):
        """载入私钥(文件加了口令就必须给口令)。"""
        with open(path, "rb") as f:
            data = f.read()
        pwd = passphrase.encode("utf-8") if passphrase else None
        return serialization.load_pem_private_key(data, password=pwd)

    def load_public_key(self, path: str):
        """载入公钥。"""
        with open(path, "rb") as f:
            data = f.read()
        return serialization.load_pem_public_key(data)

    # ================= 加密(自动生成密钥对) =================
    def encrypt(self, plaintext: str,
                public_key=None,
                key_name: str | None = None,
                sender_private_key=None,
                passphrase: str | None = None) -> str:
        """
        加密，返回单件 base64 密文包。

        public_key  : 收方公钥。不传就自动生成一对并落盘(本类的核心便利点)
        key_name    : 生成/查找用的密钥名字；不传则用 auto_时间戳_随机
        sender_private_key : 可选，传了就对密文做 PSS 签名
        passphrase  : 自动生成私钥时用的口令(不传则用 self.passphrase)
        """
        if not plaintext:
            raise ValueError("明文不能为空")

        kid = key_name or ""
        if public_key is None:
            # 没给公钥 -> 现场造一对，私钥留本机，公钥用于本次加密
            name = key_name or self._auto_name()
            pwd = passphrase if passphrase is not None else self.passphrase
            priv_path = self.private_path(name)
            if os.path.exists(priv_path):
                # 同名密钥已存在 -> 直接复用，别覆盖(覆盖后老密文就解不开了)
                priv = self.load_private_key(priv_path, pwd)
                pub = priv.public_key()
            else:
                priv, pub = self.generate_keypair()
                self.save_private_key(priv, priv_path, pwd)
                self.save_public_key(pub, self.public_path(name))
            self.last_generated = {
                "name": name,
                "private": priv_path,
                "public": self.public_path(name),
            }
            public_key = pub
            kid = name

        sk = AESGCM.generate_key(bit_length=256)                       # ① 会话密钥
        nonce = os.urandom(12)                                         # ② GCM 随机数
        ct = AESGCM(sk).encrypt(nonce, plaintext.encode("utf-8"), None)  # ③ 加密正文
        enc_sk = public_key.encrypt(sk, _oaep())                       # ④ 封装会话密钥

        sig_b64 = ""
        if sender_private_key is not None:
            sig_b64 = b64(sender_private_key.sign(ct, _pss(), hashes.SHA256()))  # ⑤ 签名

        bundle = {
            "v": 1,                 # 版本号
            "kid": kid,             # 密钥名字(只是个文件名提示，不是密钥)
            "enc_sk": b64(enc_sk),  # 被收方公钥封装的会话密钥
            "nonce": b64(nonce),    # AES-GCM 随机数
            "ct": b64(ct),          # 正文密文(含 GCM 标签)
            "sig": sig_b64,         # 发方对密文的签名(可为空)
        }
        return b64(json.dumps(bundle, ensure_ascii=False).encode("utf-8"))

    # ================= 解密(自动找私钥) =================
    def decrypt(self, artifact: str,
                private_key=None,
                key_name: str | None = None,
                passphrase: str | None = None,
                sender_public_key=None) -> str:
        """
        解密，入参就是 encrypt() 给出的那串密文包。

        private_key : 不传则按 key_name / 密文包里的 kid 自动到 key_dir 找私钥
        sender_public_key : 密文带签名时必须给，用来先验签
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
            raise ValueError("密文包格式非法，应传入 encrypt() 给出的整串 base64") from e

        if private_key is None:
            name = key_name or bundle.get("kid", "")
            if not name:
                raise ValueError("未提供私钥，且密文包里没有 kid，无法自动定位私钥")
            pwd = passphrase if passphrase is not None else self.passphrase
            private_key = self.load_private_key(self.private_path(name), pwd)

        if sig_b64:
            if sender_public_key is None:
                raise ValueError("该密文带签名，但未提供发送方公钥，无法验签")
            try:
                sender_public_key.verify(ub64(sig_b64), ct, _pss(), hashes.SHA256())
            except InvalidSignature as e:
                raise ValueError("签名验证失败：密文被篡改，或不是对方所发") from e

        sk = private_key.decrypt(enc_sk, _oaep())
        try:
            return AESGCM(sk).decrypt(nonce, ct, None).decode("utf-8")
        except InvalidTag as e:
            raise ValueError("解密失败：密钥不匹配或密文已损坏") from e

    # ================= 独立签名 / 验签 =================
    def sign(self, data: bytes,
             private_key=None,
             key_name: str | None = None,
             passphrase: str | None = None) -> str:
        """用自己的私钥签名。不传私钥时，按 key_name / 最近生成的密钥自动取。"""
        if private_key is None:
            name = key_name or (self.last_generated or {}).get("name", "")
            if not name:
                raise ValueError("未提供私钥，也没有最近自动生成的密钥")
            pwd = passphrase if passphrase is not None else self.passphrase
            private_key = self.load_private_key(self.private_path(name), pwd)
        return b64(private_key.sign(data, _pss(), hashes.SHA256()))

    @staticmethod
    def verify(data: bytes, signature_b64: str, public_key) -> bool:
        """用对方公钥验签。True = 确实来自对方且未被篡改。"""
        try:
            public_key.verify(ub64(signature_b64), data, _pss(), hashes.SHA256())
            return True
        except InvalidSignature:
            return False

    # ================= 看一眼密文包(不解密) =================
    @staticmethod
    def peek(artifact: str) -> dict:
        """查看密文包元信息: 版本、用的哪把钥匙、有没有签名、密文多长。"""
        try:
            bundle = json.loads(ub64(artifact).decode("utf-8"))
        except ValueError as e:
            raise ValueError("密文包格式非法") from e
        return {
            "version": bundle.get("v"),
            "kid": bundle.get("kid", ""),        # 只是密钥文件名的提示
            "signed": bool(bundle.get("sig")),
            "cipher_bytes": len(ub64(bundle["ct"])),
            "artifact_chars": len(artifact),
        }

    @staticmethod
    def _auto_name() -> str:
        """自动生成密钥名: auto_日期时间_随机串。"""
        return "auto_" + time.strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]


if __name__ == "__main__":
    # 工具类自检: 造临时目录跑一遍，不污染项目
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        tool = RSAUtils(key_dir=tmp)
        packet = tool.encrypt("自动生成密钥对并加密 —— 工具类自检")
        print("密文包信息:", tool.peek(packet))
        print("密文包全文:", packet)
        print("本机私钥  :", tool.list_keys())
        print("解密还原  :", tool.decrypt(packet))
        sig = tool.sign(b"contract text")
        print("签名验签  :", tool.verify(b"contract text", sig,
                                         tool.load_public_key(
                                             tool.public_path(tool.last_generated["name"]))))
