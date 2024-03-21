import sys
import socket 
import time
import socketserver
import time
import os
from helpers import get_interface_name, parse_command
import struct
from scapy.all import IP


 

#class which stores network information 
class server: 

    def __init__(self): 
        self.IP = None 
        self.sock = None
        self.UDP_IP = None
        self.UDP_PORT = None
        self.IP_header = None
        self.UDP_header = None 

    
    #function which sets values
    def setup(self):
        self.sock =  socket.socket(socket.AF_INET, #internet
                                   socket.SOCK_DGRAM)   #UDP 
        self.UDP_IP = '127.0.0.1' # local host
        self.UDP_PORT = 5005  #random port 
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        self.sock.setblocking(0)
     


    #function to set fake ip, dependent on global mote count  
    def set_fake_ip(self, input): 
        self.IP = input

       

    #function to "listen" 
    def listen(self): 
        while True: 
            pass
        
    
    # DO NOT USE ANYTHING RELATED TO CREATING AN IP HEADER 
    def create_ip_header(self, dst_ip):
        # IP Header fields
        ip_ver = 4
        ip_ihl = 5  # Header Length
        ip_dscp_ecn = 0
        ip_total_length = 0  # Kernel will fill the correct total length
        ip_id = 54321
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = socket.IPPROTO_UDP
        ip_checksum = 0  # Kernel will fill the correct checksum
        ip_saddr = socket.inet_aton(self.IP)  # Source IP
        ip_daddr = socket.inet_aton(dst_ip)  # Destination IP

        ip_ihl_ver = (ip_ver << 4) + ip_ihl

        # The ! in the pack format string means network order (big-endian)
        ip_header = struct.pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_dscp_ecn, ip_total_length, ip_id,
                                ip_frag_off, ip_ttl, ip_proto, ip_checksum, ip_saddr, ip_daddr)
        return ip_header
      
    # DO NOT USE ANYTHING RELATED TO CREATING AN UDP HEADER 
    def create_udp_header(self, dst_port, payload_length):
        udp_header_length = 8  # UDP header size is always 8 bytes
        udp_length = udp_header_length + payload_length
        udp_checksum = 0  # Let's set this to zero

        udp_header = struct.pack('!HHHH', self.UDP_PORT, dst_port, udp_length, udp_checksum)
        return udp_header
    
    #Uses scapy library to send fake package from 
    def send_packet(self, packet, dst_IP, dst_port, interface):
        #heartbeat packet
        if interface == "hearbeat":
            packet = scapy.IP(src= self.IP, dst= dst_IP) / UDP(sport = self.UDP_PORT, dport = dst_port)  / raw(load=bytearray[2]) /send(packet)
    
 



    





            


