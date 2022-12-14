#!/usr/bin/env python3

from fileinput import filename
import sys
from BitVector import *

AES_modulus = BitVector(bitstring='100011011')
subBytesTable = []      # for encryption
invSubBytesTable = []       # for decryption

#this function generates the substitution bytes tables necessary for AES
def gen_subbytes_table():
    subBytesTable = []
    c = BitVector(bitstring='01100011') #constant bitstring
    for i in range(0, 256):
        #find the multiplicative inverse and avoid error of 0 MI
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        #XOR shifted bits with each other and the constant
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable

#This generates the key schedule of 60 keywords necessary for 256-Bit AES.
#it uses the first four keywords and XORs the input. The 14 rounds then use 4 keywords
#each from the schedule
def gen_key_schedule_256(key_bv):
    #init sub byte table and vars
    byte_sub_table = gen_subbytes_table()
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    #first four keywords
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    #next 14 keywords, acting as sets of 4
    for i in range(8,60):
        #use 'g' function into an XOR
        if i%8 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-8] ^ kwd
        #simple XOR
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        #XOR and byteSubTable
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal = 
                                 byte_sub_table[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8] 
        #Circular XOR with first and last bit of the byte
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words

#this is the AES 'g' function that rotates keywords, substitutes with the byte substitution table, and
# XORs with the round constant. The round Constant is then modularly multiplied with the AES module.
def gee(keyword, round_constant, byte_sub_table):
    #rotate
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    #sub bytes
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    #XOR input and use modular multiplicaiton with 0x02 constant
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant

#AES encryption function takes in a path to unencrypted file, key, and file to write the encryption to
#pads the keys with '0'. Writes out in readable hex
def encrypt(funenc, key, fenc): #infile, key, outfile
    genTables()
    #get key and generate round keys
    key = key.strip()
    key = key.strip('\n')
    keysize = 256
    key += '0' * (keysize//8 - len(key)) if len(key) < keysize//8 else key[:keysize//8]  
    key_bv = BitVector( textstring = key )
    key_schedule = gen_key_schedule_256( key_bv )
    #generate mass bv
    bv = BitVector(filename = funenc)
    ftemp = open(fenc, 'w') #wipe old encryption file
    ftemp.close()
    while (bv.more_to_read):
        bitvec = bv.read_bits_from_file( 128 )
        #pad correctly and check for viable bv
        if bitvec.length() > 0:
            if(len(bitvec) < 128):
                bitvec.pad_from_right(128 - len(bitvec))
            #xoring input with first four keywords
            for key_inp in range(0,128,32):
                bitvec[key_inp:key_inp + 32] ^= key_schedule[int(key_inp / 32)]
            #print("After init RK: " + bitvec.get_hex_string_from_bitvector())
            #beginning rounds
            for round_key in range(4,60, 4):
            #for round_key in range(4,8,4):
                #byte subsititution
                for idx in range(0,128, 8): 
                    [row, col] = bitvec[idx:idx+8].divide_into_two()
                    bitvec[idx:idx+8] = BitVector(intVal = subBytesTable[row.int_val()*16 + col.int_val()], size = 8)
                #print("After Byte Sub: " + bitvec.get_hex_string_from_bitvector())
                #shift rows
                amt_shift = 0
                for row in range(0,32,8):
                    temp = (bitvec[row:row+8] + bitvec[row+32:row+32+8] + bitvec[row+64:row+64+8] + bitvec[row+96:row+96+8]) << amt_shift*8 #row
                    #put temp in corresponding byte positions
                    bitvec[row:row+8] = temp[0:8]
                    bitvec[row+32:row+32+8] = temp[8:16]
                    bitvec[row+64:row+64+8] = temp[16:24]
                    bitvec[row+96:row+96+8] = temp[24:32]
                    amt_shift += 1
                #print("After Row Shift: " + bitvec.get_hex_string_from_bitvector())
                #mix columns step
                if (round_key != 56):
                    temp = bitvec.deep_copy()
                    mult_table = BitVector(hexstring = "02030101010203010101020303010102") 
                    #utilizes matrix multiplication
                    for idx_mult in range(0,128, 32):
                        for idx_bv in range(0, 128, 32):
                            #temp_res = temp[idx_bv:idx_bv+8].deep_copy()
                            #print(str(idx_mult) + "x" +str(idx_bv))
                            temp_res = mult_table[idx_mult:idx_mult + 8].gf_multiply_modular(temp[idx_bv:idx_bv+8], AES_modulus,8)
                            #print(str(idx_mult+8) + "x" +str(idx_bv+8))
                            temp_res ^= mult_table[idx_mult+8:idx_mult + 16].gf_multiply_modular(temp[idx_bv+8:idx_bv+16], AES_modulus,8)
                            #print(str(idx_mult+16) + "x" +str(idx_bv+16))
                            temp_res ^= mult_table[idx_mult+16:idx_mult + 24].gf_multiply_modular(temp[idx_bv+16:idx_bv+24], AES_modulus,8)
                            #print(str(idx_mult+24) + "x" +str(idx_bv+24))
                            temp_res ^= mult_table[idx_mult+24:idx_mult + 32].gf_multiply_modular(temp[idx_bv+24:idx_bv+32], AES_modulus,8)
                            #print("Target: " + str(idx_bv + int(idx_mult/32 * 8)))
                            bitvec[idx_bv + int(idx_mult/32 * 8):idx_bv + int(idx_mult/32 * 8) + 8] = temp_res
                    #print("After column mixing: " + bitvec.get_hex_string_from_bitvector())
                #xor with round keys
                update_key = 0
                for key_inp in range(0,128,32):
                    bitvec[key_inp:key_inp + 32] ^= key_schedule[round_key + update_key]
                    update_key += 1
                #print("After round keys: " + bitvec.get_hex_string_from_bitvector())
            #write to file
            fout = open(fenc, 'a')
            hex_string = bitvec.get_hex_string_from_bitvector()
            fout.write(hex_string)
            fout.close()
    bv.close_file_object()
    
#AES decryption function takes in a path to encrypted file, key, and file to write the decryption to
#pads the keys with '0'. Assumes encryption is in readable hex
def decrypt(fenc, key, fdec):
    genTables()
    #get and create round keys
    key = key.strip()
    key = key.strip('\n')
    keysize = 256
    key += '0' * (keysize//8 - len(key)) if len(key) < keysize//8 else key[:keysize//8]  
    key_bv = BitVector( textstring = key )
    key_schedule = gen_key_schedule_256( key_bv )
    #read in hex input and create bv
    fencrypted = open(fenc,'r')
    hexstring_in = fencrypted.read()
    fencrypted.close()
    bv = BitVector(hexstring = hexstring_in)
    ftemp = open(fdec, 'w') #wipe old decryption file
    ftemp.close()
    #iterate over length of bitvector
    for idx in range(0,bv.length(),128):
        bitvec = bv[idx:idx+128]
        #pad if necessary (should not be)
        if bitvec.length() > 0:
            if(len(bitvec) < 128):
                bitvec.pad_from_right(128 - len(bitvec))
            #xoring input with last four keywords
            key_sel = 56
            for key_inp in range(0,128,32):
                bitvec[key_inp:key_inp + 32] ^= key_schedule[key_sel]
                key_sel += 1
            
            #print("After init RK: " + bitvec.get_hex_string_from_bitvector())
            #beginning rounds
            for round_key in range(56,0, -4):
                #inverse shift rows
                amt_shift = 0
                for row in range(0,32,8):
                    #shifting a row
                    temp = (bitvec[row:row+8] + bitvec[row+32:row+32+8] + bitvec[row+64:row+64+8] + bitvec[row+96:row+96+8]) >> amt_shift*8 
                    #delivering bytes into corresponding positions
                    bitvec[row:row+8] = temp[0:8]
                    bitvec[row+32:row+32+8] = temp[8:16]
                    bitvec[row+64:row+64+8] = temp[16:24]
                    bitvec[row+96:row+96+8] = temp[24:32]
                    amt_shift += 1
                #inverse substitute bytes
                for idx in range(0,128, 8): 
                    [row, col] = bitvec[idx:idx+8].divide_into_two()
                    bitvec[idx:idx+8] = BitVector(intVal = invSubBytesTable[row.int_val()*16 + col.int_val()], size = 8)
                #add round keys
                update_key = -4
                for key_inp in range(0,128,32):
                    bitvec[key_inp:key_inp + 32] ^= key_schedule[round_key + update_key]
                    update_key += 1
                #inverse mix columns
                if (round_key != 4):
                    temp = bitvec.deep_copy()
                    mult_table = BitVector(hexstring = "0e0b0d09090e0b0d0d090e0b0b0d090e") 
                    #utilizes matrix multiplication
                    for idx_mult in range(0,128, 32):
                        for idx_bv in range(0, 128, 32):
                            #temp_res = temp[idx_bv:idx_bv+8].deep_copy()
                            #print(str(idx_mult) + "x" +str(idx_bv))
                            temp_res = mult_table[idx_mult:idx_mult + 8].gf_multiply_modular(temp[idx_bv:idx_bv+8], AES_modulus,8)
                            #print(str(idx_mult+8) + "x" +str(idx_bv+8))
                            temp_res ^= mult_table[idx_mult+8:idx_mult + 16].gf_multiply_modular(temp[idx_bv+8:idx_bv+16], AES_modulus,8)
                            #print(str(idx_mult+16) + "x" +str(idx_bv+16))
                            temp_res ^= mult_table[idx_mult+16:idx_mult + 24].gf_multiply_modular(temp[idx_bv+16:idx_bv+24], AES_modulus,8)
                            #print(str(idx_mult+24) + "x" +str(idx_bv+24))
                            temp_res ^= mult_table[idx_mult+24:idx_mult + 32].gf_multiply_modular(temp[idx_bv+24:idx_bv+32], AES_modulus,8)
                            #print("Target: " + str(idx_bv + int(idx_mult/32 * 8)))
                            bitvec[idx_bv + int(idx_mult/32 * 8):idx_bv + int(idx_mult/32 * 8) + 8] = temp_res
                    #print("After column mixing: " + bitvec.get_hex_string_from_bitvector())
            #print ascii of decoded message
            fout = open(fdec, 'a')
            ascii_string = bitvec.get_bitvector_in_ascii() #flip again
            ascii_string = ascii_string.rstrip('\0')
            fout.write(ascii_string)
            fout.close()
    


#Generates the sub bytes table and inverse sub bytes table
def genTables():
    #table generation constants
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))
