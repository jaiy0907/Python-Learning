ROOTPATH = '/Users/jaikishan.yadav/Documents/python-learning'
import os
import shutil

class User:
    def __init__(self, username, password, load=False):
        self._username = username
        self._password = password
        self._path = ROOTPATH + '/' + username
        self._files = []
        self._sshconfig = {}
        self.sshout = {"current": [], "background": []}
        self.sshin = []
        
        if load == False:
            self.create_user_directory()

        if load == True:
            self.load_files()
            self.load_sshconfig()

    def create_user_directory(self):
        os.mkdir(self._path)
        with open(self._path + '/filebase.txt', 'w+t') as f:
            pass
        with open(self._path + '/sshconfig.txt', 'w+t') as f:
            pass

    def delete_user_directory(self):
        shutil.rmtree(self._path)
        
    def load_files(self):
        with open(self._path + '/filebase.txt', 'rt') as f:
            self._files = f.readlines()
            for i, filename in enumerate(self._files):
                self._files[i] = filename.strip('\n')
    
    def load_sshconfig(self):
        with open(self._path + '/sshconfig.txt', 'r+t') as f:
            lines = []
            lines = f.readlines()
            for line in lines:
                line = line.strip('\n')
                sshuname, sshpassword = line.split(':')
                self._sshconfig[sshuname] = sshpassword
    
    def get_sshprocesses(self):
        return(self.sshout, self.sshin)
