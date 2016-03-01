import ExpList as EL
import numpy as np
import sys

if __name__ == '__main__':
    argv = sys.argv
    if len(argv)!=3:
        print 'argv error'
        exit()
    info = EL.GetVideoInfo(argv[1],argv[2])
    a = np.load('%s/results_fundM.npy'%info['pano_path'])
    print a
