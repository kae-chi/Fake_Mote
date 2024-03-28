import sys
import argparse 
from components import network, sniffer
import time 
from scapy.all import *
import threading 
import csv

#global variables 

start_time = time.strftime('%I:%M:%S %p %D', time.localtime())




 

        
def send_heartbeat(myNetwork, dst_IP, dst_PORT):
        while True: 
            myNetwork.send_packet(dst_IP, dst_PORT)
            myNetwork.send_packet(dst_IP, dst_PORT)
            time.sleep(1)


#function to receive actuator tuple
#input -- [id num, binary number]

def receieve_actuator_command(input):
    #slice the tuple 
    id_num = input[0]
    data = input[2]




#Main function
if __name__ == "__main__": 
 
    sniffy = sniffer()
    sniffy.begin_sniffing('gse')
   







  
    
    




