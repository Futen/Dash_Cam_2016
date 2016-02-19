#! /usr/bin/env python

import sys
sys.path.append('/home/Futen/Dash_Cam_2016')
import SystemParameter as SP
import subprocess
import os

TYPE = 'pos'

if __name__ == '__main__':
    lst = SP.GetVideoList(TYPE)
    for one in lst:
        info = SP.GetPath(one,TYPE)
        if info['downloadpano'] == 'no':
            s = one + 'no download'
            print s
        else:
            f = open('%s/fra')
