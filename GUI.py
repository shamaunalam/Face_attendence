# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 16:12:49 2020

@author: AI & ML
"""

from PyQt5 import  QtWidgets,uic



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
    

app = QtWidgets.QApplication([])

homePage = uic.loadUi('Uifiles/FrontPage.ui')
studentLoginPage = uic.loadUi('Uifiles/student_login.ui')
facultyLoginPage = uic.loadUi("Uifiles/faculty_login.ui")

homePage.show()
homePage.studentLoginBut.clicked.connect(gotostudentlogin)
homePage.facultyLoginBut.clicked.connect(gotofacultylogin)


facultyLoginPage.backBut.clicked.connect(backfromfaclogin)


studentLoginPage.backBut.clicked.connect(backfromstudentlogin)

app.exec()