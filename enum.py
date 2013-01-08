#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# this one creates an array of connected devices called dev
# and acts as enum in standalone mode 

from tinkerforge.ip_connection import IPConnection
from settings import HOST, PORT

dev = []
def cb_enumerate(uid, name, stack_id, is_new):
    
    if is_new:
        print("New device:")
        dev.append([name, uid, stack_id])
    else:
        print("Removed device:")
        for i in dev:
            if i[1] == uid:
                dev.remove(i)
    if __name__ == "__main__":
        print(" Name:     " + name)
        print(" UID:      " + uid)
        print(" Stack ID: " + str(stack_id))
        print("")
     
if __name__ == "__main__":
    ipcon = IPConnection(HOST, PORT) # Create IP connection to brickd
    ipcon.enumerate(cb_enumerate) # Enumerate Bricks and Bricklets

    raw_input('Press key to exit\n') # Use input() in Python 3
    ipcon.destroy()