import sys
sys.path.append('..')
sys.path.append('../Google_Library')
import ExpList as EL
import os
import numpy as np
import SendEmail
import GoogleSV
from multiprocessing import Pool
TYPE = 'pos'

output_dic = {}
def GetMatchResult(video_comprass):
    v_name = video_comprass[0][0]
    source = video_comprass[0][1]
    seg_type = video_comprass[1]
    info = EL.GetVideoInfo(v_name, seg_type)
    results = np.load('%s/fisher_results.npy'%info['pano_path'])
    score = np.load('%s/results_fundM.npy'%info['pano_path'])
    f = open('%s/match_score.txt'%info['pano_path'],'w')
    frame_sift_lst = [x for x in sorted(os.listdir(info['frame_sift_path'])) if x.endswith('.sift')]
    pano_sift_lst = [x for x in sorted(os.listdir(info['pano_sift_path'])) if x.endswith('.sift')]

    for index, name in enumerate(frame_sift_lst):
        match_score = score[index]
        scoreSort = match_score.argsort()
        best_index = results[index][scoreSort[-1]]
        best_pano_name = pano_sift_lst[best_index]

        best_score = match_score[scoreSort[-1]]
        best_pano_name = best_pano_name.split('.')[0] + '.jpg'
        frame_name = name.split('.')[0] + '.jpg'
        s = '%s\t%s\t%d\n'%(frame_name, best_pano_name, best_score)
        f.write(s)
    f.close()
def GetBestResult(video_comprass):
    global output_dic
    v_name = video_comprass[0][0]
    source = video_comprass[0][1]
    seg_type = video_comprass[1]
    info = EL.GetVideoInfo(v_name, seg_type)
    f = open('%s/match_score.txt'%info['pano_path'],'r')
    dic = {}
    for line in f:
        line = line[0:-1].split('\t')
        frame_name = line[0]
        pano_name = line[1]
        try:
            dic[pano_name] += 1
        except:
            dic[pano_name] = 1
    f.close()
    max_time = 0
    max_pano = ''
    for i,j in enumerate(dic):
        if dic[j] > max_time:
            max_time = dic[j]
            max_pano = j
    pano_id = max_pano[5:27]
    location = GoogleSV.getLocationbyID(pano_id)
    #print '%s %d %s %s'%(max_pano,max_time, location[0], location[1])
    data = dict({'pano':max_pano, 'time':max_time, 'lat':location[0], 'lon':location[1]})
    output_dic[v_name] = data
    print data

if __name__ == '__main__':
    test = [('000501','GGGG'),'pos']
    GetMatchResult(test)
    GetBestResult(test)
    '''
    lst = EL.GetList(TYPE)
    lst = EL.ArgumentComprass(lst, TYPE)
    pool = Pool(processes = 4)
    pool.map(GetMatchResult, lst)
    if TYPE == 'pos':
        f_name = 'pos_final.txt'
    elif TYPE == 'neg':
        f_name = 'neg_final.txt'
    f = open(f_name, 'w')
    for one in lst:
        v_name = one[0][0]
        s = '%s\t%s\t%d\t%s\t%s\n'%(v_name, output_dic[v_name]['pano'], output_dic[v_name]['time'], output_dic[v_name]['lat'], output_dic[v_name]['lon'])
        f.write(s)
    f.close()
    '''
