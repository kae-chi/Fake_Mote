import sys
import socket 
import time
import socketserver
import time
import os
from helpers import get_interface_name, parse_command 




#class which stores network information 
class server: 

    def __init__(self): 
        self.sock = None
        self.UDP_IP = None
        self.UDP_PORT = None

    
    #function which sets values
    def setup(self):
        self.sock =  socket.socket(socket.AF_INET, #internet
                                   socket.SOCK_DGRAM)   #UDP 
        #ask about this 
        self.UDP_IP = '127.0.0.1'
        self.UDP_PORT = 5005 
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        self.sock.setblocking(0)

    #function to get IP 
  
    





            


