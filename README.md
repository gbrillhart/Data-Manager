# Dataman (Data-Manager) #

### Program Info: ###
Dataman is a lightweight AES and hashing platform to secure files and passwords written in pure Python 3. It utilizes an AES encryption program written by myself for a previous Computer Security class at Purdue and adapted for use in this program. It also utilizes the open source Bitvector 3.5 module, written by Purdue Professor Avi Kak which allows access and use of individual bits in pure Python. This program intent was to create a usable password and encryption program to facilitate my own learning and to present my own Python coding skills. It is secure for the average computer user, but not recommended against any serious and highly-skilled attackers.
- - - -
### Usage: ###
 To use the included example encryption file, simply use  `python3 dataman.py`or `python dataman.py` to run, and enter password `helloworld` to unpack.

 To create your own data and encrypted dataman file, first delete "dataman.enc". Then use `python3 dataman.py`or `python dataman.py` (This will wipe the previous data entered).
 
### Dependencies: ###
Bitvector 3.5 module API page can be found at https://pypi.org/project/BitVector/ and https://engineering.purdue.edu/kak/dist/BitVector-3.5.0.html and installed with `pip install BitVector` or by including the provided folder within the repo in local path. All other dependencies are native to Python 3.

### Packing and Unpacking: ###
Dataman holds an encrypted file of all login information created by the user. This file will be unpacked by the user at startup, asking for the unpacking password. Dataman never writes the packing password to a file for security, instead testing of whether or not decrypting the dataman.enc file provides actual data. If no dataman.enc file can be found, dataman will request a password and create a new one. Upon termination of the program, dataman automatically encrypts and writes the login information to the dataman.enc file and destroys the dataman.dec file. For security, this happens on forced termination, errors, and the correct exit command so that the decrypted file will not remain and the encryption will be written back. The only method around this would be a hard crash (loss of power, computer freeze, etc.) and regardless the attacker would still need to have already previously bypassed the unpacking password. A fix for this would be to encrypt and decrypt on the fly upon all data altering, but this would introduce a time wait upon almost all actions.
- - - -
### Menu: ###
The menu is the base state and user can select any of the actions from here. The options are:
    (0) Add a new login entry
    (1) Edit a previous login entry
    (2) View a login entry
    (3) Delete a login entry
    (4) Encrypt a document
    (5) Decrypt a document
    (6) Hash a document
    (7) Change packing password 
    (8) Print all logins
    (9) Save and Exit Dataman

**(0) Add a new login entry:**
This action allows the user to enter in a name, username, password, and email address for a login. The user can then confirm and overwrite a previous entry if they so choose.

**(1) Edit a previous login entry**
This action  allows a user to search for a login by name, and then edit any of the peices of data in that specific login.

**(2) View a login entry**
This action allows a user to search for a login by name and display all the information attached to it.

**(3) Delete a login entry**
This action allows a user to delete any login entries by searching up the name.

**(4) Encrypt a document**
This action allows a user to provide a identifying name, path to the document to encrypt, a key for the encryption and a path to the new encrypted document. The program then does AES encryption on the document using the provided key and creates the new encrypted document.

**(5) Decrypt a document**
This action allows a user to provide a identifying name, path to the document to decrypt, a key for the decryption and a path to the new decrypted document. The program then does AES decryption on the document using the provided key and creates the new decrypted document.

**(6) Hash a document**
This action uses hashlib to quickly do a SHA512 hash on a user provided document path and then creates a new hashed document, with the pass also provided by the user.

**(7) Change the packing password**
This action calls for the user to provide the old packing password, and then gets a new password from the user which it will then use to pack/encrypt from then on.

**(8) Print all logins**
This action prints all logins that dataman has stored. Generally not recommended to output every login into terminal, but up to user discretion.

**(9) Save and Exit Dataman**
Graceful exit from the program, but Ctrl-C works just fine as it saves and encrypts regardless.
- - - -
### Files: ###

**dataman.py**
This is the main executing file that controls the flow of the program. Contains all menu controls and user I/O.

**AES.py**
Encryption and decryption AES program. The two main encrypt and decrypt functions take in the file to read path, encryption key, and file to write path. This could have been easily done with a python library such as PyCrypto (which would be faster), but I wanted to use my own program.

**LoginInfo.py**
Contains the LoginInfo class to neatly package data and have a few helpful functions

**util.py**
Contains a few helpful functions to make code more ubiquitous and standalone.

### Other files: ###

**dataman.enc**- encrypted data of trivial logins. Packed with "helloworld" if the user would like to test.

**dataman.dec**- decrypted data of trivial logins. Is wiped upon exit, but can be viewed in plaintext while program is running as it is sort of a temporary holder.

**unecrypted.txt**- plaintext file for encrypting and hashing purposes

**encrypted.txt**- encrypted version of unencrypted.txt with key "helloworld".

**hashedsha512.txt**- sha512 hash of unencrypted.txt

**Bitvector 3.5 Folder**- Open source Bitvector module designed to use bitstrings in pure python. Written by Purdue Professor Avi Kak.
- - - -
Thanks for reading!

**Creator -**
    Garrett Brillhart: creator of code, email garrett.brillhart@gmail.com for questions
    
**Additional Credits -**
    Avi Kak: creator of Bitvector 3.5 module, additional support functions on AES.py
