import requests
import json
import time

def query_chinaz_whois_with_retry(domain_name, max_retries=3):
    """
    查询Chinaz WHOIS信息（带重试机制）

    Args:
        domain_name (str): 要查询的域名
        max_retries (int): 最大重试次数
    """

    for attempt in range(max_retries):
        try:
            # 添加适当的延时避免请求过频
            if attempt > 0:
                time.sleep(2 ** attempt)

            # 生成必要的参数
            ts = "1763423214991"  # 使用实际请求中的时间戳
            rd = "338"  # 从实际请求中获取的固定值
            tk = "cfce623101caff0beed07515dabcdb8d"  # 从实际请求中获取

            # 正确构建包含所有必要参数的URL
            url = f"https://tooldata.chinaz.com/whois/web/api/otherSuffixesPriceData/{domain_name}?ts={ts}&rd={rd}&tk={tk}"

            # 设置完整请求头信息，模拟真实浏览器请求
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/json",
                "Origin": "https://whois.chinaz.com",
                "Referer": f"https://whois.chinaz.com/{domain_name}",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Priority": "u=1, i",
                "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "module": "otherSuffixesPriceData",
                # 添加必要的Cookie信息
                "Cookie": "qHistory=Ly93aG9pcy5jaGluYXouY29tL19XSE9JU+afpeivog==; Hm_lvt_ca96c3507ee04e182fb6d097cb2a1a4c=1763423166; HMACCOUNT=2DE14DCA0545597D; _clck=ulmgro%5E2%5Eg13%5E0%5E2147; cz_statistics_visitor=fe84df37-bace-6025-7260-903119fd425c; JSESSIONID=70C099ED60FCC92D4DD74F7B46510459; _clsk=14xb49s%5E1763423210677%5E3%5E0%5Eb.clarity.ms%2Fcollect; Hm_lpvt_ca96c3507ee04e182fb6d097cb2a1a4c=1763423214"
            }

            # 发送GET请求
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # 检查请求是否成功
                if data.get("module") == "otherSuffixesPriceData":
                    print(f"域名 {domain_name} 的价格数据:")
                    print(json.dumps(data, indent=2, ensure_ascii=False))
                    return data
                else:
                    print(f"第{attempt + 1}次尝试失败:", data)
                    if data.get("code") == 17 and attempt < max_retries - 1:
                        print(f"正在进行第{attempt + 1}次重试...")
                        continue
            else:
                print(f"第{attempt + 1}次尝试HTTP请求失败，状态码:", response.status_code)

        except requests.exceptions.Timeout:
            print(f"第{attempt + 1}次请求超时，正在进行重试...")
            if attempt < max_retries - 1:
                continue
        except requests.exceptions.RequestException as e:
            print(f"第{attempt + 1}次网络请求异常: {e}")
            if attempt < max_retries - 1:
                continue
        except json.JSONDecodeError:
            print("响应数据解析失败")
            break
        except Exception as e:
            print(f"未知错误: {e}")
            break

    print(f"经过{max_retries}次尝试后仍未能成功获取数据")
    return None


if __name__ == "__main__":
    domain = input("请输入要查询的域名（例如 baidu.com）：")
    query_chinaz_whois_with_retry(domain)
