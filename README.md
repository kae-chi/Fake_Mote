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
% python3 fakemote.py <config file name>
```
Fake MOTE should be running at this point in the corresponding terminal 

> Kae is developing a widget with the QT framework, will continue to update documentation (9/2)
## Networking Things 

### Relevant IP addresses  


**Fake MOTE** 
- Actual IP: 127.0.0.1
- Spoofed IP: 192.168.1.10x  
> x is an arbitrary number for the mote number 

- Port: Randomly generated upon the code compiling 
> This is to avoid conflicting ports and loss of information 

**GUI** 
- IP: 127.0.0.1
- PORT: 5001 
> In the program, the sniffer will be listening on port 8888 (all ports)


## Bit Encoding Schemes 



### 1. Sensors 




```
  ┌───────────────────────────────────────┐
  │ GUI                         Fake MOTE │
  │                                       │
  │  │         configuration           │  │
  │  │ ──────────────────────────────► │  │
  │  │                                 │  │
  │  │             data                │  │
  │  │ ◄───────────────────────────────│  │
  │  │                                 │  │
  │  │                                 │  │
  └───────────────────────────────────────┘
      
        
```


 **Data**
> 5 byte packet sent from MOTE to GUI with data taken from sensor # 
```
  ┌──────┬─────────┐  
  │ [0]  │   [1:4] │  
  │ pin #│   data  │  
  └──────┴─────────┘    
```
                                              

### 2. Actuators   

<pre>
  ┌───────────────────────────────────────┐
  │ GUI                         Fake MOTE │
  │                                       │
  │  │         configuration           │  │
  │  │ ──────────────────────────────► │  │
  │  │                                 │  │
  │  │             data                │  │
  │  │ ◄───────────────────────────────│  │
  │  │                                 │  │
  │  │                                 │  │
  └───────────────────────────────────────┘          

</pre>

 **ACK packet**
>5 byte packet sent from MOTE to GUI to acknowledge configuration

```
  ┌────────────┬─────────┐
  │    [0]     │  [1:4]  │
  │ pin # + 100│  config │
  └────────────┴─────────┘
```

### Configuration Packet 
> 2 byte packet sent from GUI to MOTE, used for both actuator and sensor configurations 
<br />


```
  ┌──────────────────────────────────┐
  │ [0000]    [0000]         [0000]  │
  │ pin #  sensor/actuator interface │
  └──────────────────────────────────┘
```
### Sensory/Actuator Byte
<pre>
0000
</pre>

 1. The first bit is the **actuator/sensor indicator** 
     - 1 - is an **actuator**
     - 0 - is a **sensor**

2. The second bit is the **actuator state** (only applicable to an actuator configuration)
      - 1 - Actuator is on **TRUE** state
      - 0 - Actuator is on **FALSE** state



 In order for the GUI to process any information sent from fake mote, it must be a **5 byte array** in the following order: 
 1. Pin number 
 2. Remaining 4 bytes of relevant information packaged in a struct in **little endian** ordering 
<br />
> Why little endian? That's just how MOTE was made
