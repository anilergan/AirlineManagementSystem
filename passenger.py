class Passenger(Main):
    def __init__(self, name, passport_number, date_of_birth):
        self.__name = name
        self.__passport_number = passport_number
        self.__date_of_birth = date_of_birth

    def get_passport_number(self):
        return self.__passport_number