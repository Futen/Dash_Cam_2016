import sys
sys.path.append('../')
sys.path.append('../Google_Library')
import ExpList as EL
import numpy as np
from yael import ynumpy
import ReadSift
import os
import subprocess

def GetList(file_name):
    if not os.path.isfile(file_name) :
        print 'file error'
        print file_name
        exit()
    lst = []
    f = open(file_name, 'r')
    for line in f:
        lst.append(line[0:-1])
    f.close()
    return lst

if __name__ == '__main__':
    pos_lst = EL.GetList('pos')
    neg_lst = EL.GetList('neg')
    all_dec = []
    
    for one in pos_lst:
        info = EL.GetVideoInfo(one[0], 'pos')
        frame_sift_lst = GetList(info['pano_path'] + '/frame_sift_lst.txt')
        frame_sift_lst = [x for x in os.listdir(info['frame_sift_path']) if x.endswith('.sift')]
        frame_sift_lst = np.random.choice(frame_sift_lst, 10)
        pano_sift_lst = GetList(info['pano_path'] + '/pano_sift_lst.txt')
        pano_sift_lst = [x for x in os.listdir(info['pano_sift_path']) if x.endswith('.sift')]
        pano_sift_lst = np.random.choice(pano_sift_lst, 30)
        for frame_sift in frame_sift_lst:
            (loc, des) = ReadSift.ReadSift(info['frame_sift_path'] + '/' + frame_sift)
            if des.size == 0: 
                des = np.zeros((0, 128), dtype = 'uint8')
            all_dec.append(des)
        for pano_sift in pano_sift_lst:
            (loc, des) = ReadSift.ReadSift(info['pano_sift_path'] + '/' + pano_sift)
            if des.size == 0:
                des = np.zeros((0, 128), dtype = 'uint8')
            all_dec.append(des)
    
    for one in neg_lst:
        info = EL.GetVideoInfo(one[0], 'neg')
        frame_sift_lst = GetList(info['pano_path'] + '/frame_sift_lst.txt')
        frame_sift_lst = [x for x in os.listdir(info['frame_sift_path']) if x.endswith('.sift')]
        frame_sift_lst = np.random.choice(frame_sift_lst, 10)
        pano_sift_lst = GetList(info['pano_path'] + '/pano_sift_lst.txt')
        pano_sift_lst = [x for x in os.listdir(info['pano_sift_path']) if x.endswith('.sift')]
        pano_sift_lst = np.random.choice(pano_sift_lst, 30)
        for frame_sift in frame_sift_lst:
            (loc, des) = ReadSift.ReadSift(info['frame_sift_path'] + '/' + frame_sift)
            if des.size == 0: 
                des = np.zeros((0, 128), dtype = 'uint8')
            all_dec.append(des)
        for pano_sift in pano_sift_lst:
            (loc, des) = ReadSift.ReadSift(info['pano_sift_path'] + '/' + pano_sift)
            if des.size == 0:
                des = np.zeros((0, 128), dtype = 'uint8')
            all_dec.append(des)
    all_desc = np.vstack(all_dec)
    print np.shape(all_desc)
    k = 256
    n_sample = k*6000
    sample_indices = np.random.choice(all_desc.shape[0], n_sample)
    sample = all_desc[sample_indices]
    sample = sample.astype('float32')
    print sample.shape
    mean = sample.mean(axis = 0)
    sample = sample - mean
    cov = np.dot(sample.T, sample)
    eigvals, eigvecs = np.linalg.eig(cov)
    perm = eigvals.argsort()
    pca_transform = eigvecs[:, perm[64:128]]
    sample = np.dot(sample, pca_transform)
    A = np.isfinite(sample)
    gmm = ynumpy.gmm_learn(sample, k)
    np.savez('../gmm_2step',a=gmm[0],b=gmm[1],c=gmm[2],mean=mean,pca_transform=pca_transform)
