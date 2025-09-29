import time
import random
import threading
from DrissionPage import ChromiumPage

# 定义要访问的地址列表
urls = [
    "https://www.goofish.com/item?id=978882160967&spm=widle.12011849.0.0&ut_sk=",
    "https://www.goofish.com/item?id=976990295214&spm=widle.12011849.0.0&ut_sk=",
    "https://www.goofish.com/item?id=976991963358&spm=widle.12011849.0.0&ut_sk="
]

# 设置刷新次数和间隔
max_refreshes_per_url = 10  # 每个URL最大刷新次数，防止无限循环
min_interval = 10     # 最小刷新间隔(秒)
max_interval = 15    # 最大刷新间隔(秒)

# 存储每个线程的浏览器实例
browser_instances = {}
browser_lock = threading.Lock()

def refresh_url(url, url_index):
    """
    为单个URL创建浏览器实例并刷新
    """
    # 为每个线程创建独立的浏览器实例
    page = ChromiumPage()

    # 将浏览器实例存储在全局字典中，以便后续统一关闭
    with browser_lock:
        browser_instances[url_index] = page

    try:
        print(f"[线程 {url_index + 1}] 开始处理URL: {url}")

        # 初始访问指定网址
        page.get(url)

        # 等待页面加载
        time.sleep(5)

        # 输出页面标题
        print(f"[线程 {url_index + 1}] 页面标题: {page.title}")

        # 输出当前URL
        print(f"[线程 {url_index + 1}] 当前URL: {page.url}")

        # 为每个URL保存初始截图
        initial_screenshot_name = f'goofish_item_page_url{url_index + 1}.png'
        page.get_screenshot(path=initial_screenshot_name)
        print(f"[线程 {url_index + 1}] 初始页面截图已保存为 {initial_screenshot_name}")

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

            # 可选：每隔10次刷新保存一次截图
            if refresh_count % 10 == 0:
                screenshot_name = f'goofish_item_page_url{url_index + 1}_refresh_{refresh_count}.png'
                page.get_screenshot(path=screenshot_name)
                print(f"[线程 {url_index + 1}] 第 {refresh_count} 次刷新后截图已保存为 {screenshot_name}")

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
