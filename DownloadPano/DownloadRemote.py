#! /usr/bin/env python

import sys
sys.path.append('/home/Futen/Dash_Cam_2016/')
import os
import subprocess
import SystemParameter as SP
import libRundownload
from multiprocessing import Pool

def GetList(f_name):
    f = open(f_name, 'r')
    lst = []
    for line in f:
        lst.append(line[0:-1])
    f.close()
    return lst

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) != 2 or not(os.path.isfile(argv[1])):
        print 'Argument error'
        return
    lst = GetList(argv[1])
    print lst
