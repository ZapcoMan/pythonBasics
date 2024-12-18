import requests
import json


def get_phone_location(mobile, saorao=True):
    """
    查询手机位置信息

    该函数通过调用外部API接口，获取指定手机号码的位置信息。可以根据需求选择是否查询骚扰号数据。

    参数:
    mobile (str): 需要查询的手机号码。
    saorao (bool, 可选): 是否同时查询该手机号是否为骚扰号，默认为True。

    返回:
    str: 包含手机位置信息的JSON格式字符串。如果查询失败或发生错误，则返回None。
    """
    # 构建请求URL
    url = f"https://api.mir6.com/api/mobile?mobile={mobile}&saorao={str(saorao).lower()}"

    try:
        # 发起GET请求并获取响应
        response = requests.get(url)
        # 检查HTTP请求状态，确保请求成功
        response.raise_for_status()

        # 将响应体中的JSON数据解析为Python字典
        data = response.json()
        # 将解析后的字典转换为格式化的JSON字符串
        data = json.dumps(data, indent=4, ensure_ascii=False)

        # 返回格式化的JSON字符串
        return data
    except requests.RequestException as e:
        # 处理网络请求相关的异常
        print(f"请求错误: {e}")
        return None
    except ValueError as e:
        # 处理JSON解码错误
        print(f"解析JSON数据出错: {e}")
        return None


# 调用函数并打印结果
result = get_phone_location('18923264253', saorao=True)
print(result)
