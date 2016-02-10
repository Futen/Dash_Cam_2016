#! /usr/bin/env python

import sys
sys.path.append('/home/Futen/Dash_Cam_2016')
from geopy.distance import VincentyDistance
import numpy as np
import PanoProcess
import SystemParameter

step_latlon = 0.0009
step_ten_meter = step_latlon/2 # step_latlon/10-->every ten meter
RADIUS = SystemParameter.RADIUS #km

def GetCircleBound(center): # lat, lon
    circle = []
    last_val = 0
    shutdown = 0
    add_val = step_latlon
    difference = 0
    while shutdown == 0: # lon
        dis = VincentyDistance(center, (center[0], center[1]+add_val)).km
        if dis >= RADIUS:
            difference = add_val
            shutdown = 1
        add_val += step_latlon
    bound_lat = (center[0]-difference, center[0]+difference)
    bound_lon = (center[1]-difference, center[1]+difference)
    bound_lat = np.arange(bound_lat[0], bound_lat[1], step_ten_meter)
    bound_lon = np.arange(bound_lon[0], bound_lon[1], step_ten_meter)
    #print bound_lat 
    #print bound_lon
    for lat in bound_lat:
        for lon in bound_lon:
            if VincentyDistance(center, (lat,lon)).km <= RADIUS:
                latlon = [lat,lon]
                circle.append(latlon)
    circle = np.array(circle)
    return circle

if __name__ == '__main__':
    argv = []
    #print len(sys.argv)-1
    for i in range(1, len(sys.argv)):
        argv.append(float(sys.argv[i]))
    #print VincentyDistance((argv[0], argv[1]), (argv[2], argv[3])).km
    circle = GetCircleBound(argv)
    print len(circle)
    f = open('tmp.txt',"w")
    a = 0
    for i in circle:
        panoid = PanoProcess.GetPanoID(i)
        if panoid != None:
            print a
            f.write(panoid + '\t ' + str(i[0]) + ' ' + str(i[1])  + '\n')
            a+=1
