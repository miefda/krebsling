#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_gps import GPS
from settings import HOST, PORT, GPSUID
from array import array


ipcon = IPConnection(HOST, PORT) # Create ip connection to brickd

gps = GPS(GPSUID) # Create device object
ipcon.add_device(gps) # Add device to ip connection
coords = gps.get_coordinates()
lon = coords.longitude/1000000.0
lat = coords.latitude/1000000.0
print('Latitude: ' + str(lat) + '° ' + coords.ns)
print('Longitude: ' + str(lon/1000000.0) + '° ' + coords.ew)
if coords.ns == "S":
    lat = 0 - lat
if coords.ew == "W":
    lon = 0 - lon
arr = array(lat, lon)


try:
    # This will create a new file or **overwrite an existing file**.
    f = open("location.txt", "w")
    try:
        arr.tofile(f)
    finally:
        f.close()
except IOError:
    pass



raw_input('saved.... \n Press key to exit\n') # Use input() in Python 3
ipcon.destroy()