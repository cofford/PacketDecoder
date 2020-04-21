from threading import Thread, Event
from xplane import xplane
from time import sleep
import xdata
from datacollector import DataCollector
from hxr_serial import hxr_serial



event = Event()




t = Thread(target=xplane)
t.start()
pfd = DataCollector('192.168.0.1')
t2 = Thread(target=pfd.run)
t2.start()
t3 = Thread(target=hxr_serial)
t3.start()

while True:
        try:
                #print(xdata.longitude, xdata.latitude)
                sleep(1)
        except KeyboardInterrupt:
                event.set()
                break
t.join()
print(xdata.longitude)