# Fake Mote


## Purpose and Design Philosophy: 

Fake MOTE is a command line python script which is meant to interact with the the Web-Based Graphic User Interaface (Web GUI) 
by sending data through UDP packages, ultimately mimicking data being sent from both MOTES. 

The design philosophy behind the following program is the act of "hoodle", or hardware out of the loop testing. 
Given the spacial limitations fo the lap, we cannot always  ave the MOTE lying out at all times. 
By creating a program which allows the MOTE's behaviors to be remotely accessiable at all times, I hope the following are achieved: 

1. Significant amounts of time when testing firmware and software 

2. Allow for flexibility by offering a remote option for projects which may involve physically connecting MOTE during the testing phase 


## Dependencies: 

1. **Python 3.12 + ** 
 - Mac: https://www.python.org/downloads/macos/ 
 - Windows: https://www.python.org/getit/windows/ 
 - Linux: https://docs.python.org/3/using/unix.html 

2. ** Rocket GUI **
 -  https://github.com/lukkn/rocket_gui/wiki    

3. ** Scapy library for Python ** 
 - https://scapy.net/ 


## How to install scapy 


### Windows and Mac

1. Install pip 
    -  https://pip.pypa.io/en/stable/installation/ 

2. Open terminal (mac) / powershell (windows) and enter the following: 

  $ pip install scapy 



### Linux 

1. Install libpcap 

 **For debian and ubuntu**
 $ sudo apt-get install libpcap-dev  
 

 **For fedora**



2. Install scapy via   `pip` or `apt`


Please consult the following link (scapy documentation) for any additional information. 
https://scapy.readthedocs.io/en/latest/installation.html 




## Networking Things 

### Relevant IP addresses  


**Fake MOTE** 
Actual IP: 127.0.0.1
> Hosted Locally 
Spoofed IP: 192.168.1.10x  
> x is an arbitrary number for the mote number 
Port: Randomly generated upon the code compiling 
> This is to avoid conflicting ports and loss of information 

**GUI** 
IP: 127.0.0.1
>Hosted locally 
PORT: 5001 
> In the program, the sniffer will be listening on port 8888 (all ports)


## Relevant Bit Schemes 



### 1. Sensors 


  ```
    ┌─────────────────────────────────────┐      
     │GUI                         Fake MOTE│      
     │                                     │      
     │ │                               │   │      
     │ │           configuration       │   │      
     │ │ ────────────────────────────► │   │      
     │ │                               │   │      
     │ │              data             │   │      
     │ │ ◄──────────────────────────── │   │      
     │ │                               │   │      
     │ │                               │   │      
     └─────────────────────────────────────┘ 
 ```

 

 **Data**
 ``
    ┌──────┬─────────┐  
    │ [0]  │   [1:4] │  
    │ pin #│   data  │  
    └──────┴─────────┘    
 ``
                                              

### 2. Actuators   

   ``                                      
    ┌────────────────────────────────────────────┐
    │GUI                                Fake MOTE│
    │                                            │
    │ │                                        │ │
    │ │                                        │ │
    │ │               configuration            │ │
    │ │ ─────────────────────────────────────► │ │
    │ │                                        │ │
    │ │           ack packet                   │ │
    │ │ ◄───────────────────────────────────── │ │
    │ │                                        │ │
    └────────────────────────────────────────────┘
    ``
 *** ACK packet ***

 
    ┌────────────┬─────────┐
    │    [0]     │  [1:4]  │
    │ pin # + 100│  config │
    └────────────┴─────────┘


 **Sensor and Actuator Configuration** 
> Bit packet sent by the GUI 
 
    ┌──────────────────────────────────┐
    │[0000] │     [0000]     | [0000]  |
    │ pin # │ sensor/actuator|interface|
    │       | & act. state   |         |
    └──────────────────────────────────┘


 1. The first bit in the second byteactuator/sensor indicator 
     - 1 - is an actuator 
     - 0 - is a sensor 


2. actuator state 
 - 1 - Actuator is on **TRUE** state
 - 0 - Actuator is on **FALSE** state





 In order for the GUI to process any information sent from fake mote, it must be a byte array of **5 bytes** in the following order: 1. pin number 2. remaining 4 bytes of relevant information packaged in a struct in little endian ordering  \

> Why little endian? Because that's how 1. GUI is able to parse the data 2. Real MOTE works like that 



Sniffer Design Logic 

Sensor Dictionary 

Key: Pin number
Value: [data, interface]


Actuator Dictionary 
Value: [state, Interface] 

Bitmasking and Parsing  Logic 


First bit- which command/interface the returned information is for 

0b10000000

0- Sensor 
1- Actuator 

Second bit- the state of the actuator
0b01000000  
0- False 
1- true

Third through eight bits- packaged interface 

0b00111111

