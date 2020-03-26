#'7e5b01ff0a1a00010000000084c501f4aa010000000000c201d6af01000000001cce0188d5010000000006f301f4f5014e4e000000000000000000000000000000000000001f008002000000000000010200000000000000000014000000000000f7457e'

import crcmod
import binascii
import struct

flagbyte = '7e'
stuffedflag = '7d5e'
escbyte = '7d'
stuffedbytes = '7d5d'

def unstuff(payload):
    
    x = payload[2:-2].replace (escbyte, stuffedbytes)
    y = x.replace (flagbyte, stuffedflag)
    return y #return value

def stuff(payload):
    
    x = payload.replace (stuffedflag, flagbyte)
    y = x.replace (stuffedbytes, escbyte)
    return y #return value


payload = '7e5b01ff0a1a00010000000084c501f4aa010000000000c201d6af01000000001cce0188d5010000000006f301f4f5014e4e000000000000000000000000000000000000001f008002000000000000010200000000000000000014000000000000f7457e'
#print(payload)
unstuffed = unstuff(payload)
print('unstuffed: ', unstuffed)
stuffed = stuff(unstuffed)[:-4]  
print('stuffed: ', stuffed)
crc_func = crcmod.predefined.mkCrcFun('x-25')
crc = crc_func(binascii.unhexlify(stuffed))
#print(crc)
checksum = hex(struct.unpack("<H", struct.pack(">H", crc))[0])[2:]
print(checksum)
stuffed_payload = stuff(unstuffed[:-4] + checksum)  #removes existing checksum, adds new one
print(payload)
print(flagbyte + stuffed_payload + flagbyte)