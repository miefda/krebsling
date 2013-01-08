#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_gps import GPS
from settings import HOST, PORT, GPSUID, point1
from haversine import getDistance, getBearing


# Callback function for coordinates
def cb_coordinates(latitude, ns, longitude, ew, pdop, hdop, vdop, epe):
    fix, NULL, NULL = gps.get_status()
    course, speed = gps.get_motion()
    if fix == 3 or fix == 2:
        latitude = latitude/1000000.0
        longitude = longitude/1000000.0

        if ns == "S":
            latitude = 0 - latitude
        if ew == "W":
            longitude = 0 - longitude

        distance = getDistance(latitude, longitude, point1[0], point1[1])
        bearing = getBearing(latitude, longitude, point1[0], point1[1])
        bearing = (bearing + 360) % 360
        #course = (course - 180)
        course = course/100.0000
        speed = speed/100.0
        bcdiff = (bearing - course)
        #print('Latitude: ' + str(latitude) + '° ' + ns)
        #print('Longitude: ' + str(longitude) + '° ' + ew)
        #print('Course: ' + str(course) + ' speed: ' + str(speed) )
        print("Distace: " + str(distance) )
        print("Course: " + str(course))
        print("Bearing " + str(bearing) )
        print("bc diff: " + str(bcdiff))
        #return distance, bearing, course, speed, bcdiff


    else:
        print('STOP! ' + str(fix) + " " + str(type(fix)))

def cb_status(fix, sat, use):
    if fix == 3 or fix == 2:
        enable = True
    else:
        print("stop!!!1")



if __name__ == "__main__":
    ipcon = IPConnection(HOST, PORT) # Create ip connection to brickd

    gps = GPS(GPSUID) # Create device object
    ipcon.add_device(gps) # Add device to ip connection
    # Don't use device before it is added to a connection

    # Set Period for coordinates callback to 1s (1000ms)
    # Note: The callback is only called every second if the 
    #       coordinates have changed since the last call!
    gps.set_coordinates_callback_period(500)
    gps.set_status_callback_period(50)
    # Register current callback to function cb_current
    gps.register_callback(gps.CALLBACK_COORDINATES, cb_coordinates)
    gps.register_callback(gps.CALLBACK_STATUS, cb_status)
    








    raw_input('Press key to exit\n') # Use input() in Python 3
    ipcon.destroy()