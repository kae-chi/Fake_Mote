import time
import threading
import scapy.all as scapy
import random
import platform
import csv
import struct
import sys

from os import path


class mote:

    def __init__(self, mote_num):
        self.source_ip = "192.168.1.10" + f"{mote_num}"
        self.dest_ip = None
        self.dest_port = 8888
        self.src_port = 12345
        self.interface = None
        self.ip_filters = []
        self.sensors = {}
        self.actuators = {}

        if platform.system() == "Windows":
            print("windows detected! ")
            self.interface = "Ethernet"
        elif platform.system() == "Darwin":
            print("mac detected! ")
            self.interface = "en0"
        else:
            print("linux detected! ")
            self.interface = "eth0"

    def set_dest_ip(self, input):
        self.dest_ip = input

    def send_packet(self, message):
        ip_layer = scapy.IP(src=self.source_ip, dst=self.dest_ip)
        udp_layer = scapy.UDP(dport=self.dest_port, sport=self.src_port)
        payload = scapy.Raw(load=message)
        scapy.send(x=(ip_layer / udp_layer / payload), verbose=False)

    def add_ip_filters(self, input):
        for e in input:
            if e not in self.ip_filters:
                self.ip_filters.append(e)

    def packet_handler(self, packet):
        # print(packet)

        if scapy.IP in packet:
            # print("nice")
            src_ip = packet[scapy.IP].src
            dst_ip = packet[scapy.IP].dst
            if (
                not self.ip_filters
                or src_ip in self.ip_filters
                or dst_ip in self.ip_filters
            ):
                # print("hi!")
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
                            self.actuators = {}
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
                                    actuator_state,
                                    interface_type_number,
                                ]
                                print(
                                    f"pin {pin_num} is an actuator with the state {actuator_state} with the interface of {interface_type_number}"
                                )
                                packet = bytearray(5)
                                ack_pin = 100 + pin_num
                                packet[0] = int(ack_pin)
                                packet[1:5] = struct.pack(">f", config)

                                self.send_packet(packet)

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
                    packet[index + 1 : index + 5] = struct.pack(
                        ">f", random.randint(0, 100)
                    )

                # send packet at the end
                self.send_packet(packet)
                time.sleep(0.03)

    def tare(self, number):
        if self.actuators[number][1] == False:
            # some mathemetical operation occurs to the censors
            pass


def send_heartbeat(mote, message):
    while True:
        mote.send_packet(message)
        time.sleep(1)


def spawn_mote_threads(config_name):
    mote_nums = []
    try:
        with open(
            path.join("configs", f"{config_name}.csv"), mode="r", newline=""
        ) as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row and row[0] == "Mote id": 
                    continue
                if row and row[0] not in mote_nums:
                    mote_nums.append(row[0])
    except:
        print("no offset file found")


    for n in mote_nums:
        mote_n = mote(n)
        print(mote_n.source_ip)
        mote_n.set_dest_ip("127.0.0.1")
        mote_n.add_ip_filters([mote_n.source_ip])

        thread1 = threading.Thread(target=send_heartbeat, args=(mote_n, bytes([0])))
        thread2 = threading.Thread(target=mote_n.start_sniffing)
        thread3 = threading.Thread(target=mote_n.fuzzing)

        thread1.start()
        thread2.start()
        # thread3.start()


# Main function
if __name__ == "__main__":
    config_file = sys.argv[1]
    spawn_mote_threads(config_file)
    

