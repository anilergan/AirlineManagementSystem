class Flight:
    def __init__(self, flight_number, departure, arrival, duration_in_hours, duration_in_minutes):
        self.__flight_number = flight_number
        self.__departure = departure
        self.__arrival = arrival
        self.__duration_in_minutes = duration_in_minutes
        self.__duration_in_hours = duration_in_hours

        self.__weekly_schedules = []
        self.__custom_schedules = []
        self.__flight_instances = []

    def get_flight_number(self): return self.__flight_number
    def get_departure(self): return self.__departure
    def get_arrival(self): return self.__arrival
    def get_duration_in_minutes(self): return self.__duration_in_minutes
    def get_duration_in_hours(self): return self.__duration_in_hours
