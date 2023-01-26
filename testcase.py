import unittest
from unittest.mock import patch

class Tests(unittest.Testcase):
    def setUp(self):
        createuser("user1", "password")
        createuser()
        createuser()

    def ssh_fail_test(self):
        ssh(test = True, "test1@test2", "wrongsshpass")
        assertEqual(main.users[main.currentuser].sshin["current"][0], "test2")

        pass
    def ssh_success_test(self):
        pass
    def ssh_touch_test(self):
        pass
    def ssh_cat_test(self):
        pass
    def sshclose_test(self):

    def teardown(self):
        deleteuser()
        deleteuser()
        deleteuser()
