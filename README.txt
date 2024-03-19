Purpose and Design Philosophy: 

Mirage is a command line python script which is meant to interact with the the Web-Based Graphic User Interaface (Web GUI) 
by sending data through UDP packages, ultimately mimicking data being sent to the flight computer. 

The design philosophy behind the following program is the act of "hoodle", or hardware out of the loop testing. 
Given the spacial limitations fo the lap, we cannot always  ave the MOTE lying out at all times. 
By creating a program which allows the MOTE's behaviors to be remotely accessiable at all times, I hope the following are achieved: 

1) Significant amounts of time when testing firmware and software 

2) Allow for flexibility by offering a remote option for projects which may involve physically connecting MOTE during the testing phase p

INPUT: 
- sensor data at any point 

OUPUT: 
- actuator commands received from the GUI 
Acutator Commands 

0b10000000

First bit- command


0b01000000  
Second bit- the state of the actuator

0b00111111
Third bit- interface type


-s: initiate testing sequence, data will be random number values. 

-md:  prompts user to manually sets sensor values, will not exit until all actuators are set

-ad [data.csv]: sets data points using a specific csv file


