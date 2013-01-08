#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import math
from settings import *




# Convert between degrees-minutes-seconds & decimal degrees
# http://www.movable-type.co.uk/scripts/latlong.html
#
#function currently not in use! and not ready to use!


def geotodegr(lat, ns, lon, ew):
	if ns == "s":
		lat = 0 - lat
	if ew == "w":
		lon = 0 - lon

	return (float()/float(1))+(float()/float(60))+(float()/float(3600))





def getDistance(lat1, lon1, lat2, lon2): 
	dlat = math.radians(lat2 - lat1)
	dlon = math.radians(lon2 - lon1)

	lat1 = math.radians(lat1)
	lat2 = math.radians(lat2)

	a = math.sin(dlat/2) * math.sin(dlat/2) + math.sin(dlon/2) * math.sin(dlon/2) * math.cos(lat1) * math.cos(lat2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = earthRadius * c
	return d



def getBearing(lat1, lon1, lat2, lon2): 
	dlat = math.radians(lat2 - lat1)
	dlon = math.radians(lon2 - lon1)

	lat1 = math.radians(lat1)
	lat2 = math.radians(lat2)

	y =  math.sin(dlon) * math.cos(lat2)
	x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
	brng = math.degrees(math.atan2(y, x))
	return brng









#def navigate(long, ns, lat, ew, course, speed, dlong, dns, dlat, dew)