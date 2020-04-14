#!/usr/bin/python3
#

import socket
import sys
from decode import Decode

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

IP = "0.0.0.0"
PORT = 10001

udphello = bytes.fromhex('5B01FF0A00010001947F')
gpsmessage = bytes.fromhex('7e5b01ff0a09001369ab8c05dafc3c424f36f5c2000afa06056100e2c77e')
# Bind the socket to the port
server_address = (IP, PORT)
print('starting up UDP on {} port {}'.format(*server_address))
sock.bind(server_address)

address = ''
while '192.168.0.1' not in address:
    print('\nwaiting to receive UDP message')
    data, address = sock.recvfrom(4096)

print('received {} bytes from {}'.format(
    len(data), address))
print(data.hex())

if data:
    sent = sock.sendto(udphello, address)
    print('sent {} bytes back to {}'.format(
        sent, address))
    print(udphello.hex())

tcphello = bytes.fromhex('7E5B01FF0A00010001947F7E')

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind the socket to the port
print('starting up TCP on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a TCP connection')
    connection, client_address = sock.accept()
    try:
        print('TCP connection from', client_address)
        i = 0
        # Receive data
        while True:
            data = connection.recv(1024)
            print('received {!r}'.format(data.hex()))
            connection.sendall(gpsmessage)
            Decode(data)
            if data:
                if i == 20:
                    connection.sendall(tcphello)
                    #print('sending data back to the client')
                    i = 0
                i = i+1
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
