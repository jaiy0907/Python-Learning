#!/usr/bin/python3 -i

import os
import system
import commands
from commands import *

PASSWORD_ATTEMPTS = 3
ROOTPATH = '/Users/jaikishan.yadav/Documents/python-learning'
DATABASEPATH = '/Users/jaikishan.yadav/Documents/python-learning/database.txt'
FILEBASENAME = 'filebase.txt'
SSHCONFIG = 'sshconfig.txt'
users = {}
usersloginflags = {}
currentuser = "root"

def load_users():
    with open(DATABASEPATH, mode="rt", encoding="utf-8") as f:
        lines = f.readlines()
        lines = [line.strip('\n') for line in lines]
        for line in lines:
            if line == '':
                continue
            username, password = line.split(':')
            u = system.User(username, password, load=True)
            users[username] = u
            usersloginflags[username] = False

load_users()
if __name__ == "__main__": 
    print(users)




