import sys
import socket 
import time
import socketserver
import time
import os
from helpers import get_ip, get_interface_type_number


# DO NOT REMOVE: ignore error, path is appended and libary will import at runtime
custom_libs_path = os.path.abspath("./libs2")
sys.path.insert(0, custom_libs_path)

# For threading
from threading import Thread





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
        self.UDP_IP = get_ip()
        self.UDP_PORT = 5005 
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        self.sock.setblocking(0)

    #function to get IP 
   


    





            


