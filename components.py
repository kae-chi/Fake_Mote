import sys
import socket 
import time
from helpers import get_interface_name, parse_command
import scapy.all as scapy


 

#class which stores network information 
class network: 

    def __init__(self): 
        self.IP = None 
        self.UDP_IP = None
        self.UDP_PORT = None
        self.mote_num = None 
        self.pins = {}
    
    #function which sets values
    def setup(self):
        self.UDP_IP = '127.0.0.1' # local host
        self.UDP_PORT = 12345  #random port 
  
     


    #function to set fake ip, dependent on global mote count  
    def set_fake_ip(self, input): 
        self.IP = input


    #function to "listen" 
    def listen(self): 
        while True: 
            pass
        

    #Uses scapy library to send fake package from 
    def send_packet(self, dst_IP, dst_port):
        ip = scapy.IP(src = self.IP, dst = dst_IP)
        udp = scapy.UDP(sport=self.UDP_PORT, dport=dst_port)
        payload = "Hello UDP!!"

        scapy.send(ip/udp/payload)
    



    





            


