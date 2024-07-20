
import scapy.all as scapy


 

#class which stores network information 
class network: 

    def __init__(self): 
        self.IP = None 
        self.UDP_IP = '127.0.0.1'
        self.UDP_PORT =  12345 
        self.mote_num = None 
        self.pins = {}
    


    #function to set fake ip, dependent on global mote count  
    def set_fake_ip(self, input): 
        self.IP = input




    #Uses scapy library to send fake package from 
    def send_packet(self, dst_IP, dst_port,payload):
        try: 
            ip = scapy.IP(src = self.IP, dst = dst_IP)
            udp = scapy.UDP(sport=self.UDP_PORT, dport=dst_port)
            scapy.send(ip/udp/payload)
        except Exception as e: 
            print(f"Error sending packet: {e}")


class Sniffer:
    def __init__(self):
        self.udp_packets = []
        self.actuator_packets = []  # Placeholder for future use
        self.sensor_packets = []  # Placeholder for future use
        self.dest_ip = None

    def set_dest_ip(self, desired_ip):
        self.dest_ip = desired_ip

    def find_packet(self, packet):
        if scapy.IP in packet and packet[scapy.IP].dst == self.dest_ip:
            if scapy.UDP in packet:
                print(f"UDP packet to {self.dest_ip}: ", packet.summary())
                self.udp_packets.append(packet)
                print

    def start_sniffing(self):
        scapy.sniff(prn=self.find_packet, store=False, filter="udp")






        
