Documentation for Mirage 

Purpose and Design Philosophy: 

Mirage is a command line python script which is meant to interact with the the Web-Based Graphic User Interaface (Web GUI) 
by sending data through UDP packages, ultimately mimicking data being sent to the flight computer. 

The design philosophy behind the following program is the act of "hoodle", or
also known as the hardware out of the loop testing. Given the spacial limitations fo the lap, we cannot always 
have the MOTE lying out at all times. By creating a program which is remotely accessiable at all times, 
this will save time with 1) setting up to test firmware and software and 2)allow for flexibility with remote work

Used Libraries
1) Click (8.1.x) - python package for creating command line interfaces 
    https://click.palletsprojects.com/en/8.1.x/
2) 

How to set up virtual enviorment 
Reference: https://click.palletsprojects.com/en/8.1.x/quickstart/
1) create virtual enviorment (python3 -m venv .venv) 
2) activate the actual enviorment (. .venv/bin/activate)
3) if you're down with the virtual enviorment use the following command (deactive)