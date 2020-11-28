# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 16:12:49 2020

@author: AI & ML
"""

from PyQt5 import  QtWidgets,uic
import sqlite3 as sql
from dbms import Student

def gotostudentlogin():
    homePage.close()
    studentLoginPage.show()

def gotofacultylogin():
    homePage.close()
    facultyLoginPage.show()

def backfromfaclogin():
    facultyLoginPage.close()
    homePage.show()

def backfromstudentlogin():
    studentLoginPage.close()
    homePage.show()

def gotofacultydashboard():
    facultyLoginPage.close()
    facultyDashboard.show()    

def backtofacultylogin():
    facultyDashboard.close()
    facultyLoginPage.show()


def gotostudentregister():
    facultyDashboard.close()
    studentRegisterPage.show()

def backfromstudentregister():
    studentRegisterPage.close()
    facultyDashboard.show()
    
def capturedata():
    
    Sid = studentRegisterPage.rollEnter.text()
    Sname = studentRegisterPage.nameEnter.text()
    Sclass_id = studentRegisterPage.classEnter.text()
    Sphone_no = studentRegisterPage.phoneEnter.text()
    Spassword = studentRegisterPage.passwordEnter.text()
    URL = studentRegisterPage.urlEnter.text()
    s = Student()
    s.register(URL, Sid, Sname, Sclass_id, Sphone_no, Spassword)
    
def gotostudentdashboard():
    
    phone = studentLoginPage.phoneEnter.text()
    password = studentLoginPage.passwordEnter.text()
    
    s = Student()
    ret = s.fetch_student(phone,password)
    if ret is not False:        
        studentLoginPage.close()
        studentDashboard.welcomeLabel.setText('Welcome '+ret['Sname'])
        studentDashboard.show()
    

def studentlogout():
    studentDashboard.close()
    studentLoginPage.show()

def viewattendence():
    start = studentDashboard.startDate.text()
    stop = studentDashboard.endDate.text()
    pass



app = QtWidgets.QApplication([])

homePage = uic.loadUi('Uifiles/FrontPage.ui')
studentLoginPage = uic.loadUi('Uifiles/student_login.ui')
facultyLoginPage = uic.loadUi("Uifiles/faculty_login.ui")
facultyDashboard = uic.loadUi("Uifiles/faculty_dashboard.ui")
studentRegisterPage = uic.loadUi("Uifiles/student_register.ui")
studentDashboard = uic.loadUi("Uifiles/studentDashboard.ui")
viewAttendence = uic.loadUi('Uifiles/view_attendence.ui')


homePage.show()
homePage.studentLoginBut.clicked.connect(gotostudentlogin)
homePage.facultyLoginBut.clicked.connect(gotofacultylogin)

facultyLoginPage.backBut.clicked.connect(backfromfaclogin)
facultyLoginPage.loginBut.clicked.connect(gotofacultydashboard)


studentLoginPage.backBut.clicked.connect(backfromstudentlogin)
studentLoginPage.loginBut.clicked.connect(gotostudentdashboard)

studentDashboard.logoutBut.clicked.connect(studentlogout)
studentDashboard.viewBut.clicked.connect(viewattendence)

facultyDashboard.backBut.clicked.connect(backtofacultylogin)
facultyDashboard.registerStudentBut.clicked.connect(gotostudentregister)

studentRegisterPage.backBut.clicked.connect(backfromstudentregister)
studentRegisterPage.captureBut.clicked.connect(capturedata)
app.exec()