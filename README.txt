Purpose and Design Philosophy: 

Mirage is a command line python script which is meant to interact with the the Web-Based Graphic User Interaface (Web GUI) 
by sending data through UDP packages, ultimately mimicking data being sent from both MOTES. 

The design philosophy behind the following program is the act of "hoodle", or hardware out of the loop testing. 
Given the spacial limitations fo the lap, we cannot always  ave the MOTE lying out at all times. 
By creating a program which allows the MOTE's behaviors to be remotely accessiable at all times, I hope the following are achieved: 

1) Significant amounts of time when testing firmware and software 

2) Allow for flexibility by offering a remote option for projects which may involve physically connecting MOTE during the testing phase 


Networking Things 

MOTE 
IP: 192.168.0.x
x- is the number of MOTE, either 2/3 

FAKE MOTE (hosted locally)
IP: 127.0.0.1

* note that they will share the same port, since the address of MOTE is just a spoof 
*both random
PORT: 12345 



GUI (hosted locally )
IP: 127.0.0.1
PORT: 5001 


Sniffer Design Logic 

Sensor Dictionary 

Key: Pin number
Value: [data, interface]


Actuator Dictionary 
Value: [state, Interface] 

Bitmasking and Parsing  Logic 


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

