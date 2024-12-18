# 导入ChromiumOptions类，用于配置Chrome浏览器的路径
from DrissionPage import ChromiumOptions

# 设置Chrome浏览器的路径
path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

# 创建ChromiumOptions对象，设置浏览器路径，并保存配置
ChromiumOptions().set_browser_path(path).save()
