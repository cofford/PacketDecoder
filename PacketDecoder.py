import struct

#data = bytes.fromhex('7E5B01FF0A0231383D3400687D5D7E')
#data = bytes.fromhex('7e5b01ff0a0f0a8b00ce00ce00ce00ce000000000125012501250125000000000000000000000000000000000000e0419a99b541000000000000ffdd00643a0000000000000000000000000000000000000000004500000000000000000000000000002aef7e')
data = bytes.fromhex('7e5b01ff0a0903001369ab8c05a5a77e') #time, date from GPS
#data = bytes.fromhex('7e5b01ff0a09001369ab9c0552fd3c424e36f5c2000dfa06055e00c4a37e') #GPRMC time, date, position, mag var

#unstuff bytes here.  7d5d = 7d, 7d5e = 7e

protocol = data[1]
source = data[2]
destination = data[3]
ttl = data[4]
packet_type = data[5]
payload = data[6:-3]
checksum = data[-3:-1].hex()

#print(protocol)
#print(source)
#print(destination)
#print(packet_type)
#print(payload.hex())
#print(checksum)

if packet_type == 9:
      subpacket_type = payload[0]

      if subpacket_type == 0: #time, date, position, mag var, from current GPS source, like GPRMC
        time = int.from_bytes(payload[2:6], byteorder='little')
        latitude = struct.unpack("f", payload[6:10])[0]
        longitude = struct.unpack("f", payload[10:14])[0]
        track = struct.unpack("h", payload[14:16])[0]
        magvar = struct.unpack("h", payload[16:18])[0]
        gndspeed = struct.unpack(">h", payload[18:20])[0]
     
        year = payload[1]   
        month = time & 15
        day = (time >> 4) & 31
        hour = (time >> 9) & 31
        min = (time >> 14) & 63
        sec = (time >> 20) & 63
        status = (time >> 26) & 1
        
        track = track/10
        magvar = magvar/100
        gndspeed = gndspeed/10

        print('subpacket type: {}'.format(subpacket_type))
        print('20{}/{}/{}, {}:{}:{}, Status: {}'.format(year, month, day, hour, min, sec, status))
        print('latitude: {}, longitude: {}'.format(latitude, longitude))
        print('track: {}\N{DEGREE SIGN}, gndspeed: {} kts, magvar: {}\N{DEGREE SIGN}'.format(track, gndspeed, magvar))
        

        #if subpacket_type == 1: navigation data to active waypoint, like GPRMB

        #if subpacket_type == 2: waypoints in active flight plan from current GPS source

      if subpacket_type == 3:
        time = int.from_bytes(payload[3:7], byteorder='little')
        
        year = payload[2]   
        month = time & 15
        day = (time >> 4) & 31
        hour = (time >> 9) & 31
        min = (time >> 14) & 63
        sec = (time >> 20) & 63
        status = (time >> 26) & 1
       
        print('subpacket type: {}'.format(subpacket_type))
        print('20{}/{}/{}, {}:{}:{}, Status: {}'.format(year, month, day, hour, min, sec, status))

        #if subpacket_type == 4: GPS altitide and geoidal difference, fix quality, number of satellites in fix, from current GPS source like GPGGA
        
        