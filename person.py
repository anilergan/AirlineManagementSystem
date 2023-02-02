from address import Address
from account import Account

class Person:
    def __init__(self, name, surname, address: Address, phone, account: Account):
        self.__name = name
        self.__surname = surname #ben ekledim
        self.__address = address
        self.__phone = phone
        self.__account = account

        

    def get_name(self): return self.__name
    def get_surname(self): return self.__surname
    def get_mail(self): return self.__email
    def get_phone(self): return self.__phone
    def get_address_street(self): return self.__address.get_street()
    def get_address_city(self): return self.__address.get_city()
    def get_address_state(self): return self.__address.get_state()
    def get_address_zip_code(self): return self.__address.get_zip_code()
    def get_address_country(self): return self.__address.get_country()
    def get_mail(self): return self.__email
    def get_phone(self): return self.__phone
    def get_account_person_type(self): return self.__account.get_person_type()
    def get_account_mail(self): return self.__account.get_mail()
    def get_account_password(self): return self.__account.get__password()
