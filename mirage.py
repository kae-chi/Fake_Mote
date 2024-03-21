import sys
import argparse 
from components import server
import time 
from scapy.all import *

#global variables 

start_time = time.strftime('%I:%M:%S %p %D', time.localtime())

 

        
def send_heartbeat(myNetwork, dst_IP, dst_PORT):
        while True: 
            myNetwork.send_packet(dst_IP, dst_PORT)
            myNetwork.send_packet(dst_IP, dst_PORT)
            time.sleep(2.5)
    

#Main function
if __name__ == "__main__": 
    network2 = server()
    network2.setup()
    network2.set_fake_ip('192.168.0.2')
    send_heartbeat(network2, '127.0.0.1', 5001)
    network3 = server()
    network3.set_fake_ip('192.168.0.3')
    send_heartbeat(network3, '127.0.0.1', 5001)







  
    
    




