#! /usr/bin/env python

import os
import subprocess
import sys
sys.path.append('/home/Futen/Dash_Cam/Google_Library')
import GoogleSV
import GetCutout
import math
import cv2
import numpy as np

wfov = 70
wfov = math.radians(wfov)
yaw = 0

def GetPanoID(latlon):
    return GoogleSV.getIDbyloc(lat = latlon[0], lon = latlon[1])

def GetPanoByID(ID, save_dir):
    if not(os.path.isdir(save_dir)):
        subprocess.call('mkdir -p %s'%save_dir, shell=True)
    GoogleSV.getpanobyID(ID,DIR=save_dir)

def CutPano(input_name, output_dir):
    if not(os.path.isdir(output_dir)):
        subprocess.call('mkdir -p %s'%output_dir, shell=True)
    short_name = input_name.split('/')[-1]

    image = cv2.imread(input_name)
    if np.shape(image)!=():
        output_name = output_dir + '/' + short_name.split('.')[0] + '_0'
        GetCutout.cut(image, yaw, wfov, output_name)

        output_name = output_dir + '/' + short_name.split('.')[0] + '_180'
        crop_src_1 = image[:,:3328]
        crop_src_2 = image[:,3328:]
        size = 3328, 6656, 3
        m = np.zeros(size, dtype=np.uint8)
        m[:,3328:]=crop_src_1
        m[:,:3328]=crop_src_2 
        GetCutout.cut(m, yaw, wfov, output_name)

if __name__ == '__main__':
    #name = 'pano_nKASUC9FjDDijTyhtDLAHg.jpg' 
    
    a = GetPanoID((25.0454202604, 121.55787478))
    print a
    GetPanoByID(a, 'tt')
    '''
    GetPanoByID(a, 'tt')
    a = 'tt/pano_' + a + '.jpg'
    
    #a = 'tt/pano_MZH5QF-NIGNwNQquVjRZHg.jpg'
    CutPano(a, 'tt/tt')
    '''
