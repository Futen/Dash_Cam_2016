import sys
sys.path.append('../')
import subprocess
import SystemParameter as SP
import os

f = open('../DataList/positive_check.txt','r')
v_lst = []
lst = SP.GetNegSourceList()
for line in f:
    line = line[0:-1].split('\t')
    v_name = line[4]
    name = line[0].split('.')[0]
    info = SP.GetPath(name,'pos')
    info_source = SP.GetNegSourcePath(v_name)
    if v_name in lst and info['state']['panodownload'] == 'yes' and info_source['state']['panodownload'] == 'no':
        print '%s %s'%(name, v_name)
        source_info = SP.GetNegSourcePath(v_name)
        command = 'cp %s/*.txt %s/'%(info['pano_path'], source_info['pano_path'])
        print command
        subprocess.call(command, shell=True)
        command = 'cp %s/*.jpg %s/'%(info['pano_uncut_path'], source_info['pano_uncut_path'])
        print command
        subprocess.call(command, shell=True)
        command = 'cp %s/*.jpg %s/'%(info['pano_cut_path'], source_info['pano_cut_path'])
        print command
        subprocess.call(command, shell=True)
f.close()
