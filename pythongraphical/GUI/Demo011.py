class Pupil(object):
    def __init__(self, id, name, age, sex):
        self.id = id
        self.name = name
        self.age = age
        self.sex = sex

    def __str__(self):
        return ("id:{0}".format(self.id) + "\t"
                + "name:{0}".format(self.name) + "\t"
                + "age:{0}".format(self.age) + "\t"
                + "sex:{0}".format('男' if self.sex == 0 else '女'))
            

if __name__ == '__main__':
    PupList = [Pupil('20240001', '方苒溪', '18', '0'),
               Pupil('20240002', '谢晨涵', '18', '1'),
               Pupil('20240003', '毛东东', '18', '1'),
               Pupil('20240004', '万敏', '18', '0')]
    for i in range(len(PupList)):

        print(PupList[i])
