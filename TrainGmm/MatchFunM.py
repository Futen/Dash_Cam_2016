import sys
sys.path.append('../')
sys.path.append('../Google_Library')
import os
import subprocess
import ReadSift
import lib_SIFTmatch
import cv2
import numpy as np
import ExpList as EL
import SendEmail
from multiprocessing import Pool

TYPE = 'pos'
def MatchFunM(video_comprass):
    v_name = video_comprass[0][0]
    source = video_comprass[0][1]
    seg_type = video_comprass[1]
    info = EL.GetVideoInfo(v_name, seg_type)
    print info
    results = np.load('%s/fisher_results.npy'%info['pano_path'])
    frame_sift_lst = [x for x in sorted(os.listdir('%s/'%info['frame_sift_path'])) if x.endswith('.sift')]
    pano_sift_lst = [x for x in sorted(os.listdir('%s/'%info['pano_sift_path'])) if x.endswith('.sift')]
    MM = []
    for index, name in enumerate(frame_sift_lst):
        Mi = []
        frame_short_name = name.split('.')[0]
        for i in range(0,results.shape[1]):
            pano_name = pano_sift_lst[results[index, i]]
            pano_short_name = pano_name.split('.')[0]
            kp_pairs = lib_SIFTmatch.flann_match('%s/%s'%(info['frame_sift_path'],frame_short_name),
                                                 '%s/%s'%(info['pano_sift_path'],pano_short_name))
            (mkp1, mkp2) = zip(*kp_pairs)
            mkp1_pts = [ (x[0],x[1]) for x in mkp1 ]
            mkp2_pts = [ (x[0],x[1]) for x in mkp2 ]
            mkp1_pts = np.float32(mkp1_pts)
            mkp2_pts = np.float32(mkp2_pts)
            F, mask = cv2.findFundamentalMat(mkp1_pts,mkp2_pts,cv2.FM_RANSAC)
            q_pts = mkp1_pts[mask.ravel()==1]
            t_pts = mkp2_pts[mask.ravel()==1]
            Mi.append(len(q_pts))
        MM.append(Mi)
    np.save('%s/results_fundM'%info['pano_path'],MM)

if __name__ == '__main__':
    lst = EL.GetList(TYPE)
    lst = EL.ArgumentComprass(lst, TYPE)
    do_lst = []
    for one in lst:
        v_name = one[0][0]
        info = EL.GetVideoInfo(v_name, TYPE)
        if info['state']['fisher'] == 'yes':
            do_lst.append(one)
    print len(do_lst)
    MatchFunM(do_lst[0])
    #pool = Pool(processes = 10)
    #pool.map(MatchFunM, do_lst)




