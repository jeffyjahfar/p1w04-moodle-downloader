#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import os

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        #self.setToolTip('Login with your<b>LDAP</b> username and password')
        username = QtGui.QLabel('Username')
        password = QtGui.QLabel('Password')
       
        usernameEdit = QtGui.QLineEdit()
        passwordEdit = QtGui.QLineEdit()
       

        grid = QtGui.QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(username, 1, 0)
        grid.addWidget(usernameEdit, 1, 1)

        grid.addWidget(password, 2, 0)
        grid.addWidget(passwordEdit, 2, 1)
        
        self.setLayout(grid) 
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Moodle File Downloader')
        self.setWindowIcon(QtGui.QIcon('moodleicon.png'))     
        
        
        btn = QtGui.QPushButton('Login', self)
        btn.resize(btn.sizeHint())
        btn.move(35, 120)
        
        qbtn = QtGui.QPushButton('Cancel', self)
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(135, 120)
        
        self.show()
        
       
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    