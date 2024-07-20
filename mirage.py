import time
import threading
import scapy.all as scapy
from helpers import get_interface_name, parse_command, get_config_size

# Class to store and manage network information
class Network:
    def __init__(self):
        self.IP = None
        self.UDP_IP = '127.0.0.1'  # Localhost by default
        self.UDP_PORT = 12345  # Random port
        self.mote_num = None
        self.pins = {}

    def set_fake_ip(self, ip_address):
        self.IP = ip_address

    def send_packet(self, dst_IP, dst_port, payload):
        try:
            ip = scapy.IP(src=self.IP, dst=dst_IP)
            udp = scapy.UDP(sport=self.UDP_PORT, dport=dst_port)
            scapy.send(ip / udp / payload)
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
                print(f"Packet content: {bytes(packet)}")
                self.udp_packets.append(packet)
                self.intercept_actuator_command(packet)

    def intercept_actuator_command(self, packet):
        # Example logic for identifying send_actuator_command packets
        if b'send_actuator_command' in bytes(packet):
            print(f"Intercepted actuator command: {packet}")
            # Add additional processing logic here

    def start_sniffing(self):
        try:
            print("Start sniffing")
            scapy.sniff(prn=self.find_packet, store=False, filter="udp")
        except Exception as e:
            print(f"Error sniffing packets: {e}")

def send_heartbeat(my_network, dst_IP, dst_PORT):
    packet = "heartbeat"
    while True:
        my_network.send_packet(dst_IP, dst_PORT, packet)
        time.sleep(1)

# Main function
if __name__ == "__main__":

    fakemote1 = Network()
    fakemote1.set_fake_ip('192.168.0.1')

    sniffer1 = Sniffer()
    sniffer1.set_dest_ip('192.168.0.1')

    fakemote2 = Network()
    fakemote2.set_fake_ip('192.168.0.2')
    
    fakemote3 = Network()
    fakemote3.set_fake_ip('192.168.0.2')

    thread4 = threading.Thread(target=send_heartbeat, args=(fakemote1, '127.0.0.1', 8888))
    thread4.start()

    thread5 = threading.Thread(target=send_heartbeat, args=(fakemote2, '127.0.0.1', 8888))
    thread5.start()

    thread6 = threading.Thread(target=send_heartbeat, args=(fakemote3, '127.0.0.1', 8888))
    thread6.start()
    
    sniffer_thread = threading.Thread(target=sniffer1.start_sniffing)
    sniffer_thread.start()
