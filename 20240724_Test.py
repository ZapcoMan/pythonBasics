class Student:
    time = ""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def goToSchool(self):
        print('%s去学校' % self.name)

    # def goToSchool(name):
    #     print('%s去学校' % name)


if __name__ == '__main__':
    stu1 = Student('张三', 18)
    stu1.goToSchool()
    print(stu1.name)
    stu1.time = "2024-07-24"
    print(stu1.time)
