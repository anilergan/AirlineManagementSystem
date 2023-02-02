
from person import Person
from address import Address
from account import Account
from PyQt5.QtWidgets import QMessageBox, QWidget
import pandas as pd
import random


class newPersonCreator(QWidget):
    continue_check = False

    def __init__(self, name, surname, street, city, state, zip_code, country, mail, phone, password, password2, person_type, db_person):
        super().__init__()

        self.newPerson_name = name
        self.newPerson_surname = surname
        self.newPerson_street = street
        self.newPerson_city = city
        self.newPerson_state = state
        self.newPerson_zip_code = zip_code
        self.newPerson_country = country
        self.newPerson_mail = mail
        self.newPerson_phone = phone
        self.newPerson_password = password
        self.newPerson_password2 = password2
        self.newPerson_person_type = person_type
        self.persondb = db_person

        # check name
        if self.newPerson_name.isalpha() == False:
            QMessageBox.critical(self, 'Name Error', f'Please use alphabet keys for name enter: {self.newPerson_name}')
            return None
        # name first letter check
        self.newPerson_name = self.newPerson_name.title()
        
        # check surname
        if self.newPerson_surname.isalpha() == False:
            QMessageBox.critical(self, 'Surname Error', f'Please use alphabet keys for surname enter: {self.newPerson_surname}')
            return None
        # surname first letter check
        self.newPerson_surname = self.newPerson_surname.title()

        #check whether newuser_input_password and new_user_password2 are same or not  
        if self.newPerson_password != self.newPerson_password2:
            QMessageBox.critical(self, 'Password Error', 'Please be sure to enter same password both password box')
            return None
        self.auto_id = self.auto_id(self.persondb)
        # newPersonObject, Person tipinde bir obje
        self.newPersonObject = Person(self.newPerson_name, 
                                      self.newPerson_surname, 
                                      Address(self.newPerson_street, 
                                              self.newPerson_city, 
                                              self.newPerson_state, 
                                              self.newPerson_zip_code, 
                                              self.newPerson_country), 
                                              self.newPerson_phone, 
                                      Account(self.newPerson_person_type, 
                                              self.newPerson_mail, 
                                              self.newPerson_password))

        # Person tipindeki yeni objenin bilgilerini dataframe içerisine atacak
        self.newList =  [self.auto_id,
                         self.newPersonObject.get_name(), 
                         self.newPersonObject.get_surname(), 
                         self.newPersonObject.get_account_mail(),
                         self.newPersonObject.get_phone(),
                         self.newPersonObject.get_account_password(),
                         self.newPersonObject.get_account_person_type(),
                         self.newPersonObject.get_address_street(), 
                         self.newPersonObject.get_address_city(), 
                         self.newPersonObject.get_address_state(), 
                         self.newPersonObject.get_address_zip_code(), 
                         self.newPersonObject.get_address_country()]
    
        self.newDf = pd.DataFrame(columns=[ 'Id',
                                            'Name', 
                                            'Surname', 
                                            'Mail', 
                                            'Phone', 
                                            'Password', 
                                            'Person type', 
                                            'Street', 
                                            'City', 
                                            'State', 
                                            'Zipcode', 
                                            'Country'])
        
        self.newDf.loc[len(self.newDf)] = self.newList


        try:
            # self.newDf.to_sql(con=self.engine, name='person', if_exists='append', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='overlay') as writer:
                self.newDf.to_excel(writer, index=False, sheet_name='Person', header=False, startrow=len(self.newDf)+1)
        except: 
            QMessageBox.critical(self, 'Sign Up Error', 'Your mail adress is already registered by another account')
        else:
            type(self).continue_check = True



    def auto_id(self, db):
        self.persondb = db
        self.persondb_ids_serie = self.persondb.loc[:,'Id']
        while True:
            self.exp_id = random.randint(0,100)
            if self.exp_id not in self.persondb_ids_serie:
                return self.exp_id
                

