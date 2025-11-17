import requests
import json
import time

def query_whois(domain_name):
    url = f"https://whois.aliyun.com/whois/api_whois_info?domainName={domain_name}&umToken=whois-web-hichina-com%3Ab7d9aea42bbf7f276f79766fa8d0b876&_={int(time.time() * 1000)}"

    # 完善请求头信息，模拟真实浏览器请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"https://whois.aliyun.com/domain/{domain_name}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=1, i"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                module = data["module"]
                print(f"域名: {module['domainName']}")
                print(f"注册商: {module['registrar']}")
                print(f"注册商URL: {module['registrarURL']}")
                print(f"创建日期: {module['standardFormatCreationDate']}")
                print(f"到期日期: {module['standardFormatExpirationDate']}")
                print(f"最后更新: {module['formatUpdatedDate']}")
                print(f"Name Servers:")
                for ns in module["nameServers"]:
                    print(f"  - {ns}")
                print("\n状态列表:")
                for item in module["statusInfos"]:
                    if 'desc' in item and 'tip' in item:
                        print(f"  [{item['status']}]: {item['desc']} ({item['tip']})")
            else:
                print("请求失败：", data.get("message", "未知错误"))
        else:
            print("HTTP 请求失败，状态码:", response.status_code)

    except requests.exceptions.Timeout:
        print("请求超时，请检查网络连接")
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {e}")
    except json.JSONDecodeError:
        print("响应数据解析失败")
    except Exception as e:
        print(f"未知错误: {e}")

if __name__ == "__main__":
    domain = input("请输入要查询的域名（例如 baidu.com）：")
    query_whois(domain)
