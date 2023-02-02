
class CustomSchedule:
    def __init__(self, custom_date, departure_time):
        self.__custom_date = custom_date
        self.__departure_time = departure_time

    def get_custom_date(self): return self.__custom_date
    def get_departure_time(self): return self.__departure_time