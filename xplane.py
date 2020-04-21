UDP_IP = "127.0.0.1"
UDP_PORT = 49000

import socket
import struct 
import xdata

datarefs = [
  
    # ( dataref, unit, description, num decimals to display in formatted output )
    #("sim/flightmodel/position/latitude","°N","The latitude of the aircraft",6),
    #("sim/flightmodel/position/longitude","°E","The longitude of the aircraft",6),
    #("sim/flightmodel/misc/h_ind", "ft", "",0),
    #("sim/flightmodel/position/y_agl","m", "AGL", 0), 
    ("sim/flightmodel/position/mag_psi"),#, "°", "The real magnetic heading of the aircraft",0),
    ("sim/flightmodel/position/indicated_airspeed"),# "kt", "Air speed indicated - this takes into account air density and wind direction",0), 
    ("sim/flightmodel/position/groundspeed"),#"m/s", "The ground speed of the aircraft",0),
    #("sim/flightmodel/position/vh_ind", "m/s", "vertical velocity",1)
    ("sim/cockpit2/engine/indicators/engine_speed_rpm[0]"),
    ("sim/cockpit2/engine/indicators/CHT_deg_C[0]"),
    ("sim/cockpit2/engine/indicators/EGT_deg_C[0]"),
    ("sim/cockpit2/engine/indicators/fuel_flow_kg_sec[0]"),
    ("sim/cockpit2/engine/indicators/fuel_pressure_psi[0]"),
    ("sim/cockpit2/engine/indicators/oil_pressure_psi[0]"),
    ("sim/cockpit2/engine/indicators/oil_temperature_deg_C[0]"),
    ("sim/cockpit2/engine/indicators/MPR_in_hg[0]"),
    ("sim/cockpit2/engine/indicators/carburetor_temperature_C[0]"),
    ("sim/cockpit2/temperature/outside_air_temp_degf[0]"),
    ("sim/time/hobbs_time"), #seconds
    ("sim/time/total_flight_time_sec"),
    ("sim/flightmodel/engine/ENGN_bat_volt[0]"),
    ("sim/cockpit2/fuel/fuel_quantity[0]"), #kgs
    ("sim/flightmodel/position/magnetic_variation")
   


    

  ]


print('Starting UDP connection with Xplane on port ', UDP_PORT)
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

#def RequestData(sock):
 # Send one RPOS Command.
 # Give them an index number and a frequency in Hz.
 # To disable sending you send frequency 0. 
cmd = b"RPOS\x00"
freq=b"20\x00"
message = struct.pack("<5s2s", cmd, freq)
sock.sendto(message, (UDP_IP, UDP_PORT))
print('Requesting Xplane Dataref data...')


for index,dataref in enumerate(datarefs):
    # Send one RREF Command for every dataref in the list.
    # Give them an index number and a frequency in Hz.
    # To disable sending you send frequency 0. 
    cmd = b"RREF\x00"
    freq = 20
    #string = datarefs[index][0].encode()
    string = datarefs[index].encode()
    #print(string)
    message = struct.pack("<5sii400s", cmd, freq, index, string)
    assert(len(message)==413)
    sock.sendto(message, (UDP_IP, UDP_PORT))
    #print(message)


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
   
        #print("Longitude: ", values[1])
        xdata.longitude = values[1]
        #print(" Latitude: ", values[2])
        xdata.latitude = values[2]
        #print(" Altitude: ", values[3])
        xdata.altitude = values[3] 
        #print("      AGL: ", values[4])
        #print("    Pitch: ", values[5])
        xdata.pitch = values[5] 
        #print(" HeadingT: ", values[6])
        xdata.headingt = values[6]
        #print("     Roll: ", values[7])
        xdata.roll = values[7]
        #print("   VSpeed: ", values[9])
        xdata.vspeed = values[9]

        rposdata = 1

    else:
     for key,val in values.items():
      #print(("{0:10."+str(datarefs[key][3])+"f} {1:<5} {2}").format(val[0],val[1],val[2]))
        if (key==0):
            xdata.headingm=val
            #print('mag track: ', val)
        if (key==1):
            xdata.airspeed=val
        if (key==2):
            xdata.gndspeed=val
        if (key==3):
            xdata.rpm=val
        if (key==4):
            xdata.cht=val
        if (key==5):
            xdata.egt=val
        if (key==6):
            xdata.fuelflow=val
        if (key==7):
            xdata.fuelpressure=val
        if (key==8):
            xdata.oilpressure=val
        if (key==9):
            xdata.oiltemp=val
        if (key==10):
            xdata.manifoldpressure=val
        if (key==11):
            xdata.manifoldtemp=val
        if (key==12):
            xdata.oat=val
        if (key==13):
            xdata.hobbs=val
        if (key==14):
            xdata.flighttime=val
        if (key==15):
            xdata.volts=val   
        if (key==16):
            xdata.fuelqty=val
        if (key==17):
            xdata.magvar=val
            
        
        
        
        rrefdata = 1
    
    

    if (rposdata == 1 and rrefdata == 1):
        #print(longitude, latitude, altitude, pitch, roll, headingt, headingm, airspeed, gndspeed)
        rposdata = 0
        rposdata = 0

        
        

    

    

if __name__ == '__main__':
  xplane()
