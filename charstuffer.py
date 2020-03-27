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
    x = payload[2:-2].replace (escbyte, stuffedbytes)
    y = x.replace (flagbyte, stuffedflag)
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
    x = payload.replace (stuffedflag, flagbyte)
    y = x.replace (stuffedbytes, escbyte)
    
    return (flagbyte + y + flagbyte)

'''
#Test code
#payload = '7e5b01ff0a1a00010000000084c501f4aa010000000000c201d6af01000000001cce0188d5010000000006f301f4f5014e4e000000000000000000000000000000000000001f008002000000000000010200000000000000000014000000000000f7457e'
payload = '5b01ff0a1a00010000000084c501f4aa010000000000c201d6af01000000001cce0188d5010000000006f301f4f5014e4e000000000000000000000000000000000000001f008002000000000000010200000000000000000014000000000000'
payload2 = '7e5b01ff0a000100001d6e7e'
#payload = '5b01ff0a00010000'
print('Original payload:   ', payload)
stuffed = stuff(payload)
print(' Stuffed payload: ', stuffed)

print(' Original payload:   ', payload2)
unstuffed = unstuff(payload2)
print('Unstuffed payload:     ', unstuffed)
'''