import time
import threading
import sys
import scapy.all as scapy
from helpers import get_interface_name, parse_command, get_config_size


class Network:
    def __init__(self):
        source_ip = None
        dest_ip = None
        self.dest_port = 8888
        self.src_port = scapy.RandShort()

    def set_source_ip(self, input):
        self.source_ip = input

    def set_dest_ip(self, input):
        self.dest_ip = input

    def send_packet(self, message):
        ip_layer = scapy.IP(src=self.source_ip, dst=self.dest_ip)
        udp_layer = scapy.UDP(dport=self.dest_port, sport=self.src_port)
        payload = scapy.Raw(message)
        scapy.send(ip_layer / udp_layer / payload)

class Sniffer:
    def __init__(self):
        self.interface = "en0"
        self.ip_filters =[]
        self.bytes = [] 

    def add_ip_filters(self, input): 
        for e in input: 
            if e not in self.ip_filters: 
                self.ip_filters.append(e)
        

    def packet_handler(self, packet):
        if scapy.IP in packet:
            src_ip = packet[scapy.IP].src
            dst_ip = packet[scapy.IP].dst
            if not self.ip_filters or src_ip in self.ip_filters or dst_ip in self.ip_filters:
               packet.show()
               
                    
                
                

    def start_sniffing(self):
        scapy.sniff(iface=self.interface, prn=self.packet_handler)
        print()


def send_heartbeat(network, message):
    while True:
        network.send_packet(message)
        time.sleep(1)


# Main function
if __name__ == "__main__":

      # Replace with your network interface

    sniffer = Sniffer()
    sniffer.add_ip_filters(["192.168.1.101", "192.168.1.104"])

    thread2 = threading.Thread(target = sniffer.start_sniffing)

    fakemote1 = Network()
    fakemote1.set_source_ip("192.168.1.101")
    fakemote1.set_dest_ip("127.0.0.1")
    thread1 = threading.Thread(target=send_heartbeat, args=(fakemote1, "hello"))


    thread1.start()
    thread2.start() 

