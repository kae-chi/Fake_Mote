import sys
import argparse 
from components import network
import time 
from scapy.all import *
import threading 

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
    fakemote1 = network()
    fakemote1.setup()
    fakemote1.set_fake_ip('192.168.0.1')
    thread1 = threading.Thread(target=send_heartbeat, args=(fakemote1, '127.0.0.1', 8888))
    thread1.start()  # Start the first thread


    
   







  
    
    




