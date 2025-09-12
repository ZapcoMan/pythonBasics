import requests
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 定义请求参数
API_URL = "http://181.cdn.zcapi.cc.cdn.cloudflare.net/api/submit.php"
BASE_PARAMS = {
    "yqr": "20021"
}

# 设置请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Host": "181.cdn.zcapi.cc.cdn.cloudflare.net",
    "Referer": "http://181.cdn.zcapi.cc.cdn.cloudflare.net/l12/?yqr=20021&bj=https%3A%2F%2Fwx.y.gtimg.cn%2Fmusic%2Fphoto_new%2FT053XD00003lMc702x1l9e.jpg&url=http%3A%2F%2F5ucuCA.img.kk.qqapi.cc.cdn.cloudflare.net%2Fuploads%2Fasia%2F20250911125749_1552a0eb.jpg&smsType=1",
    "X-Requested-With": "XMLHttpRequest"
}

# 中国主要手机号号段前缀
PHONE_PREFIXES = [
    # 移动号段
    134, 135, 136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159,
    178, 182, 183, 184, 187, 188, 195, 197, 198,
    # 联通号段
    130, 131, 132, 145, 155, 156, 166, 175, 176, 185, 186, 196,
    # 电信号段
    133, 149, 153, 162, 173, 177, 180, 181, 189, 191, 193, 199,
    # 虚拟运营商号段
    170, 171, 165, 167
]

# 统计变量
stats = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0
}

# 线程锁，用于保护统计变量
stats_lock = threading.Lock()

def generate_random_phone():
    """
    生成随机手机号码

    :return: 随机生成的手机号码字符串
    """
    prefix = random.choice(PHONE_PREFIXES)
    # 剩余8位数字随机生成
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    return str(prefix) + suffix

def send_api_request(url, params, headers, request_id=None):
    """
    发送API请求

    :param url: 请求的URL
    :param params: 请求参数字典
    :param headers: 请求头字典
    :param request_id: 请求标识符（用于多线程时区分不同请求）
    :return: (response, success) 其中success表示请求是否成功
    """
    try:
        # 发送GET请求
        response = requests.get(url, params=params, headers=headers, timeout=10)

        # 输出响应信息
        thread_id = threading.current_thread().name
        identifier = f"[{request_id}] " if request_id else ""

        # 判断请求是否成功（状态码为200系列）
        success = 200 <= response.status_code < 300

        print(f"{identifier}线程 {thread_id}: 请求URL: {response.url}")
        print(f"{identifier}线程 {thread_id}: 状态码: {response.status_code} ({'成功' if success else '失败'})")

        # 如果响应是JSON格式，也可以解析JSON
        if response.headers.get('content-type', '').startswith('application/json'):
            print(f"{identifier}线程 {thread_id}: JSON数据: {response.json()}")
        else:
            print(f"{identifier}线程 {thread_id}: 响应内容长度: {len(response.text)} 字符")

        return response, success

    except requests.exceptions.RequestException as e:
        thread_id = threading.current_thread().name
        identifier = f"[{request_id}] " if request_id else ""
        print(f"{identifier}线程 {thread_id}: 请求发生错误: {e}")
        return None, False

def send_single_request(request_id):
    """
    发送单个请求（用于多线程调用）

    :param request_id: 请求标识符
    :return: 请求是否成功
    """
    # 为每次请求生成随机手机号
    params = BASE_PARAMS.copy()
    params["phone"] = generate_random_phone()

    response, success = send_api_request(API_URL, params, HEADERS, request_id)

    # 更新统计信息
    with stats_lock:
        stats["total_requests"] += 1
        if success:
            stats["successful_requests"] += 1
        else:
            stats["failed_requests"] += 1

    return success

def send_requests_multithreaded(num_requests, max_workers=5):
    """
    使用多线程发送多个请求

    :param num_requests: 要发送的请求数量
    :param max_workers: 最大线程数
    """
    print(f"开始发送 {num_requests} 个请求，最大线程数: {max_workers}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_request_id = {
            executor.submit(send_single_request, i): i
            for i in range(1, num_requests + 1)
        }

        # 处理完成的任务
        successful_tasks = 0
        failed_tasks = 0

        for future in as_completed(future_to_request_id):
            request_id = future_to_request_id[future]
            try:
                success = future.result()
                if success:
                    successful_tasks += 1
                else:
                    failed_tasks += 1
                print(f"[{request_id}] 请求完成 - {'成功' if success else '失败'}")
            except Exception as e:
                failed_tasks += 1
                print(f"[{request_id}] 请求异常: {e}")

    return successful_tasks, failed_tasks

def print_statistics():
    """
    打印请求统计信息
    """
    print("\n=== 请求统计 ===")
    print(f"总请求数: {stats['total_requests']}")
    print(f"成功请求数: {stats['successful_requests']}")
    print(f"失败请求数: {stats['failed_requests']}")

    if stats['total_requests'] > 0:
        success_rate = (stats['successful_requests'] / stats['total_requests']) * 100
        print(f"成功率: {success_rate:.2f}%")

def reset_statistics():
    """
    重置统计信息
    """
    with stats_lock:
        stats["total_requests"] = 0
        stats["successful_requests"] = 0
        stats["failed_requests"] = 0

if __name__ == "__main__":
    # 重置统计信息
    reset_statistics()

    # 使用线程池方式发送10个并发请求
    print("=== 使用线程池方式 ===")
    successful, failed = send_requests_multithreaded(num_requests=9000, max_workers=200)

    # 打印统计信息
    print_statistics()

    # 重置统计信息
    reset_statistics()


