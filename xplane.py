UDP_IP = "127.0.0.1"
UDP_PORT = 49000

import socket
import struct 

datarefs = [
  
    # ( dataref, unit, description, num decimals to display in formatted output )
    #("sim/flightmodel/position/latitude","°N","The latitude of the aircraft",6),
    #("sim/flightmodel/position/longitude","°E","The longitude of the aircraft",6),
    #("sim/flightmodel/misc/h_ind", "ft", "",0),
    #("sim/flightmodel/position/y_agl","m", "AGL", 0), 
    ("sim/flightmodel/position/mag_psi", "°", "The real magnetic heading of the aircraft",0),
    ("sim/flightmodel/position/indicated_airspeed", "kt", "Air speed indicated - this takes into account air density and wind direction",0), 
    ("sim/flightmodel/position/groundspeed","m/s", "The ground speed of the aircraft",0),
    #("sim/flightmodel/position/vh_ind", "m/s", "vertical velocity",1)
    

  ]


print('Starting UDP connection with Xplane on port ', UDP_PORT)
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

#def RequestData(sock):
 # Send one RPOS Command.
 # Give them an index number and a frequency in Hz.
 # To disable sending you send frequency 0. 
cmd = b"RPOS\x00"
freq=b"1\x00"
message = struct.pack("<5s2s", cmd, freq)
sock.sendto(message, (UDP_IP, UDP_PORT))
print('Requesting Xplane Dataref data...')

for index,dataref in enumerate(datarefs):
    # Send one RREF Command for every dataref in the list.
    # Give them an index number and a frequency in Hz.
    # To disable sending you send frequency 0. 
    cmd = b"RREF\x00"
    freq=1
    string = datarefs[index][0].encode()
    message = struct.pack("<5sii400s", cmd, freq, index, string)
    assert(len(message)==413)
    sock.sendto(message, (UDP_IP, UDP_PORT))

def DecodePacket(data):
  retvalues = {}
  # Read the Header "RREFO".
  header=data[0:4]
  if(header==b"RPOS"):
    retvalues = struct.unpack("<5sdddffffffffff", data)

  if(header==b"RREF"):
    # We get 8 bytes for every dataref sent:
    #    An integer for idx and the float value. 
    values =data[5:]
    lenvalue = 8
    numvalues = int(len(values)/lenvalue)
    idx=0
    value=0
    for i in range(0,numvalues):
      singledata = data[(5+lenvalue*i):(5+lenvalue*(i+1))]
      (idx,value) = struct.unpack("<if", singledata)
      #retvalues[idx] = (value, datarefs[idx][1], datarefs[idx][0])
      retvalues[idx] = value

  
  #else:
       #print("Unknown packet: ", data)
  
  return retvalues

def xplane():
  rposdata = 0
  rrefdata = 0

  while (rposdata == 0 or rrefdata == 0):
    # Receive packet
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    # Decode Packet
    values = DecodePacket(data)
    
    header=data[0:4]
    if(header==b"RPOS"):
   
        print("Longitude: ", values[1])
        longitude = values[1]
        print(" Latitude: ", values[2])
        latitude = values[2]
        print(" Altitude: ", values[3])
        altitude = values[3] 
        print("      AGL: ", values[4])
        print("    Pitch: ", values[5])
        pitch = values[5] 
        print(" HeadingT: ", values[6])
        headingt = values[6]
        print("     Roll: ", values[7])
        roll = values[7]
        print("   VSpeed: ", values[9])
        vspeed = values[9]

        rposdata = 1

    else:
     for key,val in values.items():
      #print(("{0:10."+str(datarefs[key][3])+"f} {1:<5} {2}").format(val[0],val[1],val[2]))
        if (key==0):
            headingm=val
            print(" Headingm: ", headingm)
        if (key==1):
            airspeed=val
            print (" Airspeed: ", airspeed)
        if (key==2):
            gndspeed=val
        
        rrefdata = 1
    
    #return (longitude, latitude, altitude, pitch, roll, headingt, headingm, airspeed, gndspeed))

    while (rposdata == 1 and rrefdata ==1):
        #print(longitude, latitude, altitude, pitch, roll, headingt, headingm, airspeed, gndspeed)
        rposdata = 0
        rposdata = 0

        return [longitude, latitude, altitude, pitch, roll, headingt, headingm, airspeed, gndspeed]

    

    #print(values)

if __name__ == '__main__':
  xplane()
