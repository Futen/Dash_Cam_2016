import sys

sys.path.append('Library')
import numpy as np
import ReadSift
import cv2


#############################################################################
def feature_match(qname,tname): # query,train imgs


    (q_meta,q_des) = ReadSift.ReadSift("gmm_video/%s.sift" % qname)
    (t_meta,t_des) = ReadSift.ReadSift("gmm_pano/%s.sift" % tname)


    #img1 = cv2.imread('gmm_video/%s.jpg' % qname,0)  #queryimage # left image
    #img2 = cv2.imread('gmm_pano/%s.jpg' % tname ,0) #trainimage # right image

    #sift = cv2.SIFT()

    # find the keypoints and descriptors with SIFT
    #kp1, des1 = sift.detectAndCompute(img1,None)
    #kp2, des2 = sift.detectAndCompute(img2,None)
    
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(np.array(q_des,np.float32),np.array(t_des,np.float32),k=2)
    

    #bf = cv2.BFMatcher()
    #matches = bf.knnMatch(q_des,t_des,k=2)

    good = []
    q_pts = []
    t_pts = []
    #pts1 = []
    #pts2 = []

    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.8*n.distance:
            good.append(m)
            #pts2.append(kp2[m.trainIdx].pt)
            #pts1.append(kp1[m.queryIdx].pt)
            t_pts.append((t_meta[m.trainIdx][0],t_meta[m.trainIdx][1]))
            q_pts.append((q_meta[m.queryIdx][0],q_meta[m.queryIdx][1]))


    q_pts = np.float32(q_pts)
    t_pts = np.float32(t_pts)
    F, mask = cv2.findFundamentalMat(q_pts,t_pts,cv2.FM_RANSAC,20)
    #pts1 = np.float32(pts1)
    #pts2 = np.float32(pts2)
    #F, mask = cv2.findFundamentalMat(pts1,pts2,cv2.FM_RANSAC)


    # We select only inlier points
    q_pts = q_pts[mask.ravel()==1]
    t_pts = t_pts[mask.ravel()==1]

    #pts1 = pts1[mask.ravel()==1]
    #pts2 = pts2[mask.ravel()==1]

#    print len(matches), len(good), len(q_pts)

#    return len(q_pts)
    return (q_pts,t_pts)


