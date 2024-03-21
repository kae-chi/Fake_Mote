import sys
import argparse 
from components import server
import time 
import scapy 


#global variables 

network = server()
network.setup()
start_time = time.strftime('%I:%M:%S %p %D', time.localtime())





def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-start', help='Initiate testing sequence, data will be random number values.')
    parser.add_argument('-aa','--configuration csv',type=str,help='CSV with specific set of data')
    parser.add_argument('-ma', help= "prompts user to manually sets data values, will not exit until all actuators are set")
    parser.add_argument('-mpa' '--sensor_name', type=str, help="user can modify a specific value by typing in the according to sensor")
    parser.add_argument('-status', help="displays status through terminal")
    args = parser.parse_args()
    return args


#parses argument and calls appropriate subroutine
def subroutine_for_args(input):
    if input == '-s': 
        #subrouting for initiating generic start sequence
        pass
    elif input == "-ma":
        #subroutine for manually setting data
        pass
    elif input == "-mpa": 
        #subroutine for pre-made set of data and user input csv 
        pass
    elif input == '-aa': 
        #subroutine for testing a specific set of values 
        pass
    elif input == '-status': 
        #subroutine for showing basic information 
        pass
        
    

    

#Main function
if __name__ == "__main__": 
    network = server()
    network.setup()

    network.set_fake_ip('192.168.0.2')
    dst_ip = '127.0.0.1'
    dst_port = 5001

    network.send_packet(dst_ip, dst_port, 'heartbeat')
  
    
    




