import time
import threading
import scapy.all as scapy
import random
import sys
import struct
import contextlib 
import os



def suppress_output():
    with open(os.devnull, 'w') as fnull:
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = fnull
        sys.stderr = fnull
        try:
            yield
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr


class Network:
    def __init__(self):
        source_ip = None
        dest_ip = None
        self.dest_port = 8888
        self.src_port = scapy.RandShort()
        self.interface = "en0"
        self.ip_filters = []
        self.sensors = {}
        self.actuators = {}

    def set_source_ip(self, input):
        self.source_ip = input

    def set_dest_ip(self, input):
        self.dest_ip = input

    def send_packet(self, message):
        ip_layer = scapy.IP(src=self.source_ip, dst=self.dest_ip)
        udp_layer = scapy.UDP(dport=self.dest_port, sport=self.src_port)
        payload = scapy.Raw(load=message)
        with open(os.devnull, 'w') as fnull:
            with contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
                scapy.send(ip_layer / udp_layer / payload)

    def add_ip_filters(self, input):
        for e in input:
            if e not in self.ip_filters:
                self.ip_filters.append(e)

    def packet_handler(self, packet):

        if scapy.IP in packet:
            src_ip = packet[scapy.IP].src
            dst_ip = packet[scapy.IP].dst
            if (
                not self.ip_filters
                or src_ip in self.ip_filters
                or dst_ip in self.ip_filters
            ):
                if scapy.Raw in packet:
                    data = packet[scapy.Raw].load
                    if len(data) != 2:
                        pass
                    else:
                        # heartbeat
                        if data == bytes([int(100), 235]):
                            pass
                        # reset sensors command
                        elif data == bytes([0, 44]):
                            print("resetting!")
                            self.sensors = {}
                        else:
                            print("data recieved, now parsing")
                            pin_num = data[0]
                            config = data[1]

                            is_an_actuator = config & 0b10000000 == 0b10000000
                            interface_type_number = config & 0b00111111

                            if is_an_actuator:
                                actuator_state = config & 0b01000000 == 0b01000000
                                # pin num: [actuator state, interface number]
                                self.actuators[pin_num] = [
                                    boolean(actuator_state),
                                    interface_type_number,
                                ]
                                print(
                                    f"pin {pin_num} is an actuator with the state {actuator_state} with the interface of {interface_type_number}"
                                ) 
                                packet = bytearray(4)
                                
                                # first byte is the pin
                                packet[0] = pin_num
                                # translating the random fuzz to bytes and filling in the remaining 4 bytes
                                packet[ 1 : 3] = struct.pack(">f", random.random())
                            else:
                                print(
                                    f"pin {pin_num} is a sensor with the interface {interface_type_number}"
                                )
                                self.sensors[pin_num] = [interface_type_number]

    def start_sniffing(self):
        scapy.sniff(iface=self.interface, prn=self.packet_handler)

    def fuzzing(self):

        while True:
            if len(self.sensors) > 0:
                the_sensors = list(self.sensors)
                packet = bytearray(5 * len(the_sensors))

                for i, k in enumerate(the_sensors):
                    # offset
                    index = 5 * i
                    # first byte is the pin
                    packet[index] = k
                    # translating the random fuzz to bytes and filling in the remaining 4 bytes
                    packet[index + 1 : index + 5] = struct.pack(">f", random.random())

                # send packet at the end
                self.send_packet(packet)
                time.sleep(0.03)

    def tare(self, number):
        if self.actuators[number][1] == False:
            # some mathemetical operation occurs to the censors
            pass


# helpers
def boolean(bit):
    if bit == 1:
        return True
    return False


def send_heartbeat(network, message):
    while True:
        network.send_packet(message)
        time.sleep(1)


# Main function
if __name__ == "__main__":

    fakemote1 = Network()
    fakemote1.set_source_ip("192.168.1.101")
    fakemote1.set_dest_ip("127.0.0.1")
    fakemote1.add_ip_filters(["192.168.1.101"])

    thread1 = threading.Thread(target=send_heartbeat, args=(fakemote1, "hello!"))
    thread2 = threading.Thread(target=fakemote1.start_sniffing)
    thread3 = threading.Thread(target=fakemote1.fuzzing)

    thread1.start()
    thread2.start()
    thread3.start()
