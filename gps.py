import struct
from charstuffer import stuff

'''
    UDP listens for a HELLO packet from HXr
    Format:
        HELLO
        --> 7e frame flag
        --> 5b vendor protocol code
        --> 01 source=1 (Primary ID)
        --> ff destination=255 (broadcast)
        --> 0a TTL=10
        --> 00 packet type=0 (hello)
        --> 01 link version=1
        --> 00 serial number=1
        --> 01 (LSB of serial number)
        --> 94 checksum=0x7f94
        --> 7f (MSB of checksum)
        --> 7e frame flag


    protocol = data[1]
    source = data[2]
    destination = data[3]
    ttl = data[4]
    packet_type = data[5]
    payload = data[6:-3]
    checksum = data[-3:-1].hex()
   
Packet type 9.
Byte 0: 0 (GPS position packet)
Byte 1: Last two digits of year (year mod 100), zero if unknown
Byte 2-5: packed LSB first: month (4 bits) | day (5 bits) | hour (5 bits) | min (6 bits) | sec (6 bits) | status (1 bit)
The date and time fields are all zeroes if unknown.
The status bit is 1 when the GPS has indicated its data is valid.
The EFIS may try to use this data as a time source if the day is non-zero and status is 1.
Byte 6-9: latitude (32-bit float)
Byte 10-13: longitude (32-bit float)
Byte 14-15: Ground track in tenths of a degree, MSB first
Byte 16-17: Magnetic variation in hundredths of a degree, MSB first, positive west
Byte 18-19: Ground speed in tenths of a knot, MSB first
Byte 20: bit field
Bit 0 = GPS2 input is configured on this unit
Bit 1 = This data is from GPS2
'''

def gps(latitude, longitude, track, magvar, gndspeed): #latlong are floats.  track/magvar/gndspeed are short

    protocol = 91
    source = 1
    destination = 255
    ttl = 10
    packet_type = 9
    subpacket_type = 0
    year = 20
    
    track = int(track*10)
    magvar = int(magvar*100) 
    gndspeed = int(gndspeed*10)
    print('track, magvar, speed:  ', track, magvar, gndspeed)
    
    #status = '1'
    #latitude = 47.12345 #32 bit float f
    #longitude = -122.12345 #32 bit float f
    #track = = 3590 #ground track in tenths, h
    #magvar = -1700 #magvar in hundreths, pos west, h
    #gndspeed = 2300 #groundspeed in tenths, MSB first, h
    bits = 0
    '''
    month = time & 15
    day = (time >> 4) & 31
    hour = (time >> 9) & 31
    minute = (time >> 14) & 63
    sec = (time >> 20) & 63
    status = (time >> 26) & 1
    '''
    time = 94153577
    #'7e5b01ff0a09001369ab9c0552fd3c424e36f5c2000dfa06055e00c4a37e'
    #payload = data[6:-3]
    #checksum = data[-3:-1].hex()
    #print(data)
    #payload = struct.pack("7BIff", protocol, source, destination, ttl, packet_type, subpacket_type, year, time, latitude, longitude)
    
    payload = struct.pack("7B", protocol, source, destination, ttl, packet_type, subpacket_type, year)
    payload2 = struct.pack("Iff", time, latitude, longitude)
    payload3= struct.pack(">HhHb", track, magvar, gndspeed, bits)
    #print(payload.hex())
    #print(payload2.hex())
    #print(payload3.hex())    
    message = stuff((payload+payload2+payload3).hex())
    return message


#year = 19
#month = 0
#day = 0
#hour = 0
#minute = 0
#sec = 0
#status = 1
##latitude = 46.24738311767578
#longitude = -121.60606384277344
#track = 13
#magvar = -1530
#gndspeed = 1374



#gps_payload  = gps(latitude, longitude, track, magvar, gndspeed)
#print(gps_payload)



 

            

        