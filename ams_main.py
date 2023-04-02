#     My Moduls
from creating_new_person import newPersonCreator
from login import Login
from admin import Admin
from ams_add_schedule import AddScheduleWindow

#     Tasarım kütüphaneleri
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from amsqt2 import Ui_MainWindow

#     Veri tabanı kütüphaneler
# from sqlalchemy import create_engine
import pandas as pd


#    Diğer kütüphaneler
# from datetime import datetime, timedelta






#Code


class AppWindow(QMainWindow):

    #   Veri tabanı bağlantısı
    # engine = create_engine("mysql+pymysql://root:Hd3yxfGb@localhost/ams")
    # local values
    flight_trw = 0 #total row number of flight table



    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        #Manuel QT Tasarım Ayarlamalar
        self.ui.combobox_person_type.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.ui.combobox_person_type.view().window().setAttribute(Qt.WA_TranslucentBackground)

        #page index values
        self.Page_welcome_index = 0
        self.Page_newuser_index = 1
        self.Page_login_index = 2
        self.Page_admin_index = 3
        self.Page_customer_index = 4
        self.Page_pilot_index = 5

        



        #start program at first page
        self.go_page_welcome() #0

        #welcome page buttons
        self.ui.button_login.clicked.connect(self.go_page_login) #1.1
        self.ui.button_signup.clicked.connect(self.go_page_newuser) #1.2

        #newuser page buttons
        self.ui.button_to_login_page.clicked.connect(self.go_page_login) #1.1
        self.ui.button_signin_confirm.clicked.connect(self.progress_of_creating_new_person) #2.1

        #login page buttons
        self.ui.button_back_signup.clicked.connect(self.go_page_newuser) #1.2
        self.ui.button_login_confirm.clicked.connect(self.progress_of_login) #3.1


    #admin page buttons
        #flight tab buttons
        self.ui.button_flight_add.clicked.connect(self.reach_add_flight) #4.1
        self.ui.button_cal_duration.clicked.connect(self.reach_calculate_duration)
        
        self.ui.button_flight_cancel.clicked.connect(self.reach_cancel_flight) #4.2

        self.ui.button_flight_add_schedule.clicked.connect(self.reach_add_flight_schedule) #4.4
        self.ui.button_get_schedule.clicked.connect(self.reach_get_flight_schedule) #4.4
        self.ui.button_cancel_schedule_w.clicked.connect(self.reach_cancel_schedule_weekly)
        self.ui.button_cancel_schedule_c.clicked.connect(self.reach_cancel_schedule_custom)
        self.ui.button_get_instance.clicked.connect(self.reach_get_flight_instances) #4.4
        self.ui.button_cancel_instance.clicked.connect(self.reach_cancel_flight_instances) #4.4
        self.ui.button_resync_tables.clicked.connect(self.reach_return_db)


        self.ui.button_current_flights.clicked.connect(self.reach_current_flight_instances)
        self.ui.button_past_flights.clicked.connect(self.reach_past_flight_instances)
        
        #aircraft tab buttons
        self.ui.aircraft_button_add.clicked.connect(self.reach_add_aircraft)
        self.ui.aircraft_button_delete.clicked.connect(self.reach_del_aircraft)
        self.ui.aircraft_button_assign.clicked.connect(self.reach_assign_aircraft)

        #pilot tab buttons
        self.ui.button_assign_pilot.clicked.connect(self.reach_assign_pilot)
        self.ui.button_del_assign_pilot.clicked.connect(self.reach_del_assign_pilot)

        #logout tab button 
        self.ui.admin_logout.clicked.connect(self.go_page_login)
    

    #pilot page buttons
        self.ui.pilot_logout.clicked.connect(self.go_page_login)


    # ***************** SIGNAL- SLOT ********************

# -------------------------- PILOT -------------------------------

    def show_pilot_name(self):
        # db = pd.read_sql('person', self.engine)
        db = pd.read_excel('ams_database.xlsx', sheet_name='Person')
        self.pilot_mail = self.ui.login_input_mail.text()
        self.db_pilot = db[db['Mail'] == self.pilot_mail][['Name', 'Surname']]
        self.pilot_name = self.db_pilot.iloc[0,0] 
        self.pilot_surname = self.db_pilot.iloc[0,1]
        self.pilot_name = self.pilot_name + ' ' + self.pilot_surname
        self.ui.pilot_name.setText(self.pilot_name)




# -------------------------- ADMIN -------------------------------

    def reach_del_assign_pilot(self):
        self.newAdmin = Admin()
        self.db = self.newAdmin.del_assign_pilot(
            self.ui.assign_pilot_name.text(),
            self.ui.assign_pilot_surname.text(),
            self.ui.assign_pilot_flight_number.text()            
        )
        self.check_db = isinstance(self.db, pd.core.frame.DataFrame)
        if self.check_db == True:
            self.ui.table_pilot_assign.setRowCount(len(self.db))
            for row in range(0, len(self.db)):
                for col in range(0,len(self.db.columns)):
                    self.ui.table_pilot_assign.setItem(row, col, QTableWidgetItem(str(self.db.iloc[row,col])))
            QMessageBox.information(self, 'Pilot assigned is deleted', f'Pilot assigned is deleted succeed!')       
   
    
    def reach_assign_pilot(self):
        self.newAdmin = Admin()
        self.db = self.newAdmin.assign_pilot(
            self.ui.assign_pilot_name.text(),
            self.ui.assign_pilot_surname.text(),
            self.ui.assign_pilot_flight_number.text()
        )
        self.check_db = isinstance(self.db, pd.core.frame.DataFrame)
        if self.check_db == True:
            self.ui.table_pilot_assign.setRowCount(len(self.db))
            for row in range(0, len(self.db)):
                for col in range(0,len(self.db.columns)):
                    self.ui.table_pilot_assign.setItem(row, col, QTableWidgetItem(str(self.db.iloc[row,col])))
            QMessageBox.information(self, 'Pilot has assigned', f'Pilot {self.ui.assign_pilot_name.text()} {self.ui.assign_pilot_surname.text()} has been assigned succeed!')       



    def reach_add_aircraft(self):
        self.newAdmin = Admin()
        self.db = self.newAdmin.add_aircraft(
            self.ui.aircraft_input_name.text(),
            self.ui.aircraft_input_model.text(),
            self.ui.aircraft_input_man_year.text(),
            self.ui.aircraft_combo_airline.currentText(),
            self.ui.aircraft_input_add_id.text()
        )

        self.check_db = isinstance(self.db, pd.core.frame.DataFrame)
        if self.check_db == True:
            self.ui.table_aircraft.setRowCount(len(self.db))
            for row in range(0, len(self.db)):
                for col in range(0,len(self.db.columns)):
                    self.ui.table_aircraft.setItem(row, col, QTableWidgetItem(str(self.db.iloc[row,col])))
            QMessageBox.information(self, 'Aircraft has added', 'The aircraft has been regestered succeed!')       

    
    def reach_assign_aircraft(self):
        self.newAdmin = Admin()
        self.db = self.newAdmin.assign_aircraft(
            self.ui.aircraft_input_assign_flight_number.text(),
            self.ui.aircraft_input_assign_id.text()          
        )
        self.check_db = isinstance(self.db, pd.core.frame.DataFrame)
        if self.check_db == True:
            self.ui.table_aircraft.setRowCount(len(self.db))
            for row in range(0, len(self.db)):
                for col in range(0,len(self.db.columns)):
                    self.ui.table_aircraft.setItem(row, col, QTableWidgetItem(str(self.db.iloc[row,col])))
            QMessageBox.information(self, 'Aircraft has been assigned', 'The aircraft has been assigned succeed!')           


    def reach_del_aircraft(self):
        self.newAdmin = Admin()
        self.db = self.newAdmin.del_aircraft(
            self.ui.aircraft_input_delete_no.text()

        )

        self.check_db = isinstance(self.db, pd.core.frame.DataFrame)
        if self.check_db == True:
            self.ui.table_aircraft.setRowCount(len(self.db))
            for row in range(0, len(self.db)):
                for col in range(0,len(self.db.columns)):
                    self.ui.table_aircraft.setItem(row, col, QTableWidgetItem(str(self.db.iloc[row,col])))
            QMessageBox.information(self, 'Aircraft has deleted', 'The aircraft has been deleted succeed!')       



    def reach_cancel_schedule_weekly(self):

        self.newAdmin = Admin()
        self.db = self.newAdmin.cancel_flight_schedule_weekly(self.ui.input_schedule_flight_number.text())
        
        check_db = isinstance(self.db, pd.core.frame.DataFrame)
        if check_db == True:
            self.ui.table_w_schedule.setRowCount(len(self.db))
            for row in range(0, len(self.db)):
                for col in range(0,len(self.db.columns)):
                    self.ui.table_w_schedule.setItem(row, col, QTableWidgetItem(str(self.db.iloc[row,col])))
            QMessageBox.information(self, 'Cancel Succeed', f'The flight schedule has canceled succeed')
               


    def reach_cancel_schedule_custom(self): 
        self.newAdmin = Admin()
        self.db = self.newAdmin.cancel_flight_schedule_custom(self.ui.input_schedule_flight_number.text())
        
        self.check_db = isinstance(self.db, pd.core.frame.DataFrame)
        if self.check_db == True:
            self.ui.table_c_schedule.setRowCount(len(self.db))
            for row in range(0, len(self.db)):
                for col in range(0,len(self.db.columns)):
                    self.ui.table_c_schedule.setItem(row, col, QTableWidgetItem(str(self.db.iloc[row,col])))
            QMessageBox.information(self, 'Cancel Succeed', f'The flight schedule has canceled succeed')


    def reach_add_flight_schedule(self):
        self.newAdmin = Admin() #admin open the page
        self.newAdmin.open_add_flight_schedule()



    
    
    def reach_get_flight_schedule(self):
        self.newAdmin = Admin()
        self.newAdmin.get_flight_schedule_process(
            self.ui.input_schedule_flight_number.text()
        )
        if self.newAdmin.check_get_flight == True:
            self.df_weekly = self.newAdmin.get_weekly_flight_schedule(
                self.ui.input_schedule_flight_number.text())
            self.df_custom = self.newAdmin.get_custom_flight_schedule(
                self.ui.input_schedule_flight_number.text())
        else: 
            self.df_weekly = 'None'
            self.df_custom = 'None'
        
        self.check_df_weekly = isinstance(self.df_weekly, pd.core.frame.DataFrame)
        if self.check_df_weekly == True:  
            self.ui.table_w_schedule.setRowCount(len(self.df_weekly))
            for row in range(0,len(self.df_weekly)):
                for col in range(0,len(self.df_weekly.columns)):
                    self.ui.table_w_schedule.setItem(row,col,QTableWidgetItem(str(self.df_weekly.iloc[row,col])))
        
        self.check_df_custom = isinstance(self.df_custom, pd.core.frame.DataFrame)
        if self.check_df_custom == True: 
            self.ui.table_c_schedule.setRowCount(len(self.df_custom))
            for row in range(0,len(self.df_custom)):
                for col in range(0,len(self.df_custom.columns)):
                    self.ui.table_c_schedule.setItem(row,col,QTableWidgetItem(str(self.df_custom.iloc[row,col])))
        
        if self.check_df_custom == True and self.check_df_weekly != True:
            QMessageBox.information(self, 'Operation Succeed', f'Flight of {self.ui.input_schedule_flight_number.text()} has {len(self.df_custom)} custom and no weekly schedule')
        elif self.check_df_custom != True and self.check_df_weekly == True:
            QMessageBox.information(self, 'Operation Succeed', f'Flight of {self.ui.input_schedule_flight_number.text()} has {len(self.df_weekly)} weekly and no custom schedule')
        elif self.check_df_custom == True and self.check_df_weekly == True:
            QMessageBox.information(self, 'Operation Succeed', f'Flight of {self.ui.input_schedule_flight_number.text()} has {len(self.df_weekly)} weekly and {len(self.df_custom)} custom schedule')
        else: 
            QMessageBox.information(self, 'No detected Schedule', f'There is no detected schedule of the flight {self.ui.input_schedule_flight_number.text()}')



    def reach_cancel_flight_instances(self):
        self.newAdmin = Admin()
        self.newAdmin.cancel_flight_instances(
            self.ui.input_instance_flight_number.text()
        )
    
    def reach_current_flight_instances(self):
        self.newAdmin = Admin()
        self.db = self.newAdmin.current_flight
 

    def reach_past_flight_instances(self):
        pass
    
    def reach_get_flight_instances(self):
        self.newAdmin = Admin()
        self.db = self.newAdmin.get_flight_instances(
            self.ui.input_instance_flight_number.text()
        )
        check_db = isinstance(self.db, pd.core.frame.DataFrame)
        if check_db == True:
            self.ui.table_flight_instance.setRowCount(len(self.db))
            for row in range(0, len(self.db)):
                for col in range(0,len(self.db.columns)):
                    self.ui.table_flight_instance.setItem(row, col, QTableWidgetItem(str(self.db.iloc[row,col])))
            QMessageBox.information(self, 'Cancel Succeed', f'The flight instance has canceled succeed')


    def reach_db_for_pilot(self):
        self.newAdmin = Admin()
        self.p_db = self.newAdmin.return_pilotassign_db()
        self.i_db = self.newAdmin.return_instance_db()

        # db = pd.read_sql('person', self.engine)
        db = pd.read_excel('ams_database.xlsx', sheet_name='Person')
        self.pilot_mail = self.ui.login_input_mail.text()
        self.db_pilot = db[db['Mail'] == self.pilot_mail][['Name', 'Surname']]
        self.pilot_name = self.db_pilot.iloc[0,0] 
        self.pilot_surname = self.db_pilot.iloc[0,1]        
        self.p_dbS = self.p_db[(self.p_db['Pilot Name'] == self.pilot_name) & (self.p_db['Pilot Surname'] == self.pilot_surname)][['Flight Number']]
        if len(self.p_dbS) == 0:
            QMessageBox.information(self,'No Assignment', f'There is no flight that is assigned to you, {self.pilot_name} {self.pilot_surname}')
        else:
            self.pilotnum = self.p_dbS.iloc[0,0]
            self.i_db_pilotnum = self.i_db[self.i_db['Flight Number'] == self.pilotnum]   
            self.ui.table_forpilot.setRowCount(len(self.i_db_pilotnum))
            for row in range(0, len(self.i_db_pilotnum)):
                for col in range(0,len(self.i_db_pilotnum.columns)):
                    self.item = QTableWidgetItem(str(str(self.i_db_pilotnum.iloc[row,col])))
                    self.item.setTextAlignment(Qt.AlignCenter)
                    self.ui.table_forpilot.setItem(row, col, self.item)


    def reach_return_db(self):
        self.newAdmin = Admin()
        self.f_db = self.newAdmin.return_flight_db()
        self.ws_db = self.newAdmin.return_weekly_schedule_db()
        self.c_db = self.newAdmin.return_custom_schedule_db()
        self.a_db = self.newAdmin.return_aircraft_db()
        self.i_db = self.newAdmin.return_instance_db()
        self.p_db = self.newAdmin.return_pilotassign_db()

        #do not show flight instances with flight status 'PAST'
        # self.i_db = self.i_db[self.i_db['Status'] != 'PAST']

        #flight table bastır
        self.ui.table_flight.setRowCount(len(self.f_db))
        for row in range(0, len(self.f_db)):
            for col in range(0,len(self.f_db.columns)):
                self.ui.table_flight.setItem(row, col, QTableWidgetItem(str(self.f_db.iloc[row,col])))
        #weekly schedule table bastır
        self.ui.table_w_schedule.setRowCount(len(self.ws_db))
        for row in range(0, len(self.ws_db)):
            for col in range(0, len(self.ws_db.columns)):
                self.ui.table_w_schedule.setItem(row, col, QTableWidgetItem(str(self.ws_db.iloc[row,col])))

        #custom schedule table bastır
        self.ui.table_c_schedule.setRowCount(len(self.c_db))
        for row in range(0, len(self.c_db)):
            for col in range(0,len(self.c_db.columns)):
                self.ui.table_c_schedule.setItem(row, col, QTableWidgetItem(str(self.c_db.iloc[row,col])))
        # aircraft table bastır
        self.ui.table_aircraft.setRowCount(len(self.a_db))
        for row in range(0, len(self.a_db)):
            for col in range(0,len(self.a_db.columns)):
                self.ui.table_aircraft.setItem(row, col, QTableWidgetItem(str(self.a_db.iloc[row,col])))
        
        # pilot assign table bastır
        self.ui.table_pilot_assign.setRowCount(len(self.p_db))
        for row in range(0, len(self.p_db)):
            for col in range(0,len(self.p_db.columns)):
                self.ui.table_pilot_assign.setItem(row, col, QTableWidgetItem(str(self.p_db.iloc[row,col])))
        
        # instance table bastır
        self.ui.table_flight_instance.setRowCount(len(self.i_db))
        for row in range(0, len(self.i_db)):
            for col in range(0,len(self.i_db.columns)):
                self.ui.table_flight_instance.setItem(row, col, QTableWidgetItem(str(self.i_db.iloc[row,col])))
        



    def reach_add_flight(self):
        self.newAdmin = Admin()
        self.db = self.newAdmin.add_flight(
            self.ui.combobox_flight_departure.currentText(),
            self.ui.combobox_flight_arrival.currentText(),
            self.ui.input_add_flight_number.text())
        check_db = isinstance(self.db, pd.core.frame.DataFrame)
        if check_db == True:
            self.ui.table_flight.setRowCount(len(self.db))
            for row in range(0, len(self.db)):
                for col in range(0,len(self.db.columns)):
                    self.ui.table_flight.setItem(row, col, QTableWidgetItem(str(self.db.iloc[row,col])))
            QMessageBox.information(self, 'Flight has added!', 'The flight has been regestered succeed!')       


    def reach_calculate_duration(self):
        self.newAdmin = Admin()

        self.duration = self.newAdmin.calculate_duration(
            self.ui.combobox_flight_departure.currentText(),
            self.ui.combobox_flight_arrival.currentText(),
            )
    
        self.duration = int(self.duration)
        self.hour = int(self.duration/60)
        self.hour = str(self.hour)
        self.minute = self.duration%60
        self.minute = str(self.minute)
        self.ui.label_show_evaluate_duration_hour.setText(self.hour)
        self.ui.label_show_evaluate_duration_minute.setText(self.minute)



    
    def reach_cancel_flight(self):
        self.newAdmin = Admin()
        self.db = self.newAdmin.cancel_flight(self.ui.input_cancel_flight_number.text())
        
        check_db = isinstance(self.db, pd.core.frame.DataFrame)
        if check_db == True:
            self.ui.table_flight.setRowCount(len(self.db))
            for row in range(0, len(self.db)):
                for col in range(0,len(self.db.columns)):
                    self.ui.table_flight.setItem(row, col, QTableWidgetItem(str(self.db.iloc[row,col])))
            QMessageBox.information(self, 'Cancel Succeed', f'The flight described by {self.ui.input_cancel_flight_number.text()} has canceled succeed')
       


        # ----------------------------------------------------------------------------------------------------

    #start program at first page
    def go_page_welcome(self): 
        self.ui.stackedWidget.setCurrentIndex(self.Page_welcome_index)
    

    #welcome page buttons
    def go_page_newuser(self):   
        self.ui.stackedWidget.setCurrentIndex(self.Page_newuser_index)

    #welcome page buttons
    def go_page_login(self):
        self.ui.login_input_mail.clear()
        self.ui.login_input_pasword.clear()
        self.ui.stackedWidget.setCurrentIndex(self.Page_login_index)



    # This one called from creating_new_person
    def sign_in_page_director(self):
        if self.person_type == 'Customer':
            self.ui.stackedWidget.setCurrentIndex(self.Page_customer_index)
            QMessageBox.information(self, 'Sign up notification', 'Regestering succesed!')
        elif self.person_type == 'Pilot': 
            self.ui.stackedWidget.setCurrentIndex(self.Page_pilot_index)
            QMessageBox.information(self, 'Sign up notification', 'Sign up succesed!')
        elif self.person_type == 'Crew': 
            self.ui.stackedWidget.setCurrentIndex(self.Page_pilot_index)
            QMessageBox.information(self, 'Sign up notification', 'Sign up succesed!')
    
    #login page buttons
    def log_in_page_director(self, ptype, name):
        self.ptype = ptype
        self.name = name
        if ptype == 'Customer':
            self.ui.stackedWidget.setCurrentIndex(self.Page_customer_index)
            QMessageBox.information(self, 'Customer Login Succeed', f'Dear {self.name}, welcome to AMS!')
        elif ptype == 'Pilot':
            self.ui.stackedWidget.setCurrentIndex(self.Page_pilot_index)
            self.show_pilot_name()
            self.reach_db_for_pilot()
            QMessageBox.information(self, 'Pilot Login Succeed', f'Dear {self.name}, welcome to AMS!')
        elif ptype == 'Crew':
            self.ui.stackedWidget.setCurrentIndex(self.Page_pilot_index)
            self.reach_db_for_pilot()
            QMessageBox.information(self, 'Crew Login Succeed', f'Dear {self.name}, welcome to AMS!')
        elif ptype == 'Admin':
            self.ui.stackedWidget.setCurrentIndex(self.Page_admin_index)
            self.reach_return_db()
            self.validator_admin()
            QMessageBox.information(self, 'Admin Login Succeed', 'Hey admin! How have you been?')



    #login page buttons
    def progress_of_creating_new_person(self):
        self.name = self.ui.newuser_input_name.text()
        self.surname = self.ui.newuser_input_surname.text()
        self.street = self.ui.newuser_input_streetaddress.text()
        self.city = self.ui.newuser_input_city.text()
        self.state =  self.ui.newuser_input_state.text()
        self.zip_code = self.ui.newuser_input_zipcode.text()
        self.country = self.ui.newuser_input_country.text()        
        self.mail = self.ui.newuser_input_mail.text()
        self.phone = self.ui.newuser_input_phone.text()
        self.password = self.ui.newuser_input_password.text()
        self.password2 = self.ui.newuser_input_password2.text()
        self.person_type = self.ui.combobox_person_type.currentText()
        self.dbperson = pd.read_excel('ams_database.xlsx', sheet_name='Person')
        
        self.personCreator = newPersonCreator(self.name, 
                                              self.surname, 
                                              self.street, 
                                              self.city, 
                                              self.state, 
                                              self.zip_code, 
                                              self.country, 
                                              self.mail, 
                                              self.phone, 
                                              self.password, 
                                              self.password2,
                                              self.person_type,
                                              self.dbperson)

        if newPersonCreator.continue_check == True:
            self.sign_in_page_director()
        

    #login page buttons
    def progress_of_login(self):
        self.input_mail = self.ui.login_input_mail.text()
        self.input_password = self.ui.login_input_pasword.text()
        
        self.newLogin = Login(self.input_mail, self.input_password)
        
        if self.newLogin.check_login == True:
            self.person_type = self.newLogin.person_type_director()
            self.person_fullname = self.newLogin.recognise_person()
            self.log_in_page_director(self.person_type, self.person_fullname)


    def validator_admin(self):
        self.ui.input_add_flight_number.setValidator(QIntValidator(self))
        self.ui.input_cancel_flight_number.setValidator(QIntValidator(self))
        self.ui.input_schedule_flight_number.setValidator(QIntValidator(self))       
        self.ui.input_instance_flight_number.setValidator(QIntValidator(self))
        


def runApp():
    app = QApplication([])
    newWindow = AppWindow()
    newWindow.show()
    app.exec_()
runApp()

