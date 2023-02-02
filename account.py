
class Account:
    def __init__(self, person_type, Id, password):
        self.__person_type = person_type
        self.__mail = Id
        self.__password = password

    def get_person_type(self): return self.__person_type
    def get_mail(self): return self.__mail
    def get__password(self): return self.__password

    def reset_password(self):
        None