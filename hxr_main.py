from xplane import xplane
from gps import gps
from datacollector import DataCollector

#get xplane data
xplanedata = xplane()
#return [longitude, latitude, altitude, pitch, roll, headingt, headingm, airspeed, gndspeed]
#print(xplanedata)
longitude = xplanedata[0]
latitude = xplanedata[1]
altitide = xplanedata[2]
pitch = xplanedata[3]
roll = xplanedata[4]
headingt = xplanedata[5]
headingm = xplanedata[6]
airspeed = xplanedata[7]
gndspeed = xplanedata[8]

#construct gps message

magvar = -15.9
gps_message = gps(latitude, longitude, headingt, magvar, gndspeed)
print(gps_message)

#send gps message
pfd = DataCollector('192.168.0.1')
pfd.run()
#pfd.send_gps(gps_message)
#mfd = DataCollector('192.168.0.2')


#initialize connections
