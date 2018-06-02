#!/usr/bin/env python

"""
Copyright (C) 2017 AeroSys Engineering, Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Revision History:
  2017-09-17: KSB, created in support of weather station creation

"""
# define a version for the file
VERSION = "1.0.20170917a"

from random import randint
import cPickle as pickle
import time
import socket

class RoofStationData():
    def __init__(self):
        return





class METARData():
    def __init__(self):
        return


class Receiver():
    def __init__(self):
        self.addr = socket.gethostbyname('roofpi')
        self.sock = 24831
        return
  
    def get_data(self):
        # create an INET, STREAMing socket
        self.rx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # connect to the server
        try:
            self.rx_socket.connect((self.addr, self.sock))
        except socket.error, exc:
            print "Receiver.get_data(): Unable to connect: %s"%exc
            return
        
        try:
            data = pickle.loads(self.rx_data())
        except RuntimeError, exc:
            print "Receiver.get_data(): Unable to received data: %s"%exc
            return
    
        # show what we got
        print data.show()
        
        return
  
    def rx_data(self):
        header_length = 14
        
        # get the header to find the length
        header = self.rx_bytes(header_length)
        data_length = header.split(' ')[1]
        
        # get the datablock
        return self.rx_bytes(int(data_length))
      
    def rx_bytes(self, length):
        chunks = []
        bytes_received = 0
        while bytes_received < length:
            chunk = self.rx_socket.recv(length-bytes_received)
            if chunk == b'':
                raise RuntimeError("Receiver.rx_data: socket connection broken")
            chunks.append(chunk)
            bytes_received += len(chunk)
        return b''.join(chunks)

# only run main if this file is run directly
if __name__ == '__main__':
    # start here
    rx = Receiver()
      
    while True:
        delay = randint(1,5)
        print "Sleeping %d seconds"%delay
        time.sleep(delay)
        
        # get the data
        rx.get_data()
  
