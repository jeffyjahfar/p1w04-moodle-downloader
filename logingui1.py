#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import os
from openmoodle import Sync_Account

class LoginGUI(QtGui.QWidget):
    
    def __init__(self):
        super(LoginGUI, self).__init__()
        self.isset_credentials = False
        self.sync = Sync_Account()
        self.initUI()
        
    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        #self.setToolTip('Login with your<b>LDAP</b> username and password')
        ###################### Login Frame ###########################
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid) 
        self.setGeometry(300, 300, 300, 180)
        self.setWindowTitle('Moodle File Downloader')
        self.setWindowIcon(QtGui.QIcon('moodleicon.png')) 

        self.username = QtGui.QLabel('Username')
        self.password = QtGui.QLabel('Password')
       
        self.usernameEdit = QtGui.QLineEdit()
        self.passwordEdit = QtGui.QLineEdit()
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.Password)

        grid.addWidget(self.username, 1, 0)
        grid.addWidget(self.usernameEdit, 1, 1)

        grid.addWidget(self.password, 2, 0)
        grid.addWidget(self.passwordEdit, 2, 1)
       
        self.cb = QtGui.QCheckBox("Remember Credentials")
        grid.addWidget(self.cb,3,1)
        self.cb.toggle()
       #cb.stateChanged.connect(self.rem_credentials(self,username,password))      call rem_credentials() function here    
                
        self.login_button = QtGui.QPushButton("&Login")
        #self.login_button.resize(login_button.sizeHint())
        grid.addWidget(self.login_button, 4, 1)   

        self.connect( self.login_button, QtCore.SIGNAL("clicked()"), self.initiate_login)
 

      # btn.clicked.connect(login_moodle(self))        
      #  qbtn = QtGui.QPushButton('Cancel', self)
      #  qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
      #  qbtn.resize(qbtn.sizeHint())
      # grid.addWidget(qbtn,4,1)
        
        self.show()

    def initiate_login(self):
        self.login_button.setEnabled(False)
        print "Adding Credentials"
        u = self.usernameEdit.text()
        p = self.passwordEdit.text()
        #print u,p
        if self.cb.isChecked():
            print "Saving Credentials"
            f = open("./.savedcredentials","w")
            f.write("%s|%s" % (u,p))
            f.close()
        #else:
        #    os.remove("./.savedcredentials") # Remove credentials if the user doesn't want to keep them remembered.
        self.isset_credentials = True
        self.u = u
        self.p = p
        print "Now firing thread request"
        self.sync.loginCredentials(u,p)
        
       
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = LoginGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
