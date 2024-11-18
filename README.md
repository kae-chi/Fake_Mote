# Fake Mote


## Purpose and Design Philosophy: 
Fake MOTE is a command line script and testing framework for the BURPG Web-Based Graphic User Interface (Web GUI). 
On a high level, the program creates "virtual hardware" by utilizing the scapy library to IP spoof as hardware, undo bitmasking operations, and perform the appropriate network protocols to mimic MOTE behavior. 

The design philosophy behind the following program is the act of "HOOTL", or hardware out-of-the-loop testing. 

By creating a software framework that allows a singular or network of MOTEs to be remotely accessible at all times, I hope the following are achieved: 

1. Significant amounts of time saved when testing firmware and software 

2. Allow for flexibility by offering a remote option for projects that may involve physically connecting MOTE during the testing phase]

3. Serve as a tool for data replay of previous testing operations and simulate potential new scenarios. 


## Dependencies: 

1. **Python 3.12 +** 
 - Mac: https://www.python.org/downloads/macos/ 
 - Windows: https://www.python.org/getit/windows/ 
 - Linux: https://docs.python.org/3/using/unix.html 

2. **Rocket GUI**
 -  https://github.com/lukkn/rocket_gui/wiki    

3. **Scapy library for Python** 
 - https://scapy.net/ 

4. **Libcap/NPcap**
 - https://npcap.com/ 
 - https://www.tcpdump.org/

## How To Install Dependencies

### Linux and Mac
---

1. Install pip 
    -  https://pip.pypa.io/en/stable/installation/ 

2. Run the following line, which allows the Makefile to install the necessary dependencies: 
```
 make install
``` 

3. Run the following line, to run both the virtual environment and the program

```
make run <my/file/path>
``` 

### Windows 
---

1. Install pip 
    -  https://pip.pypa.io/en/stable/installation/ 

2. Open Powershell and enter the following: 
 ```
  % pip install scapy 
 ```

3. Install Npcap from the website
    - https://npcap.com/ 






## How to launch GUI 

1. Open terminal (Mac) or git bash (windows) and enter the following

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
% cd ../fakemote
% python3 fakemote.py  <path/to/config/file>
```

Fake MOTE should be running at this point in the corresponding terminal. 

## Command Line Functions 

> will update more on this documentation once the data replay feature is fully implemented 


1. **Flagging pins** - Flags a single pin based on data points
```
% fs  <mote_number> <pin number> <data point>
```


2. **Exiting out the program** - exits out of program, disconnecting motes
```
% e 
```
3. **Disconnecting a Mote**- Disconnects a single MOTE
```
d <mote_number>
``` 
4. **Re-connecting/Adding a Mote** - Reconnects and enables all mote previously running MOTEfeatures

```
a <mote_number>
```



## CSV Logging 

There exists a csv log for each component of the mote they are located in logs/, each log will be stored in a folder with a name formatted as **year-month-date-hour-minute-second** of when you first called the ```s``` function. 

In this folder you will find the following CSV Files

1. **mote_config.csv**- stores information of the generated motes from the configuration file. The format is as follows: mote number and the IP. 

2. **sensors.csv** - stores all sensors data from the GUI. The format is as follows: mote number, human name, pin number, and interface. 

3. **actuators.csv** - stores all actuators data received from GUI. The format is as follows: mote number, human name, pin number, interface, and state. 
    > - Even after fakemote is connected to GUI, there will be no entries unless the actuator state is changed from its original configuration. 
     > - There will be repetition in entries, representing 
     each time an actuator state is changed
 
   
4. **flags.csv** - stores all sensors and the data which they are flagged with. The format is as follows: mote number, human name, pin number, and the flagged value. 
    > - Until a pin is flagged, nothing will appear in the csv file. 
    >  - There will be repetition in entries if a pin's flagged value is changed multiple times. 

      







