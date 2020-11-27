# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 16:12:49 2020

@author: AI & ML
"""

from PyQt5 import  QtWidgets,uic
from dbms import Student,Employee

def gotostudentlogin():
    homePage.close()
    studentLoginPage.show()

def gotofacultylogin():
    homePage.close()
    facultyLoginPage.phoneEnter.setText('')
    facultyLoginPage.passwordEnter.setText('')
    facultyLoginPage.show()

def backfromfaclogin():
    facultyLoginPage.close()
    homePage.show()

def backfromstudentlogin():
    studentLoginPage.close()
    homePage.show()

def gotofacultydashboard():
    
    Ephone = facultyLoginPage.phoneEnter.text()
    Epassword = facultyLoginPage.passwordEnter.text()
    
    e = Employee()
    ret = e.fetch_faculty(Ephone,Epassword)
    
    if ret:
        facultyLoginPage.close()
        facultyDashboard.show()
    else:
        facultyLoginPage.phoneEnter.setText('')
        facultyLoginPage.passwordEnter.setText('')

def backtofacultylogin():
    facultyLoginPage.phoneEnter.setText('')
    facultyLoginPage.passwordEnter.setText('')
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
    studentLoginPage.close()
    studentDashboard.show()
    

def studentlogout():
    studentDashboard.close()
    studentLoginPage.show()


app = QtWidgets.QApplication([])

homePage = uic.loadUi('Uifiles/FrontPage.ui')
studentLoginPage = uic.loadUi('Uifiles/student_login.ui')
facultyLoginPage = uic.loadUi("Uifiles/faculty_login.ui")
facultyDashboard = uic.loadUi("Uifiles/faculty_dashboard.ui")
studentRegisterPage = uic.loadUi("Uifiles/student_register.ui")
studentDashboard = uic.loadUi("Uifiles/studentDashboard.ui")

homePage.show()
homePage.studentLoginBut.clicked.connect(gotostudentlogin)
homePage.facultyLoginBut.clicked.connect(gotofacultylogin)

facultyLoginPage.backBut.clicked.connect(backfromfaclogin)
facultyLoginPage.loginBut.clicked.connect(gotofacultydashboard)


studentLoginPage.backBut.clicked.connect(backfromstudentlogin)
studentLoginPage.loginBut.clicked.connect(gotostudentdashboard)

studentDashboard.logoutBut.clicked.connect(studentlogout)

facultyDashboard.backBut.clicked.connect(backtofacultylogin)
facultyDashboard.registerStudentBut.clicked.connect(gotostudentregister)

studentRegisterPage.backBut.clicked.connect(backfromstudentregister)
studentRegisterPage.captureBut.clicked.connect(capturedata)
app.exec()