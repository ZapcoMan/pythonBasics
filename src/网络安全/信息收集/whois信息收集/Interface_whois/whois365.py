import requests
from bs4 import BeautifulSoup
import re

def query_domain_whois(domain_name):
    """
    查询域名的WHOIS信息并解析HTML结果
    """
    url = f"https://whois365.com/cn/domain/{domain_name}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://whois365.com/cn/",
        "Cache-Control": "no-cache"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # 解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')

            # 检查是否需要验证码
            captcha_form = soup.find('form', id='captchaform')
            if captcha_form:
                print("网站要求输入验证码，请稍后重试或手动访问网站")
                return None

            # 提取域名信息
            domain_info = soup.find('div', id='domain-info')
            if domain_info:
                domain_items = domain_info.find_all('li')
                print("=== 域名基本信息 ===")
                for item in domain_items:
                    print(item.get_text(strip=True))

            # 提取WHOIS结果
            whois_result = soup.find('div', id='whois-result')
            if whois_result:
                print("\n=== WHOIS详细信息 ===")

                # 查找包含原始WHOIS数据的p标签
                whois_paragraphs = whois_result.find_all('p')
                for p in whois_paragraphs:
                    # 跳过通知和广告类段落
                    if p.get('class') and 'notice' in p.get('class'):
                        continue

                    # 获取文本内容
                    whois_content = p.get_text('\n').strip()
                    if whois_content and len(whois_content) > 50:  # 过滤太短的内容
                        print(whois_content)

                        # 解析关键字段
                        extract_key_info(whois_content)
                        break

            return response.text
        else:
            print(f"请求失败，状态码: {response.status_code}")
    except requests.exceptions.Timeout:
        print("请求超时，请检查网络连接")
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {e}")
    except Exception as e:
        print(f"解析异常: {e}")

def extract_key_info(whois_text):
    """
    从WHOIS文本中提取关键信息
    """
    print("\n=== 关键信息提取 ===")

    # 常见的关键字段模式
    patterns = {
        '注册商': r'Registrar:\s*(.+)',
        '创建日期': r'Creation Date:\s*(.+)',
        '过期日期': r'Expiration Date:\s*(.+)',
        '更新日期': r'Updated Date:\s*(.+)',
        '域名状态': r'Status:\s*(.+)',
        '注册人': r'Registrant Organization:\s*(.+)'
    }

    found_any = False
    for key, pattern in patterns.items():
        match = re.search(pattern, whois_text, re.IGNORECASE)
        if match:
            print(f"{key}: {match.group(1).strip()}")
            found_any = True

    if not found_any:
        print("未找到标准格式的关键信息")

if __name__ == "__main__":
    domain = input("请输入要查询的域名（例如 baidu.com）：")
    query_domain_whois(domain)
