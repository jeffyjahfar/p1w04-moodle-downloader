#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import os
#from main import *

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
        grid.setSpacing(10)

        grid.addWidget(username, 1, 0)
        grid.addWidget(usernameEdit, 1, 1)

        grid.addWidget(password, 2, 0)
        grid.addWidget(passwordEdit, 2, 1)
       
        self.setLayout(grid) 
        self.setGeometry(300, 300, 300, 180)
        self.setWindowTitle('Moodle File Downloader')
        self.setWindowIcon(QtGui.QIcon('moodleicon.png')) 

        cb = QtGui.QCheckBox('Remember Credentials', self)
        grid.addWidget(cb,3,1)
        cb.toggle()
       #cb.stateChanged.connect(self.rem_credentials(self,username,password))      call rem_credentials() function here    
                
        btn = QtGui.QPushButton('Login', self)
        btn.resize(btn.sizeHint())
        grid.addWidget(btn, 4, 1)
       # btn.clicked.connect(login_moodle(self))
        
      #  qbtn = QtGui.QPushButton('Cancel', self)
      #  qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
      #  qbtn.resize(qbtn.sizeHint())
       # grid.addWidget(qbtn,4,1)
        
        self.show()

"""  def rem_credentials(self, username,password) : 
       find out how to do it
      
        if state == QtCore.Qt.Checked:
            pass
        else:
            pass 
"""

        
       
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    