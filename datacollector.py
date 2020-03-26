#!/usr/bin/python3
import socket
import time
import sys
from decode import Decode
from signal import signal, SIGINT

class DataCollector:
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
    '''
    def __init__(self):
        self.isRunning = True
        
        # UDP socket
        self.sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address_local = (('', 10001))
        self.addresses_remote = ['192.168.0.1', '192.168.0.2']
        self.udphello = bytes.fromhex('5B01FF0A00010001947F')
        print('Starting UDP server on {} port {}...'.format(*self.address_local))
        self.sock_udp.bind(self.address_local)
        self.hello = False
        self.data = ''
        self.address = ('', 0)

        # TCP socket
        print('Starting TCP server')
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.sock_tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
        self.sock_tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
        self.sock_tcp.bind(self.address_local)
        self.sock_tcp.listen(1)

        # Watchdog timer functionality
        self.count = 0
        self.timeout = 10
    
    def handler(self, signal_received, frame):
        # Handle any cleanup here
        # self.connection.shutdown(0)
        self.connection.close()
        self.connection = None
        self.sock_tcp.shutdown(0)
        self.sock_tcp.close()
        self.sock_tcp = None
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        sys.exit(0)

    def send_hello(self):
        self.sock_udp.sendto(self.udphello, self.address)
        return bytes.fromhex('7E5B01FF0A00010001947F7E')

    def tcp_data(self):
        data = self.connection.recv(1024)
        if data:
            print('received {!r}'.format(data.hex()))
            Decode(data)
            # print(bytes.fromhex(data))

    def stop(self):
        self.isRunning = False
    
    def run(self):
        while self.isRunning:
            while not self.hello:
                print('Waiting to receive UDP message...')
                self.data, self.address = self.sock_udp.recvfrom(10)
                for i in self.addresses_remote:
                    if i in self.address:
                        self.hello = True
                        print('Received message from {}'.format(i))
                        if self.data:
                            self.tcphello = self.send_hello()
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
            except ValueError:
                self.connection.close()
            time.sleep(0.01)
            
if __name__ == "__main__":
    
    uc = UdpCollector()
    signal(SIGINT, uc.handler)
    print('Running. Press CTRL-C to exit.')
    uc.run()

            