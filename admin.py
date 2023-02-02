

from PyQt5.QtWidgets import QWidget, QMessageBox 
from flight import Flight
from aircraft import Aircraft
import pandas as pd
from sqlalchemy import create_engine
from ams_add_schedule import AddScheduleWindow 
from datetime import datetime, timedelta
import string
import random



class Admin(QWidget):
    continue_check = False
    excel_db = pd.read_excel('ams_database.xlsx')

    def __init__(self):
        super().__init__()


    def del_assign_pilot(self,name,surname,num):

        self.list_inputs = [name, surname, num]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None
        

        self.name = name
        self.surname = surname
        self.num = num


        self.check_number_numeric = self.num.isnumeric()
        if self.check_number_numeric == False:
            QMessageBox.critical(self, 'Error', 'Invalid Flight Number!')
            return None    

        # self.database = pd.read_sql('pilotassign', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Pilot Assign')
        self.check_name = ((self.database['Pilot Name'] == self.name) & (self.database['Pilot Surname'] == self.surname) & (self.database['Flight Number'] == int(self.num))).any()
        if self.check_name == False:
            QMessageBox.critical(self, 'Error Number', f"There is no pilot detected that is assigned to flight {self.num}")
            return None  
        
        self.database = self.database[(self.database['Pilot Name'] != self.name) | (self.database['Pilot Surname'] != self.surname) | (self.database['Flight Number'] != int(self.num))]
        # self.database.to_sql(con=self.engine, name='pilotassign', if_exists='replace', index=False)
        with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='replace') as writer:
            self.database.to_excel(writer,sheet_name = 'Pilot Assign', index=False)
        # self.database = pd.read_sql('pilotassign', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Pilot Assign')

        return self.database        

    
    def assign_pilot(self,name,surname, num):

        self.list_inputs = [name, surname, num]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None

        self.name = name
        self.surname = surname
        self.num = num

        self.check_name = self.name.isspace()
        if self.name == '' or self.check_name == True:
            QMessageBox.critical(self, 'Name Error', 'Name is empty')
            return None  

        self.check_surname = self.surname.isspace()
        if self.surname == '' or self.check_surname == True:
            QMessageBox.critical(self, 'Surname Error', 'Surname is empty')
            return None            
        
        self.check_num = (self.num).isspace()
        if self.num == '' or self.check_num == True:
            QMessageBox.critical(self, 'Number Error', 'Flight Number is empty')
            return None    

        self.check_number_numeric = (self.num).isnumeric()
        if self.check_number_numeric == False:
            QMessageBox.critical(self, 'Error', 'Invalid Flight Number!')
            return None    

        # self.database = pd.read_sql('flightinstance', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Flight Instance')
        self.check_num = self.database.loc[:,['Flight Number']].isin([int(self.num)]).any().any()
        if self.check_num == False:
            QMessageBox.critical(self, 'Error Number', 'There is no flight with this flight number')
            return None  

        # self.database = pd.read_sql('person', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Person')
        self.check_name = ((self.database['Name'] == self.name) & (self.database['Surname'] == self.surname) & (self.database['Person type'] == 'Pilot')).any()
        if self.check_name == False:
            QMessageBox.critical(self, 'Error Number', f"There is no pilot whose name is {self.name} {self.surname}")
            return None  
        
        # self.database = pd.read_sql('pilotassign', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Pilot Assign')
        self.check_exist = ((self.database['Pilot Name'] == self.name) & (self.database['Pilot Surname'] == self.surname) & (self.database['Flight Number'] == int(self.num))).any()
        if self.check_exist == True:
            QMessageBox.critical(self, 'Pilot', f"Pilot {self.name} {self.surname} is already assigned for flight {self.num}")
            return None          
        
        # self.database = pd.read_sql('pilotassign', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Pilot Assign')
        self.database_check = self.database[self.database['Flight Number'] == int(self.num)]
        if len(self.database_check) == 2:
            QMessageBox.critical(self, 'Flight Quota Error', f"Two pilot is already assign for the flight instance with flight number {self.num} ")
            return None               

        self.newList = [
            self.num,
            self.name,
            self.surname,
        ]

        self.newDf = pd.DataFrame(columns=[
            'Flight Number',
            'Pilot Name',
            'Pilot Surname'
        ])

        self.newDf.loc[len(self.newDf)] = self.newList

        try:
            # self.newDf.to_sql(con=self.engine, name='pilotassign', if_exists='append', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='overlay') as writer:
                self.newDf.to_excel(writer, index=False, sheet_name='Pilot Assign', header=False, startrow=len(self.database)+1)
        except: 
            QMessageBox.critical(self, 'Error', 'Unexpeccted Error')
            return None
        else:
            # self.newDb = pd.read_sql('pilotassign', self.engine)
            self.newDb = pd.read_excel('ams_database.xlsx', sheet_name='Pilot Assign')
            return self.newDb     
                     


    def del_aircraft(self, Id):
        
        self.list_inputs = [Id]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None

        self.id = Id
        self.id = int(self.id)
        
        # self.database = pd.read_sql('aircraft', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Aircraft')
        self.check_id = self.database.loc[:,['Id']].isin([self.id]).any().any()
 
        if self.check_id == False:
            QMessageBox.critical(self, 'Id Error', 'There is no aircraft detected described by id')
            return None
        else: 
            self.database = self.database[self.database['Id'] != int(self.id)]
            # self.database.to_sql(con=self.engine, name='aircraft', if_exists='replace', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.database.to_excel(writer,sheet_name = 'Aircraft', index=False)            # self.database = pd.read_sql('aircraft', self.engine)
            self.database = pd.read_excel('ams_database.xlsx', sheet_name='Aircraft')
            return self.database


    def add_aircraft(self,acn,acm,acman,airl,iD):
        self.list_inputs = [acn,acm,acman,airl,iD]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None
        # self.check_add_aircraft = False

        self.name = acn
        self.model = acm
        self.man_year = acman
        self.man_year = int(self.man_year)
        self.airline = airl
        self.id = iD
        self.id = int(self.id)
               
        # self.database = pd.read_sql('aircraft', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Aircraft')
        self.check_aircraft = ((self.database['Aircraft Name'] == self.name) & (self.database['Aircraft Model'] == self.model) & (self.database['Manufacturing Year'] == self.man_year ) & (self.database['Airline'] == self.airline)).any()
        if self.check_aircraft == True:
            QMessageBox.critical(self, 'Error Aircraft', 'This aircraft is already exist')
            return None      

        self.check_id = self.database.loc[:,['Id']].isin([self.id]).any().any()
        if self.check_id == True:
            QMessageBox.critical(self, 'Error Id', 'This id is already used by another aircraft')
            return None


        self.newAircraft = Aircraft(self.name, self.model, self.man_year, self.airline, self.id)
        
        self.assigned_flight_number = '-'
        self.newList = [
            self.newAircraft.get_id(),
            self.assigned_flight_number,
            self.newAircraft.get_name(),
            self.newAircraft.get_modal(),
            self.newAircraft.get_airline(),
            self.newAircraft.get_man_year()
        ]

        self.newDf = pd.DataFrame(columns=[
            'Id',
            'Flight Number',
            'Aircraft Name',
            'Aircraft Model',
            'Manufacturing Year',
            'Airline'
        ])

        self.newDf.loc[len(self.newDf)] = self.newList

        try:
            # self.newDf.to_sql(con=self.engine, name = 'aircraft', if_exists = 'append', index = False) 
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='overlay') as writer:
                self.newDf.to_excel(writer, index=False, sheet_name='Aircraft', header=False, startrow=len(self.database)+1)
        except: 
            QMessageBox.critical(self, 'Unexpected Error', 'Unexpected Error Occured')
            return None  
        
        else: 
            # self.newDb = pd.read_sql('aircraft', self.engine)
            self.newDb = pd.read_excel('ams_database.xlsx', sheet_name='Aircraft')
            return self.newDb

    def assign_aircraft(self,num,iD):
        self.list_inputs = [num,iD]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None

        self.num = num
        self.num = int(self.num)
        self.iD = iD
        self.iD = int(self.iD)
        


        # self.database = pd.read_sql('aircraft', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Aircraft')
        self.check_num = self.database.loc[:,['Id']].isin([self.iD]).any().any()
        if self.check_num == False:
            QMessageBox.critical(self, 'Error Id', 'There is no aircraft with this id')
            return None  

        # self.database = pd.read_sql('flightinstance', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Flight Instance')
        self.check_num = self.database.loc[:,['Flight Number']].isin([self.num]).any().any()
        if self.check_num == False:
            QMessageBox.critical(self, 'Flight Number Error', f'There is no flight instance with flight number {self.num} to assign a aircraft.\nReminder: Aircrafts are able assigned for exist flight instances only')
            return None 

        # self.database = pd.read_sql('aircraft', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Aircraft')
        self.database.loc[self.database['Id'] == self.iD, ['Flight Number']] = self.num

        try:
            # self.database.to_sql(con=self.engine, name='aircraft', if_exists='replace', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.database.to_excel(writer,sheet_name = 'Aircraft', index=False)
        except: 
            QMessageBox.critical(self, 'Error', 'Unexpeccted Error')
            return None
        else:
            # self.newDb = pd.read_sql('aircraft', self.engine)
            self.newDb = pd.read_excel('ams_database.xlsx', sheet_name='Aircraft')
            return self.newDb  


    def add_flight(self,dep,arr,fn):

        self.list_inputs = [dep,arr,fn]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None
       
        self.departure = dep
        self.arrival = arr
        self.flight_number = fn
        self.flight_number = int(self.flight_number)

        self.duration = self.calculate_duration(self.departure,self.arrival)
        self.duration = int(self.duration)
        self.duration_in_hours = int(self.duration/60)
        self.duration_in_hours = str(self.duration_in_hours)
        self.duration_in_minutes = self.duration%60
        self.duration_in_minutes = str(self.duration_in_minutes)

        self.check_fn = str(self.flight_number).isspace() 
        if self.flight_number == '' or self.check_fn == True:
            QMessageBox.critical(self, 'Flight Number is empty', 'Please enter a flight number first')
            return None
        if self.departure == self.arrival:
            QMessageBox.critical(self, 'Same Departure-Arrival Point', 'Please chose different airport to departure or arrival')
            return None
        
        # self.database = pd.read_sql('flight', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Flight')

        check_fn = self.database.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        if check_fn == True:
            QMessageBox.critical(self, 'Flight Number Error', 'This flight number is being used by other flight')
            return None
        
        self.newFlight = Flight(self.flight_number, self.departure, self.arrival, self.duration_in_hours, self.duration_in_minutes)

        self.newList = [
            self.newFlight.get_flight_number(),
            self.newFlight.get_departure(),
            self.newFlight.get_arrival(),
            self.newFlight.get_duration_in_hours(),
            self.newFlight.get_duration_in_minutes(),
            self.newFlight.get_departure() + '-' + self.newFlight.get_arrival()
        ]


        self.newDf = pd.DataFrame(columns=[
            'Flight Number',
            'Departure Airport',
            'Arrival Airport',
            'Duration (Hour)',
            'Duration (Minute)',
            'Airport Couple'
        ])

        self.newDf.loc[len(self.newDf)] = self.newList

        try:
            # self.newDf.to_sql(con=self.engine, name='flight', if_exists='append', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='overlay') as writer:
                self.newDf.to_excel(writer, index=False, sheet_name='Flight', header=False, startrow=len(self.database)+1)
        except: 
            QMessageBox.critical(self, 'Database Error', 'Database load failed')
            return None
        # else: 
        #     type(self).continue_check = True  

        
        # if type(self).continue_check != True:
        #     return None  
        else: 
            # self.newDb = pd.read_sql('flight', self.engine)
            self.newDb = pd.read_excel('ams_database.xlsx', sheet_name='Flight')
            return self.newDb           

    
    def return_flight_db(self):
        # self.database = pd.read_sql('flight', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Flight')
        return self.database
    
    def return_weekly_schedule_db(self):
        # self.database = pd.read_sql('weeklyschedule', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Weekly Schedule')
        return self.database
    
    def return_custom_schedule_db(self):
        # self.database = pd.read_sql('customschedule', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Custom Schedule')
        return self.database
    
    def return_aircraft_db(self):
        # self.database = pd.read_sql('aircraft', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Aircraft')
        return self.database
        
    def return_instance_db(self):
        # self.database = pd.read_sql('flightinstance', self.engine)
        self.database_finst = pd.read_excel('ams_database.xlsx', sheet_name='Flight Instance')
        self.database_flight = pd.read_excel('ams_database.xlsx', sheet_name='Flight')
        
        self.database = self.flight_status_automation(self.database_finst, self.database_flight)
        with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='replace') as writer:
            self.database.to_excel(writer,sheet_name = 'Flight Instance', index=False)
        
        return self.database

    def return_pilotassign_db(self):
        # self.database = pd.read_sql('pilotassign', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Pilot Assign')
        return self.database

    def cancel_flight(self,fn):
        self.list_inputs = [fn]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None

        self.flight_number = fn
        self.flight_number = int(self.flight_number)

        # varsa weekly schedule da sil
        # self.db = pd.read_sql('weeklyschedule', self.engine)
        # with pd.ExcelWriter('ams_database.xlsx) as writer
 
        
        self.db = pd.read_excel('ams_database.xlsx', sheet_name='Weekly Schedule')
        self.check_weekly_schedule = self.db.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        if self.check_weekly_schedule == True:
            self.db = self.db[self.db['Flight Number'] != self.flight_number]
            # self.db.to_sql(con=self.engine, name='weeklyschedule', if_exists='replace', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.db.to_excel(writer,sheet_name = 'Weekly Schedule', index=False)        # varsa custom schedule da sil
        # self.db = pd.read_sql('customschedule', self.engine)
        self.db = pd.read_excel('ams_database.xlsx', sheet_name='Custom Schedule')
        
        self.check_weekly_schedule = self.db.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        if self.check_weekly_schedule == True:
            self.db = self.db[self.db['Flight Number'] != self.flight_number]
            # self.db.to_sql(con=self.engine, name='customschedule', if_exists='replace', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.db.to_excel(writer,sheet_name = 'Custom Schedule', index=False)        # varsa flight instance 'da silinecek
        # self.db = pd.read_sql('flightinstance', self.engine)
        self.db = pd.read_excel('ams_database.xlsx', sheet_name='Flight Instance')
        
        self.check_instance = self.db.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        if self.check_instance == True:
            self.db = self.db[self.db['Flight Number'] != self.flight_number]
            # self.db.to_sql(con=self.engine, name='flightinstance', if_exists='replace', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.db.to_excel(writer,sheet_name = 'Flight Instance', index=False)
        # self.database = pd.read_sql('flight', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Flight')
        self.check_fn = self.database.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        
        if self.check_fn == False:
            QMessageBox.critical(self, 'Flight Number Error', 'There is no flight detected described by this flight number. ')
            return None
        else: 
            # geçerli flight number satırını df içinden sil
            self.database = self.database[self.database['Flight Number'] != self.flight_number] 
            # df'i db'ye geri döndür
            # self.database.to_sql(con=self.engine, name='flight', if_exists='replace', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.database.to_excel(writer,sheet_name = 'Flight', index=False)            # db'nin güncel halini çek ve döndür
            # self.database = pd.read_sql('flight', self.engine)
            self.database = pd.read_excel('ams_database.xlsx', sheet_name='Flight')
            return self.database
            # ams_main üzerinden döndürülen değerler ile qtable güncelle

    def cancel_flight_schedule_weekly(self,fn):
        self.list_inputs = [fn]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None
        self.flight_number = fn
        self.flight_number = int(self.flight_number)

        # self.db = pd.read_sql('flightinstance', self.engine)
        self.db = pd.read_excel('ams_database.xlsx', sheet_name='Flight Instance')
        self.check_instance = self.db.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        if self.check_instance == True:
            self.db = self.db[self.db['Flight Number'] != self.flight_number]
            # self.db.to_sql(con=self.engine, name='flightinstance', if_exists='replace', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.db.to_excel(writer,sheet_name = 'Flight Instance', index=False)        # self.database = pd.read_sql('weeklyschedule', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Weekly Schedule')
        check_fn = self.database.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        if check_fn == False:
            QMessageBox.critical(self, 'Flight Number Error', 'There is no flight detected described by this flight number. ')
            return None
        else: 
            # geçerli flight number satırını df içinden sil
            self.database = self.database[self.database['Flight Number'] != self.flight_number] 
            # df'i db'ye geri döndür
            # self.database.to_sql(con=self.engine, name='weeklyschedule', if_exists='replace', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.database.to_excel(writer,sheet_name = 'Weekly Schedule', index=False)            # db'nin güncel halini çek ve döndür
            # self.database = pd.read_sql('weeklyschedule', self.engine)
            self.database = pd.read_excel('ams_database.xlsx', sheet_name='Weekly Schedule')

            return self.database
            # ams_main üzerinden döndürülen değerler ile qtable güncelle




    def cancel_flight_schedule_custom(self,fn):

        self.list_inputs = [fn]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None

        self.flight_number = fn
        self.flight_number = int(self.flight_number)

        # self.db = pd.read_sql('flightinstance', self.engine)
        self.db = pd.read_excel('ams_database.xlsx', sheet_name='Flight Instance')
        self.check_instance = self.db.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        if self.check_instance == True:
            self.db = self.db[self.db['Flight Number'] != self.flight_number]
            # self.db.to_sql(con=self.engine, name='flightinstance', if_exists='replace', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.db.to_excel(writer,sheet_name = 'Flight Instance', index=False)
        # self.database = pd.read_sql('customschedule', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Custom Schedule')
        check_fn = self.database.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        if check_fn == False:
            QMessageBox.critical(self, 'Flight Number Error', 'There is no flight detected described by this flight number. ')
            return None
        else: 
            # geçerli flight number satırını df içinden sil
            self.database = self.database[self.database['Flight Number'] != self.flight_number] 
            # df'i db'ye geri döndür
            # self.database.to_sql(con=self.engine, name='customschedule', if_exists='replace', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.database.to_excel(writer,sheet_name = 'Custom Schedule', index=False)            # db'nin güncel halini çek ve döndür
            # self.database = pd.read_sql('customschedule', self.engine)
            self.database = pd.read_excel('ams_database.xlsx', sheet_name='Custom Schedule')
            return self.database
            # ams_main üzerinden döndürülen değerler ile qtable güncelle


    def open_add_flight_schedule(self):

        self.add_schedule_window = AddScheduleWindow()
        self.add_schedule_window.show()
       

    def close_add_flight_schedule(self):
        self.add_schedule_window.clear_inputs()
        self.add_schedule_window.close()


        




    def get_flight_schedule_process(self,fn):
        self.check_get_flight = False
        self.list_inputs = [fn]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None

        self.check_get_flight = False
        self.flight_number = fn
        self.flight_number = int(self.flight_number)
        
        if self.flight_number == '':
            QMessageBox.critical(self, 'Flight Number is empty', 'Please enter a flight number first')
            return None
        
        # self.database = pd.read_sql('flight', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Flight')
        self.check_fn = self.database.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        if self.check_fn == False:
            return None

        self.check_get_flight = True

    def get_weekly_flight_schedule(self,fn):
        self.list_inputs = [fn]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None

        self.flight_number = fn
        self.flight_number = int(self.flight_number)

        # self.database_w = pd.read_sql('weeklyschedule', self.engine)
        self.database_w = pd.read_excel('ams_database.xlsx', sheet_name='Weekly Schedule')
        self.check_fn_weekly = self.database_w.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        if self.check_fn_weekly == True:
            self.database_w_fn = self.database_w[self.database_w['Flight Number'] == self.flight_number]
            return self.database_w_fn
        else: return None
    
    def get_custom_flight_schedule(self,fn):
        self.list_inputs = [fn]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None
        self.flight_number = fn
        self.flight_number = int(self.flight_number)
        
        # self.database_c = pd.read_sql('customschedule', self.engine)
        self.database_c = pd.read_excel('ams_database.xlsx', sheet_name='Custom Schedule')
        self.check_fn_custom = self.database_c.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        if self.check_fn_custom == True:
            self.database_c_fn = self.database_c[self.database_c['Flight Number'] == self.flight_number]
            return self.database_c_fn
        else: return None



    def cancel_flight_instances(self,fn):
        self.list_inputs = [fn]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None
        self.flight_number = fn
        self.flight_number = int(self.flight_number)
        
        # self.db = pd.read_sql('flightinstance', self.engine)
        self.db = pd.read_excel('ams_database.xlsx', sheet_name='Flight Instance')
        
        self.check_instance = self.db.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        if self.check_instance == True:
            self.db_minus_fn = self.db[self.db['Flight Number'] == self.flight_number]
            self.db = self.db[self.db['Flight Number'] != self.flight_number] 
        else: 
            QMessageBox.critical(self, 'Flight Number Error', 'There is no flight detected described by this flight number')
            return None

        self.check_instance_cancel = self.db_minus_fn.loc[:,['Status']].isin(['CANCEL']).any().any()
        if self.check_instance_cancel:
            self.db_no_cancel_fn = self.db_minus_fn[self.db_minus_fn['Status'] != 'CANCEL']
        else: 
            self.db_no_cancel_fn = self.db_minus_fn

        self.status_block_list = ['GATE OPEN', 'BOARDING', 'LAST CALL', 'IN AIR', 'ARRIVED']
        self.cancelled_flights = 0
        for status in range(0,len(self.db_minus_fn)):
            if self.db_minus_fn.iloc[status,5] not in self.status_block_list:
                self.db_minus_fn.iloc[status,5] = 'CANCEL'
                self.cancelled_flights +=1
            
        QMessageBox.information(self,'Canceling Process Done', f"{self.cancelled_flights} flight instance is canceled succeed \n{len(self.db_minus_fn['Status'])-self.cancelled_flights} flight instance could not canceled due to them status")

        

        
        self.newdb = self.db.append(self.db_no_cancel_fn, ignore_index=True)

        try:
            # self.newdb.to_sql(con=self.engine, name = 'flightinstance', if_exists = 'replace', index = False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.newdb.to_excel(writer,sheet_name = 'Flight Instance', index=False) 
        except: 
            QMessageBox.critical(self, 'Unexpected Error', 'Unexpected Error Occured')
            return None
        else: 
            QMessageBox.information(self, 'Recall about canceling process','If you cancel a flight with a status of CANCEL again, it will be permanently removed from the table.')
             
    

    def get_flight_instances(self,fn):
        self.list_inputs = [fn]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None 
        self.flight_number = fn
        self.flight_number = int(self.flight_number)
        
        # self.database = pd.read_sql('flightinstance', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Flight Instance')
        self.check_fn = self.database.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        if self.check_fn == True:
            self.database = self.database[self.database['Flight Number'] == self.flight_number]
            return self.database
        else: return None
    


    def flight_status_automation(self, i_db, f_db):
        #databaseleri çektik
        self.i_db = i_db
        self.f_db = f_db
        #instance'ı olan flight numberları flight tablosundan çekelim
        #flight instancesların durationına flight tablosundan erişelim
        self.fn_serie = self.i_db['Flight Number']
        self.df_flight_finst = pd.DataFrame()
        for num in self.fn_serie:
            self.df_filter = f_db[f_db['Flight Number'] == num][['Flight Number','Duration (Hour)', 'Duration (Minute)']]
            self.df_flight_finst = pd.concat([self.df_filter, self.df_flight_finst], ignore_index=True)

        # self.df_flight_finst
        # flight number     duration hour     duration minute
        for row in range(0,len(self.i_db)):
            self.df_serie = i_db.iloc[row,:]
            self.fn_serie = self.df_serie['Flight Number']
            
            self.duration_df = self.f_db[self.f_db['Flight Number'] == self.fn_serie][['Duration (Hour)', 'Duration (Minute)']]
            self.duration_df = self.duration_df.reset_index(drop=True)
            self.duration_df_row = self.duration_df.iloc[0,:]

            self.duration_serie = pd.Series(self.duration_df_row)
            
            self.df_serie = pd.Series(self.df_serie)
            self.update_serie = self.update_status(self.df_serie, self.duration_serie)
            i_db.iloc[row,:] = self.update_serie
        
        return self.i_db
        


    def update_status(self, serie, duration_serie):
        #serie datas
        self.serie = serie
        self.num = self.serie['Flight Number']
        self.day = self.serie['Day']
        self.date = self.serie['Date']
        self.gate = self.serie['Gate']
        self.dep = self.serie['Departure']
        self.status = self.serie['Status']
        #duration datas
        self.duration_serie = duration_serie
        self.dur_hour = self.duration_serie['Duration (Hour)']
        self.dur_min = self.duration_serie['Duration (Minute)']

        #time datas
        self.now = datetime.now()
        self.now_day = self.now.strftime('%A')
        self.now_date = self.now.strftime('%d %B')

        self.dur_hour = datetime.strptime(str(self.dur_hour), '%H')
        self.dur_min = datetime.strptime(str(self.dur_min), '%M')
        self.dep = datetime.strptime(str(self.dep), '%H:%M')



        self.now_time_delta = timedelta(hours=self.now.hour, minutes=self.now.minute)
        self.dep_time_delta = timedelta(hours=self.dep.hour, minutes= self.dep.minute)
        self.time_to_flight = self.dep_time_delta - self.now_time_delta
        self.time_in_air = self.now_time_delta - self.dep_time_delta


        self.duration_delta = timedelta(hours=self.dur_hour.hour, minutes=self.dur_min.minute)
        
        self.check_flight_date_day = ((self.day == self.now_day) | (self.date == self.now_date))

        #update the status of flight
        if (self.check_flight_date_day) & ((self.status == 'UNKNOWN')):
            self.status = 'ACTIVE'
            self.gate = self.random_gate()
        
        if (self.check_flight_date_day) & ((self.status == 'SCHEDULED')):
            self.status = 'ACTIVE'
        
        if (self.time_to_flight.seconds < 60*60+15*60) & (self.status == 'ACTIVE') :
            self.status = 'GATE OPEN'

        
        if (self.time_to_flight.seconds < 45*60) & (self.status == 'GATE OPEN'):
            self.status = 'BOARDING'
            
        
        if (self.time_to_flight.seconds < 20*60) & (self.status == 'BOARDING'):
            self.status = 'LAST CALL'
        
        if (self.time_to_flight.seconds < 10*60) & (self.status == 'LAST CALL'):
            self.status = 'GATE CLOSED'
       
        if (self.time_in_air.seconds > 0) & (self.status == 'GATE CLOSED'):
            self.status = 'DEPARTED'
        
        if (self.time_in_air.seconds > 10*60) & (self.status == 'DEPARTED'):
            self.status = 'IN AIR'

        if (self.time_in_air.seconds >= self.duration_delta.seconds) & (self.status == 'IN AIR'):
            self.status = 'LANDED'
       
        if (self.time_in_air.seconds >= (self.duration_delta.seconds + 10*60)) & (self.status == 'LANDED'):
            self.status = 'ARRIVED'
        
        if (self.time_in_air.seconds >= (self.duration_delta.seconds + 2*60*60)) & (self.status == 'ARRIVED'):
            self.status = 'UNKNOWN'
        

        self.serie['Flight Number'] = self.num
        self.serie['Day'] = self.day
        self.serie['Date'] = self.date
        self.serie['Gate'] = self.gate
        self.dep = self.dep.strftime('%H:%M')
        self.serie['Departure'] = self.dep
        self.serie['Status'] = self.status

        return self.serie
    

    def random_gate(self):

        self.letters = string.ascii_uppercase
        self.letters = self.letters[0:9]
        self.random_letter1 = random.choice(self.letters)
        self.random_letter2 = random.choice(self.letters)
        self.random_number = str(random.randint(1,9))
        self.gate_rnd = self.random_letter1 + self.random_number + self.random_letter2
        return self.gate_rnd

    
    def calculate_duration(self,dep,arr):

        self.dep = dep
        self.arr = arr
        self.couple = self.dep + '-' + self.arr

        if self.couple == 'IST-ESB' or self.couple == 'ESB-IST':
            self.min = '120'
            return self.min

        elif self.couple == 'IST-ADB' or self.couple == 'ADB-IST':
            self.min = '70'
            return self.min
        
        elif self.couple == 'IST-ATH' or self.couple == 'ATH-IST':
            self.min = '85'
            return self.min
        
        elif self.couple == 'IST-CPH' or self.couple == 'CPH-IST':
            self.min = '210'
            return self.min
        # -------------------------------------------------------------------------

        elif self.couple == 'ADB-ESB' or self.couple == 'ESB-ADB':
            self.min = '75'
            return self.min
        
        elif self.couple == 'ADB-ATH' or self.couple == 'ATH-ADB':
            self.min = '75'
            return self.min
        
        elif self.couple == 'ADB-CPH' or self.couple == 'CPH-ADB':
            self.min = '220'
            return self.min
        # -------------------------------------------------------------------------

        elif self.couple == 'ESB-ATH' or self.couple == 'ATH-ESB':
            self.min = '275'
            return self.min
        
        elif self.couple == 'ESB-CPH' or self.couple == 'CPH-ESB':
            self.min = '145'
            return self.min
        # -------------------------------------------------------------------------

        elif self.couple == 'CPH-ATH' or self.couple == 'ATH-CPH':
            self.min = '140'
            return self.min
            
        else: return 0
        
