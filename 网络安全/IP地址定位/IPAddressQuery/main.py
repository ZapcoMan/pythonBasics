import requests
import yaml
import json


def get_ip_geolocation(ip_address: str, api_key: str) -> dict:
    """
    获取指定 IP 的地理位置信息。

    通过调用 IP Geolocation API，可以获取到与 IP 地址相关的地理位置信息，如国家、城市、经纬度等。

    参数:
    ip_address (str): 需要查询地理位置信息的 IP 地址。
    api_key (str): 使用 API 服务所需的密钥，用于验证用户身份。

    返回:
    dict: 包含 IP 地址地理位置信息的字典。如果请求失败或发生错误，返回一个空字典。
    """
    # 定义 API 请求的 URL 和参数
    url = "https://api.ipgeolocation.io/v2/ipgeo"
    params = {
        "apiKey": api_key,
        "ip": ip_address
    }

    try:
        # 发起 HTTP GET 请求获取地理位置信息
        response = requests.get(url, params=params, timeout=10)
        # 检查响应状态码，如果状态码表明请求成功，则返回响应的 JSON 数据
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # 如果发生网络请求错误，则打印错误信息并返回一个空字典
        print(f"请求过程中发生错误：{e}")
        return {}


def bulk_query_ips(api_key: str, ips: list):
    """
    批量查询多个 IP 的地理信息。

    参数:
    api_key (str): IP 地理信息查询的 API 密钥。
    ips (list): 需要查询的 IP 地址列表。

    返回:
    list: 查询到的 IP 地理信息列表。
    """
    # 打印 API 密钥以便调试
    print(f"api_key:{api_key}")
    # 构造请求 URL
    url = f"https://api.ipgeolocation.io/v2/ipgeo-bulk?apiKey={api_key}"
    # 将 IP 列表转换为 JSON 格式，准备作为请求负载
    payload = json.dumps({
        "ips": ips
    })
    # 发送 POST 请求以查询 IP 地理信息
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, data=payload, headers=headers, timeout=(10, 30))
        # 如果响应状态码是 200，表示请求成功
        response.raise_for_status()
        # 返回查询结果的 JSON 数据
        return response.json()

    except requests.exceptions.HTTPError as e:
        # 处理 HTTP 错误响应
        if response.status_code == 401:
            print("❌ HTTP 401 错误：API 密钥无效，请检查 apiKey 是否正确。")
        elif response.status_code == 403:
            print("❌ HTTP 403 错误：当前 API 密钥无权限访问此接口。")
        elif response.status_code == 429:
            print("❌ HTTP 429 错误：API 请求频率超过限制，请稍后再试。")
        else:
            print(f"❌ HTTP 请求失败：{e}")
        return []

    except requests.exceptions.RequestException as e:
        # 处理网络请求过程中的其他错误
        print(f"网络请求过程中发生错误：{e}")
        return []



def get_local_country(api_key: str):
    """
    获取调用者所在 IP 的国家名称（无需传入 IP）。

    参数:
    api_key (str): API 的密钥，用于认证用户。

    返回:
    dict: 包含国家名称的字典，如果请求失败或解析错误，则返回空字典。
    """
    # 构建API请求URL，将api_key嵌入到URL中
    url = f"https://api.ipgeolocation.io/v2/ipgeo?apiKey={api_key}"
    # 指定只获取国家名称字段，以减少不必要的数据传输
    params = {"fields": "location.country_name"}
    try:
        # 发起HTTP GET请求，包含超时设置以防止长时间等待
        response = requests.get(url, params=params, timeout=10)
        # 确保请求成功，否则抛出HTTPError异常
        response.raise_for_status()
        # 解析响应的JSON数据并返回
        return response.json()
    except requests.exceptions.RequestException as e:
        # 请求失败时，输出错误信息
        print(f"获取本地国家失败：{e}")
        # 在错误情况下返回空字典
        return {}



def get_specific_fields(api_key: str, ip: str, fields: list):
    """
    查询指定字段的信息（例如 country_name 和 organization）。
    """
    url = f"https://api.ipgeolocation.io/v2/ipgeo?apiKey={api_key}&ip={ip}"
    params = {"fields": ",".join(fields)}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取指定字段失败：{e}")
        return {}


def load_api_key_from_config(config_path: str) -> str:
    """
    从 YAML 配置文件中加载 API 密钥。
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            return config.get('api_key', '')
    except Exception as e:
        print(f"读取配置文件时出错：{e}")
        return ''


def display_geolocation_info(data: dict):
    """
    显示完整的 IP 地理位置信息（英文字段）。
    """
    if not data:
        print("没有可显示的地理信息。")
        return

    location = data.get("location", {})
    network = data.get("network", {}).get("asn", {})

    print("\n🌍 地理位置信息")
    print(f"IP地址: {data.get('ip', '未知')}")
    print(f"大陆代码: {location.get('continent_code', '未知')}")
    print(f"大陆名称: {location.get('continent_name', '未知')}")
    print(f"国家名称: {location.get('country_name', '未知')}")
    print(f"省份/州: {location.get('state_prov', '未知')} ({location.get('state_code', '未知')})")
    print(f"城市: {location.get('city', '未知')}")
    print(f"经纬度: {location.get('latitude', '未知')}, {location.get('longitude', '未知')}")
    print(f"组织信息: {network.get('organization', '未知')}")


def display_bulk_result(results):
    """
    显示批量查询结果。
    """
    if not results:
        print("无批量数据返回。")
        return

    for item in results:
        location = item.get("location", {})
        print(f"{item['ip']}: {location.get('country_name', '未知')}")


def display_local_country_info(data: dict):
    """
    显示本机 IP 所在国家名称。
    """
    if not data:
        print("无法获取本地国家信息。")
        return

    location = data.get("location", {})
    print(f"\n📍 你的 IP 所属国家是：{location.get('country_name', '未知')}")


def display_specific_fields(data: dict):
    """
    显示指定字段的信息。
    """
    if not data:
        print("未找到指定字段信息。")
        return

    location = data.get("location", {})
    network = data.get("network", {}).get("asn", {})

    print(f"\n🔍 指定字段信息")
    print(f"国家名称: {location.get('country_name', '未知')}")
    print(f"组织信息: {network.get('organization', '未知')}")


def get_ip_geolocation_with_lang(ip_address: str, api_key: str, lang: str = "en") -> dict:
    """
    获取指定 IP 的地理位置信息，并以指定语言返回。

    参数:
    ip_address (str): 需要查询的 IP 地址。
    api_key (str): API 密钥。
    lang (str): 返回内容的语言，例如 'en'、'cn'、'ja'、'es'、'de' 等。

    返回:
    dict: 包含地理位置信息的字典，如果请求失败则返回空字典。
    """
    url = "https://api.ipgeolocation.io/v2/ipgeo"
    params = {
        "apiKey": api_key,
        "ip": ip_address,
        "lang": lang  # 设置语言参数
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误：{e}")
        return {}


def display_geolocation_info_cn(data: dict):
    """
    使用中文字段格式化展示 IP 地理位置相关信息。
    """
    if not data:
        print("没有可显示的地理信息。")
        return

    location = data.get("location", {})

    print("\n🌍 地理位置信息（中文）")
    print(f"IP地址: {data.get('ip', '未知')}")
    print(f"大陆名称: {location.get('continent', '未知')}")
    print(f"国家名称: {location.get('country', '未知')}")
    print(f"省份/州: {location.get('region', '未知')} ({location.get('region_code', '未知')})")
    print(f"城市: {location.get('city', '未知')}")
    print(f"邮编: {location.get('zipcode', '未知')}")
    print(f"经纬度: {location.get('latitude', '未知')}, {location.get('longitude', '未知')}")
    print(f"是否欧盟国家: {'是' if location.get('is_eu', False) else '否'}")


def display_geolocation_info_ja(data: dict):
    """
    使用日文字段格式化展示 IP 地理位置相关信息。
    """
    if not data:
        print("地理情報がありません。")
        return

    location = data.get("location", {})

    print("\n🌍 地理位置情報（日本語）")
    print(f"IPアドレス: {data.get('ip', '不明')}")
    print(f"大陸名: {location.get('continent', '不明')}")
    print(f"国名: {location.get('country', '不明')}")
    print(f"都道府県: {location.get('region', '不明')} ({location.get('region_code', '不明')})")
    print(f"都市: {location.get('city', '不明')}")
    print(f"郵便番号: {location.get('zipcode', '不明')}")
    print(f"緯度・経度: {location.get('latitude', '不明')}, {location.get('longitude', '不明')}")
    print(f"EU加盟国: {'はい' if location.get('is_eu', False) else 'いいえ'}")


def display_geolocation_info_es(data: dict):
    """
    使用西班牙语字段格式化展示 IP 地理位置相关信息。
    """
    if not data:
        print("No hay información geográfica disponible.")
        return

    location = data.get("location", {})

    print("\n🌍 Información de Ubicación Geográfica (Español)")
    print(f"Dirección IP: {data.get('ip', 'Desconocida')}")
    print(f"Continente: {location.get('continent', 'Desconocido')}")
    print(f"País: {location.get('country', 'Desconocido')}")
    print(f"Estado/Provincia: {location.get('region', 'Desconocido')} ({location.get('region_code', 'Desconocido')})")
    print(f"Ciudad: {location.get('city', 'Desconocida')}")
    print(f"Código Postal: {location.get('zipcode', 'Desconocido')}")
    print(f"Latitud y Longitud: {location.get('latitude', 'Desconocido')}, {location.get('longitude', 'Desconocido')}")
    print(f"Miembro de la UE: {'Sí' if location.get('is_eu', False) else 'No'}")


def display_geolocation_info_de(data: dict):
    """
    使用德语字段格式化展示 IP 地理位置相关信息。
    """
    if not data:
        print("Keine geografischen Informationen verfügbar.")
        return

    location = data.get("location", {})

    print("\n🌍 Geografische Standortinformationen (Deutsch)")
    print(f"IP-Adresse: {data.get('ip', 'Unbekannt')}")
    print(f"Kontinent: {location.get('continent', 'Unbekannt')}")
    print(f"Land: {location.get('country', 'Unbekannt')}")
    print(f"Bundesland: {location.get('region', 'Unbekannt')} ({location.get('region_code', 'Unbekannt')})")
    print(f"Stadt: {location.get('city', 'Unbekannt')}")
    print(f"Postleitzahl: {location.get('zipcode', 'Unbekannt')}")
    print(f"Breiten- und Längengrad: {location.get('latitude', 'Unbekannt')}, {location.get('longitude', 'Unbekannt')}")
    print(f"EU-Mitglied: {'Ja' if location.get('is_eu', False) else 'Nein'}")


def main_menu(config_path: str):
    """
    命令行主菜单，用户选择功能。
    """
    api_key = load_api_key_from_config(config_path)
    if not api_key:
        print("❌ 未能读取到有效的 API 密钥，请检查 config.yaml 文件。")
        return

    while True:
        print("\n🌐 请选择要执行的操作：")
        print("1 - 查询单个 IP 地理信息")
        print("2 - 批量查询多个 IP 地理信息")
        print("3 - 获取本机 IP 所属国家")
        print("4 - 查询指定字段（国家+组织）+ 支持多语言")
        print("5 - 查询带中文返回的 IP 地理信息")
        print("0 - 退出程序")

        choice = input("请输入选项 (0-5): ")

        if choice == "1":
            ip = input("请输入要查询的 IP 地址: ")
            result = get_ip_geolocation(ip, api_key)
            display_geolocation_info(result)

        elif choice == "2":
            ips_input = input("请输入多个 IP（以空格分隔）: ")
            ips = ips_input.strip().split()
            print(ips)
            results = bulk_query_ips(api_key, ips)
            display_bulk_result(results)

        elif choice == "3":
            result = get_local_country(api_key)
            display_local_country_info(result)

        elif choice == "4":
            ip = input("请输入要查询的 IP 地址: ")
            print("请选择语言：")
            print("1 - English")
            print("2 - 中文")
            print("3 - 日本語")
            print("4 - Español")
            print("5 - Deutsch")
            lang_choice = input("请输入语言编号 (1-5): ")

            lang_map = {
                "1": "en",
                "2": "cn",
                "3": "ja",
                "4": "es",
                "5": "de"
            }

            lang = lang_map.get(lang_choice, "en")
            result = get_ip_geolocation_with_lang(ip, api_key, lang)

            if lang == "en":
                display_geolocation_info(result)
            elif lang == "cn":
                display_geolocation_info_cn(result)
            elif lang == "ja":
                display_geolocation_info_ja(result)
            elif lang == "es":
                display_geolocation_info_es(result)
            elif lang == "de":
                display_geolocation_info_de(result)

        elif choice == "5":
            ip = input("请输入要查询的 IP 地址: ")
            result = get_ip_geolocation_with_lang(ip, api_key, lang="cn")
            display_geolocation_info_cn(result)

        elif choice == "0":
            print("👋 正在退出程序...")
            break

        else:
            print("❌ 无效选项，请重新输入。")


if __name__ == "__main__":
    # 配置文件路径
    config_path = "config.yaml"

    # 启动交互式菜单
    main_menu(config_path)
