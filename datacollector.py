#!/usr/bin/python3
import socket
import time
import sys
from decode import Decode
from signal import signal, SIGINT
#from xplane import xplane
from message import gps, eis
import xdata

class DataCollector:
    '''
    UDP listens for a HELLO packet from HXrfrom datacollector import DataCollector
        --> 7e frame flag
        --> 5b vendor protocol code
        --> 01 source=1 (Primary ID)
        --> ff destination=255 (broadcast)
        --> 0a TTL=10
        --> 00 packet type=0 (hello)self.connection.sendall(self.tcp_hello)
        --> 01 link version=1
        --> 00 serial number=1
        --> 01 (LSB of serial number)
        --> 94 checksum=0x7f94
        --> 7f (MSB of checksum)
        --> 7e frame flag
    '''
    def __init__(self, hxr_host):
        self.isRunning = True
        
        # UDP socket
        self.sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address_local = (('', 10001))
        self.addresses_remote = hxr_host
        self.udphello = bytes.fromhex('5B01FF0A00010001947F')
        print('Starting UDP server on port {}...'.format(self.address_local[1]))
        self.sock_udp.bind(self.address_local)
        self.hello = False
        self.data = ''
        self.address = ('', 0)

        # TCP socket
        print('Starting TCP server')
        self.tcp_hello = bytes.fromhex('7E5B01FF0A00010001947F7E')
        self.tcp_hxr_hello = '7e5b01ff0a000100001d6e7e'
        self.keepalive_last_time = time.strftime('%s')
        self.keepalive_trigger = False
        self.keepalive_diff = '9'
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.sock_tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
        self.sock_tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
        self.sock_tcp.bind(self.address_local)
        self.sock_tcp.listen(1)
        

        #temp
        #self.gps_message = bytes.fromhex('7e5b01ff0a09001369ab9c0552fd3c424e36f5c2000dfa06055e00c4a37e')
        

        # Watchdog timer functionality
        self.count = 0
        self.timeout = 10
    
    def handler(self, signal_received, frame):
        # Handle any cleanup here
        self.connection.close()
        self.connection = None
        self.sock_tcp = None
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        sys.exit(0)

    def send_hello(self):
        self.sock_udp.sendto(self.udphello, self.address)
        return bytes.fromhex('7E5B01FF0A00010001947F7E')
     
    def tcp_data(self):
        
        data = self.connection.recv(1024)
        if data:
            Decode(data)
            if self.tcp_hxr_hello in data.hex():
                print('\n\tHeartbeat response!\n')
                self.connection.sendall(self.tcp_hello)
            else:
                print('received {}:\n\t{!r}'.format(time.asctime(), data.hex()))
                
            

    def send_data(self):
        
        gps_message = bytes.fromhex(gps())
        #print(gps_message.hex())
        self.connection.send(gps_message)
        time.sleep(0.01)
        
        eis_message = bytes.fromhex(eis())
        #print(eis_message.hex())
        self.connection.send(eis_message)
        time.sleep(0.01)
        

    def stop(self):
        self.isRunning = False
    
    def run(self):
        while self.isRunning:
            while not self.hello:
                print('Waiting to receive UDP message...')
                self.data, self.address = self.sock_udp.recvfrom(10)
                if self.addresses_remote in self.address:
                    self.hello = True
                    print('Received message from {}'.format(self.address))
                    if self.data:
                        self.tcp_hello = self.send_hello()
                        print('waiting for a TCP connection')
                        self.connection, self.client_address = self.sock_tcp.accept()
                else:
                    time.sleep(1)
                    self.count +=1
                    if self.count == self.timeout:
                        print("Reached timout. Exiting")
                        sys.exit(254)
            try:
                self.tcp_data()
                #time.sleep(0.1)
            #try:
                self.send_data()
                #time.sleep(0.1)
                
                
                

            except ValueError:
                self.connection.close()
            time.sleep(0.01)
            
if __name__ == "__main__":
    # Create and instance of the class using the HXr hostname.
    uc = DataCollector(hxr_host='192.168.0.2')
    signal(SIGINT, uc.handler)
    print('Running. Press CTRL-C to exit.')
    uc.run()

            