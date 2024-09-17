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

1. **Python 3.12 +** 
 - Mac: https://www.python.org/downloads/macos/ 
 - Windows: https://www.python.org/getit/windows/ 
 - Linux: https://docs.python.org/3/using/unix.html 

2. **Rocket GUI**
 -  https://github.com/lukkn/rocket_gui/wiki    

3. **Scapy library for Python** 
 - https://scapy.net/ 


## How To Install Scapy 


### Windows and Mac

1. Install pip 
    -  https://pip.pypa.io/en/stable/installation/ 

2. Open terminal (mac) / powershell (windows) and enter the following: 
 ```
  % pip install scapy 
 ```



### Linux 

1. Install libpcap 

 **For debian and ubuntu**
```
% sudo apt-get install libpcap-dev  
 ```

2. Install scapy via   `pip` or `apt`


Please consult the following link (scapy documentation) for any additional information. 
https://scapy.readthedocs.io/en/latest/installation.html 

## How to launch GUI 

1. Open terminal (mac) or git bash (windows) and enter the following

```
% git clone https://phab.burpg.space/diffusion/80/webgui.git
```
2. Go into webgui directory and then FlaskGUI directory 
```
% cd  ../webgui 
% cd FlaskGUI
```
3. Then enter the following to run the app
```
% python3 app.py 
```

At this point, the GUI webpage should open in your browser 

## How To Run Fake Mote (command line)
1. Open terminal (mac) or git bash (windows) and enter the following: 

```
%cd ../fakemote
% python3 fakemote.py

```

Fake MOTE should be running at this point in the corresponding terminal 

## Important Command Lines

> Fake MOTE must be running at this point for any of the following command lines to work

1. Spawning (fake) motes 
```
% -s <path/to/config/file>
```
Spawns and sets up motes based on configuration file. 

2. Flagging pins 
```
% -fs  <mote_number>  <pin number> <data point>

Flags a single pin based off of data points


## CSV Logging 

There exists a csv log for each component of the mote they are located in logs/, in the folder of when you called the -s command. 
To find the appropriate one, the file name is function.csv. For sensors, it would be sensors.csv. 





