#! /usr/bin/env python

import sys
sys.path.append('/home/Futen/Dash_Cam')
import SystemParameter
import GetCircleBound
import PanoProcess
import subprocess
import numpy as np


info_path = SystemParameter.VIDEO_INFO_PATH
video_file = open('%s/video_to_process.txt'%info_path, 'r')

