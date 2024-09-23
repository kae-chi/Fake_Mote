
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
