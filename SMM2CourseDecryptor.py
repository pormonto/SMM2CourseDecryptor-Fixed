#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SMM2CourseDecryptor
# A Script For The Decryption And Encryption Of Super Mario Maker 2 Binary Course Data Files (*.bcd) and Super Mario Maker 2 Binary Course Thumbnail Files (*.btl).
# Version 0.2
# Created By MarioPossamato With Help From Kinnay (https://github.com/Kinnay/)

# This File Is Part Of SMM2CourseDecryptor.

#==== Module and library imports ====#
import sys             # Built-in module
import os              # Built-in module
import io              # Built-in module
import struct          # Built-in module
import binascii        # Built-in module
import zlib            # Built-in module
from Crypto.Hash import CMAC
from Crypto.Cipher import AES
from Crypto import Random
from SMM2 import encryption

def main():
    if len(sys.argv) == 3:
        f = open(sys.argv[1], "rb")
        f.seek(0, 2)

        #==== Thumbnail Data ====#
        if f.tell() == 0x1C000: #==== Encrypted Thumbnail Data ====#
            print("Decrypting Thumbnail Data...")
            data = open(sys.argv[1], "rb").read()
            thumb = encryption.Thumbnail(data)
            thumb.decrypt() #==== Decrypt The Thumbnail Data ====#
            open(os.path.splitext(sys.argv[2])[0]+".jpg", "wb").write(thumb.data)

        elif os.path.splitext(sys.argv[1])[1] in (".jpg", ".jpeg"): #==== Decrypted Thumbnail Data ====#
            print("Encrypting Thumbnail Data...")
            data = open(sys.argv[1], "rb").read()
            if(f.tell()<=0x1BFD0):
                pass
            else:
                print("Error: Thumbnail is too large!")
                return
            thumb = encryption.Thumbnail(data+b'\0'*(0x1BFD0 - len(data)))
            thumb.encrypt() #==== Encrypt The Thumbnail Data ====#
            open(sys.argv[2], "wb").write(thumb.data)

        #==== Course Data ====#
        elif f.tell() == 0x5C000: #==== Encrypted Course Data ====#
            print("Decrypting Course Data...")
            data = open(sys.argv[1], "rb").read()
            course = encryption.Course(data)
            course.decrypt() #==== Decrypt The Course Data ====#
            open(sys.argv[2], "wb").write(course.data)

        elif f.tell() == 0x5BFC0: #==== Decrypted Course Data ====#
            print("Encrypting Course Data...")
            data = open(sys.argv[1], "rb").read()
            course = encryption.Course(data)
            course.encrypt() #==== Encrypt The Course Data ====#
            open(sys.argv[2], "wb").write(course.data)

        #==== Unsupported File ====#
        else:
            print("Error: Unsupported file!")
            return

    elif len(sys.argv) == 2:
        f = open(sys.argv[1], "rb")
        f.seek(0, 2)

        #==== Thumbnail Data ====#
        if f.tell() == 0x1C000: #==== Encrypted Thumbnail Data ====#
            print("Decrypting Thumbnail Data...")
            data = open(sys.argv[1], "rb").read()
            thumb = encryption.Thumbnail(data)
            thumb.decrypt() #==== Decrypt The Thumbnail Data ====#
            open(os.path.splitext(sys.argv[1])[0]+".jpg", "wb").write(thumb.data)

        elif os.path.splitext(sys.argv[1])[1] in (".jpg", ".jpeg"): #==== Decrypted Thumbnail Data ====#
            print("Encrypting Thumbnail Data...")
            data = open(sys.argv[1], "rb").read()
            if(f.tell()<=0x1BFD0):
                pass
            else:
                print("Error: Thumbnail is too large!")
                return
            thumb = encryption.Thumbnail(data+b'\0'*(0x1BFD0 - len(data)))
            thumb.encrypt() #==== Encrypt The Thumbnail Data ====#
            open(os.path.splitext(sys.argv[1])[0]+".btl", "wb").write(thumb.data)

        #==== Course Data ====#
        elif f.tell() == 0x5C000: #==== Encrypted Course Data ====#
            print("Decrypting Course Data...")
            data = open(sys.argv[1], "rb").read()
            course = encryption.Course(data)
            course.decrypt() #==== Decrypt The Course Data ====#
            open(sys.argv[1], "wb").write(course.data)

        elif f.tell() == 0x5BFC0: #==== Decrypted Course Data ====#
            print("Encrypting Course Data...")
            data = open(sys.argv[1], "rb").read()
            course = encryption.Course(data)
            course.encrypt() #==== Encrypt The Course Data ====#
            open(sys.argv[1], "wb").write(course.data)

        #==== Unsupported File ====#
        else:
            print("Error: Unsupported file!")
            return
    else:
        print("Usage: %s <input> [output]" % sys.argv[0])
        return
    print("Done!")

if __name__ == "__main__":
    main()
