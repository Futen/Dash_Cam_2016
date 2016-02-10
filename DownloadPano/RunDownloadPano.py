#! /usr/bin/env python

import sys
sys.path.append('/home/Futen/Dash_Cam_2016')
import SystemParameter as SP
import GetCircleBound
import PanoProcess
import subprocess
import numpy as np
from multiprocessing import Pool

TYPE = 'pos'

def Download(v_name):
    info = SP.GetPath(v_name, TYPE)
    if info['state']['panolist'] == 'no':
        return 
    print info
    pano_file = open(info['pano_path']+'/pano_lst_finish.txt','r')
    pano_out_file = open(info['pano_path']+'/pano_lst_tmp.txt','w')
    for line in pano_file:
        line = line.split('\t')
        ID = line [0]
        location = PanoProcess.GoogleSV.getLocationbyID(ID)
        #print location
        PanoProcess.GetPanoByID(ID, 'tmp/')
        name = 'tmp/pano_' + ID + '.jpg'
        PanoProcess.CutPano(name, 'tmp/cut/')
        command = 'mv %s %s'%(name, info['pano_uncut_path'])
        subprocess.call(command, shell=True)
        command = 'mv tmp/cut/*.jpg %s'%info['pano_cut_path']
        subprocess.call(command, shell=True)
        #print location
        s = 'pano_' + ID + '.jpg' + '\t' + location[0] + '\t' + location[1] + '\n'
        pano_out_file.write(s)
    pano_file.close()
    pano_out_file.close()
    subprocess.call('mv %s %s'%(info['pano_path']+'/pano_lst_tmp.txt', info['pano_path']+'/pano_lst_precise.txt'),shell=True)
    return 

if __name__ == '__main__':
    #poiol = Pool(processes = 12)
    lst = SP.GetVideoList(TYPE)
    Download(lst[-1])
    #pool.map(Download, lst)
