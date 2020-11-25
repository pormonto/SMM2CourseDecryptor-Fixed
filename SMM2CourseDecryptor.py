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
from nintendo.sead import random
from nintendo.enl import crypto
from PIL import Image

#==== Key Tables ====#
CourseKeyTable = [ #==== Table For Decrypting Course data ====#
	0x7AB1C9D2, 0xCA750936, 0x3003E59C, 0xF261014B,
	0x2E25160A, 0xED614811, 0xF1AC6240, 0xD59272CD,
	0xF38549BF, 0x6CF5B327, 0xDA4DB82A, 0x820C435A,
	0xC95609BA, 0x19BE08B0, 0x738E2B81, 0xED3C349A,
	0x45275D1,  0xE0A73635, 0x1DEBF4DA, 0x9924B0DE,
	0x6A1FC367, 0x71970467, 0xFC55ABEB, 0x368D7489,
	0xCC97D1D,  0x17CC441E, 0x3528D152, 0xD0129B53,
	0xE12A69E9, 0x13D1BDB7, 0x32EAA9ED, 0x42F41D1B,
	0xAEA5F51F, 0x42C5D23C, 0x7CC742ED, 0x723BA5F9,
	0xDE5B99E3, 0x2C0055A4, 0xC38807B4, 0x4C099B61,
	0xC4E4568E, 0x8C29C901, 0xE13B34AC, 0xE7C3F212,
	0xB67EF941, 0x8038965,  0x8AFD1E6A, 0x8E5341A3,
	0xA4C61107, 0xFBAF1418, 0x9B05EF64, 0x3C91734E,
	0x82EC6646, 0xFB19F33E, 0x3BDE6FE2, 0x17A84CCA,
	0xCCDF0CE9, 0x50E4135C, 0xFF2658B2, 0x3780F156,
	0x7D8F5D68, 0x517CBED1, 0x1FCDDF0D, 0x77A58C94
]

ReplayKeyTable = [ #==== Table For Decrypting Replay Data ====#
	0xFAE9A964, 0xD15BE83B, 0xA8935637, 0x6BFB6458,
	0xF431F0BD, 0x9A1726E1, 0xCA4D4B97, 0x4679263D,
	0x38A3639,  0x1756A282, 0xB38EA547, 0x3A1E61CD,
	0x594C78AC, 0x8A2BA1D6, 0xA83A362C, 0x5B5A20B7,
	0xE6677DE5, 0xD4E7289,  0xEEB36782, 0x64980EEC,
	0xEB5CBCDC, 0xD39B30E4, 0x6C61F7DC, 0x6D1839C7,
	0xE1FC8B5A, 0x1EAE0662, 0x9F5996F7, 0xF1E5724D,
	0xAD7CD854, 0x840CF0F,  0x7E9E433D, 0xE76FEFD0,
	0xF0CBE6D2, 0x314D14F0, 0x36C48B1B, 0xB1E6897E,
	0x19A7D19C, 0x8439386C, 0xE8F98D89, 0xCC2D805D,
	0xA331DCE6, 0x1795B737, 0xEA452CB8, 0x523A22DB,
	0xF2C7F032, 0x36BBDB41, 0xFBA7AB6F, 0x9F22F129,
	0x50B3DE30, 0x15C034BF, 0x2140EB8E, 0x3972860,
	0xA930B6D4, 0x3E36B38C, 0xD631BA09, 0xEA56903E,
	0xC7784D40, 0xEF2BB717, 0xD43FA779, 0x88FA47DE,
	0x571FCE26, 0x87BA1473, 0xC7448847, 0x15184657
]

LaterKeyTable = [ #==== Table For Decrypting later.dat ====#
	0x1CBC16C1, 0xF468AFCF, 0x6F56A9CD, 0xFF234473, 
	0x79D75E19, 0xCE13762E, 0xA7C3B9EC, 0x2DBD57D2, 
	0x52B04A8B, 0x91BA89AB, 0x2AA963A, 0x372F4D1C, 
	0xB0DFE6F,  0x10791D7B, 0x48E6ADB2, 0x446B8979, 
	0xF6C22D64, 0xA1A850C9, 0x1E0873A7, 0xDF669A3A,
	0xF2444EE4, 0x26B7F6FF, 0x23085C49, 0x724379C3, 
	0xB869BE34, 0x235E09DB, 0xAA73EE66, 0x2CC099EE, 
	0x5119DD31, 0x2CD16119, 0x3601C35D, 0x48A9B1F9, 
	0xFA096C03, 0xD0F8B7F1, 0x8B3DFFEB, 0xBF91B778, 
	0x6B6F8E77, 0x51F6D398, 0x2D3FD2EA, 0x553D9AF7,
	0xC716204,  0x3B2FFD8E, 0x7B185872, 0xBDDA19A5, 
	0xC9CED66B, 0xA935CEB5, 0xCA3EBC89, 0xC0EE4C4D, 
	0xFFDDA782, 0xCC0C1069, 0x91F3FAC0, 0x5FAFBDF4, 
	0xA42FBF7D, 0xAA88D236, 0xE7606B88, 0x71D7FF31, 
	0x1022D446, 0xDA78A3DF, 0x596E8949, 0xA1FC82EB,
	0x665D7428, 0x5E9161D3, 0x1C1BDCC7, 0xEEE25BD0
]

SaveKeyTable = [ #==== Table For Decrypting save.dat ====#
	0x5C736064, 0x3F9178C3, 0x9D11DBD3, 0xD8B11DE9, 
	0xBCAFD10B, 0x85E013EB, 0xAB4CB7A5, 0x12DF234A, 
	0x69BD8F28, 0x9718796A, 0x467E510E, 0xC9002264, 
	0xF5EF9EF5, 0xFE19683B, 0x9E739A59, 0x8330F69F, 
	0x158E467C, 0xDCC25B0B, 0xCC96E901, 0x5AFF8BE1,
	0xBB08745E, 0xF9C232E5, 0xDB7E0641, 0x9B5E1AD7, 
	0x25B8D979, 0xE35251D3, 0x9C1E9ADB, 0x256902E2, 
	0xCA67B195, 0x16CDB407, 0xFD95C734, 0xD019C133, 
	0x5F39E755, 0x118168FC, 0xAA796804, 0xC9AC1148, 
	0x2EC0C6B4, 0xDE6E18F6, 0x5F7FAA46, 0x9FAE6A3,
	0x6BF9D926, 0xD41D2628, 0xC91BD99B, 0xB4F43F73, 
	0x37B8C265, 0xA8AD2CDB, 0xF2F7A186, 0x4842B092, 
	0xC6C69499, 0x5171F6D5, 0xB21A4FA7, 0x7E97D996, 
	0x6FD8C33C, 0x5C9A8698, 0x7BB249D5, 0xD43D9B4,
	0xAAAC5F3D, 0x264A8038, 0x8DF13471, 0x1C912EC2,
	0xB5D226E7, 0x807803C2, 0xD07EC9D7, 0x8ED952BB
]

QuestKeyTable = [ #==== Table For Decrypting quest.dat ====#
	0x45161724, 0x1D628088, 0xEF1E1690, 0xD706180D, 
	0x2CD75E,   0xE8C54C2B, 0xE37E094F, 0xFBE29E78, 
	0xA55D19AA, 0xF3E9EE1F, 0x99336DD8, 0xC633334A, 
	0xCB0FB5AB, 0x79527874, 0x583E363A, 0xA67FA640, 
	0xAEDD8316, 0xBAFFF13E, 0x43BC03B,  0xF6C744CE,
	0x7E3D100A, 0x65E5199C, 0x760F0BE7, 0x33CA6B78, 
	0x281F702E, 0xF131398F, 0xC0737FF2, 0x3A608374, 
	0xBC5865F1, 0xCA43A35B, 0x6D766010, 0x770BE2C2, 
	0xA77D3D9E, 0xE93F1DB3, 0xCE5E26EC, 0xAA9DC229, 
	0xDD79665E, 0x5A412697, 0x45870A1C, 0x3ADF5F4C,
	0x8830A112, 0x8E27D707, 0x1B1CEFC2, 0x3B6FA2A5, 
	0xB852CFAE, 0x242ADD3F, 0x4C7DFEC6, 0x57D72147, 
	0x5B5612DD, 0x603951BF, 0x600A4D77, 0x8404482, 
	0xD3617496, 0xF4401AC6, 0x82C7DCD6, 0xD4916D8A, 
	0x60028D8F, 0xC54C79F0, 0x599C898F, 0xB6387382,
	0x6A7ED543, 0x8D0A0C82, 0x83C0C4B5, 0x4B17698
]

NetworkKeyTable = [ #==== Table For Decryping network.dat ====#
	0xEE7AC92,  0xF29F5875, 0xCBB2572B, 0x6DC86B3, 
	0x553B9F0B, 0x5DFD99C5, 0xED6FFBB,  0x37D69AC2, 
	0x30A16D25, 0xA22D3C0D, 0xA6D5C8C1, 0xB18F8E99, 
	0x2865CF2,  0xE4A7A62E, 0x37DD1F79, 0xD2A6A211, 
	0x85A60435, 0x1628233,  0x2CFD6417, 0xFFC307E9,
	0x4442D40B, 0x8A11105A, 0x108FB62C, 0xC1B9F529, 
	0x60468D41, 0x6F7DB950, 0x51A8DB7C, 0xDF1FA64C, 
	0xEA508456, 0x6EFA4C34, 0x90AF1DFD, 0x42276A9E, 
	0xB7C94364, 0x6BA070D0, 0xD4C21979, 0x8511B7A3, 
	0x47D42CC0, 0x5DC58EAE, 0xFBFB56F0, 0xAEC981EA, 
	0x45355D36, 0xA862859F, 0x272AD5ED, 0x696CCA17, 
	0x24483704, 0x1E7C03F2, 0xAACB9CEE, 0xB0C75827, 
	0x28D0FDE2, 0x1B382F8E, 0x8E738624, 0x2E6A356D, 
	0xF00D88EF, 0xD22A903E, 0x34339DBC, 0xCB1116F1, 
	0xE9AD1838, 0xA37E340C, 0xE1D64C9E, 0xB8EAAF32,
	0x9D81506D, 0xB79AA1B3, 0x39BD904E, 0x65CEA34D
]

InfoKeyTable = [ #==== Table For Decrypting info.dat ====#
	0xEE2436CA, 0x23A2A1AD, 0x192009F9, 0x60B4EBC9, 
	0x7C6A9E95, 0x35DB824A, 0xE532D84B, 0xAD0B01D6, 
	0x4AF5C2B7, 0xEC108771, 0x23A733E4, 0xA8146A6C, 
	0x8B63CDAD, 0xC0233831, 0xC4A67530, 0xCC610258, 
	0x2B43C00A, 0x7C37E4F4, 0x7ECF64B0, 0x5C4B06A3,
	0xF3105273, 0x1B0030AC, 0xEB3219D9, 0xD1BEBEBB, 
	0x3D457F2A, 0xA5ED8018, 0x64DA8ACD, 0xDEE4877B, 
	0xD167C45,  0xED8A94F7, 0x38A635AD, 0x2F1A9428, 
	0x612641F0, 0xB46034C7, 0xD1A8B152, 0xDF9D0873, 
	0x26130151, 0x8A87EDCB, 0x899B46E7, 0xB732CCCB,
	0xB8C88007, 0x61A23CEF, 0xA6EF4DC4, 0x230D5BDC, 
	0x295A6CC2, 0x5FE0ECCC, 0xE9156285, 0x4911709, 
	0x58D23398, 0x9F03CE36, 0xCF071EB6, 0xB46C7A3, 
	0x26D675A4, 0xE0030ACC, 0xC35642C6, 0xC1ABB9C4, 
	0x44916496, 0x2636F2C8, 0x7708EC6B, 0xC9C6CA70,
	0x50674A95, 0x71CB9A36, 0xB363543F, 0xF43D165A
]

ThumbKeyTable = [ #==== Table For Decrypting Thumbnail BTLs ====#
	0x39B399D2, 0xFAE40B38, 0x851BC213, 0x8CB4E3D9,
	0x7ED1C46A, 0xE8050462, 0xD8D24F76, 0xB52886FC,
	0x67890BF0, 0xF5329CB0, 0xD597FB28, 0x2B8EE0EA,
	0x47574C51, 0xF7569D9,  0xCF1163AE, 0xE4A153BF,
	0xD1FAE468, 0xD4C64738, 0x360106F5, 0xDD7EB113,
	0xC296F3E2, 0x2C58F258, 0x79B554E1, 0x85DF9D06,
	0xAA307330, 0x1410F69,  0xB2F2C573, 0x82B93EB1,
	0xF351A11C, 0x63098693, 0x885B5DA5, 0x8872A8ED,
	0xACD9CB13, 0xED7FBCAD, 0xE6A41EC2, 0x5F44E79F,
	0x8346F5B5, 0x389FE6ED, 0x507124B5, 0xE9B23EAA,
	0x577113F0, 0xA95ED917, 0x2F62D158, 0x47843F86,
	0xC65637D0, 0x2F272052, 0xBA4A4CC4, 0xB5F146F6,
	0x501B87A7, 0x51FC3A93, 0x6EDE3F02, 0x3D265728,
	0x9B809440, 0x75B89229, 0xF6A280CC, 0x8537FA68,
	0x5B5ED19A, 0x6FC05BB6, 0xF4EF5261, 0xAA1B7D4F,
	0xFCB26110, 0xAD3D74,   0xC0E73A4B, 0xF132E7C7
]

UnknownKeyTable = [ #==== Unknown Key Table At 0x7101D79AB0 ====#
	0x7EF2CF75, 0xBCC721F3, 0x3B3DEA13, 0x71703BC9,
	0x59671165, 0x3B67EBBB, 0x9576D83,  0x4642B550, 
	0x8804CA57, 0x390A5067, 0x9298F245, 0x31BA0BFF, 
	0xE8A47324, 0x2E49C434, 0xD8090200, 0xBE3A1C42, 
	0x453497AC, 0xF601CA15, 0xCF721F2D, 0xF89BD2B0,
	0x154F7523, 0x3D906E7D, 0x3FC59F8A, 0xD958F9AB, 
	0x7E3C2D62, 0xCB154D3C, 0x46838AE1, 0xDD0B24A0, 
	0x16C2CABD, 0xCBCA7DDF, 0x40E76BF4, 0xEEAAB9C, 
	0xC7E67237, 0xD3758268, 0xD0082970, 0x77E4A842, 
	0x8B1671A5, 0x235EFFCA, 0x932BFBD1, 0xB55D4F58,
	0xA3F9B95A, 0xBC328F1B, 0x8CC45564, 0xDABCD453, 
	0x716D14D6, 0xA328CD5,  0xB48AD50B, 0x5618FD4B, 
	0x3CACA3DA, 0x2FF6F154, 0x3C6D6A2F, 0x319C4E89, 
	0xE0441007, 0x9628224D, 0x40EDA90B, 0x8B523C7D, 
	0x983A3CF4, 0xEDE1F7A7, 0x590F8E25, 0x865EE19C,
	0xF8D36974, 0x8AD5E61F, 0x8887B5A8, 0x303C31A
]
#====================================#

#==== Decrypt Data ====#
def DecryptData(data, KeyTable, HeaderSize):
    Header = data[:HeaderSize]
    EncryptedCourseData = data[HeaderSize:-0x30]
    CryptoConfig = data[-0x30:]

    context = struct.unpack_from("<IIII", CryptoConfig, 0x10)
    rand = random.Random(*context)

    key = crypto.create_key(rand, KeyTable, 0x10)
    aes = AES.new(key, AES.MODE_CBC, CryptoConfig[:0x10])
    DecryptedCourseData = aes.decrypt(EncryptedCourseData)

    key = crypto.create_key(rand, KeyTable, 0x10)
    mac = CMAC.new(key, ciphermod=AES)
    mac.update(DecryptedCourseData)
    mac.verify(CryptoConfig[0x20:])

    return Header + DecryptedCourseData

#==== Encrypt Data ====#
def EncryptData(data, KeyTable, HeaderSize):
    Header = data[:HeaderSize]
    DecryptedCourseData = data[HeaderSize:]
    RandomState = Random.get_random_bytes(16)

    context = struct.unpack("<IIII", RandomState)
    rand = random.Random(*context)
    
    key = crypto.create_key(rand, KeyTable, 16)
    aes = AES.new(key, AES.MODE_CBC, Random.get_random_bytes(16))
    EncryptedCourseData = aes.encrypt(DecryptedCourseData)

    key = crypto.create_key(rand, KeyTable, 16)
    mac = CMAC.new(key, ciphermod=AES)
    mac.update(DecryptedCourseData)
    mac.digest()

    return Header + EncryptedCourseData + aes.iv + RandomState + mac.digest()

def main():
    if(len(sys.argv)==3):
        f = open(sys.argv[1], "rb")
        f.seek(0,2)

        #==== Thumbnail Data ====#
        if(f.tell()==0x1C000): #==== Encrypted Thumbnail Data ====#
            print("Decrypting Thumbnail Data...")
            data = open(sys.argv[1], "rb").read()
            data = DecryptData(data, ThumbKeyTable, 0x0) #==== Decrypt The Thumbnail Data ====#
            open(os.path.splitext(sys.argv[2])[0]+".jpg", "wb").write(data)
        elif(os.path.splitext(sys.argv[1])[1] in (".jpg", ".jpeg")): #==== Decrypted Thumbnail Data ====#
            print("Encrypting Thumbnail Data...")
            data = open(sys.argv[1], "rb").read()
            if(f.tell()<=0x1BFD0):
                pass
            else:
                print("Error: Thumbnail is too large!")
                return
            data = EncryptData(data+b'\0'*(0x1BFD0 - len(data)), ThumbKeyTable, 0x0) #==== Encrypt The Thumbnail Data ====#
            open(os.path.splitext(sys.argv[1])[0]+".btl", "wb").write(data)

        #==== Course Data ====#
        elif(f.tell()==0x5C000): #==== Encrypted Course Data ====#
            print("Decrypting Course Data...")
            data = open(sys.argv[1], "rb").read()
            data = DecryptData(data, CourseKeyTable, 0x10) #==== Decrypt The Course Data ====#
            open(sys.argv[2], "wb").write(data)
        elif(f.tell()==0x5BFD0): #==== Decrypted Course Data ====#
            print("Encrypting Course Data...")
            data = open(sys.argv[1], "rb").read()
            data = bytearray(data)
            data[0x8:0xC] = int.to_bytes(zlib.crc32(data[0x10:]), 0x4, 'little')
            data = EncryptData(data, CourseKeyTable, 0x10) #==== Encrypt The Course Data ====#
            open(sys.argv[2], "wb").write(data)
        else:
            print("Error: Unsupported file!")
            return
    else:
        if(len(sys.argv)==2):
            f = open(sys.argv[1], "rb")
            f.seek(0,2)

            #==== Thumbnail Data ====#
            if(f.tell()==0x1C000): #==== Encrypted Thumbnail Data ====#
                print("Decrypting Thumbnail Data...")
                data = open(sys.argv[1], "rb").read()
                data = DecryptData(data, ThumbKeyTable, 0x0) #==== Decrypt The Thumbnail Data ====#
                open(os.path.splitext(sys.argv[1])[0]+".jpg", "wb").write(data)
            elif(os.path.splitext(sys.argv[1])[1] in (".jpg", ".jpeg")): #==== Decrypted Thumbnail Data ====#
                print("Encrypting Thumbnail Data...")
                data = open(sys.argv[1], "rb").read()
                if(f.tell()<=0x1BFD0):
                    pass
                else:
                    print("Error: Thumbnail is too large!")
                    return
                data = EncryptData(data+b'\0'*(0x1BFD0 - len(data)), ThumbKeyTable, 0x0) #==== Encrypt The Thumbnail Data ====#
                open(os.path.splitext(sys.argv[1])[0]+".btl", "wb").write(data)

            #==== Course Data ====#
            elif(f.tell()==0x5C000): #==== Encrypted Course Data ====#
                print("Decrypting Course Data...")
                data = open(sys.argv[1], "rb").read()
                data = DecryptData(data, CourseKeyTable, 0x10) #==== Decrypt The Course Data ====#
                open(sys.argv[1], "wb").write(data)
            elif(f.tell()==0x5BFD0): #==== Decrypted Course Data ====#
                print("Encrypting Course Data...")
                data = open(sys.argv[1], "rb").read()
                data = bytearray(data)
                data[0x8:0xC] = int.to_bytes(zlib.crc32(data[0x10:]), 0x4, 'little')
                data = EncryptData(data, CourseKeyTable, 0x10) #==== Encrypt The Course Data ====#
                open(sys.argv[1], "wb").write(data)
            else:
                print("Error: Unsupported file!")
                return
        else:
            print("Usage: "+sys.argv[0]+" <input> [output]")
            return
    print("Done!")

if __name__ == "__main__":
    main()
