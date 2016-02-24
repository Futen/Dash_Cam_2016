#! /usr/bin/env python

import sys
sys.path.append('/home/Futen/Dash_Cam_2016')
import SystemParameter as SP
import PanoProcess
import subprocess
import os
import GetPanoByID
import time

def ArgumentComprass(v_lst, seg_type):
    out = []
    for one in v_lst:
        tmp = (one, seg_type)
        out.append(tmp)
    return out
def DownloadPano(v_name_comprass):
    start = time.time()
    v_name = v_name_comprass[0]
    seg_type = v_name_comprass[1]
    info = SP.GetPath(v_name, seg_type)
    if info['state']['panolist'] == 'no':
        return 
    print info
    if os.path.isfile('%s/pano_lst_precise.txt'%info['pano_path']):
        return
    #subprocess.call('rm %s/*'%info['pano_uncut_path'], shell=True)
    #subprocess.call('rm %s/*'%info['pano_cut_path'],shell=True)
    pano_file = open(info['pano_path']+'/pano_lst_finish.txt','r')
    pano_out_file = open(info['pano_path']+'/pano_lst_tmp.txt','w')
    finish_lst = []
    for line in pano_file:
        line = line.split('\t')
        ID = line[0]
        location = PanoProcess.GoogleSV.getLocationbyID(ID)
        #print location
        if ID in finish_lst or os.path.isfile(info['pano_cut_path'] + '/pano_' + ID + '_0.jpg'):
            if os.path.isfile(info['pano_cut_path'] + '/pano_' + ID + '_0.jpg'):
                if not ID in finish_lst:
                    finish_lst.append(ID)
                s = 'pano_' + ID + '.jpg' + '\t' + location[0] + '\t' + location[1] + '\n'
                pano_out_file.write(s)
            continue
        check = GetPanoByID.GetPanoByID(ID, info['pano_cut_path'])
        if check == True:
            s = 'pano_' + ID + '.jpg' + '\t' + location[0] + '\t' + location[1] + '\n'
            pano_out_file.write(s)
            finish_lst.append(ID)
        else:
            print 'error %s'%ID
            error_file = open('%s/download_error_lst.txt'%info['pano_path'],'a')
            #subprocess.call('rm -r */', shell=True)
            if location != None:
                error_file.write('%s\t%s\t%s\n'%(ID,location[0], location[1]))
            error_file.close()
            continue
        #time.sleep(1)
        
    pano_file.close()
    pano_out_file.close()
    subprocess.call('mv %s %s'%(info['pano_path']+'/pano_lst_tmp.txt', info['pano_path']+'/pano_lst_precise.txt'),shell=True)

    pano_cut_lst = open(info['pano_path'] + '/pano_cut_lst.txt','w')
    cut_lst = os.listdir(info['pano_cut_path'])
    cut_lst.sort()
    for img in cut_lst:
        img = img + '\n'
        pano_cut_lst.write(img)
    pano_cut_lst.close()
    total_time = time.time() - start
    print '%s Consume %f minutes'%(v_name, total_time/60)
    return 
