import sys
sys.path.append('/home/Futen/Dash_Cam_2016')
sys.path.append('/home/Futen/Dash_Cam_2016/DownloadPano')
import ExpList as EL
from multiprocessing import Pool
import libRundownload as LR
import subprocess

TYPE = 'neg'

def CopyImage(video_pack):
    v_name = video_pack[0][0]
    source = video_pack[0][1]
    seg_type = video_pack[1]
    info = EL.GetVideoInfo(v_name, seg_type)
    source_info = EL.GetVideoInfo(source, 'NegSource')
    command = 'cp %s/* %s/'%(source_info['pano_cut_path'], info['pano_cut_path'])
    print command
    subprocess.call(command, shell=True)
    command = 'cp %s/*.txt %s/'%(source_info['pano_path'], info['pano_path'])
    print command
    subprocess.call(command, shell=True)
if __name__ == '__main__':
    lst = EL.GetList(TYPE)
    lst = LR.ArgumentComprass(lst, TYPE)
    #CopyImage(lst[0])
    pool = Pool(processes = 4)
    pool.map(CopyImage, lst)
