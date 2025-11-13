import urllib.request
import urllib.parse
from urllib.parse import unquote

# 解码URL参数
encoded_sv = "ZXlKaFkzUWlPaUp6ZGlJc0ltUmhkR0VpT25zaWRYTmxjaUk2SWpZek5USTVPRFUySWl3aWNHRnpjeUk2SW1kb2FtdHNiVzVpZG1wa0luMTk%3D"
decoded_sv = unquote(encoded_sv)
print(decoded_sv)
# 构建完整的URL
url = f"https://ev.gaysnboys.com/app/data.php?sv={decoded_sv}"

# 创建请求对象
req = urllib.request.Request(url)

# 设置请求头
req.add_header("Sec-Ch-Ua-Platform", '"Windows"')
req.add_header("X-Requested-With", "XMLHttpRequest")
req.add_header("Accept-Language", "zh-CN,zh;q=0.9")
req.add_header("Accept", "*/*")
req.add_header("Sec-Ch-Ua", '"Chromium";v="139", "Not;A=Brand";v="99"')
req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")
req.add_header("Sec-Ch-Ua-Mobile", "?0")
req.add_header("Sec-Fetch-Site", "same-origin")
req.add_header("Sec-Fetch-Mode", "cors")
req.add_header("Sec-Fetch-Dest", "empty")
req.add_header("Referer", "https://ev.gaysnboys.com/step_in/")
req.add_header("Accept-Encoding", "gzip, deflate, br")
req.add_header("Priority", "u=1, i")

# 添加Cookie
req.add_header("Cookie", "PHPSESSID=d344578e1494054e3002cd3ac4dba112")

# 发送请求
# 发送HTTP请求并处理响应数据
# 参数:
#     req: urllib.request.Request对象，包含请求的URL和相关配置
# 返回值:
#     无返回值，直接打印响应数据或错误信息
try:
    # 发送HTTP请求并获取响应
    with urllib.request.urlopen(req) as response:
        data = response.read().decode('utf-8')
        print(f"Status Code: {response.getcode()}")
        print(f"Response Content: {data}")

# 捕获HTTP错误异常并打印错误信息
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}")

