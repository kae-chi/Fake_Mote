import sys
import socket 
import time
import socketserver
import time
import os


# DO NOT REMOVE: ignore error, path is appended and libary will import at runtime
custom_libs_path = os.path.abspath("./libs2")
sys.path.insert(0, custom_libs_path)

# For threading
from threading import Thread

#Function for getting IP 
def get_ip(self,mote_id=None):
        if mote_id == None:
            return '127.0.0.1'
        return '192.168.1.' + str(100 + (int(mote_id)))

#Function for retrieving an interface's number from a string 
def get_interface_type_number(interface_name):
    if interface_name == 'servoPWM_12V':
        print("12 Volt Servo")
        return 5
    if interface_name == 'Bang-Bang':
        return 41
    if interface_name == 'FireX':
        return 42
    if interface_name == 'Heartbeat':
        return 43
    if interface_name == 'Clear_Config':
        return 44
    if interface_name == "Start_Log":
        return 45
    interface_list = ['Teensy ADC', 'i2c ADC 1ch', 'i2c ADC 2ch',
                      'FlowMeterCounter', 'servoPWM', 'Binary GPIO',
                      'i2c ADC 2ch PGA2', 'i2c ADC 2ch PGA4', 'i2c ADC 2ch PGA8',
                      'i2c ADC 2ch PGA16', 'i2c ADC 2ch PGA32', 'i2c ADC 2ch PGA64',
                      'i2c ADC 2ch PGA128', 'ADC Internal Temp', 'SPI_ADC_1ch', 
                      'SPI_ADC_2ch', 'SPI_ADC_2ch PGA2', 'SPI_ADC_2ch PGA4', 'SPI_ADC_2ch PGA8', 
                      'SPI_ADC_2ch PGA16', 'SPI_ADC_2ch PGA32', 'SPI_ADC_2ch PGA64', 'SPI_ADC_2ch PGA128',
                      'Icarus_ALT', 'Icarus_IMU', 'Volt_Monitor', 'Loop_Timer']

    # +1 because interface numbers start at 1, not 0
    return interface_list.index(interface_name) + 1



# Function to create a dictionary from an actuator list
# converts list of sensors and actuators to a single dictionary for O(1) lookup time
def create_sensor_dictionary(sensor_and_actuator_list):
    dict = {}
    for sensor in sensor_and_actuator_list:
        dict[sensor["Mote id"] + ", " + sensor["Pin"]] = [sensor["P and ID"], sensor["Interface Type"], sensor["Sensor or Actuator"], sensor["Unit"]]
    return dict

#class which stores network information 
class server: 

    def __init__(self): 
        self.sock = None
        self.UDP_IP = None
        self.UDP_PORT = None

    
    #function which sets values
    def setup(self):
        self.sock =  socket.socket(socket.AF_INET, #internet
                                   socket.SOCK_DGRAM)   #UDP 
        #ask about this 
        self.UDP_IP = get_ip()
        self.UDP_PORT = 5005 
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        self.sock.setblocking(0)

    #function to get IP 
    
  

    def send_actuator_command(self, mote_id, pin_num, state, interface_type, button_ID=None): 
        #For all actual operations 
        if interface_type != "Hearbeat": 
            print(f"Sending {state} command to pin {pin_num} on MoTE {mote_id}, via {interface_type}")
        #Pre-existing button ID
        if button_ID is not None: 
             pass 

        actuator_write_command = 0b10000000
        actuator_state_mask = 0b01000000 if state else 0
        interface_type_number =  & 0b00111111
        config_byte = actuator_write_command | actuator_state_mask | interface_type_number
        ip = get_ip(mote_id=mote_id)
        self.sock.sendto(bytes([int(pin_num), config_byte]), (ip, 8888))

    def send_heartbeats(self): 
        #send 3 unique heartbeats 
        while True: 
            print("sending heartbeats bump bump")
            self.send_actuator_command(1, 100, True, interfaceType="Heartbeat")
            self.send_actuator_command(2, 100, True, interfaceType="Heartbeat")
            self.send_actuator_command(3, 100, True, interfaceType="Heartbeat")


    

#function to parse 2 byte data 
def parse_command(data): 
    #checks for correct data size 
    if len(data) != 2: 
        print("Packet is incorrect size")
        return 
    #Begin parsing packet
    pin_num = data[0]
    config_num = data[1]
    # if largest bit is 1: checks for if data packet is intended to write to an actuator command
    if (pin_num and 0b10000000) == 0b10000000: 
        #execute appropriate command
        pass 
    #if largest bit is 0: must be a configuration command 
    else: 
        interface_num = data.slice(3,7)
        interface_num = int(config_num) 

        #switch case for the appropriate interface
        pass 
        print("ERROR. No interface was found. ")



            


