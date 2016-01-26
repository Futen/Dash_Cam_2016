import sys
sys.path.append('Library')
import numpy as np
import ReadSift
import cv2
from scipy import spatial
import time

#############################################################################
def bf_match(img1,img2):
    """Given two images, returns the matches"""
    matcher = cv2.BFMatcher(cv2.NORM_L2)

    (kp1,desc1) = ReadSift.ReadSift("%s.sift" % img1) # query image
    (kp2,desc2) = ReadSift.ReadSift("%s.sift" % img2) # train image

    raw_matches = matcher.knnMatch(desc1, trainDescriptors = desc2, k = 2)
    kp_pairs = filter_matches(kp1, kp2, raw_matches)

    return kp_pairs

def Kuan_bf_match_images(kp1,desc1,kp2,desc2,mask):
    """Given two images, returns the matches"""
    matcher = cv2.BFMatcher(cv2.NORM_L2)

    raw_matches = matcher.knnMatch(desc1, trainDescriptors = desc2, k = 2, mask=mask)
    kp_pairs = filter_matches(kp1, kp2, raw_matches)

    return kp_pairs


def flann_match(img1, img2):
    """Given two images, returns the matches"""

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params,search_params)
    (kp1,desc1) = ReadSift.ReadSift("%s.sift" % img1) # query image
    (kp2,desc2) = ReadSift.ReadSift("%s.sift" % img2) # train image


    raw_matches = flann.knnMatch(np.array(desc1,np.float32),np.array(desc2,np.float32), k = 2)
    kp_pairs = filter_matches(kp1, kp2, raw_matches)
    return kp_pairs


def filter_matches(kp1, kp2, matches, ratio = 0.75):
    mkp1, mkp2 = [], []
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            m = m[0]
            mkp1.append( kp1[m.queryIdx] )
            mkp2.append( kp2[m.trainIdx] )
    kp_pairs = zip(mkp1, mkp2)
    return kp_pairs


def kuanting_match_images(img1, img2, xratio, yratio, radius):
    """Given two images, returns the matches"""

    (kp1,desc1) = ReadSift.ReadSift("%s.sift" % img1) # frame: train img
    (kp2,desc2) = ReadSift.ReadSift("%s.sift" % img2) # pano: query img


    tree = spatial.KDTree( kp1[:,:2] ) # using frame img to construct kdtree

    ### test
    i = 0
    kp2[:,0] = kp2[:,0]*xratio
    kp2[:,1] = kp2[:,1]*yratio

    start_time = time.time()
    raw_matches = []
    matcher = cv2.BFMatcher(cv2.NORM_L2)
#    for i in xrange(0,kp2.shape[0]):
    for i in [0]:
        near_index = tree.query_ball_point( kp2[i,:2], radius) #test
        #print near_index,len(near_index)

        raw_matches_tmp = matcher.knnMatch(desc2[np.newaxis,i,:], trainDescriptors = desc1[near_index,:], k = 2)
        raw_matches.append(raw_matches_tmp[0])
        #print  raw_matches[0][0].distance,raw_matches[0][1].distance
#    return raw_matches
    kp_pairs = filter_matches(kp1, kp2, raw_matches)
    print raw_matches
    print("mymetod: --- %s seconds ---" % (time.time() - start_time))

    return kp_pairs

