from src.网络安全.社工.IDCardTools.IDCardTools import IDCardTool
from src.网络安全.社工.IDCardTools.QQNumberInfo import QQNumberInfo

if __name__ == "__main__":
    # 使用示例
    # 创建QQ号码信息对象，加载地区数据文件并指定QQ号码
    qq_info = QQNumberInfo("regions.json", 3164866298)

    # 获取该QQ号码对应的身份证地区信息
    id_card_regions = qq_info.get_id_card_regions()

    # 打印身份证地区信息
    print(id_card_regions)

    # 创建IDCardTool工具类实例
    tool = IDCardTool()
    # 初始化身份证前缀、姓名、性别变量
    idcard_prefix = ""
    name = ""
    gender = ""
    # 调用工具类的run方法处理身份证信息
    tool.run(idcard_prefix, name, gender)

