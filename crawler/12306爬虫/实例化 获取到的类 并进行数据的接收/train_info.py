# train_info.py

class TrainInfo:
    def __init__(self, train_number, departure_time, time_of_arrival, time_consuming,
                 premier_class, first_class_seat, second_class, soft_sleeper, hard_sleeper,
                 soft_seat, hard_seat, without_seat, business_class, first_class_sleeping,
                 second_class_bedroom, superior_soft_sleeper):
        self.train_number = train_number
        self.departure_time = departure_time
        self.time_of_arrival = time_of_arrival
        self.time_consuming = time_consuming
        self.premier_class = premier_class
        self.first_class_seat = first_class_seat
        self.second_class = second_class
        self.soft_sleeper = soft_sleeper
        self.hard_sleeper = hard_sleeper
        self.soft_seat = soft_seat
        self.hard_seat = hard_seat
        self.without_seat = without_seat
        self.business_class = business_class
        self.first_class_sleeping = first_class_sleeping
        self.second_class_bedroom = second_class_bedroom
        self.superior_soft_sleeper = superior_soft_sleeper

    def __str__(self):
        return (f"车次: {self.train_number}, 出发时间: {self.departure_time}, "
                f"到达时间: {self.time_of_arrival}, 耗时: {self.time_consuming}, "
                f"特等座: {self.premier_class}, 一等座: {self.first_class_seat}, "
                f"二等座: {self.second_class}, 软卧: {self.soft_sleeper}, "
                f"硬卧: {self.hard_sleeper}, 软座: {self.soft_seat}, "
                f"硬座: {self.hard_seat}, 无座: {self.without_seat}, "
                f"商务座: {self.business_class}, 一等卧: {self.first_class_sleeping}, "
                f"二等卧: {self.second_class_bedroom}, 高级软卧: {self.superior_soft_sleeper}")
