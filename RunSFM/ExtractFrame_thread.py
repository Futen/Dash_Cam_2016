#! /usr/bin/env python

import subprocess
import os
import sys
sys.path.append('/home/Futen/Dash_Cam_2016/')
import SystemParameter as SP
from multiprocessing import Pool

TYPE = 'neg' # I should choose neg or pos

file_name = ''
source_folder = ''
if TYPE == 'pos':
    file_name = '/home/Futen/Dash_Cam_2016/DataList/positive_check.txt'
    source_folder = '/home/Futen/Dash_Cam_2016/Videos_Source_File/pos_video'
elif TYPE == 'neg':
    file_name = '/home/Futen/Dash_Cam_2016/DataList/negative_check.txt'
    source_folder = '/home/Futen/Dash_Cam_2016/Videos_Source_File/neg_video'
else:
    print 'Type error'
    exit()

def Extract(v_name):
    info = SP.GetPath(v_name, TYPE)
    if not(os.path.isdir(info['video_path'])):
        print 'video path error'
        exit()
    source_video = source_folder + '/' + v_name + '.mp4'
    if not(os.path.isfile(source_video)):
        print 'source video path error'
        exit()
    #print source_video
    command = 'ffmpeg -i %s -r 10 -qscale:v 1 %s/'%(source_video, info['frame_path']) + 'image-%5d.jpg'
    subprocess.call(command, shell=True)
    #print command

if __name__ == '__main__':
    pool = Pool(processes = 8)
    f = open(file_name, 'r')
    v_name_lst = []
    for line in f:
        line = line.split('\t')
        v_name = line[0].split('.')[0]
        v_name_lst.append(v_name)
    #print v_name_lst
    pool.map(Extract, v_name_lst)




