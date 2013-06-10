#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from MFD_Main import Sync_Account
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time

class MFD(QMainWindow):
    def __init__(self, parent=None):
        self.isset_credentials = False
        self.sync = Sync_Account()

        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Moodle File Downloader')
        self.setWindowIcon(QIcon('moodleicon.png'))   
        self.create_menu()
        self.create_status_bar()
        self._init_frames()
        self.show_login_frame()

        self.logged_in = False

    def _init_frames(self):
        self.login_frame = QWidget()
        self.main_frame = QWidget()

        ###################### Login Frame ###########################
        vbox = QVBoxLayout()

        # Login Credentials :: Group Box
        qg = QGroupBox("Enter your login credentials :")
        qvbox = QGridLayout()

        # Fields
        ulabel = QLabel("Username:")
        plabel = QLabel("Password:")

        self.usernameEdit = QLineEdit()
        self.usernameEdit.setMinimumWidth(200)
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.passwordEdit.setMinimumWidth(200)

        self.save_credentials = QCheckBox("Remember Credentials")
        self.login_button = QPushButton("&Login")


        qvbox.addWidget(ulabel,0,0)
        qvbox.addWidget(self.usernameEdit,0,1)
        qvbox.addWidget(plabel,1,0)
        qvbox.addWidget(self.passwordEdit,1,1)
        qvbox.addWidget(self.save_credentials,2,1)
        qvbox.addWidget(self.login_button,3,1)

        qg.setLayout(qvbox)
        vbox.addWidget(qg)

        self.login_frame.setLayout(vbox)

        self.connect( self.login_button, SIGNAL("clicked()"), self.initiate_login)

        ####################### Main Frame ###############################
        self.main_frame_box = QVBoxLayout()
        view = QListView()
        self.model = QStandardItemModel()
        view.setModel(self.model)

        self.start_sync_button = QPushButton("&Sync With PC")
        self.log_out_button = QPushButton("&Log Out")

        self.pdfGet = QCheckBox("Download PDF files")
        self.pdfGet.setCheckState(Qt.Checked)
        self.pdfGet.setCheckable(True)

        self.main_frame_box.addWidget(view)
        self.main_frame_box.addWidget(self.start_sync_button)
        self.main_frame_box.addWidget(self.log_out_button)
        self.main_frame_box.addWidget(self.pdfGet)

        self.main_frame.setLayout(self.main_frame_box)


        self.connect( self.start_sync_button, SIGNAL("clicked()"), self.start_sync )
        self.connect( self.log_out_button, SIGNAL("clicked()"), self.log_out)

        ####################### THREAD CONNECTORS ########################
        self.connect(self.sync, SIGNAL("finished()"), self.updateUi)
        self.connect(self.sync, SIGNAL("terminated()"), self.updateUi)
        self.connect(self.sync, SIGNAL("login_status(QString)"), self.login_done)
        self.connect(self.sync, SIGNAL("courses(PyQt_PyObject)"), self.load_courses)
        self.connect(self.sync, SIGNAL("sync_courses(QString)"), self.sync_done)

    def msg_about(self):
        msg = """ 
        Moodle File Downloader
         * Moodle File Downloader is used to sync accounts from moodle
         * Set your username and password
         * Select the folders to be synced
         * Do not close the window unless u want to be logged out
         * Files, as and when uploaded, will be downloaded to the folder
           if the user is logged in.
        """
        QMessageBox.about(self, "Moodle File Downloader", msg.strip())

    def updateUi(self):
        self.start_sync_button.setEnabled(True)
        try:
            self.login_button.setEnabled(True)
        except RuntimeError:
        	print "No Login button"

    def show_login_frame(self):
        self.main_frame.hide()
        self.setCentralWidget(self.login_frame)
        self.login_frame.show()

        try:
            if not self.isset_credentials:
                print "Trying to load credentials from past"
                f = open("./.savedcredentials","r")
                contents = f.read()
                self.u,self.p = contents.split('|')
                self.usernameEdit.setText(self.u)
                self.passwordEdit.setText(self.p)
                self.save_credentials.setCheckState(Qt.Checked) #If the user has ticked "remember credentials" before
        except:
            print "Failed to load credentials :: Loading login frame"

    def login_done(self, msg):
        self.status_text.setText(msg)
        if msg == "Logged In":
            self.logged_in = True
            self.show_main_frame()

    def load_courses(self,courses_list):
        print courses_list
        try:
            f = open("./.selected_list","r")
            selected_list = f.read().split("|")
        except:
            selected_list = []

        print "Selected List"
        print selected_list
        self.checkboxes = []
        
        for item in courses_list:
            cb = QStandardItem(item)
            check = Qt.Checked if item in selected_list else Qt.Unchecked
            cb.setCheckState(check)
            cb.setCheckable(True)
            self.checkboxes.append(cb)
            self.model.appendRow(cb)

    def show_main_frame(self):
        print "Loading Main Frame"
        if not self.logged_in:
            self.show_login_frame()
            return

        self.login_frame.hide()
        self.sync.listCourses()

        self.setCentralWidget(self.main_frame)
        self.main_frame_box.addWidget(self.pdfGet)
        self.main_frame.show()

    def initiate_login(self):
        self.login_button.setEnabled(False)
        print "Adding Credentials"
        u = self.usernameEdit.text()
        p = self.passwordEdit.text()
        #print u,p
        if self.save_credentials.isChecked():
            print "Saving Credentials"
            f = open("./.savedcredentials","w")
            f.write("%s|%s" % (u,p))
            f.close()
       
        self.isset_credentials = True
        self.u = u
        self.p = p
        print "Now firing thread request"
        self.sync.loginCredentials(u,p)

    def start_sync(self):
        checklist = []
        try:
            for box in self.checkboxes:
                if box.checkState() == Qt.Checked:
                    checklist.append(str(box.text()))

            print checklist
        except AttributeError:
            print "No list... Reloading..."
            self.sync.listCourses()            
        f = open("./.selected_list","w")
        f.write("|".join(checklist))
        f.close()
        folderNames={}
        for i in checklist:
            folderNames[i]=i
        self.start_sync_button.setEnabled(False)
        self.status_text.setText("Syncing ... ")
        self.sync.syncCourses(checklist, folderNames, (self.pdfGet.checkState()==Qt.Checked))

    def sync_done(self, msg):
        self.status_text.setText("Finished sync")
        self.start_sync_button.setEnabled(True)

    def log_out(self):
        print "calling log out"
        self.status_text.setText("Logging Out..")
        
        self.sync.logged_out = False
        print "logged out"
        self.status_text.setText("Logged Out")
        self.main_frame.hide()
        exit()

    def create_status_bar(self):
        self.status_text = QLabel("Login Required")
        self.statusBar().addWidget(self.status_text, 1)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")

     	clear_credentials = self.create_action("&Clear Saved Passwords", slot=self.clear_history,
            shortcut="Ctrl+D", tip="Clear Saved Credentials")

        quit_action = self.create_action("&Quit", slot=self.close,
            shortcut="Ctrl+Q", tip="Close the application")

        #open_location = self.create_action("&Open Containing folder", slot=self.open_folder,
        	#shortcut="Ctrl+L", tip="Open the Location of downloaded files")

        self.add_actions(self.file_menu, (clear_credentials,))
        #self.add_action(self.file_menu, (open_location,))
        self.add_actions(self.file_menu, (quit_action,))
        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About",
            shortcut='F1', slot=self.msg_about,
            tip='About Moodle File Downloader')

        self.add_actions(self.help_menu, (about_action,))

    def clear_history(self):
    	print "Clearing Saved Credentials"
        os.remove("./.savedcredentials")

    """ def open_folder(self):
    	pass # find how to do this """


    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action( self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sample = MFD()
    sample.show()
    app.exec_()
    del sample
