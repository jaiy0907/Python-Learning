
'''
Commands to interact with the terminal
'''
import main
import system
import os
import sys



def ssh(test=False, cli_input=None, password=None):
    '''
    SSH into a host. Username Password implementation of SSH.

    Args:
        cli_input: a string in the form of [username@hostname]
    '''
   
    if main.currentuser == "root":
        print("Login into an user to run this command.")
        return 

    if len(main.users[main.currentuser].sshout["current"]) != 0:
        print("Command inaccessible.")
        return 

    if test == False:
        cli_input = input()

    client, server = cli_input.split('@')
    if server not in main.users:
        print("Server doesn't exist")
        return 

    if client not in main.users[server]._sshconfig:
        print("User doesn't exist in the server")
        return


    if server in main.users[main.currentuser].sshout["background"] and (client in main.users[server].sshin):
        print("Connection already running. Bringing it to foreground")
        main.users[main.currentuser].sshout["current"].append(server)
        main.users[main.currentuser].sshout["background"].remove(server)
        sys.ps1 =  cli_input + ">>> "
        return 


    if test=False:
        password = input("Enter Password: ")
    tries = main.PASSWORD_ATTEMPTS
    while tries:
        if password == main.users[server]._sshconfig[client]:
            break
        tries -= 1
        if test=False
        inp_password = input("Wrong password. Enter password(attempts left= {}): ".format(tries))

    if tries == 0:
        print("Unable to establish connection. Wrong credentials.")
        return 

    print("Connecting....")
    main.users[main.currentuser].sshout["current"].append(server)
    main.users[server].sshin.append(client)
    sys.ps1 = cli_input + ">>> "
    print("Connection Established.")
    
    
def sshclose():
    '''
    Closes the current SSH connection
    '''
    if len(main.users[main.currentuser].sshout["current"]) == 0:
        print("No SSH connection running.")
        return 0
    
    main.users[main.users[main.currentuser].sshout["current"][0]].sshin.remove(main.currentuser)
    main.users[main.currentuser].sshout["current"].clear()
    
    sys.ps1 = main.currentuser + ">>> "
    print("Connection closed.")



def sshbackground():
    '''
    Moves the current ssh connection to the background
    '''
    if len(main.users[main.currentuser].sshout["current"]) == 0:
        print("No SSH connection running.")

    main.users[main.currentuser].sshout["background"].append(main.users[main.currentuser].sshout["current"][0])
    main.users[main.currentuser].sshout["current"].clear()
    sys.ps1 = main.currentuser + ">>> "
    print("Process now running in background.")
    
    
def sshprocesses():
    '''
    Prints the all the ssh processes of the current user
    '''
    if main.currentuser == "root":
        print("Login into an user to use this command.")
        return 

    if len(main.users[main.currentuser].sshout["current"]) != 0:
        print("Command inaccessible.")
        return

    process = main.users[main.currentuser].get_sshprocesses()
    print("Outgoing SSH connections:")
    print(process[0])
    print("Incoming SSH connections:")
    print(process[1])


        

def createuser(test=False, username=None, password=None):
    '''
    Creates a new user. Can only be executed when in root.

    Args:
        Username: Set the new username
        Password: Set the password
    '''
    if main.currentuser != "root":
        print("Command can only be executed while in root")
        return

    username = input("Enter new user name: ")
    if username in main.users:
        print("User already exists")
        return
    password = input("Set Password: ")
    print("Creating user....")
    u = system.User(username, password)             #Creates the User object 
    with open(main.DATABASEPATH, 'at') as f:        #Saves the username and password in database.txt
        usr_pwd = username + ':' + password + '\n'
        f.write(usr_pwd)
    main.users[username] = u                        #Pushes the User object into main.users dictionary
    main.usersloginflags[username] = False            #Sets the loginflag of the newly created user to 0
    print(main.users)
    print("Done.")


def deleteuser(test=False, username=None, password=None):
    '''
    Deletes an already existing user. Can only be executed when in root.

    Args:
        Username: username for the user to be deleted
        Password: the password for the user being deleted
    '''
    if main.currentuser != "root":
        print("Command can only be executed while in root")
        return
    username = input("Enter username for the user to be deleted: ")
    if username not in main.users:
        print(username, main.users)
        print("User doesnt exist")
        return
    tries = main.PASSWORD_ATTEMPTS
    while (tries):
        inp_password = input("Enter password(required for deleting): ")
        if inp_password == main.users[username]._password:
            print("Deleting user....")
            usr_pswd = username + ":" + inp_password + '\n'
            main.users[username].delete_user_directory()    #Deletes the User's files and directory
            main.users.pop(username)                        #Pops the User object from main.users dictionary
            main.usersloginflags.pop(username)              #Pops the User object out of main.usersloginflags
            lines = []
            with open(main.DATABASEPATH, "rt") as f:        #Deletes the username and password from database.txt
                lines = f.readlines()
            lines.remove(usr_pswd)
            with open(main.DATABASEPATH, "wt") as f:
                f.writelines(lines)
            print("Done.")
            return
        tries -= 1
        print("Wrong passwords. Enter password(attempts left= {}): ".format(tries))

    if tries == 0:
        print("Unable to delete user. Wrong credentials")

    

    

def login(test=False, username=None, password=None):
    '''
    Logs into an user.
    
    Args:
        Login Credentials: Username and Password

    '''
    username = input("Enter username: ")
    if username not in main.users:                              #Checks whether user trying to login exists or not
        print("User doesn't exist")
        return
    if main.usersloginflags[username] == 1:                     #If already logged in switches to the desired user
        print("Already logged in. Switching user...")
        main.currentuser = username
        sys.ps1 = main.currentuser + ">>> "
        print("Done.")
        return 
    
    tries = main.PASSWORD_ATTEMPTS                              #Authenticating the users login credentials
    while (tries):
        inp_password = input("Enter password: ")            
        if inp_password == main.users[username]._password:
            print("Logging in....")
            main.currentuser = username                         #Setting main.currentuser to the desired user
            main.usersloginflags[main.currentuser] = True       #Setting the user's login flag to 1
            sys.ps1 = main.currentuser + ">>> "
            print("Done.")
            return
        tries -= 1
        print("Wrong passwords. Enter password(attempts left= {}): ".format(tries))

    if tries == 0:
        print("Unable to login. Wrong credentials")
        
    


def logout():
    '''
    Logs a user out of the system. If not logged into a user, does nothing.

    '''
    
    if main.currentuser != "root":
        if len(main.users[main.currentuser].sshout["current"]) != 0 or len(main.users[main.currentuser].sshout["background"])!= 0:
            print("SSH session running. Please close them to logout")
            return
        print("Logging out...")
        main.currentuser = "root"
        main.usersloginflags[main.currentuser] = False
        sys.ps1 = ">>> "
        print("Done.")
    else:
        print("At root.")



def checkuser():
    if len(main.users[main.currentuser].sshout["current"]) != 0:
        return  main.users[main.users[main.currentuser].sshout["current"][0]]
    return main.users[main.currentuser]


def touch(filename, content=None):
    '''
    Creates a file and writes into it if needed.

    Args:
        filename: The name of the that needs to be created 
                  (possible file extensions: .txt, .py, .c)

    '''
    if main.currentuser == "root":
        print("Login into an user to use this command.")
        return
    tempuser = checkuser()
    if filename in tempuser._files:
        print("File already exists.")
        if content != None:
            ch = input("Overwrite[O]/Append[A]/[N]: ")
            if ch == 'O':
                with open(tempuser._path + '/' + filename, 'wt') as f:
                    f.write(content)
            if ch == 'A':
                with open(tempuser._path + '/' + filename, 'at') as f:
                    f.write(content)
            return
    
    with open(tempuser._path + '/' + main.FILEBASENAME, 'at') as f:
        f.write(filename + '\n')
    tempuser.load_files()
    with open(tempuser._path + '/' + filename, 'w+t') as f:
        pass
    if content != None:
        with open(tempuser._path + '/' + filename, 'wt') as f:
            f.write(content)


def ls():
    '''
    Prints the name of all the files in the user directory
    '''
    if (main.currentuser == "root"):
        print("Login into an user to use this command.")
        return
    tempuser = checkuser()
    print(tempuser._files)



def cat(filename):
    '''
    Prints the contents of a file 

    Args:
        filename: the name of the file whose content has to be printed
    '''
    if main.currentuser == "root":
        print("Login into an user to use this command")
        return
    tempuser = checkuser()
    if filename not in tempuser._files:
        print("The file doesn't exist.")
        return
    output = []
    with open(tempuser._path + '/' + filename, 'rt') as f:
        output = f.readlines()
    for line in output:
        line = line.strip('\n')
        print(line)

def rm(filename):
    '''
    Deletes a file.

    Args:
        filename: the name of the file to be deleted.
    '''
    if main.currentuser == "root":
        print("Login into an user to use this command")
        return
    tempuser = checkuser()
    if filename not in tempuser._files:
        print("File does not exist")
        return
    os.remove(tempuser._path + '/' + filename)
    tempuser._files.remove(filename)
    


def whoami():
    '''
    Displays the current user
    '''
    print(main.currentuser)
