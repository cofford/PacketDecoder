#stuffs and unstuffs messages for HXr

import crcmod
import binascii
import struct

flagbyte = '7e'
stuffedflag = '7d5e'
escbyte = '7d'
stuffedbytes = '7d5d'

def unstuff(payload):
    #remove flags and unstuff payload
    x = payload[2:-2].replace (stuffedflag, flagbyte)
    y = x.replace (stuffedbytes, escbyte)
    
    return y 

def stuff(payload):
    #define checksum function
    crc_func = crcmod.predefined.mkCrcFun('x-25')
    
    #calculate checksum
    crc = crc_func(binascii.unhexlify(payload))
    
    #swap checksum bits
    checksum = hex(struct.unpack("<H", struct.pack(">H", crc))[0])[2:]
    payload = (payload + checksum) 
    
    #stuff characters
    x = payload.replace (escbyte, stuffedbytes)
    y = x.replace (flagbyte, stuffedflag)
    
    return (flagbyte + y + flagbyte)

