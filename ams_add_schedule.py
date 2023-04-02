
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtCore import pyqtSignal
import pandas as pd
# from sqlalchemy import create_engine
from datetime import datetime, timedelta

from weeklyschedule import WeeklySchedule
from customschedule import CustomSchedule
from flightinstance import FlightInstance
from amsqt_add_schedule2 import Ui_WindowAddSchedule



class AddScheduleWindow(QWidget):
    check_continue = False

    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowAddSchedule()
        self.ui.setupUi(self)

        self.second_page_validator()
        

        self.ui.add_schedule_button_add_weekly_schedule.clicked.connect(self.button_add_weekly_sch)
        self.ui.add_schedule_button_add_custom_schedule.clicked.connect(self.button_add_custom_sch)
        self.ui.add_schedule_button_add_finst.clicked.connect(self.button_add_flight_instance)


    def button_add_weekly_sch(self):
        self.check_continue = False
        
        self.flight_number = self.ui.add_schedule_input_fn.text()
        self.hour = self.ui.add_schedule_input_weekly_time_hour.text()
        self.min =  self.ui.add_schedule_input_weekly_time_min.text()
        self.day = self.ui.add_schedule_combo_choose_day.currentText()
        self.departure = self.ui.add_schedule_input_weekly_time_hour.text() + ':' + self.ui.add_schedule_input_weekly_time_min.text()
        
        self.list_inputs = [self.flight_number, self.hour, self.min, self.day]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None 
        
        self.flight_number = int(self.flight_number)



        # self.database = pd.read_sql('flight', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Flight')
        check_fn = self.database.isin([self.flight_number]).any().any()
        if check_fn == False:
            QMessageBox.critical(self, 'Flight Number Error', 'There is no flight detected described by this flight number.')
            return None
        
        # self.db_weekly = pd.read_sql('weeklyschedule', self.engine)
        self.db_weekly = pd.read_excel('ams_database.xlsx', sheet_name='Weekly Schedule')
        check_fn2 = ((self.db_weekly['Flight Number'] == self.flight_number) & (self.db_weekly['Day of Week'] == self.day) & (self.db_weekly['Departure'] == self.departure)).any()
        
        if check_fn2 == True:
            QMessageBox.critical(self, 'Schedule is already exist','This specific weekly schedule that you try to create is already exist for this flight number.\nPlease, change duration time or day of week and try again.')
            return None

        elif (len(self.min) == 1) | (len(self.hour) == 1):
            QMessageBox.critical(self, 'Digit Number Error', 'Please enter two digit to define time\nFor instance, 01 instead of 1')
            return None 
        
        self.hour = int(self.hour)
        self.min = int(self.min)
        
        if (self.hour) < 0 or (self.hour) > 23:
            QMessageBox.critical(self, 'Time error', 'Please enter a time between 00:00 - 23:59')
            return None
        
        if (self.min) < 0 or (self.min) > 59:
            QMessageBox.critical(self, 'Time error', 'Please enter a time between 00:00 - 23:59')
            return None

        self.add_weekly_schedule(self.db_weekly)
        if self.check_continue == True:
            QMessageBox.information(self, 'Operation Succeed', 'Weekly schedule of flight has defined succeed')



    def add_weekly_schedule(self, db_weekly):
        self.db_instance = pd.read_excel('ams_database.xlsx', sheet_name='Flight Instance')
        self.flight_number = self.ui.add_schedule_input_fn.text()
        self.day_of_week = self.ui.add_schedule_combo_choose_day.currentText()
        self.departure_time = self.ui.add_schedule_input_weekly_time_hour.text() + ':' + self.ui.add_schedule_input_weekly_time_min.text()
        
        self.newWeeklySchedule = WeeklySchedule(self.day_of_week,self.departure_time)
        self.newList = [
            self.flight_number,
            self.newWeeklySchedule.get_day_of_week(),
            self.newWeeklySchedule.get_departure_time()
        ]
        self.newDf = pd.DataFrame(columns=[
            'Flight Number',
            'Day of Week',
            'Departure'
        ])

        self.newDf.loc[len(self.newDf)] = self.newList

        try:
            # self.newDf.to_sql(con=self.engine, name='weeklyschedule',if_exists='append', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='overlay') as writer:
                self.newDf.to_excel(writer, index=False, sheet_name='Weekly Schedule', header=False, startrow=len(db_weekly)+1)
        except:
            QMessageBox.critical(self, 'Error', 'Unexpected Error')
            return None


        self.gate = '-'
        self.status = 'SCHEDULED'
        self.aircraft = '-'
        self.newInstance = FlightInstance(self.newWeeklySchedule.get_departure_time(), self.gate, self.status, self.aircraft) 
        self.customschedule = '-'
        self.newList = [
            self.flight_number,
            self.newWeeklySchedule.get_day_of_week(),
            self.customschedule,
            self.newInstance.get_departure_time(),
            self.newInstance.get_gate(),
            self.status
        ]

        self.newDf = pd.DataFrame(columns=[
            'Flight Number',
            'Day',
            'Date',
            'Departure',
            'Gate',
            'Status'
        ]) 

        self.newDf.loc[len(self.newDf)] = self.newList

        try:
            # self.newDf.to_sql(con=self.engine, name='flightinstance',if_exists='append', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='overlay') as writer:
                self.newDf.to_excel(writer, index=False, sheet_name='Flight Instance', header=False, startrow=len(self.db_instance)+1)
        except:
            QMessageBox.critical(self, 'Error', 'Unexpected Error')
            return None

        self.check_continue = True

            

       
        



    def button_add_flight_instance(self):
        self.check_instance = False
        
        self.flight_number = self.ui.add_schedule_input_fn.text()
        # self.flight_number = int(self.flight_number)
        self.daydate = self.ui.add_schedule_input_daydate.text()
        self.hour = self.ui.add_schedule_input_finst_current_hour.text()
        # self.hour = int(self.hour)
        self.min = self.ui.add_schedule_input_finst_current_min.text()
        # self.min = int(self.min)
        self.update_hour = self.ui.add_schedule_input_finst_update_hour.text()
        # self.update_hour = int(self.update_hour)
        self.update_min = self.ui.add_schedule_input_finst_update_min.text()
        # self.update_min = int(self.update_min)
        self.update_departure = self.hour + ':' + self.min
        self.gate = self.ui.add_schedule_input_inst_gate.text()

        self.list_inputs = [self.flight_number, self.daydate, self.hour, self.min, self.update_hour, self.update_min, self.gate]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None 
        
        self.flight_number = int(self.flight_number)

 
        # self.database = pd.read_sql('flightinstance', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Flight Instance')


        self.check_fn = self.database.loc[:,['Flight Number']].isin([self.flight_number]).any().any()
        if self.check_fn == False:
            QMessageBox.critical(self, 'Flight Number Error', 'There is no flight detected described by this flight number.')
            return None
        
        self.database_fn = self.database.loc[self.database['Flight Number'] == self.flight_number, ['Day', 'Date']]
        self.check_daydate = self.database_fn.isin([self.daydate]).any().any()
        if self.check_daydate == False:
            QMessageBox.critical(self, 'Day/Date Error', 'There is no weekly or custom schedule detected described by this flight number.\n So there is no flight instance that you are trying to update')
            return None
        
    
        elif (len(self.min) == 1) | (len(self.hour) == 1):
            QMessageBox.critical(self, 'Digit Number Error', 'Please enter two digit to define time\nFor instance, 01 instead of 1')
            return None

        self.hour = int(self.hour)
        self.min = int(self.min) 
        
        if self.hour < 0 or self.hour > 23:
            QMessageBox.critical(self, 'Time error', 'Please enter a time between 00:00 - 23:59')
            return None
        
        elif self.min < 0 or self.min > 59:
            QMessageBox.critical(self, 'Time error', 'Please enter a time between 00:00 - 23:59')
            return None

        elif (len(self.update_min) == 1)  | (len(self.update_hour) == 1):
            QMessageBox.critical(self, 'Digit Number Error', 'Please enter two digit to define time\nFor instance, 01 instead of 1')
            return None 
        
        self.update_hour = int(self.update_hour)
        self.update_min = int(self.update_min)
        
        if self.update_hour < 0 or self.update_hour > 23:
            QMessageBox.critical(self, 'Time error', 'Please enter a time between 00:00 - 23:59')
            return None
        
        elif self.update_min < 0 or self.update_min > 59:
            QMessageBox.critical(self, 'Time error', 'Please enter a time between 00:00 - 23:59')
            return None

        else: 
            self.add_flight_instance(self.database)
            if self.check_instance == True:
                QMessageBox.information(self, 'Operation Succeed', 'Flight instance of flight has defined succeed')

    
    
    def add_flight_instance(self,db):
        self.flight_number = self.ui.add_schedule_input_fn.text()
        self.departure_time = self.ui.add_schedule_input_finst_current_hour.text() + ':' + self.ui.add_schedule_input_finst_current_min.text()
        self.gate = self.ui.add_schedule_input_inst_gate.text()
        self.daydate = self.ui.add_schedule_input_daydate.text()
        self.update_dep = self.ui.add_schedule_input_finst_update_hour.text() + ':' + self.ui.add_schedule_input_finst_update_min.text()
        
        self.departure_time_dt = datetime.strptime(self.departure_time, '%H:%M')
        self.update_time_dt = datetime.strptime(self.update_dep, '%H:%M')

        self.list_inputs = [self.flight_number, self.daydate, self.gate, self.departure_time, self.update_dep]


        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None
        
        self.flight_number = int(self.flight_number)
    

        self.db = db
        self.db_check_status = self.db[(db['Flight Number'] == self.flight_number) & (db['Departure'] == self.departure_time) & ((db['Day'] == self.daydate) | (db['Date'] == self.daydate))][['Status']]
        self.db_check_status = self.db_check_status.iloc[0,:]
        self.db_check_status = pd.Series(self.db_check_status)

        self.dbS = self.db[(self.db['Flight Number'] == self.flight_number) & ((self.db['Day'] == self.daydate) | (self.db['Date'] == self.daydate)) & (self.db['Departure'] == self.departure_time)]
        

        self.db = self.db[(self.db['Flight Number'] != self.flight_number) | ((self.db['Day'] != self.daydate) & (self.db['Date'] != self.daydate)) | (self.db['Departure'] != self.departure_time)]
        self.dbS = self.dbS.reset_index(drop=True)

        if self.dbS.loc[0,'Status'] == 'CANCEL':
            QMessageBox.critical(self,'Flight instance was cancaled', 'The flight instance you are trying to update was canceled')
            return None
        
        self.status_block_list = ['CHECK-IN','GATE OPEN', 'BOARDING', 'LAST CALL', 'IN AIR', 'ARRIVED']
        if self.db_check_status['Status'] in self.status_block_list:
            QMessageBox.critical(self,"Flight Status Blocked", "The Flight's status is not appropriate for modifying")
            return None 

        self.check_delay = self.departure_time_dt < self.update_time_dt #If True => Delay
        if (self.db_check_status['Status'] == 'ACTIVE') & (self.check_delay == False):
            QMessageBox.critical(self,"Flight Status Block", "The Flight's status is not appropriate to update departure time earlier")
            return None 

        elif (self.db_check_status['Status'] == 'ACTIVE') & self.check_delay:
             self.dbS.loc[0,'Status'] = 'DELAYED'
             QMessageBox.information(self,"Delayed Succeed", f"The Flight's departure time is delayed succeed")
             #bilet sahiplerine bildirim gönder

        elif (self.db_check_status['Status'] != 'ACTIVE') & (self.check_delay) == False:
             QMessageBox.information(self,"Scheduled Succeed", f"The Flight's departure time is rescheduled succeed")    
             #bilet sahiplerine bildirim gönder!
        
                     
        elif (self.db_check_status['Status'] != 'ACTIVE') & (self.departure_time_dt == self.update_time_dt) :
             QMessageBox.information(self,"Scheduled Succeed", f"The Flight's departure time is scheduled succeed") 
             #bilet sahiplerine bildirim gönder!


        elif (self.db_check_status['Status'] == 'ACTIVE') & (self.departure_time_dt == self.update_time_dt) :
             QMessageBox.critical(self,"Update Time Error", f"Update time and current time are the same\n Flight's status is 'ACTIVE', flight's departure time can not be changed but only can be delayed")
             return None         

            

        
        # self.dbS.loc[0,'Status'] = 'SCHEDULED'
        self.dbS.loc[0,'Departure'] = self.update_dep
        self.dbS.loc[0,'Gate'] = self.gate


    
        # day or date?
        self.check_dayordate  = self.daydate.isalpha()
        
        if self.check_dayordate == True:
            self.day = self.daydate
            self.dbS.loc[0,'Day'] = self.day

    
        else:
            self.date = self.daydate
            self.dbS.loc[0,'Date'] = self.date
        

# df3 = df1.append(df2, ignore_index=True)
        self.newDb = self.dbS.append(self.db, ignore_index=True)

         
        with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.newDb.to_excel(writer,sheet_name = 'Flight Instance', index=False)    
        
       
        self.check_instance = True
        self.df = pd.read_excel('ams_database.xlsx', sheet_name='Flight Instance')
   


    def button_add_custom_sch(self):
        self.check_continue = False
        
        self.flight_number = self.ui.add_schedule_input_fn.text()
        self.hour = self.ui.add_schedule_input_custom_time_hour.text()
        self.min =  self.ui.add_schedule_input_custom_time_min.text()
        self.day = self.ui.add_schedule_input_custom_day.text()
        self.month = self.ui.add_schedule_combo_choose_month.currentText()
        self.year = '2023'
        self.departure = self.hour + ':' + self.min

        self.list_inputs = [self.flight_number, self.hour, self.min, self.day, self.month, self.year, self.departure]
        for check in self.list_inputs:
            self.check_space = check.isspace()
            self.check_null = check == ''
            if (self.check_space) | (self.check_null):
                QMessageBox.critical(self,'Error: Null Values', 'Some inputs are null!')
                return None 
        self.flight_number = int(self.flight_number)

        # Check: Flight Number var mı, yok mu? 
        # self.database = pd.read_sql('flight', self.engine)
        self.database = pd.read_excel('ams_database.xlsx', sheet_name='Flight')

        check_fn = self.database.isin([self.flight_number]).any().any()
        if check_fn == False:
            QMessageBox.critical(self, 'Flight Number Error', 'There is no flight detected described by this flight number.')
            return None

        # Check: spesifik olarak bu kayıt mecvut mu
        # self.db_custom = pd.read_sql('customschedule', self.engine)
        self.db_custom = pd.read_excel('ams_database.xlsx', sheet_name='Custom Schedule')
        check_fn2 = ((self.db_custom['Flight Number'] == self.flight_number) & (self.db_custom['Date'] == self.day) & (self.db_custom['Departure'] == self.departure)).any()
        if check_fn2 == True:
            QMessageBox.critical(self, 'Schedule is already exist','This specific weekly schedule that you try to create is already exist for this flight number.\nPlease, change duration time or day of week and try again.')
            return None

        elif (len(self.min) == 1) | (len(self.hour) == 1) | (len(self.day) == 1) :
            QMessageBox.critical(self, 'Digit Number Error', 'Please enter two digit to define time\nFor instance, 01 instead of 1')
            return None
        self.hour = int(self.hour)
        self.min = int(self.min)
        
        if (self.min) < 0 or (self.min) > 59:
            QMessageBox.critical(self, 'Time error', 'Please enter a time between 00:00 - 23:59')
            return None
        
        elif (self.hour) < 0 or (self.hour) > 23:
            QMessageBox.critical(self, 'Time error', 'Please enter a time between 00:00 - 23:59')
            return None

        elif (self.month == 'January' or self.month =='March' or self.month =='May'or self.month =='July' or self.month =='August' or self.month =='October' or self.month =='December') and (int(self.day) > 31 or int(self.day) < 1):
            QMessageBox.critical(self, 'Month day error', f'Number of days in {self.month} is 31.')
            return None
        elif (self.month == 'Fenruary') and ( (self.day) > 28 or int(self.day) < 1):
            QMessageBox.critical(self, 'Month day error', f'Number of days in {self.month} is 28.')
            return None
        
        elif (self.month == self.month =='April' or self.month =='June' or self.month =='September' or self.month =='November') and (int(self.day) > 30 or int(self.day) < 1):
            QMessageBox.critical(self, 'Month day error', f'Number of days in {self.month} is 30.')
            return None


        else: 
            self.add_custom_schedule(self.month, self.db_custom)
            if self.check_continue == True:
                QMessageBox.information(self, 'Operation Succeed', 'Custom schedule of flight has defined succeed')



    def add_custom_schedule(self, month, db):
        self.db_custom = db
        self.month = month
        self.newCustomSchedule = CustomSchedule(self.day,self.departure)

        
        self.newList = [
            self.flight_number,
            self.newCustomSchedule.get_custom_date() + ' ' + self.month,
            self.newCustomSchedule.get_departure_time()
        ]


        self.newDf = pd.DataFrame(columns=[
            'Flight Number',
            'Date',
            'Departure'
        ])

        self.newDf.loc[len(self.newDf)] = self.newList

        try:
            # self.newDf.to_sql(con=self.engine, name='customschedule',if_exists='append', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='overlay') as writer:
                self.newDf.to_excel(writer, index=False, sheet_name='Custom Schedule', header=False, startrow=len(self.db_custom)+1)
        except:
            QMessageBox.critical(self, 'Error', 'Unexpected Error')
            return None
        
        
        self.gate = '-'
        self.status = 'SCHEDULED'
        self.aircraft = '-'
        self.weeklyschedule = '-'
        self.newInstance = FlightInstance(self.newCustomSchedule.get_departure_time(), self.gate, self.status, self.aircraft) 

        self.newList = [
            self.flight_number,
            self.weeklyschedule,
            self.newCustomSchedule.get_custom_date() + ' ' + self.month,
            self.newInstance.get_departure_time(),
            self.newInstance.get_gate(),
            self.status
        ]

        self.newDf = pd.DataFrame(columns=[
            'Flight Number',
            'Day',
            'Date',
            'Departure',
            'Gate',
            'Status'
        ]) 

        self.newDf.loc[len(self.newDf)] = self.newList

        self.db_instance = pd.read_excel('ams_database.xlsx', sheet_name='Flight Instance')
        try:
            # self.newDf.to_sql(con=self.engine, name='flightinstance',if_exists='append', index=False)
            with pd.ExcelWriter('ams_database.xlsx', mode='a', if_sheet_exists='overlay') as writer:
                self.newDf.to_excel(writer, index=False, sheet_name='Flight Instance', header=False, startrow=len(self.db_instance)+1)
        except:
            QMessageBox.critical(self, 'Error', 'Unexpected Error')
            return None

        self.check_continue = True



    def second_page_validator(self):
        self.ui.add_schedule_input_weekly_time_hour.setValidator(QIntValidator(0,24,self))
        self.ui.add_schedule_input_weekly_time_min.setValidator(QIntValidator(0,59,self))
        self.ui.add_schedule_input_custom_time_hour.setValidator(QIntValidator(0,24,self))
        self.ui.add_schedule_input_weekly_time_min.setValidator(QIntValidator(0,59,self))
        self.ui.add_schedule_input_custom_day.setValidator(QIntValidator(self))
        self.ui.add_schedule_input_custom_time_min.setValidator(QIntValidator(self))
        # self.ui.add_schedule_input_inst_gate.setValidator(QIntValidator(self))
        self.ui.add_schedule_input_finst_current_hour.setValidator(QIntValidator(self))
        self.ui.add_schedule_input_finst_current_min.setValidator(QIntValidator(self))
        self.ui.add_schedule_input_finst_update_hour.setValidator(QIntValidator(self))
        self.ui.add_schedule_input_finst_update_min.setValidator(QIntValidator(self))
        self.ui.add_schedule_input_fn.setValidator(QIntValidator(1,99,self))

    def clear_inputs(self):
        self.ui.add_schedule_input_fn.clear()
        self.ui.add_schedule_input_weekly_time_hour.clear()
        self.ui.add_schedule_input_weekly_time_min.clear()
        self.ui.add_schedule_input_custom_time_min.clear()
        self.ui.add_schedule_input_custom_time_min.clear()
        self.ui.add_schedule_input_custom_day.clear()