#!/usr/bin/env python3

import AES
import LoginInfo

def verifyEnc(fdec) -> bool:
    decrypted = open(fdec, 'r')
    firstline = decrypted.readline()
    decrypted.close()
    if (firstline == "Welcome to Dataman\n"):
        return True
    return False

def getInfo(fdec) -> dict:
    logins = dict()
    try:
        decrypted = open(fdec, 'r')
        decrypted.seek(0,0)
        decrypted.readline()
        while True:
            name = decrypted.readline().strip()
            if (name == ''):
                break
            username = decrypted.readline().strip()
            password = decrypted.readline().strip()
            email = decrypted.readline().strip()
            login = LoginInfo(name, username, password, email)
            logins[login.name] = login
    except:
        return logins
    return logins

def printLogins(logins):
    print("Login Info")
    for login in logins:
        print(login)
