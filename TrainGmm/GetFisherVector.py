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

TYPE = 'pos'

def Fisher(video_comprass): # [(v_name,source), seg_type]
    v_name = video_comprass[0][0]
    source = video_comprass[0][1]
    seg_type = video_comprass[1]
    info = EL.GetVideoInfo(v_name, seg_type)
    
    frame_sift_lst = [x for x in sorted(os.listdir(info['frame_sift_path'])) if x.endswith('.sift')]
    pano_sift_lst = [x for x in sorted(os.listdir(info['pano_sift_path'])) if x.endswith('.sift')]
    
    frame_desc = []
    for one in frame_sift_lst:
        f = info['frame_sift_path'] + '/' + 'one'
        desc = ReadSift.ReadSift(f)

if __name__ == '__main__':
    pool = Pool(processes = 12)
    lst = EL.GetList(TYPE)
    try:
        SendEmail.SendEmail()
    except:
        SendEmail.SendEmail(Text = 'GGGGGGGG')

