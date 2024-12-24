class Student:
    def __init__(self, name: str, age: int):
        """
        构造函数，初始化Student对象的姓名和年龄。
        :param name: 学生的姓名，必须为字符串。
        :param age: 学生的年龄，必须为正整数。
        """
        if not isinstance(name, str):
            raise ValueError("姓名必须为字符串")
        if not isinstance(age, int) or age <= 0:
            raise ValueError("年龄必须为正整数")

        self.name = name
        self.age = age
        self.time = ""  # 实例变量，用于表示时间

    def go_to_school(self):
        """
        实例方法，打印学生去学校的信息。
        """
        print(f'{self.name}去学校')

    # 删除或改进注释掉的方法示例
    # 如果需要保留示例，可以改为更清晰的注释


if __name__ == '__main__':
    try:
        # 创建Student对象并测试其功能
        stu1 = Student('张三', 18)
        stu1.go_to_school()
        print(stu1.name)
        stu1.time = "2024-07-24"
        print(stu1.time)
    except ValueError as e:
        print(f"创建学生对象时发生错误: {e}")
