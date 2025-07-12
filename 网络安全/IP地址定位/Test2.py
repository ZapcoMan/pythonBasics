import requests

def get_ip_geolocation(ip_address: str) -> dict:
    """
    获取 IP 的地理位置信息，并返回解析后的字典数据。
    :param ip_address: 要查询的 IP 地址
    :return: 包含 IP 地理位置信息的字典，若失败则返回空字典
    """
    api_url = f'http://ip-api.com/json/{ip_address}'

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # 抛出 HTTP 错误
        ip_info = response.json()

        if ip_info.get('status') != 'success':
            print("API 返回状态异常")
            return {}

        # 输出关键信息
        print(f"状态: {ip_info.get('status', '未知')}")
        print(f"国家: {ip_info.get('country', '未知')}")
        print(f"省份: {ip_info.get('regionName', '未知')}")
        print(f"城市: {ip_info.get('city', '未知')}")
        print(f"坐标: {ip_info.get('lat', '未知')}, {ip_info.get('lon', '未知')}")
        print(f"网络服务提供商: {ip_info.get('isp', '未知')}")

        return ip_info

    except requests.RequestException as e:
        print(f"请求过程中发生错误：{e}")
        return {}
