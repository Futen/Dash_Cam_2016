import sys
sys.path.append('/home/Futen/Dash_Cam_2016/')
sys.path.append('/home/Futen/Dash_Cam_2016/DownloadPano')
sys.path.append('/home/Futen/Dash_Cam_2016/Google_Library')
import ExpList as EL
from multiprocessing import Pool
import SendEmail
import os
import libRundownload
import ReadSift
import numpy as np
from yael import ynumpy

TYPE = 'pos'

def Fisher(video_comprass): # [(v_name,source), seg_type]
    v_name = video_comprass[0][0]
    source = video_comprass[0][1]
    seg_type = video_comprass[1]
    info = EL.GetVideoInfo(v_name, seg_type)
    print info    
    frame_sift_lst = [x for x in sorted(os.listdir(info['frame_sift_path'])) if x.endswith('.sift')]
    pano_sift_lst = [x for x in sorted(os.listdir(info['pano_sift_path'])) if x.endswith('.sift')]
    
    frame_desc = []
    for one in frame_sift_lst:
        f = info['frame_sift_path'] + '/' + one
        desc = ReadSift.ReadSift(f)[1]
        if desc.size == 0:
            desc = np.zeros((0, 128), dtype = 'uint8')
        frame_desc.append(desc)
    pano_desc = []
    for one in pano_sift_lst:
        f = info['pano_sift_path'] + '/' + one
        desc = ReadSift.ReadSift(f)[1]
        if desc.size == 0:
            desc = np.zeros((0,128), dtype = 'uint8')
        pano_desc.append(desc)
    data = np.load(EL.SP.ROOT_PATH + '/' + 'gmm_2step.npz')
    gmm = (data['a'], data['b'], data['c'])
    mean = data['mean']
    pca_transform = data['pca_transform']

    image_fvs = []
    for image_dec in (frame_desc + pano_desc):
        image_dec = np.dot(image_dec - mean, pca_transform)
        fv = ynumpy.fisher(gmm, image_dec, include = 'mu')
        image_fvs.append(fv)
    image_fvs = np.vstack(image_fvs)
    image_fvs = np.sign(image_fvs) * np.abs(image_fvs) ** 0.5
    norms = np.sqrt(np.sum(image_fvs ** 2, 1))
    image_fvs /= norms.reshape(-1,1)
    print 'fisher_vector:', image_fvs.shape
    image_fvs[np.isnan(image_fvs)] = 100

    frame_fvs = image_fvs[0:len(frame_sift_lst)]
    pano_fvs = image_fvs[len(frame_sift_lst):]

    fvs_dic = {}
    for i,j in enumerate(frame_sift_lst):
        fvs_dic[j] = frame_fvs[i]
    for i,j in enumerate(pano_sift_lst):
        fvs_dic[j] = pano_fvs[i]
    np.save('%s/fvs_dict.npy'%info['pano_path'], fvs_dic)

    results, distances = ynumpy.knn(frame_fvs, pano_fvs, nnn = 15)
    np.save('%s/fisher_results'%info['pano_path'],results)

if __name__ == '__main__':
    pool = Pool(processes = 4)
    lst = EL.GetList(TYPE)
    #Fisher([('000945','gg'), 'pos'])
    lst = libRundownload.ArgumentComprass(lst, TYPE)
    print 'total %d videos'%len(lst)
    gg_lst = []
    for one in lst:
        v_name = one[0][0]
        info = EL.GetVideoInfo(v_name, 'pos')
    
        if info['state']['fisher'] == 'no' and v_name != '000219':
            print v_name
            gg_lst.append(one)
        
        '''
        if len(os.listdir(info['pano_sift_path'])) < 15:
            print v_name
            gg_lst.append(v_name)
        '''
    print len(gg_lst)
    #Fisher([('000219','ff'), 'pos'])
    try:
        pool.map(Fisher, gg_lst)
        SendEmail.SendEmail()
    except:
        SendEmail.SendEmail(Text = 'GGGGGGGG')
