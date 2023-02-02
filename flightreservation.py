
class FlightReservation:
    def __init__(self, reservation_number, flight, aircraft, creation_date, status):
        self.__reservation_number = reservation_number
        self.__flight = flight
        self.__seat_map = {}
        self.__creation_date = creation_date
        self.__status = status

    def fetch_reservation_details(self, reservation_number):
        None

    def get_passengers(self):
        None
