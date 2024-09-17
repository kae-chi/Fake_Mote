import time
import threading
import scapy.all as scapy
import random
import platform
import csv
import struct
import sys
import argparse
import os

# helper function for getting interfaces


def get_interface_name(interface_number):
    if interface_number == 5:
        return "servoPWM_12V"
    if interface_number == 41:
        return "Bang-Bang"
    if interface_number == 42:
        return "FireX"
    if interface_number == 43:
        return "Heartbeat"
    if interface_number == 44:
        return "Clear_Config"
    if interface_number == 45:
        return "Start_Log"
    if interface_number == 46:
        return "Watchdog"

    interface_list = [
        "Teensy ADC",
        "i2c ADC 1ch",
        "i2c ADC 2ch",
        "FlowMeterCounter",
        "servoPWM",
        "Binary GPIO",
        "i2c ADC 2ch PGA2",
        "i2c ADC 2ch PGA4",
        "i2c ADC 2ch PGA8",
        "i2c ADC 2ch PGA16",
        "i2c ADC 2ch PGA32",
        "i2c ADC 2ch PGA64",
        "i2c ADC 2ch PGA128",
        "ADC Internal Temp",
        "SPI_ADC_1ch",
        "SPI_ADC_2ch",
        "SPI_ADC_2ch PGA2",
        "SPI_ADC_2ch PGA4",
        "SPI_ADC_2ch PGA8",
        "SPI_ADC_2ch PGA16",
        "SPI_ADC_2ch PGA32",
        "SPI_ADC_2ch PGA64",
        "SPI_ADC_2ch PGA128",
        "BMP_ALT",
        "Icarus_IMU",
        "Volt_Monitor",
        "Loop_Timer",
        "BMP_TEMP",
        "BMP_Pressure",
    ]

    if 1 <= interface_number <= len(interface_list):
        return interface_list[interface_number - 1]

    return None


def sensor_human_name(n, pin_num):
    mote_num = n.source_ip[-1]
    try:
        with open(n.config_path, "r") as f:
            reader = csv.reader(f)
            # ["mote", "human name",  "pin number", "interface", "flag","flag value"]
            for row in reader:
                if (
                    str(mote_num) == row[0]
                    and str(pin_num) == row[4]
                    and row[1] == "sensor"
                ):
                    # return the interface of the human name
                    # REMUS NITPICKED AHHHHHHH
                    return row[3]
    except:
        print("Please make sure the mote/pin number combination is a SENSOR")


def actuator_human_name(n, pin_num):
    mote_num = n.source_ip[-1]

    try:
        with open(n.config_path, "r") as f:
            reader = csv.reader(f)
            # ["mote", "human name",  "pin number", "interface", "flag","flag value"]
            for row in reader:
                if (
                    str(mote_num) == row[0]
                    and str(pin_num) == row[4]
                    and row[1] == "actuator"
                ):
                    # return the interface of the human name
                    # Remus nitpick zzz
                    return row[3]
    except:
        print("Please make sure the mote/pin number combination is an ACUATOR")


class mote:

    def __init__(self, mote_num, mote_path, csv_path, actuator_path, config_path):
        self.source_ip = "192.168.1.10" + f"{mote_num}"
        self.dest_ip = None
        self.dest_port = 8888
        self.src_port = 12345
        self.interface = None
        self.ip_filters = []
        self.sensors = {}
        self.actuators = {}
        self.config_path = config_path
        self.csv_path = csv_path
        self.mote_path = mote_path
        self.actuator_path = actuator_path
        self.flagged_sensors = {}

        if platform.system() == "Windows":

            self.interface = "Ethernet"
        elif platform.system() == "Darwin":

            self.interface = "en0"
        else:

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
                            print("Resetting!")
                            self.sensors = {}
                            self.actuators = {}
                        else:
                            print("Data recieved, now parsing.")

                            pin_num = data[0]

                            config = data[1]

                            is_an_actuator = config & 0b10000000 == 0b10000000
                            interface_type_number = config & 0b00111111
                            #actuator condition
                            if is_an_actuator:

                                actuator_state = config & 0b01000000 == 0b01000000

                                # pin num: [actuator state, interface number]
                                self.actuators[pin_num] = [
                                    actuator_state,
                                    interface_type_number,
                                ]
                                human_name = actuator_human_name(self, pin_num)
                                print(
                                    f"MOTE {self.source_ip[-1]}, pin {pin_num} is the actuator {human_name} with the state {actuator_state} with the interface of {get_interface_name(interface_type_number)}"
                                )

                                with open(self.actuator_path, "a", newline="") as file:
                                    writer = csv.writer(file)
                                    writer.writerow(
                                        [
                                            self.source_ip[-1],
                                            human_name,
                                            pin_num,
                                            get_interface_name(pin_num),
                                            actuator_state,
                                        ]
                                    )
                                packet = bytearray(5)
                                ack_pin = 100 + pin_num
                                packet[0] = int(ack_pin)
                                packet[1:5] = struct.pack(">f", config)

                                self.send_packet(packet)

                            else:
                                #sensor condition
                                human_name = sensor_human_name(self, pin_num)
                                print(
                                    f"MOTE {self.source_ip[-1]}, pin {pin_num} is the {human_name} sensor with the interface {get_interface_name(interface_type_number)}"
                                )
                                #add to dictionary
                                self.sensors[pin_num] = 0
                                with open(self.csv_path, "a", newline="") as file:
                                    writer = csv.writer(file)
                                    writer.writerow(
                                        [
                                            self.source_ip[-1],
                                            human_name,
                                            pin_num,
                                            get_interface_name(pin_num),
                                            False,
                                        ]
                                    )
                                    

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
                time.sleep(0.01)

    def send_specific_data(self):

        while True:
            if len(self.flagged_sensors) > 0:

                the_sensors = list(self.flagged_sensors)
                packet = bytearray(5 * len(the_sensors))

                for i, k in enumerate(the_sensors):
                    # offset
                    index = 5 * i
                    # first byte is the pin
                    packet[index] = k
                    # translating the random fuzz to bytes and filling in the remaining 4 bytes
                    packet[index + 1 : index + 5] = struct.pack(
                        ">f", self.flagged_sensors[k]
                    )

                # send packet at the end
                self.send_packet(packet)
                time.sleep(0.01)


def send_heartbeat(mote, message):
    while True:
        mote.send_packet(message)
        time.sleep(1)


def flag(sensor_path, mote_list, mote_num, pin, data):
    flagged_mote = None
    for n in mote_list:
        if str(mote_num) == n.source_ip[-1]:

            flagged_mote = n

    if flagged_mote != None:
        modify_csv_for_flag(sensor_path, mote_num, pin, data)
        # remove that pin to avoid any conflict of packets
        if pin in flagged_mote.sensors:
            print(f"Flagging new pin {pin} with flagged value {data}")
            flagged_mote.sensors.pop(pin)
            flagged_mote.flagged_sensors[pin] = data
        else:
            print(f"Pin {pin} is already flagged, changing flagged value to {data}")
            flagged_mote.flagged_sensors[pin] = data
    else:
        print("Double check that mote pin pair exist.")
        return


def spawn_mote_threads(path, mote_path, csv_path, actuator_path):
    mote_nums = []
    try:
        with open(path) as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row and row[0] == "Mote id":
                    continue
                if row and row[0] not in mote_nums:
                    mote_nums.append(row[0])

    except:
        print("Please make sure your configuration file exists and ends with .csv")

    motes = []
    for n in mote_nums:

        mote_n = mote(n, mote_path, csv_path, actuator_path, path)
        print(f"Mote {mote_n.source_ip[-1]} generated! {mote_n.source_ip}")
        with open(mote_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([n, mote_n.source_ip])
        mote_n.set_dest_ip("127.0.0.1")
        mote_n.add_ip_filters([mote_n.source_ip])

        thread1 = threading.Thread(target=send_heartbeat, args=(mote_n, bytes([0])))
        thread2 = threading.Thread(target=mote_n.start_sniffing)
        thread3 = threading.Thread(target=mote_n.fuzzing)

        thread1.start()
        thread2.start()
        thread3.start()

        motes.append(mote_n)

    return motes


def spawn_motes(config_path, mote_path, csv_path, actuator_path):
    print("Generating appropriate objects.")
    try:

        the_motes = spawn_mote_threads(config_path, mote_path, csv_path, actuator_path)
        return the_motes
    except:
        print("An error occured while generating motes.")
        return False


def initiate_flagging(mote_obj):
    mote_obj.send_specific_data()


def initial_flag(sensor_path, mote_list, mote_num, pin, data):
    flagged_mote = None
    for n in mote_list:
        if str(mote_num) == n.source_ip[-1]:
            flagged_mote = n
            break

    if flagged_mote != None:
        if pin not in flagged_mote.sensors:
            print("Please double check if the mote and pin pair exists.")
            return False
        else:
            modify_csv_for_flag(sensor_path, mote_num, pin, data)
            # remove that pin to avoid any conflict of packets
            flagged_mote.flagged_sensors[pin] = data
            flagged_mote.sensors.pop(pin)

            thread4 = threading.Thread(target=initiate_flagging, args=(flagged_mote,))
            thread4.start()
            return True

    else:
        print("Error!")
        return False


def modify_csv_for_flag(sensor_path, mote_num, pin_num, value):
    # ["mote", "human name",  "pin number", "interface", "flag","flag value"]
    sensors = []

    with open(sensor_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == str(mote_num) and row[2] == str(pin_num):
                row = [row[0], row[1], row[2], row[3], True, value]
            sensors.append(row)

    

    with open(sensor_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(sensors)


def setup():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logs_folder = os.path.join(current_dir, "logs")

    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # create a folder if it does not exists
    if not os.path.exists(logs_folder):
        print("Initialzing logs directory.")
        os.mkdir(logs_folder)

    # Create unique folder for persistence
    directory_name = os.path.join(logs_folder, f"{formatted_time}")
    try:
        os.mkdir(directory_name)
    except OSError as e:
        print(f"Failed to create directory: {e}.")
        return

    # Create mote CSV file
    mote_path = os.path.join(directory_name, "mote_config.csv")
    with open(mote_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["mote number", "IP", "At least one senosr flagged"])

    # Create sensors CSV file
    csv_path = os.path.join(directory_name, "sensors.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["mote", "human name", "pin number", "interface", "flag", "flag value"]
        )

    # Create actuators CSV file

    actuator_path = os.path.join(directory_name, "actuator.csv")
    with open(actuator_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["mote", "human name", "pin number", "interface", "state"])

    print("Intialized!")

    return mote_path, csv_path, actuator_path


def main():

    mote_path = None
    csv_path = None
    actuator_path = None
    mote_list = None
    motes_flagged = {}

    # Print operating system

    print("Welcome to fakemote. Use -h to see what commands you can use. ")

    if platform.system() == "Windows":
        print("Windows detected! ")
    elif platform.system() == "Darwin":
        print("Mac detected! ")
    else:
        print("Linux detected! ")

    parser = argparse.ArgumentParser(description="Welcome to fakemote.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    # spawning fake motes
    e_parser = subparsers.add_parser("e", help="Exit out of the program")
    s_parser = subparsers.add_parser(
        "s", help="Spawn motes based on CSV configuration file"
    )
    s_parser.add_argument(
        "configuration",
        type=str,
    )
    # flagging sensors from single data point
    fs_parser = subparsers.add_parser(
        "fs", help="Flag motes based off of their pins with a single data point"
    )
    fs_parser.add_argument("mote_number", type=int)
    fs_parser.add_argument("pin_number", type=int)
    fs_parser.add_argument("data_point", type=int)

    # fa_parser = subparsers.add_parser('fa', help="Fuzz data on all sensor pins" )

    while True:
        try:
            user_input = input(">> ")
            args = parser.parse_args(user_input.split())
            if args.command == "e":
                print("Exiting out of fakemote.")
                sys.exit()
            elif args.command == "s":
                mote_path, csv_path, actuator_path = setup()
                mote_list = spawn_motes(
                    args.configuration, mote_path, csv_path, actuator_path
                )
                for i in mote_list:
                    motes_flagged[i.source_ip[-1]] = False
            elif args.command == "fs":
                print(
                    f"Flagging pin {args.pin_number} on Mote {args.mote_number} and inputting the single value {args.data_point}"
                )

                if args.data_point > (2**32 - 1):
                    print("Value is too big!")
                elif not motes_flagged[str(args.mote_number)]:
                    print("No pins in mote {args.mote_number}flagged: calling initial flagging protocol.")
                    
                    motes_flagged[str(args.mote_number)] = initial_flag(
                        csv_path,
                        mote_list,
                        args.mote_number,
                        args.pin_number,
                        args.data_point,
                    )

                else:

                    flag(
                        csv_path,
                        mote_list,
                        args.mote_number,
                        args.pin_number,
                        args.data_point,
                    )
            elif mote_list == None:
                print("Please use the command: s path/to/config_file")

        except Exception as e:
            print(f"{e}")


# Main function
if __name__ == "__main__":
    main()
