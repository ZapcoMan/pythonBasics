import time
import random
import threading
from DrissionPage import ChromiumPage, ChromiumOptions

# 定义要访问的地址列表
urls = [
    "https://m.tb.cn/h.SXh4b8r?tk=wFyP4GssUDH",
]

# 设置刷新次数和间隔
max_refreshes_per_url = 10000  # 每个URL最大刷新次数，防止无限循环
min_interval = 3     # 最小刷新间隔(秒)
max_interval = 10    # 最大刷新间隔(秒)

# 存储每个线程的浏览器实例
browser_instances = {}
browser_lock = threading.Lock()

def create_mobile_chromium_options():
    """
    创建移动端浏览器配置
    """
    co = ChromiumOptions()
    # 使用移动端用户代理
    co.set_user_agent('Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1')
    # 设置窗口大小为iPhone 12 Pro的分辨率
    co.set_argument('--window-size=390,844')
    # 设置设备像素比
    co.set_argument('--device-scale-factor=3')
    # 设置移动浏览器标志
    co.set_argument('--use-mobile-user-agent')
    return co

def refresh_url(url, url_index):
    """
    为单个URL创建浏览器实例并刷新（移动端模式）
    """
    # 创建移动端浏览器配置
    co = create_mobile_chromium_options()

    # 为每个线程创建独立的浏览器实例
    page = ChromiumPage(co)

    # 将浏览器实例存储在全局字典中，以便后续统一关闭
    with browser_lock:
        browser_instances[url_index] = page

    try:
        print(f"[线程 {url_index + 1}] 开始处理URL: {url}")
        print(f"[线程 {url_index + 1}] 使用移动端模式 (iPhone 12 Pro)")

        # 初始访问指定网址
        page.get(url)

        # 等待页面加载
        time.sleep(5)

        # 输出页面标题
        print(f"[线程 {url_index + 1}] 页面标题: {page.title}")

        # 输出当前URL
        print(f"[线程 {url_index + 1}] 当前URL: {page.url}")

        # 为每个URL单独计数刷新次数
        refresh_count = 0

        # 持续刷新页面
        while refresh_count < max_refreshes_per_url:
            # 增加刷新计数
            refresh_count += 1

            # 刷新页面
            page.refresh()

            # 随机等待时间，模拟人类行为
            wait_time = random.randint(min_interval, max_interval)
            time.sleep(wait_time)

            # 输出刷新信息
            print(f"[线程 {url_index + 1}] 第 {refresh_count} 次刷新完成，等待 {wait_time} 秒")

        print(f"[线程 {url_index + 1}] 处理完成，共刷新 {refresh_count} 次")
        return True

    except Exception as e:
        print(f"[线程 {url_index + 1}] 发生错误: {e}")
        return False

# 主程序
if __name__ == "__main__":
    # 创建并启动线程
    threads = []

    for i, url in enumerate(urls):
        thread = threading.Thread(target=refresh_url, args=(url, i))
        threads.append(thread)
        thread.start()
        # 稍微错开启动时间，避免同时访问
        time.sleep(2)

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    # 所有URL处理完成后，统一关闭所有浏览器实例
    print("所有URL处理完成，正在关闭浏览器...")
    with browser_lock:
        for index, browser in browser_instances.items():
            try:
                browser.quit()
                print(f"[浏览器 {index + 1}] 已关闭")
            except Exception as e:
                print(f"[浏览器 {index + 1}] 关闭时发生错误: {e}")

    print("所有浏览器已关闭")
