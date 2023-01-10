# username password implementation

def ssh(cli_input):
    import os
    username, servername = cli_input.split('@')
    attempts = 3
    userpswd = {"user1": "7834", "user2": "abcd", "user3": "u12312"}
    flag = 0
    if servername != "hostxyz":
        print("Server doesn't exist")
        return
    for users, password in userpswd.items():
        if (username == users):
            flag = 1
            while attempts:
                inp_passwords = input("Enter Password: ")
                if (inp_passwords == password):
                    flag = 2
                    os.chdir('./hostxyz')
                    print("Connection Established.")
                    print("You are currently at", os.getcwd())
                    break
                else: 
                    attempts -= 1
                print("Wrong Password attempts left:", attempts)
    if flag == 1:
        print("Unable to establish connection.")
    if flag == 0:
        print("User not found")

def logout():
    import os
    os.chdir('../')
    print("Logging out...")
    print("You are currently at ", os.getcwd())

