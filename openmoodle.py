import re
import mechanize
import urllib, os
import math, random, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Sync_Account(QThread):
    def __init__(self, parent= None):
        QThread.__init__(self, parent)
        self.auth_set = False
        self.logged_in = False

        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')]

    def loginCredentials(self, username, password):
        self.username = username
        self.password = password
        self.method = "loginCredentials"
        print "starting thread"
        self.start()
        
    def loginCredentialsRun(self):
        username = self.username
        password = self.password
        self.auth_set = True
        try:
            self.login()
            if self.logged_in:
                self.emit(SIGNAL("login_status(QString)"), "Logged In")
                print "logged in"
            else:
                self.emit(SIGNAL("login_status(QString)"), "Login Failed") 
                print "error logging in"
        except:
            self.emit(SIGNAL("login_status(QString)"), "Error")
            print "exception error"


    def login(self):
        self.br.open("http://moodle.iitb.ac.in")
        print self.br.title()
        assert self.br.viewing_html()
        self.br.select_form(nr=1)
        for i in range(3):
            self.br.form.controls[i].readonly = False
        self.br["username"] = self.username
        self.br["password"] = self.password
        self.br.submit()
        
        # Title of login page is "Login to Moodle"
        # If no Login in title => We are not on login page
        # Assuming we landed inside moodle
        if not "Login" in self.br.title():
           self.logged_in = True
           print "Logged In"    



    def run(self):
        if self.method == "loginCredentials":
            self.loginCredentialsRun()
     
    def __del__(self):
    
        self.exiting = True
        self.wait()    

