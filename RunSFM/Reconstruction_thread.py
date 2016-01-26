#! /usr/bin/env python

import subprocess
import os
import sys
sys.path.append('/home/Futen/Dash_Cam_2016/')
import SystemParameter as SP
from multiprocessing import Pool

TYPE = 'pos' # I should choose neg or pos

def Reconstruct(v_name):
    info = SP.GetPath(v_name,TYPE)
    command = '%s/reconstruct %s'%(SP.OPENSFM_PATH, info['video_path'])
    print command
    #subprocess.call(command, shell=True)
    #print info


if __name__ == '__main__':
    pool = Pool(processes = 1)
    v_lst = SP.GetVideoList(TYPE)
    pool.map(Reconstruct, v_lst)
