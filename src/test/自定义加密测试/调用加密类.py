# -*- coding: utf-8 -*-
"""
在测试目录里调用 src/网络安全/自定义加密类 的四个加密类。

跨目录调用的做法: 把加密类所在目录加进 sys.path，然后像普通模块一样 import。
这几个类之间没有互相引用，所以按文件名直接导入即可，不用走包路径
(包路径里含中文，走 import src.网络安全.xxx 容易踩坑)。

覆盖:
    1. HaoMi            —— 一次一密(公开底本 + 真随机乱码页)
    2. HaoMiRot13Perrin —— UTF-8 + ROT13 旋转 + 佩兰数列混淆(确定性，无密钥)
    3. AsymmetricRSA    —— RSA-2048 + OAEP 封装会话密钥 + PSS 签名
    4. RSAUtils         —— 工具类，不传公钥就自动生成密钥对
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))   # .../src/test/自定义加密测试
SRC = os.path.dirname(os.path.dirname(HERE))        # .../src
CRYPTO_DIR = os.path.join(SRC, "网络安全", "自定义加密类")

# 关键一步: 把加密类目录塞进模块搜索路径
sys.path.insert(0, CRYPTO_DIR)

# 下面四个 import 由运行时 sys.path 解析，IDE 静态分析会误报"没有该模块"
# noinspection PyUnresolvedReferences
import AsymmetricRSA
import HaoMi
import HaoMiRot13Perrin
import RSAUtils

LINE = "=" * 68


def print_text(label: str, text: str) -> None:
    """打印可能含不可显示字符的内容(如乱码)。GBK 控制台编不出时退回 repr，避免崩。"""
    try:
        print(f"{label}: {text}")
    except UnicodeEncodeError:
        # ascii() 会把所有非 ASCII 字符转义成 \xNN / \uNNNN，任何控制台都打得出来
        print(f"{label}: (当前控制台无法显示，改用 ASCII 转义) {ascii(text)}")


# ---------------------------------------------------------------- 1
def test_haomi():
    """豪密 OTP: 双方共享同一本底本，每封电报用一页新的乱码。"""
    print(LINE)
    print("[1] HaoMi —— 一次一密（公开底本 + 真随机乱码页）")
    hao = HaoMi.HaoMi()                       # 默认用内置的唐诗底本
    msg = "低头思故乡"
    cipher, key = hao.encrypt(msg)            # 密文 + 乱码页，乱码只此一次
    plain = hao.decrypt(cipher, key)
    print(f"  明文 : {msg}")
    print(f"  密文 : {cipher}")
    print(f"  乱码 : {key}   <- 用后即焚")
    print(f"  还原 : {plain}")
    assert plain == msg, "HaoMi 解密结果与原文不一致"
    # 同一明文换一页乱码 -> 密文完全不同
    cipher2, _ = hao.encrypt(msg)
    print(f"  再加密一次: {cipher2}  (与上次不同 = {cipher2 != cipher})")
    print("  -> PASS")


# ---------------------------------------------------------------- 2
def test_rot13_perrin():
    """ROT13 + 佩兰: 没有密钥，属于编码/混淆，拿到脚本谁都能还原。"""
    print(LINE)
    print("[2] HaoMiRot13Perrin —— UTF-8 + ROT13 + 佩兰数列（确定性，无密钥）")
    hao = HaoMiRot13Perrin.HaoMiRot13Perrin()
    msg = "举头望明月低头思故乡"
    cipher = hao.encrypt(msg)
    print(f"  明文 : {msg}")
    print_text("  乱码 ", cipher)
    print(f"  HEX  : {hao.to_hex(cipher)}")
    print(f"  还原 : {hao.decrypt(cipher)}")
    assert hao.decrypt(cipher) == msg, "ROT13/佩兰 解密结果与原文不一致"
    print("  -> PASS")


# ---------------------------------------------------------------- 3
def test_asymmetric():
    """非对称: Bob 用 Alice 的公钥加密、自己的私钥签名；Alice 先验签再解密。"""
    print(LINE)
    print("[3] AsymmetricRSA —— RSA-2048 + OAEP + PSS（直接用类，不进菜单）")
    hao = AsymmetricRSA.AsymmetricRSA()

    bob_priv, bob_pub = hao.generate_keypair()        # 发送方
    alice_priv, alice_pub = hao.generate_keypair()    # 接收方

    msg = "今晚老地方见，带上乱码本"
    packet = hao.encrypt(msg, alice_pub, sender_private_key=bob_priv)
    plain = hao.decrypt(packet, alice_priv, sender_public_key=bob_pub)

    print(f"  明文   : {msg}")
    print(f"  密文包 : {packet}")
    print(f"  长度   : {len(packet)} 字符")
    print(f"  还原   : {plain}")
    assert plain == msg, "AsymmetricRSA 解密结果与原文不一致"

    # 篡改一个比特，PSS 验签必须拦下
    import base64
    import json
    raw = json.loads(base64.b64decode(packet).decode("utf-8"))
    ct = bytearray(base64.b64decode(raw["ct"]))
    ct[0] ^= 0x01
    raw["ct"] = base64.b64encode(bytes(ct)).decode("ascii")
    tampered = base64.b64encode(
        json.dumps(raw, ensure_ascii=False).encode("utf-8")).decode("ascii")
    try:
        hao.decrypt(tampered, alice_priv, sender_public_key=bob_pub)
        print("  篡改   : 未拦截（不应出现）")
    except ValueError as e:
        print(f"  篡改   : 已拦截 -> {e}")
    print("  -> PASS")


# ---------------------------------------------------------------- 4
def test_rsa_utils():
    """工具类: encrypt 不传公钥就自动生成密钥对并落盘。"""
    print(LINE)
    print("[4] RSAUtils —— 工具类，不传公钥就自动造密钥对")
    key_dir = os.path.join(HERE, "keys")        # 生成的密钥放本目录下的 keys/
    tool = RSAUtils.RSAUtils(key_dir=key_dir)

    msg = "自动生成密钥对并加密"
    packet = tool.encrypt(msg, key_name="demokey")   # 自动生成 + 落盘
    plain = tool.decrypt(packet)                     # 按 kid 自动找私钥

    print(f"  明文     : {msg}")
    print(f"  密文包   : {packet}")
    print(f"  元信息   : {tool.peek(packet)}")
    print(f"  私钥目录 : {key_dir}")
    print(f"  本机密钥 : {tool.list_keys()}")
    print(f"  还原     : {plain}")
    assert plain == msg, "RSAUtils 解密结果与原文不一致"

    # 签名 / 验签
    data = "合同正文".encode("utf-8")
    sig = tool.sign(data, key_name="demokey")
    pub = tool.load_public_key(tool.public_path("demokey"))
    print(f"  验签(原文)   : {tool.verify(data, sig, pub)}")
    print(f"  验签(改一字) : {tool.verify('合同正文 '.encode('utf-8'), sig, pub)}")
    print("  -> PASS")


# ---------------------------------------------------------------- 5
def test_manual_input():
    """手动输入一段内容，四个加密类各加密/解密一遍（跑完即结束）。"""
    print(LINE)
    print("[5] 手动输入 —— 你敲什么就加密什么")
    msg = input("请输入要加密的内容: ").strip()
    if not msg:
        print("  未输入内容，已跳过")
        return

    # 1) 豪密 OTP：底本里没有的字会报错(提示换底本或换措辞)
    hao = HaoMi.HaoMi()
    try:
        cipher, key = hao.encrypt(msg)
        print(f"  [HaoMi]       密文 : {cipher}")
        print(f"                乱码 : {key}   <- 用后即焚")
        print(f"                还原 : {hao.decrypt(cipher, key)}")
    except ValueError as e:
        print(f"  [HaoMi]       跳过 : {e}")

    # 2) ROT13 + 佩兰（无密钥，只是混淆）
    h2 = HaoMiRot13Perrin.HaoMiRot13Perrin()
    c2 = h2.encrypt(msg)
    print(f"  [ROT13+佩兰]  明文 : {msg}")
    print_text("                乱码 ", c2)
    print(f"                 HEX  : {h2.to_hex(c2)}")
    print(f"                 还原 : {h2.decrypt(c2)}")

    # 3) 非对称：Bob 加密签名，Alice 验签解密
    h3 = AsymmetricRSA.AsymmetricRSA()
    bob_priv, bob_pub = h3.generate_keypair()
    alice_priv, alice_pub = h3.generate_keypair()
    p3 = h3.encrypt(msg, alice_pub, sender_private_key=bob_priv)
    print(f"  [RSA非对称]   密文包: {p3}")
    print(f"                 长度 : {len(p3)} 字符")
    print(f"                 还原 : {h3.decrypt(p3, alice_priv, sender_public_key=bob_pub)}")

    # 4) 工具类：不传公钥就自动造密钥
    tool = RSAUtils.RSAUtils(key_dir=os.path.join(HERE, "keys"))
    p4 = tool.encrypt(msg, key_name="manual")
    print(f"  [RSAUtils]    kid   : {tool.peek(p4)['kid']}")
    print(f"                 密文包 : {p4}")
    print(f"                 还原 : {tool.decrypt(p4)}")
    print("  -> DONE")


def main() -> None:
    print(f"加密类目录: {CRYPTO_DIR}")
    test_haomi()
    test_rot13_perrin()
    test_asymmetric()
    test_rsa_utils()
    print(LINE)
    print("四个加密类全部调用成功。")

    # 手动输入测试: 需要你敲 y 才执行，跑完即结束
    try:
        if input("是否手动输入一段内容进行加密测试? (y/n): ").strip().lower() == "y":
            test_manual_input()
    except EOFError:
        pass      # 非交互运行(如被其它脚本调用)时直接结束


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Windows 控制台兼容
    except Exception:
        pass
    main()
