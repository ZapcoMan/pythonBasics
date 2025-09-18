import time
import random
from DrissionPage import ChromiumPage

# 实例化浏览器对象
page = ChromiumPage()

# 设置要访问的地址列表
urls = [
    "https://www.goofish.com/item?id=978882160967&spm=widle.12011849.0.0&ut_sk=",
    "https://www.goofish.com/item?id=976990295214&spm=widle.12011849.0.0&ut_sk=",
    "https://www.goofish.com/item?id=976991963358&spm=widle.12011849.0.0&ut_sk="
]

# 设置刷新次数和间隔
max_refreshes_per_url = 100  # 每个URL最大刷新次数，防止无限循环
min_interval = 3     # 最小刷新间隔(秒)
max_interval = 10    # 最大刷新间隔(秒)

try:
    # 遍历每个URL
    for url_index, url in enumerate(urls):
        print(f"\n开始处理第 {url_index + 1} 个URL: {url}")

        # 访问指定网址
        page.get(url)

        # 等待页面加载
        time.sleep(5)

        # 输出页面标题
        print(f"页面标题: {page.title}")

        # 输出当前URL
        print(f"当前URL: {page.url}")

        # 为每个URL保存初始截图
        initial_screenshot_name = f'goofish_item_page_url{url_index + 1}.png'
        page.get_screenshot(path=initial_screenshot_name)
        print(f"初始页面截图已保存为 {initial_screenshot_name}")

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
            print(f"URL {url_index + 1} - 第 {refresh_count} 次刷新完成，等待 {wait_time} 秒")

            # 可选：每隔10次刷新保存一次截图
            if refresh_count % 10 == 0:
                screenshot_name = f'goofish_item_page_url{url_index + 1}_refresh_{refresh_count}.png'
                page.get_screenshot(path=screenshot_name)
                print(f"第 {refresh_count} 次刷新后截图已保存为 {screenshot_name}")

        print(f"URL {url_index + 1} 处理完成，共刷新 {refresh_count} 次\n")

finally:
    # 关闭浏览器
    page.quit()
    print(f"浏览器已关闭，所有URL处理完成")
