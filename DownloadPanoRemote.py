#! /usr/bin/env python

import sys
sys.path.append('/home/Futen/Dash_Cam_2016/')
sys.path.append('/home/Futen/Dash_Cam_2016/DownloadPano')
import os
import subprocess
import SystemParameter as SP
import libRundownload
from multiprocessing import Pool
##
TYPE = 'NegSource'
def GetList(f_name):
    f = open(f_name, 'r')
    lst = []
    for line in f:
        lst.append(line[0:-1])
    f.close()
    return lst
def Download(v_name_comprass):
    v_name = v_name_comprass[0]
    seg_type = v_name_comprass[1]
    info = SP.GetPath(v_name, seg_type)
    subprocess.call('mkdir -p %s'%info['pano_cut_path'], shell=True)
    subprocess.call('mkdir -p %s'%info['pano_uncut_path'], shell=True)
    command = 'sshpass -p pig6983152 scp Faraday:%s/pano_lst_finish.txt %s'%(info['pano_path'], info['pano_path'])
    subprocess.call(command, shell=True)
    libRundownload.DownloadPano(v_name_comprass)
    command = 'sshpass -p pig6983152 scp %s/pano_lst_precise.txt %s/pano_cut_lst.txt Faraday:%s'%(
                info['pano_path'],
                info['pano_path'],
                info['pano_path'],
    #subprocess.call(command, shell=True)
    print command
    command = 'sshpass -p pig6983152 scp %s/* Faraday:%s'%(info['pano_cut_path'], info['pano_cut_path'])
    #subprocess.call(command, shell=True)
    print command

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) != 2 or not(os.path.isfile(argv[1])):
        print 'Argument error'
        exit()
    lst = GetList(argv[1])
    lst = libRundownload.ArgumentComprass(lst, TYPE)
    tmp = ()
    #pool = Pool(processes = 1)
    #pool.map(Download, lst)
