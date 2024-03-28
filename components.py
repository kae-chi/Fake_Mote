import sys
import socket 
import time
from helpers import get_interface_name, parse_command, get_config_size
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




class sniffer: 

    def __init__(self): 
        self.actuator_packets = []
        self.sensor_packets = []

    def process_packet(self, packet): 
        if packet.haslayer(scapy.IP) and packet.haslayer(scapy.UDP):
            payload = packet[scapy.UDP].payload
            if len(payload) >= 2:
                
  
             two_byte_array = payload.load[0:1]
             binary_representation = ''.join(format(byte, '08b') for byte in two_byte_array)

             print(binary_representation)

               

    def show_packet(self, packet): 
        print(packet.summary())



    def split_paths(self, data): 
        pin_num = data[0]
        if pin_num == 1: 
            self.actuator_packets.append(data)
        else: 
            self.sensor_packets.append(data)

    def begin_sniffing(self, command): 
        scapy.sniff(count = get_config_size(command), prn=self.process_packet, store=False)

