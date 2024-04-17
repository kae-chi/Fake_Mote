import sys
import socket 
import csv
import time
import os


# DO NOT REMOVE: ignore error, path is appended and libary will import at runtime
custom_libs_path = os.path.abspath("./libs2")
sys.path.insert(0, custom_libs_path)

# For threading
from threading import Thread

# Function to create a dictionary from an actuator list
# converts list of sensors and actuators to a single dictionary for O(1) lookup time
def create_sensor_dictionary(sensor_and_actuator_list):
    dict = {}
    for sensor in sensor_and_actuator_list:
        dict[sensor["Mote id"] + ", " + sensor["Pin"]] = [sensor["P and ID"], sensor["Interface Type"], sensor["Sensor or Actuator"], sensor["Unit"]]
    return dict


#helper function which takes an input of an integer, which should match to a command 
def get_interface_name(number): 
   if number == 5: 
        return 'servoPWM_12V' 
   elif number == 41: 
        return "Bang-Bang"
   elif number == 43: 
        return "HeartBeat"
   elif number == 44: 
        return "Clear_Config"
   elif number == 45: 
        return "Start_Log"
   else: 
        interface_list = ['Teensy ADC', 'i2c ADC 1ch', 'i2c ADC 2ch',
                      'FlowMeterCounter', 'servoPWM', 'Binary GPIO',
                      'i2c ADC 2ch PGA2', 'i2c ADC 2ch PGA4', 'i2c ADC 2ch PGA8',
                      'i2c ADC 2ch PGA16', 'i2c ADC 2ch PGA32', 'i2c ADC 2ch PGA64',
                      'i2c ADC 2ch PGA128', 'ADC Internal Temp', 'SPI_ADC_1ch', 
                      'SPI_ADC_2ch', 'SPI_ADC_2ch PGA2', 'SPI_ADC_2ch PGA4', 'SPI_ADC_2ch PGA8', 
                      'SPI_ADC_2ch PGA16', 'SPI_ADC_2ch PGA32', 'SPI_ADC_2ch PGA64', 'SPI_ADC_2ch PGA128',
                      'Icarus_ALT', 'Icarus_IMU', 'Volt_Monitor', 'Loop_Timer']
        return interface_list[number]
       
#function for determining


def parse_command(data): 
    #checks for correct data size 
    if len(data) != 2: 
        print("Packet is incorrect size")
        return 
    #Begin parsing packet
    pin_num = data[0]
    config_num = data[1]
    actuator_state = config_num & 0b01000000 == 0b01000000
    interface_num = config_num & 0b00111111
    # if largest bit is 1: checks for if data packet is intended to write to an actuator command
    if (pin_num and 0b10000000) == 0b10000000: 
        #execute appropriate command
        print(f"Acutator Configuration Command: Setting pin {pin_num} to {actuator_state} with interface {get_interface_name(interface_num)} ")
        return
    #if largest bit is 0: must be a configuration command 
    else: 
        get_interface_name(pin_num)
        print(f'Sensor Configuration Command: pin {pin_num} can be read using interface {get_interface_name(interface_num)}')
        return 
    
def get_config_size(file):
     home_directory = os.path.expanduser('~')
     
     # Define the name of the subdirectory within the home directory
     subdirectory = 'Mirage/configs'

     file_name = file + '.csv'
     
     # Combine parts to form a full file path

     full_path = os.path.join(home_directory, subdirectory,file_name)

     print(full_path)


     try:
               with open(full_path, mode='r', encoding='utf-8') as csv_file:
                    reader = csv.reader(csv_file)
                    # Skip the header row
                    next(reader, None)
                    row_count = 0 
                    for row in reader:

                         row_count += 1
                    return row_count
     except FileNotFoundError:
               print(f"File not found: {full_path}")
     except Exception as e:
               print(f"An error occurred while reading {full_path}: {e}")