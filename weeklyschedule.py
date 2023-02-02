class WeeklySchedule:
    def __init__(self, day_of_week, departure_time):
        self.__day_of_week = day_of_week
        self.__departure_time = departure_time

    def get_day_of_week(self): return self.__day_of_week
    def get_departure_time(self): return self.__departure_time

