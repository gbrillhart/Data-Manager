#!/usr/bin/env python3

#Class to standardize entries into master list

class LoginInfo:
    #initialization
    def __init__(self, name, username, password, email):
        self.username = username
        self.password = password
        self.name = name
        self.email= email

    #setters
    def set_username(self, username):
        self.username = username
    def set_password(self, password):
        self.password = password
    def set_Name(self, identifier):
        self.name = identifier
    def set_email(self, email):
        self.email = email   

    #tostring
    def __str__(self) -> str:
        return "Name: " + self.name + "\nUsername: " + self.username + "\nPassword: " + self.password + "\nEmail: " + self.email

    #check name for searching purposes
    def isMatch(self, __o: object) -> bool:
        if (self.name == __o.name):
            return True
        return False
    
    #define equals for an exact match
    def __eq__(self, __o: object) -> bool:
        if (self.name == __o.name and self.username == __o.username and 
            self.password == __o.password and self.email == __o.email):
            return True
        return False
    
    def strWrite(self) -> str:
        return self.name + "\n" + self.username + "\n" + self.password + "\n" + self.email+ "\n"