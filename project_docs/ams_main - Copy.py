#     My Moduls
from creating_new_person import newPersonCreator
from login import Login
from admin import Admin

#     Tasarım kütüphaneleri
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIntValidator
from amsqt import Ui_MainWindow

#     Veri tabanı kütüphaneler
# i
from sqlalchemy import create_engine
import pandas as pd

#Code

#   Veri tabanı bağlantısı
engine = create_engine("mysql+pymysql://root:Hd3yxfGb@localhost/ams")

#   Tasarım QT
class AppWindow(QMainWindow):
    
    # local values
    flight_trw = 0 #total row number of flight table



    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        #page index values
        self.Page_welcome_index = 0
        self.Page_newuser_index = 1
        self.Page_login_index = 2
        self.Page_admin_index = 3
        self.Page_customer_index = 4
        self.Page_pilot_index = 5
        self.Page_crew_index = 6
        



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
        # self.ui.button_flight_edit_schedule.clicked.connect(self.reach_edit_flight_schedule) #4.3
        self.ui.button_flight_get_instances.clicked.connect(self.reach_get_flight_instances) #4.4
        self.ui.button_recync_tables.clicked.connect(self.reach_return_db)
        

    # ******** SIGNAL- SLOT *************
    def reach_return_db(self):
        self.newAdmin = Admin()
        self.db = self.newAdmin.return_db()
        self.ui.table_flight.setRowCount(len(self.db))
        for row in range(0, len(self.db)):
            for col in range(0,len(self.db.columns)):
                self.ui.table_flight.setItem(row, col, QTableWidgetItem(self.db.iloc[row,col]))
    
    def reach_add_flight(self):
        self.newAdmin = Admin()
        self.db = self.newAdmin.add_flight(
            self.ui.combobox_flight_departure.currentText(),
            self.ui.combobox_flight_arrival.currentText(),
            self.ui.input_add_flight_number.text(),
            self.ui.label_show_evaluate_duration_minute.text(),
            self.ui.label_show_evaluate_duration_hour.text()
            )
        check_db = isinstance(self.db, pd.core.frame.DataFrame)
        if check_db == True:
            self.ui.table_flight.setRowCount(len(self.db))
            for row in range(0, len(self.db)):
                for col in range(0,len(self.db.columns)):
                    self.ui.table_flight.setItem(row, col, QTableWidgetItem(self.db.iloc[row,col]))
            QMessageBox.information(self, 'Flight has added!', 'The flight has been regestered succeed!')       


    def reach_calculate_duration(self):
        self.newAdmin = Admin()

        duration = self.newAdmin.calculate_duration(
            self.ui.combobox_flight_departure.currentText(),
            self.ui.combobox_flight_arrival.currentText(),
            )
    
        duration = int(duration)
        self.hour = int(duration/60)
        self.hour = str(self.hour)
        self.minute = duration%60
        self.minute = str(self.minute)
        self.ui.label_show_evaluate_duration_hour.setText(self.hour)
        self.ui.label_show_evaluate_duration_minute.setText(self.minute)

        self.newAdmin.add_flight


    
    def reach_cancel_flight(self):
        self.newAdmin = Admin()
        self.db = self.newAdmin.cancel_flight(self.ui.input_cancel_flight_number.text())
        
        check_db = isinstance(self.db, pd.core.frame.DataFrame)
        if check_db == True:
            self.ui.table_flight.setRowCount(len(self.db))
            for row in range(0, len(self.db)):
                for col in range(0,len(self.db.columns)):
                    self.ui.table_flight.setItem(row, col, QTableWidgetItem(self.db.iloc[row,col]))
            QMessageBox.information(self, 'Cancel Succeed', f'The flight that described by {self.ui.input_cancel_flight_number.text()} has canceled succeed')
       
        

    def reach_get_flight_instances(self):
        self.newAdmin = Admin()
        self.newAdmin.get_flight_instances()


    #start program at first page
    def go_page_welcome(self): 
        self.ui.stackedWidget.setCurrentIndex(self.Page_welcome_index)
    

    #welcome page buttons
    def go_page_newuser(self):   
        self.ui.stackedWidget.setCurrentIndex(self.Page_newuser_index)

    #welcome page buttons
    def go_page_login(self):
        self.ui.stackedWidget.setCurrentIndex(self.Page_login_index)


    #login page buttons
    # This one called from creating_new_person
    def sign_in_page_director(self):
        if self.person_type == 'Customer':
            self.ui.stackedWidget.setCurrentIndex(self.Page_customer_index)
            QMessageBox.information(self, 'Sign up notification', 'Regestering succesed!')
        elif self.person_type == 'Pilot': 
            self.ui.stackedWidget.setCurrentIndex(self.Page_pilot_index)
            QMessageBox.information(self, 'Sign up notification', 'Sign up succesed!')
        elif self.person_type == 'Crew': 
            self.ui.stackedWidget.setCurrentIndex(self.Page_crew_index)
            QMessageBox.information(self, 'Sign up notification', 'Sign up succesed!')
    
    #login page buttons
    def log_in_page_director(self):
        if Login.person_type == 'Customer':
            self.ui.stackedWidget.setCurrentIndex(self.Page_customer_index)
            QMessageBox.information(self, 'Customer Login Succeed', f'Dear {Login.the_one_name} {Login.the_one_surname}, welcome to AMS!')
        elif Login.person_type == 'Pilot':
            self.ui.stackedWidget.setCurrentIndex(self.Page_pilot_index)
            QMessageBox.information(self, 'Pilot Login Succeed', f'Dear {Login.the_one_name} {Login.the_one_surname}, welcome to AMS!')
        elif Login.person_type == 'Crew':
            self.ui.stackedWidget.setCurrentIndex(self.Page_crew_index)
            QMessageBox.information(self, 'Crew Login Succeed', f'Dear {Login.the_one_name} {Login.the_one_surname}, welcome to AMS!')
        elif Login.person_type == 'Admin':
            self.ui.stackedWidget.setCurrentIndex(self.Page_admin_index)
            self.ui.input_add_flight_number.setValidator(QIntValidator(1,100,self))

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
                                              self.person_type)

        if newPersonCreator.continue_check == True:
            self.sign_in_page_director()
        

    #login page buttons
    def progress_of_login(self):
        self.input_mail = self.ui.login_input_mail.text()
        self.input_password = self.ui.login_input_pasword.text()
        
        self.newLogin = Login(self.input_mail, self.input_password)
        
        if Login.continue_check == True:
            self.log_in_page_director()





        








def runApp():
    app = QApplication([])
    newWindow = AppWindow()
    newWindow.show()
    app.exec_()
runApp()













