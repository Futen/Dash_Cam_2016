import sys
sys.path.append('/home/Futen/Dash_Cam_2016')
import ExpList as EL
import subprocess
import os
import SendEmail

TYPE = 'pos'

def WriteList(DIR,LIST,NAME='frame_lst.txt'):
    f = open(DIR + '/'  + NAME, 'w')
    for one in LIST:
        f.write(one + '\n')
    f.close()
if __name__ == '__main__':
    lst = EL.GetList(TYPE)
    do_lst = []
    for one in lst:
        v_name = one[0]
        info = EL.GetVideoInfo(v_name, TYPE)
        if info['state']['extractsift'] == 'no':
        #if True:
            do_lst.append(one)
            print v_name
            frame_dir = info['frame_path']
            pano_dir = info['pano_cut_path']
            frame_lst = [x for x in sorted(os.listdir(frame_dir)) if x.endswith('.jpg')]
            pano_lst = [x for x in sorted(os.listdir(pano_dir)) if x.endswith('.jpg')]
            WriteList(DIR=frame_dir, LIST=frame_lst)
            WriteList(DIR=pano_dir, LIST=pano_lst)
            subprocess.call('mkdir -p %s'%info['frame_sift_path'], shell=True)
            subprocess.call('mkdir -p %s'%info['pano_sift_path'], shell=True)
            command = 'VisualSFM siftgpu %s/frame_lst.txt'%frame_dir
            subprocess.call(command, shell=True)
            command = 'VisualSFM siftgpu %s/frame_lst.txt'%pano_dir
            subprocess.call(command, shell=True)
            frame_sift_lst = [x for x in sorted(os.listdir(frame_dir)) if x.endswith('.sift')]
            pano_sift_lst = [x for x in sorted(os.listdir(pano_dir)) if x.endswith('.sift')]
            subprocess.call('mv %s/*.sift %s'%(frame_dir, info['frame_sift_path']), shell=True)
            subprocess.call('rm %s/frame_lst.txt'%frame_dir, shell=True)
            subprocess.call('mv %s/*.sift %s'%(pano_dir, info['pano_sift_path']), shell=True)
            subprocess.call('rm %s/frame_lst.txt'%pano_dir, shell=True)
            WriteList(DIR = info['pano_path'], LIST = frame_sift_lst, NAME = 'frame_sift_lst.txt')
            WriteList(DIR = info['pano_path'], LIST = pano_sift_lst, NAME = 'pano_sift_lst.txt')
            #break
    #print len(do_lst)
    SendEmail.SendEmail(To = 'tdk356ubuntu@gmail.com')
