import json


class JsonFileOperator:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
        self.load()

    def load(self):
        """加载 JSON 文件"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"文件 {self.filename} 不存在，将创建一个新的空文件。")
        except json.JSONDecodeError:
            print(f"文件 {self.filename} 格式错误，将尝试修复或重新创建。")

    def save(self):
        """保存 JSON 文件"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def query(self, key):
        """查询特定键的值"""
        return self.data.get(key, "未找到")

    def add(self, key, value):
        """添加新的键值对"""
        if key not in self.data:
            self.data[key] = value
            return True
        else:
            print(f"键 {key} 已存在，无法添加。")
            return False

    def delete(self, key):
        """删除特定键的值"""
        if key in self.data:
            del self.data[key]
            return True
        else:
            print(f"键 {key} 不存在，无法删除。")
            return False

    def display(self):
        """显示所有内容"""
        for key, value in self.data.items():
            print(f"键: {key}, 值: {value}")


# 使用示例
# if __name__ == "__main__":
#     # 创建一个操作类实例
#     json_operator = JsonFileOperator("regions.json")
#
#     # 查询特定键的值
#     print("查询结果:")
#     print(json_operator.query("142701"))
#
#     # 添加新的键值对
#     print("\n添加新的键值对:")
#     json_operator.add("152627", "内蒙古自治区乌兰察布盟兴和县")
#
#     # 删除特定键的值
#     print("\n删除特定键的值:")
#     json_operator.delete("152627")
#
#     # 显示所有内容
#     print("\n显示所有内容:")
#     json_operator.display()
#
#     # 保存到文件
#     json_operator.save()
