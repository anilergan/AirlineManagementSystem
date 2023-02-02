class FlightInstance:
    def __init__(self, departure_time, gate, status, aircraft):
        self.__departure_time = departure_time
        self.__gate = gate
        self.__status = status
        self.__aircraft = aircraft
    
    def cancel(self):
        None

    def update_status(self, status):
        None

    def get_departure_time(self): return self.__departure_time
    def get_gate(self): return self.__gate 
    def get_status(self): return self.__status 
    def get_aircraft(self): return self.__aircraft
     
