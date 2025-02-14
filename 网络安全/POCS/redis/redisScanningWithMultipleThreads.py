# -*- coding: utf-8 -*-
# @Time    : 14 2月 2025 10:05 下午
# @Author  : codervibe
# @File    : redisScanningWithMultipleThreads.py
# @Project : pythonBasics
import concurrent.futures

from 网络安全.POCS.redis.redisScan import scan_port


def start_scan():
    """
    启动多线程扫描
    """
    # 从文件读取目标IP列表（示例路径）
    with open('ip_list.txt', 'r') as f:
        targets = [line.strip() for line in f]

    # 创建线程池（建议不超过50个线程）
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # 提交扫描任务到线程池
        futures = [executor.submit(scan_port, ip) for ip in targets]

        # 等待所有任务完成
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"扫描异常: {str(e)}")
