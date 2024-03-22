import time 
from components import server


my_mote = input("Which Mote Number")

#def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-start', help='Initiate testing sequence, data will be random number values.')
    parser.add_argument('-aa','--configuration csv',type=str,help='CSV with specific set of data')
    parser.add_argument('-ma', help= "prompts user to manually sets data values, will not exit until all actuators are set")
    parser.add_argument('-mpa' '--sensor_name', type=str, help="user can modify a specific value by typing in the according to sensor")
    parser.add_argument('-status', help="displays status through terminal")
    args = parser.parse_args()
    return args


#parses argument and calls appropriate subroutine
#def subroutine_for_args(input):
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




#function for showing nessecary statuses in terminal
def show_status(input): 
    print(f"Start Time: {start_time} \n")
    print(f"Current Time: {time.time()} \n")
    print(f"IP Address: {input.get_ip()}")
    pass 

def start(input): 
    connected = False 

