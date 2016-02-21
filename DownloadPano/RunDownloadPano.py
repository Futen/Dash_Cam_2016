#! /usr/bin/env python
import sys
sys.path.append('/home/Futen/Dash_Cam_2016/')
import SystemParameter as SP
import libRundownload
from multiprocessing import Pool

TYPE = 'NegSource'
if __name__ == '__main__':
    lst = SP.GetVideoList(TYPE)
    do_lst = []
    for one in lst:
        info = SP.GetPath(one, TYPE)
        if info['state']['panodownload'] == 'no':
            do_lst.append(one)
    pool = Pool(processes = 1)
    do_lst = libRundownload.ArgumentComprass(do_lst, TYPE)
    pool.map(libRundownload.DownloadPano, do_lst)
    #print do_lst
