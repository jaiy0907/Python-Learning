# username password implementation
'''
Commands to interact with the terminal
'''
import os


ATTEMPTS = 3
ROOTPATH = '/Users/jaikishan.yadav/Documents/python-learning'
HOSTPATH = '/Users/jaikishan.yadav/Documents/python-learning/hostxyz'
SERVERNAME = 'hostxyz'
userpswd = {"user1": "1234", 
            "user2": "abcd", 
            "user3": "u12312"}

loginflags = {"user1": 0,
              "user2": 0, 
              "user3": 0}

currentuser = "root"


def ssh(cli_input):
    '''
    SSH into a host

    Args:
        cli_input: a string in the form of [username@hostname]
    '''
    global currentuser
    username, servername = cli_input.split('@') 
    flag = 0
    if servername != SERVERNAME:
        print("Server doesn't exist")
        return
    for users, password in userpswd.items():
        if (username == users):
            if loginflags[username] == 1:
                print("User already logged in.")
                if (currentuser != username):
                    print("Switching User")
                    os.chdir(HOSTPATH)
                    currentuser = username
                return
            flag = 1
            tries = ATTEMPTS
            while tries:
                inp_passwords = input("Enter Password: ")
                if (inp_passwords == password):
                    flag = 2
                    if (os.getcwd() != HOSTPATH):
                        os.chdir(HOSTPATH)
                    currentuser = username
                    loginflags[username] = 1
                    print("Connection Established.")
                    print("You are currently at", os.getcwd())
                    break
                else: 
                    tries -= 1
                print("Wrong Password attempts left:", tries)
    if flag == 1:
        print("Unable to establish connection.")
    if flag == 0:
        print("User not found")


def logout():
    '''
    Logs a user out of the server. If not logged into a server, does nothing.
    '''
    global currentuser
    if os.getcwd() != ROOTPATH:
        loginflags[currentuser] = 0
        currentuser = "root"
        os.chdir('../')
    print("Logging out...")
    print("You are currently at ", os.getcwd())


def whoami():
    '''
    Displays the current user
    '''
    print(currentuser)
