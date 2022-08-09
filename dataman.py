#!/usr/bin/env python3
import os
import sys
from BitVector import *
import AES
import hashlib
from LoginInfo import *
from util import *


def main():

    def menu(logins,user_pass):
        user_sel = -1
        while not(user_sel == 9):
            os.system('cls||clear')
            user_sel = input(
                    "(0) Add a new login entry\n" + 
                    "(1) Edit a previous login entry\n" + 
                    "(2) View a login entry\n" +
                    "(3) Delete a login entry\n"
                    "(4) Encrypt a document\n" + 
                    "(5) Decrypt a document\n" +
                    "(6) Hash a document\n" + 
                    "(7) Change packing password\n" + 
                    "(8) Print all logins\n" +
                    "(9) Save and Exit Dataman\n" + 
                    "Please select an action: ")
            if(user_sel == '0'):
                add_new_login(logins)
            elif(user_sel == '1'):
                edit_login(logins)
            elif(user_sel == '2'):
                view_login(logins)
            elif(user_sel == '3'):
                delete_login(logins)
            elif(user_sel == '4'):
                enc_document(logins)
            elif(user_sel == '5'):
                dec_document(logins)
            elif(user_sel== '6'):
                hash_document()
            elif(user_sel== '7'):
                change_packing_pass(user_pass)
            elif(user_sel== '8'):
                print_all_logins(logins)
            elif(user_sel == '9'):
                return
            else:
                os.system('cls||clear')
                print("Sorry, that action is invalid, please try again")

    def add_new_login(logins):
        os.system('cls||clear')
        while True:
            name = input("Enter an identifying name to reference this login with: ")
            username = input("Enter an username for the login: ")
            password = input("Enter a password for the login: ")
            email = input("Enter an email for this login or leave blank: ")
            temp_login = LoginInfo.LoginInfo(name, username, password, email)
            os.system('cls||clear')
            print("Is this entry correct?\n" + str(temp_login))
            response = input("y/n: ")
            if response == 'y' or response == "yes":
                if (temp_login.name not in logins):
                    os.system('cls||clear')
                    logins[temp_login.name] = temp_login
                    print("Login Added!")
                    return
                else:
                    os.system('cls||clear')
                    print("Sorry, there is already an entry with the " + temp_login.name + " name. Overwrite?")
                    response = input("y/n: ")
                    if response == 'y' or response == "yes":
                        os.system('cls||clear')
                        logins[temp_login.name] = temp_login
                        print("Login Added!")
                        return
                    else:
                        os.system('cls||clear')
                        print("Sorry, let's try again")   
            else:
                os.system('cls||clear')
                print("Sorry, let's try again")
    def edit_login(logins):
        os.system('cls||clear')
        while True:
            name = input("Enter the name of the login you would like to edit or type \'Exit\' to return: ")
            if(name == 'Exit'):
                return
            elif name in logins:
                while True:
                    print(logins[name])
                    user_sel = input("(0) Edit Name: \n" + 
                        "(1) Edit Username: \n" + 
                        "(2) Edit Password: \n" +
                        "(3) Edit Email: \n"+
                        "(4) Done editing: ")
                    if user_sel == '0':
                        login = logins.pop(name)
                        new_name = input("Enter the new name of the login: ")
                        login.name = new_name
                        name = new_name
                        logins[new_name] = login
                        print("Name has been changed")
                        os.system('cls||clear')
                    elif user_sel == '1':
                        new_user = input("Enter the new username of the login: ")
                        logins[name].username = new_user
                        print("Username has been changed")
                        os.system('cls||clear')
                    elif user_sel == '2':
                        new_pass = input("Enter the new password of the login: ")
                        logins[name].password = new_pass
                        print("Password has been changed")
                        os.system('cls||clear')
                    elif user_sel == '3':
                        new_email = input("Enter the new email of the login: ")
                        logins[name].email = new_email
                        print("Email has been changed")
                        os.system('cls||clear')
                    elif user_sel == '4':
                        os.system('cls||clear')
                        return
                    else:
                        os.system('cls||clear')
                        print("Invalid selection, please try again")
            else:
                os.system('cls||clear')
                print("That login does not exist, please check spelling")

    def view_login(logins):
        os.system('cls||clear')
        while True:
            name = input("Enter the name of the login you would like to view or type \'Exit\' to return: ")
            if(name == 'Exit'):
                return
            elif name in logins:
                print(logins[name])
            else:
                os.system('cls||clear')
                print("Sorry, that login does not exist. Please check spelling.")
    def delete_login(logins):
        os.system('cls||clear')
        while True:
            name = input("Enter the name of the login you would like to delete or type \'Exit\' to return: ")
            if(name == 'Exit'):
                return
            elif name in logins:
                confirmation = input(str(logins[name]) + "\nDelete this login(y/n)? ")
                if (confirmation == 'y' or confirmation == 'yes'):
                    logins.pop(name)
                    os.system('cls||clear')
                    print("Login was deleted")
                else:
                    os.system('cls||clear')
                    print("Login was not deleted")
            else:
                os.system('cls||clear')
                print("Sorry, that login does not exist. Please check spelling.")
    def enc_document(logins):
        os.system('cls||clear')
        while True:
            name = input("Enter in a name for the document (Type \'Exit\' to return): ")
            if(name == 'Exit'):
                return
            username = input("Enter in the path to the document: ")
            password = input("Enter a password for the encryption: ")
            encrypt_path = input("Enter in the path for the encrypted document: ")
            temp_login = LoginInfo.LoginInfo(name, username, password, encrypt_path)
            os.system('cls||clear')
            print("Is this entry correct?\nDocument Name: " + name + "\nDocument Path: " + username + "\nKey: " + password + "\nNew Document: " + encrypt_path)
            response = input("y/n: ")
            if response == 'y' or response == "yes":
                if (temp_login.name not in logins):
                    os.system('cls||clear')
                    logins[temp_login.name] = temp_login
                    print("Encrypting...")
                    AES.encrypt(username, password, encrypt_path)
                    print("The document was encrypted and a login stored in dataman")
                    return
                else:
                    print("Sorry, there is already an entry with the " + temp_login.name + " name. Overwrite?")
                    response = input("y/n: ")
                    if response == 'y' or response == "yes":
                        os.system('cls||clear')
                        logins[temp_login.name] = temp_login
                        print("Encrypting...")
                        AES.encrypt(username, password, encrypt_path)
                        print("The document was encrypted and a login stored in dataman")
                    else:
                        os.system('cls||clear')
                        print("Sorry, let's try again")
            else:
                os.system('cls||clear')
                print("Sorry, let's try again")
    def dec_document(logins):
        os.system('cls||clear')
        while True:
            name = input("Enter in a name for the document (Type \'Exit\' to return): ")
            if(name == 'Exit'):
                return
            username = input("Enter in the path to the document: ")
            password = input("Enter a password for the decryption: ")
            decrypt_path = input("Enter in the path for the decrypted document: ")
            temp_login = LoginInfo.LoginInfo(name, username, password, decrypt_path)
            os.system('cls||clear')
            print("Is this entry correct?\nDocument Name: " + name + "\nDocument Path: " + username + "\nKey: " + password + "\nNew Document: " + decrypt_path)
            response = input("y/n: ")
            if response == 'y' or response == "yes":
                if (temp_login.name not in logins):
                    os.system('cls||clear')
                    logins[temp_login.name] = temp_login
                    print("Decrypting...")
                    AES.decrypt(username, password, decrypt_path)
                    print("The document was decrypted and a login stored in dataman")
                    return
                else:
                    print("Sorry, there is already an entry with the " + temp_login.name + " name. Overwrite?")
                    response = input("y/n: ")
                    if response == 'y' or response == "yes":
                        os.system('cls||clear')
                        logins[temp_login.name] = temp_login
                        print("Decrypting...")
                        AES.decrypt(username, password, decrypt_path)
                        print("The document was decrypted and a login stored in dataman")
                    else:
                        os.system('cls||clear')
                        print("Sorry, let's try again")
            else:
                os.system('cls||clear')
                print("Sorry, let's try again")
    def hash_document():
        os.system('cls||clear')
        while True:
            path_to_doc = input("Enter in a path for the document (Type \'Exit\' to return): ")
            if(path_to_doc == 'Exit'):
                return
            hashed_doc = input("Enter in a path for the SHA512 Hash: ")
            os.system('cls||clear')
            print("Is this entry correct?\nDocument Path: " + path_to_doc +"\nNew Document: " + hashed_doc)
            response = input("y/n: ")
            if response == 'y' or response == "yes":
                finput = open(path_to_doc,'r')
                input_doc = finput.read()
                finput.close()
                hash = hashlib.sha512(str(input_doc).encode("utf-8")).hexdigest()
                fout = open(hashed_doc,'w')
                fout.write(hash)
                fout.close
                print("The document was hashed.")
            else:
                os.system('cls||clear')
                print("Sorry, let's try again")
    def change_packing_pass(user_pass):
        while True:
            old_pass = input("Enter in previous password: ")
            if old_pass == user_pass:
                break
            else:
                print("Sorry, that's not correct")
        while True:
            new_pass = input("Enter in new password: ")
            confirm_pass = input("Confirm new password: ")
            if(new_pass == confirm_pass):
                user_pass = new_pass
                input("Packing Password has been changed! Hit enter to continue")
                return
            else:
                print("Passwords do not match, please try again.")
        return

    def print_all_logins(logins):
        print("Logins:")
        for login in logins:
            print("\n" + str(logins[login]))
        input("Press enter to continue...")
        return


    logins = dict()
    user_pass = ""
    try:
        if (os.path.exists("dataman.enc")):
            user_pass = input("Welcome to DataMan!\nPlease enter the unpacking password: ")
        else:
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
                    os.system('cls||clear')
                    print("Sorry, those passwords do not match, please try again.")
                else:
                    print("Password confirmed")
                    isCorrect = True
                    user_pass = confirm_pass1
            print("Encrypting base dataman.enc file with new password")
            AES.encrypt("dataman.dec", user_pass, "dataman.enc")
        #decrypt dataman.enc here
        #create new file dataman.dec for PT of passwords
        os.system('cls||clear')
        print("Decrypting...")
        AES.decrypt("dataman.enc", user_pass, "dataman.dec")
        #get dictionary of Login
        logins = getInfo("dataman.dec")
        #Enter UI state
        menu(logins, user_pass)
    #ensure the decrypted file is always wiped in termination of program, even on errors
    #additionally encrypt and write the current login info the dataman.enc
    finally:
        os.system('cls||clear')
        print("Saving Data...")
        decfile = open("dataman.dec", 'w')
        decfile.write("Welcome to Dataman\n")
        for login in logins:
            decfile.write(logins[login].strWrite())
        decfile.close()
        AES.encrypt("dataman.dec", user_pass, "dataman.enc")
if __name__ == "__main__":
    main()