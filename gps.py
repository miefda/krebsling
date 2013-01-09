#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_gps import GPS
from tinkerforge.brick_servo import Servo
from settings import *
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
        course = course/100.0
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
        if distance > 10.0:
            servo.set_position(steeringsrv, bcdiff * 10)
            servo.set_position(motor, speed)
        else:
            servo.set_position(steeringsrv, mid)
            servo.set_position(motor, stop)


    else:
        print('STOP! ' + str(fix) + " " + str(type(fix)))
        servo.set_position(steeringsrv, mid)
        servo.set_position(motor, stop)

def cb_status(fix, sat, use):
    if fix == 3 or fix == 2:
        enable = True
    else:
        enable = False
        print("stop!!!1")
        servo.set_position(steeringsrv, mid)
        servo.set_position(motor, stop)




if __name__ == "__main__":
    enable = False
    ipcon = IPConnection(HOST, PORT) # Create ip connection to brickd

    gps = GPS(GPSUID) # Create device object
    ipcon.add_device(gps) # Add device to ip connection
    servo = Servo(SERVOUID) # Create device object
    ipcon.add_device(servo) # Add device to IP connection
    # Don't use device before it is added to a connection
    servo.set_degree(motor, -9000, 9000)
    servo.set_pulse_width(motor, 950, 1950)
    servo.set_period(motor, 20000)
    servo.set_acceleration(motor, 7000)
    servo.set_velocity(motor, 0xFFFF) # Full speed
    servo.set_degree(steeringsrv, -3600, 3600)
    servo.set_pulse_width(steeringsrv, 955, 2000)
    servo.set_period(steeringsrv, 20000)
    servo.set_acceleration(steeringsrv, 7000) # Full acceleration 0xFFFF
    servo.set_velocity(steeringsrv, 0xFFFF) # Full speed
    

    servo.set_position(motor, stop)
    servo.set_position(steeringsrv, mid)
    servo.enable(motor)
    servo.enable(steeringsrv)


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