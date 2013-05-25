#!/usr/bin/python
# -*- coding: cp1252 -*-
from mechanize import *
import os
import ftplib

class SyncAccount:
	def __init__(self,username,password):
		 self.username = username
        self.password = password
        self.courses = {}
        self.sel_courses={}
        self.br=Browser()
        self.br.set_handle_equiv(True)
        #self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        self.logged1=False
        self.logged2=False
        try:
            self.login_moodle()
        except : None
        try:
            self.login_bighome()
        except: None

    def login_moodle(self):
        self.br.open('http://moodle.iitb.ac.in')
        print self.br.title()
        self.br.select_form(nr=1)
        self.br.form.controls[0].readonly = False # make server_id writeable
        self.br.form.controls[1].readonly = False # make server_id writeable
        self.br["username"] = self.username
        self.br["password"] = self.password
        self.br.submit()
        if not "Login" in self.br.title():
            self.logged1=True
            print "Moodle Logged In"

    def login_bighome(self):
        self.s=ftplib.FTP('bighome.iitb.ac.in' , self.username , self.password)
        if self.islog2():
            self.logged2=True
            print "Bighome Logged In"

    def islog1(self):
        if not "Login" in self.br.title():
            print "not logged in"
            return True
        else : return False

    def islog2(self):
        try :
            self.s.nlst()
            return True
        except : return False



