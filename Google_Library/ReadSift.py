import os
import numpy as np
import cv2
from matplotlib import pyplot as plt
from yael import ynumpy

### given sift files from VSFM =>  XXXX.sift
### output Descriptor Data

def ReadSift(fulPath):
	#fulPath = 'image-001.sift'

	f = open(fulPath, "rb")
	f.seek(8, os.SEEK_SET)

	raw0 = np.fromfile(f, np.int32, 1)
	npoint = raw0[0]

	f.seek(20, os.SEEK_SET)

	## Location Data
	raw1 = np.fromfile(f, np.float32, npoint*5)
	raw1 = np.reshape(raw1,(-1,5))

	## Descriptor Data
	raw2 = np.fromfile(f, np.uint8, npoint*128)
	raw2 = np.reshape(raw2,(-1,128))

	raw3 = np.fromfile(f, np.int32)


	#print npoint, raw1, raw2,raw3.shape,

	return (raw1,raw2)


def CountSift(fulPath):
	#fulPath = 'image-001.sift'

	f = open(fulPath, "rb")
	f.seek(8, os.SEEK_SET)

	raw0 = np.fromfile(f, np.int32, 1)
	npoint = raw0[0]

	f.seek(20, os.SEEK_SET)

	## Location Data
	raw1 = np.fromfile(f, np.float32, npoint*5)

	## Descriptor Data
	raw2 = np.fromfile(f, np.uint8, npoint*128)
	raw3 = np.fromfile(f, np.int32)


	#print npoint, raw1, raw2,raw3.shape,

	return npoint


