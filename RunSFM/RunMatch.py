#! /usr/bin/env python

import sys
import os
import subprocess
sys.path.append('/home/Futen/Dash_Cam_2016/')
import SystemParameter as SP

TYPE = 'neg' # I should choose neg or pos
# average 0.61 minute for one video
video_lst = SP.GetVideoList(TYPE) # get video list
video_lst.sort()
#print video_lst
for video in video_lst:
    info =  SP.GetPath(video, TYPE)
    #print info
    command = 'cp %s/config.yaml %s'%(SP.ROOT_PATH, info['video_path'])
    #print command
    subprocess.call(command, shell=True)
    command = '%s/run_match %s'%(SP.OPENSFM_PATH, info['video_path'])
    subprocess.call(command, shell=True)
