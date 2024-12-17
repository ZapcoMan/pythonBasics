import requests
from IDCardTools.JsonFileOperator import JsonFileOperator

class QQNumberInfo:
    """
    通过QQ号查询绑定的手机号码可能所在的地区。

    该类使用了一个API来查询QQ号绑定的手机号码的地区信息，并尝试从结果中提取出具体的地理位置。
    然后，它使用一个Json文件中存储的地区与身份证号码的关系，来确定可能的身份证号码地区。
    """

    def __init__(self, regions_file_path):
        """
        初始化QQNumberInfo类。

        参数:
            regions_file_path: 包含地区与身份证号码关系的Json文件路径。
        """
        self.json_operator = JsonFileOperator(regions_file_path)
        self.qq_number = 3232125474
        self.location_of_cell_phone_number = ''

    def qqNumberQueryBindingMobilePhone(self, qq_number):
        """
        通过指定的QQ号查询绑定的手机号码的地区信息。

        参数:
            qq_number: 需要查询的QQ号码。

        返回:
            如果请求成功，返回手机号码的地区信息；否则返回None。
        """
        url = f"https://api.xywlapi.cc/qqapi?qq={qq_number}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get('phonediqu')
            return data
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None

    def extract_location_from_result(self, result):
        """
        从查询结果中提取地理位置信息。

        参数:
            result: 查询到的结果字符串。

        返回:
            提取到的地理位置信息，如果没有找到则返回None。
        """
        if "移动" in result:
            return result.split("移动")[0]
        elif "联通" in result:
            return result.split("联通")[0]
        elif "电信" in result:
            return result.split("电信")[0]
        else:
            return None

    def get_id_card_region(self, location):
        """
        根据提取的地理位置信息找到可能的身份证号码地区。

        参数:
            location: 提取的地理位置信息。

        返回:
            可能的身份证号码地区列表。
        """
        return [key for key, value in self.json_operator.data.items() if location in value]

    def get_id_card_regions(self):
        """
        获取通过QQ号查询到的手机号码可能关联的身份证号码地区。

        返回:
            可能的身份证号码地区列表，如果没有找到则返回空列表。
        """
        result = self.qqNumberQueryBindingMobilePhone(self.qq_number)
        if result:
            self.location_of_cell_phone_number = self.extract_location_from_result(result)
            if self.location_of_cell_phone_number:
                return self.get_id_card_region(self.location_of_cell_phone_number)
        return []

if __name__ == '__main__':
    # 使用示例
    qq_info = QQNumberInfo("regions.json")
    id_card_regions = qq_info.get_id_card_regions()
    print(id_card_regions)
