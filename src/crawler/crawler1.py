import requests
import bs4
import validators
import chardet
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_page_title(url):
    """
    从给定的URL获取网页标题。

    :param url: 字符串，要抓取的网页的URL
    :return: 字符串，网页的标题；如果请求失败或URL无效，则返回None
    """
    # 检查URL是否为空或无效
    if not url or not validators.url(url):
        logging.error("Invalid URL")
        return None

    # 使用Session以复用TCP连接，提高性能
    session = requests.Session()
    try:
        response = session.get(url, timeout=10)

        '''
        处理HTTP响应并提取页面标题
        
        Args:
            response: HTTP响应对象
            url: 请求的URL地址
            
        Returns:
            str: 页面标题，如果获取失败则返回None
        '''

        # 更细致地处理HTTP响应状态码
        if response.status_code == 200:
            # 使用chardet检测编码
            encoding = chardet.detect(response.content)['encoding']

            # 解析HTML
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding=encoding)

            # 获取页面标题
            title = soup.title.string if soup.title else None
            return title
        elif 300 <= response.status_code < 400:  # 处理重定向
            logging.warning(f"Redirect occurred for URL: {url} with status code: {response.status_code}")
            # 可以选择处理重定向，这里为了保持简单，直接返回None
            return None
        else:
            logging.error(f"Failed to get the page with status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        logging.error(f"An error occurred: {e}")
        return None


if __name__ == '__main__':
    # 测试函数
    url = 'https://www.baidu.com'  # 更换为实际的中文网页URL
    title = get_page_title(url)
    if title:
        print(f"The title of the page is: {title}")
    else:
        print("Failed to get the page title.")
