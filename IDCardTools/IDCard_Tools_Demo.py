# 示例调用
from IDCardTools.IDCardTools import IDCardTool
from IDCardTools.QQNumberInfo import QQNumberInfo

if __name__ == "__main__":
    # 使用示例
    qq_info = QQNumberInfo("regions.json")
    id_card_regions = qq_info.get_id_card_regions()
    print(id_card_regions)

    tool = IDCardTool()
    idcard_prefix = "37152619990604"
    name = "朱振宇"
    gender = "女"
    tool.run(idcard_prefix, name, gender)