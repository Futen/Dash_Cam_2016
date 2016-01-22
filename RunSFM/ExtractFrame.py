#! /usr/bin/env python

import subprocess
import sys
sys.path.append('/home/Futen/Dash_Cam_2016/')
import SystemParameter as SP
from multiprocessing import Pool

TYPE = 'pos' # I should choose neg or pos

file_name = ''
if TYPE == 'pos':
    file_name = '/home/Futen/Dash_Cam_2016/DataList/positive_check.txt'
elif TYPE == 'neg':
    file_name = '/home/Futen/Dash_Cam_2016/DataList/negative_check.txt'
else:
    print 'Type error'
    exit()

f = open(file_name, 'r')
for line in f:
    line = line.split('\t')
    v_name = line[0].split('.')[0]
    info = SP.GetPath(v_name,TYPE)
    print info
