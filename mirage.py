import sys
import argparse 
from routine import server
import time 
#global variables 

start_time = time.time()
#Function to show status 
def show_status(input): 
    print("Start Time: {start_time} \n" )
    print("Current Time: {time.time()} \n")
    print("IP Address:  \n")



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
        
    

    

#actual routine 
if __name__ == "__main__": 
    show_status()
    #initialize server
    #network = server()
    
    




