
class Aircraft:
    def __init__(self, name, model, manufacturing_year, airline, iD):
        self.__name = name
        self.__model = model
        self.__manufacturing_year = manufacturing_year
        self.__airline = airline
        self.__id = iD
        self.__seats = []

    def get_flights(self):
        None

    def get_name(self): return self.__name
    def get_modal(self): return self.__model
    def get_man_year(self): return self.__manufacturing_year
    def get_airline(self): return self.__airline
    def get_id(self): return self.__id