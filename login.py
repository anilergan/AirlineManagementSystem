from PyQt5.QtWidgets import QMessageBox, QWidget
import pandas as pd



class Login(QWidget):


    login_continue_check = False
    person_type = None
    the_one_name = None
    the_one_surname = None
    
    def __init__(self, input_mail, input_password):
        super().__init__()
        self.check_login=False
        self.inp_mail = input_mail
        self.inp_password = input_password
        # self.query = "SELECT * from person"
 
        self.db = pd.read_excel('ams_database.xlsx', sheet_name='Person')
        self.check_mail = self.db.isin([self.inp_mail]).any().any()
        if self.check_mail == False:
            QMessageBox.critical(self,'Account Error', 'There is no account detected with this mail adress')
            return None
        
        self.df_account_password = self.db[self.db["Mail"] == self.inp_mail][["Password"]]
        self.df_account_password = self.df_account_password.reset_index(drop=True)

        self.account_password = self.df_account_password.iloc[0,0]
        if str(self.account_password) != self.inp_password:
            QMessageBox.critical(self,'Password Error', 'Wrong password')
            return None
        self.check_login=True

    def person_type_director(self):
        self.df_person_type = self.db[self.db["Mail"] == self.inp_mail][["Person type"]]
        self.df_person_type = self.df_person_type.reset_index(drop=True)
        self.person_type = self.df_person_type.iloc[0,0]
        return self.person_type

    def recognise_person(self):
        self.df_recognise_person = self.db[self.db["Mail"] == self.inp_mail][["Name","Surname"]]
        self.df_person_type = self.df_person_type.reset_index(drop=True)
        self.the_one_name = self.df_recognise_person.iloc[0,0]
        self.the_one_surname = self.df_recognise_person.iloc[0,1]
        return self.the_one_name + ' ' + self.the_one_surname

        # self.login_continue_check = True
        # return self.login_continue_check

        

            

    
        
