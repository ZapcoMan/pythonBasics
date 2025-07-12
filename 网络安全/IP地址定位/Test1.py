import requests


def get_ip_geolocation(ip_address):
    """
    获取 IP 地理位置信息。

    使用 DB-IP 的免费 API 查询指定 IP 地址的地理位置信息，并打印出来。

    参数:
    ip_address (str): 需要查询地理位置信息的 IP 地址。

    返回:
    无返回值。如果请求失败，将打印错误信息并返回 None。
    """
    # 构造请求 URL
    url = f"https://api.db-ip.com/v2/free/{ip_address}"

    try:
        # 发送 HTTP GET 请求
        response = requests.get(url)
        # 检查是否有 HTTP 错误
        response.raise_for_status()

        # 解析 JSON 响应
        geolocation_data = response.json()
        # 遍历并打印地理位置信息
        for key, value in geolocation_data.items():
            print(f"{key}: {value}")
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        print(f"请求失败: {e}")
        return None

