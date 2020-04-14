import struct

data = '7e5b01ff0a09001369ab9c0552fd3c424e36f5c2000dfa06055e00c4a37e'

def Decode(data):

    #unstuff bytes here.  7d5d = 7d, 7d5e = 7e.  Unstuff checksum to check (CRC16.X25).  Then unstuff remaining message.

    protocol = data[1]
    source = data[2]
    destination = data[3]
    ttl = data[4]
    packet_type = data[5]
    payload = data[6:-3]
    #checksum = data[-3:-1].hex()
    #print(data)

    #print(protocol)
    #print(source)
    #print(destination)
    #print(packet_type)
    #print(payload.hex())
    #print(checksum)

    if packet_type == 0:
        print('\n\tHeartbeat request!')

    #if packet_type == 1a: nav/com, transponder state
    if packet_type == 0x0f: #engine data.  fuel flow, fuel quantity, hourmeter as 32 bit floats. EGT 1-6, airspeed (2 byte int), altimeter (4 byte int). volts, VS, baroset as 32b floats.  Byte before tach2 is bitfield 0 tachstop 1 fuelflowstop 2 canbus data.
    #TACH,CHT1CHT2CHT3CHT4CHT5CHT6,EGT1EGT2EGT3EGT4EGT5EGT6,EGT7EGT8EGT9,
        tach = struct.unpack(">h", payload[0:2])[0]
        cht1 = struct.unpack(">h", payload[2:4])[0]
        cht2 = struct.unpack(">h", payload[4:6])[0]
        cht3 = struct.unpack(">h", payload[6:8])[0]
        cht4 = struct.unpack(">h", payload[8:10])[0]
        egt1 = struct.unpack(">h", payload[14:16])[0]
        egt2 = struct.unpack(">h", payload[16:18])[0]
        egt3 = struct.unpack(">h", payload[18:20])[0]
        egt4 = struct.unpack(">h", payload[20:22])[0]
        
        print('Tach: {} RPM'.format(tach))
        print('CHT1: {}\N{DEGREE SIGN}'.format(cht1))
        print('EGT1: {}\N{DEGREE SIGN}'.format(egt1))
    #if packet_type == 0b: limit settings
    #if packet_type == 4: analog inputs

    if packet_type == 9:
        subpacket_type = payload[0]

        if subpacket_type == 0: #time, date, position, mag var, from current GPS source, like GPRMC
            time = int.from_bytes(payload[2:6], byteorder='little')
            latitude = struct.unpack("f", payload[6:10])[0]
            longitude = struct.unpack("f", payload[10:14])[0]
            track = struct.unpack(">h", payload[14:16])[0]
            magvar = struct.unpack(">h", payload[16:18])[0]
            gndspeed = struct.unpack(">h", payload[18:20])[0]
        
            year = payload[1]   
            month = time & 15
            day = (time >> 4) & 31
            hour = (time >> 9) & 31
            minute = (time >> 14) & 63
            sec = (time >> 20) & 63
            status = (time >> 26) & 1
            
            track = track/10
            magvar = magvar/100
            gndspeed = gndspeed/10

            print('subpacket type: {}'.format(subpacket_type))
            print('20{}/{}/{}, {}:{}:{}, Status: {}'.format(year, month, day, hour, minute, sec, status))
            print('latitude: {}, longitude: {}'.format(latitude, longitude))
            print('track: {}\N{DEGREE SIGN}, gndspeed: {} kts, magvar: {}\N{DEGREE SIGN}'.format(track, gndspeed, magvar))
            

        if subpacket_type == 1: #navigation data to active waypoint, like GPRMB
            print('received {!r}'.format(data.hex()))

        if subpacket_type == 2: #waypoints in active flight plan from current GPS source
            print('received {!r}'.format(data.hex()))

        if subpacket_type == 3:
            time = int.from_bytes(payload[3:7], byteorder='little')
            
            year = payload[2]   
            month = time & 15
            day = (time >> 4) & 31
            hour = (time >> 9) & 31
            minute = (time >> 14) & 63
            sec = (time >> 20) & 63
            status = (time >> 26) & 1
        
            print('subpacket type: {}'.format(subpacket_type))
            print('20{}/{}/{}, {}:{}:{}, Status: {}'.format(year, month, day, hour, minute, sec, status))

            #if subpacket_type == 4: GPS altitide and geoidal difference, fix quality, number of satellites in fix, from current GPS source like GPGGA
            
Decode(data)            