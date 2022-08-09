#!/usr/bin/env python3

import AES
import LoginInfo

#verify the decryption by making sure first line of dataman matches
def verifyEnc(fdec) -> bool:
    decrypted = open(fdec, 'r')
    firstline = decrypted.readline()
    decrypted.close()
    if (firstline == "Welcome to Dataman\n"):
        return True
    return False

#return a dictionary of all logins on the dataman file
def getInfo(fdec) -> dict:
    logins = dict()
    try:
        if not verifyEnc(fdec):
            return None
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
            login = LoginInfo.LoginInfo(name, username, password, email)
            logins[login.name] = login
    except:
        return logins
    return logins
