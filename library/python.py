#!/usr/bin/python


from __future__ import print_function
import subprocess
import os
import re
import getpass

User = raw_input("sredy1: \n").lower()
if not re.match("^[a-zA-Z, 0-99]*$", User):
    print ("Error! Only letters and numbers are allowed!")
    break
Pass = getpass.getpass(prompt= "wav9Elbc$xG3: \n")


URL_login = 'cf login --skip-ssl-validation -a https://api.cloud.pcftest.com -u ' + User.lower() + ' -p ' + Pass
subprocess.call(URL_login)
os.system('cf apps > apps.csv')
