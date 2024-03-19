import sys
import socket 
import time
import socket
import socketserver
import time
import os


# DO NOT REMOVE: ignore error, path is appended and libary will import at runtime
custom_libs_path = os.path.abspath("./libs2")
sys.path.insert(0, custom_libs_path)

# For threading
from threading import Thread

import configuration
import actuator





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
    def initialize(self):
        self.sock =  socket.socket(socket.AF_INET, #internet
                                   socket.SOCK_DGRAM)   #UDP 
        self.UDP_IP = get_ip()
        self.UDP_PORT = 5005 
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        self.sock.setblocking(0)

    #function to get IP 
    def get_IP(self): 
       return '192.168.1.' + str(100 + (int(mote_id)))
            


