#!/usr/bin/env python3
import os
import sys
from BitVector import *
import AES
import hashlib
from LoginInfo import *
from util import *


def main():
    userpass = ""
    try:
        passfile = open("dataman.enc", 'r')
        user_pass = input("Welcome to DataMan!\nPlease enter the unpacking password: ")
        passfile.close()
    except:
        print("Cannot locate/open dataman.enc, creating new file...")
        decfile = open("dataman.dec", 'w')
        decfile.write("Welcome to Dataman\n")
        decfile.close()
        passfile = open("dataman.enc", 'w')
        passfile.close()
        isCorrect = False
        while not isCorrect:
            confirm_pass1 = input("Please enter in your packing password: ")
            confirm_pass2 = input("Please confirm password: ")
            if not (confirm_pass1 == confirm_pass2):
                print("Sorry, those passwords do not match, please try again.")
            else:
                print("Password confirmed")
                isCorrect = True
                user_pass = confirm_pass1
        print("Encrypting base dataman.enc file with new password")
        print(len(user_pass))
        AES.encrypt("dataman.dec", user_pass, "dataman.enc")
    #decrypt dataman.enc here
    #create new file dataman.dec for PT of passwords
    os.system('cls||clear')
    print("Decrypting...")
    AES.decrypt("dataman.enc", user_pass, "dataman.dec")
    #get dictionary of Login
    logins = getInfo("dataman.dec")
    #Enter UI state
    #menu(passfile)
    passfile.close()

def menu(fdata):
    user_sel = -1
    while not(user_sel == 9):
        user_sel = input("------------------------\n" +
                "(0) Add a new login entry\n" + 
                "(1) Edit a previous login entry\n" + 
                "(2) View a login entry\n" +
                "(3) Delete a login entry\n"
                "(4) Encrypt a document\n" + 
                "(5) Decrypt a document\n" +
                "(6) Hash a document\n" + 
                "(7) Change packing password\n" + 
                "(8) Save Dataman changes\n" +
                "(9) Exit Dataman\n" + 
                "Please select an action: ")
        if(user_sel == '0'):
            add_new_login(fdata)
        else:
            os.system('cls||clear')
            print("Sorry, that action is invalid, please try again")

def add_new_login(fdata):
    #init flag and clear system
    isCorrect = False
    os.system('cls||clear')
    new_login = LoginInfo("","","","")
    while not isCorrect:
        name = input("Enter an identifying name to reference this login with: ")
        username = input("Enter an username for the login: ")
        password = input("Enter a password for the login: ")
        email = input("Enter an email for this login or leave blank: ")
        temp_login = LoginInfo(name=name, username=username, password=password, email=email)
        os.system('cls||clear')
        print("Is this entry correct?\n" + str(temp_login))
        response = input("y/n: ")
        if response == 'y' or response == "yes":
            new_login = temp_login
            isCorrect = True
            os.system('cls||clear')
        else:
            os.system('cls||clear')
            print("Sorry, let's try again")
    return new_login
def edit_login(fdata):
    return
def view_login(fdata):
    return
def delete_login(fdata):
    return
def enc_document(fdata):
    return
def dec_document(fdata):
    return
def hash_document(fdata):
    return
def change_packing_pass(fdata):
    return


if __name__ == "__main__":
    main()