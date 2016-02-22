import os
import subprocess
# Global Parameter
ROOT_PATH = '/home/Futen/Dash_Cam_2016' # root directory
VIDEO_PATH = '/home/Futen/Dash_Cam_2016/Videos' # Location of video
VIDEO_INFO_PATH = '/home/Futen/Dash_Cam_2016/video_info'
OPENSFM_PATH = '/home/Futen/OpenSfM/bin'
# parameter for pano
RADIUS = 0.3 # download pano with RADIUS km in circle
FRAME_PATH = 'images' # Videos/vname/images
PANO_PATH = 'pano' # Videos/'vname'/pano ------> VIDEO_PATH + vname + PANO_PATH
PANO_UNCUT_PATH = '%s/download'%PANO_PATH # Video/'vname'/pano/download
PANO_CUT_PATH = '%s/cut' %PANO_PATH # Video/'vname'/pano/cut


# Do not change the following code 
# The function is to get all video name
def GetVideoList(TYPE):
    file_name = ''
    lst = []
    if TYPE == 'pos':
        file_name = '/home/Futen/Dash_Cam_2016/DataList/positive_check.txt'
    elif TYPE == 'neg':
        file_name = '/home/Futen/Dash_Cam_2016/DataList/negative_check.txt'
    elif TYPE == 'NegSource':
        return GetNegSourceList()
    else:
        print 'Type error in GetVideoList'
        exit()
    f = open(file_name, 'r')
    for line in f:
        line = line[0:-1].split('\t')
        name = line[0].split('.')[0]
        lst.append(name)
    f.close()
    return lst
# The function is to get lat lon of all video
def GetVideoLatLon(TYPE):
    file_name = ''
    lst = []
    if TYPE == 'pos':
        file_name = '/home/Futen/Dash_Cam_2016/DataList/positive_check.txt'
    elif TYPE == 'neg':
        file_name = '/home/Futen/Dash_Cam_2016/DataList/negative_check.txt'
    else:
        print 'Type error in GetVideoList'
        exit()
    f = open(file_name, 'r')
    for line in f:
        line = line[0:-1].split('\t')
        name = line[0].split('.')[0]
        info = (name, float(line[2]), float(line[3]))
        lst.append(info)
    f.close()
    return lst
# The function is to get the related folder of video
def GetPath(video_name, TYPE): #GetPath('ZCTXXXX')
    sub_dir = ''
    if TYPE != 'pos' and TYPE != 'neg' and TYPE != 'NegSource':
        print 'pos or neg???'
        exit()
    elif TYPE == 'pos':
        sub_dir = 'positive'
    elif TYPE == 'neg':
        sub_dir = 'negative'
    elif TYPE == 'NegSource':
        return GetNegSourcePath(video_name)
    video_path = VIDEO_PATH + '/' + sub_dir  + '/' + video_name

    #if not(os.path.isdir(video_path)) or '\n' in video_name:
    #    print 'error video dir or /n in name'
    #    exit()
    frame_path = video_path + '/' + FRAME_PATH
    pano_path = video_path + '/' + PANO_PATH
    pano_uncut_path = video_path + '/' + PANO_UNCUT_PATH
    pano_cut_path = video_path + '/' + PANO_CUT_PATH
    # check process state
    reconstruction = 'no'
    panolist = 'no'
    panodownload = 'no'
    if os.path.isfile(video_path + '/reconstruction.json'):
        reconstruction = 'done'
    if os.path.isfile(pano_path + '/pano_lst_finish.txt'):    
        panolist = 'yes'
        #panolist = 'no'
    if os.path.isfile(pano_path + '/pano_lst_precise.txt'):
        panodownload = 'yes'
    state = dict({'reconstruction':reconstruction, 'panolist':panolist, 'panodownload':panodownload})
    
    output = dict({'video_path':video_path,
                   'frame_path':frame_path, 
                   'pano_path':pano_path, 
                   'pano_uncut_path':pano_uncut_path, 
                   'pano_cut_path':pano_cut_path,
                   'state':state
                   })
    '''
    for index, key in enumerate(output):
        if key != 'state':
            if not(os.path.isdir(output[key])):
                subprocess.call('mkdir -p %s'%output[key], shell=True)
    '''
    return output
def GetNegSourceList(LATLON = False, SUB_VIDEO = False):
    v_lst = []
    f = open('/home/Futen/Dash_Cam_2016/DataList/negative_arrange.txt','r')
    if LATLON == False and SUB_VIDEO == False:
        for line in f:
            line = line[0:-1].split('\t')
            v_lst.append(line[0])
    elif LATLON == True and SUB_VIDEO == False:
        for line in f:
            line = line[0:-1].split('\t')
            tmp = []
            tmp.append(line[0])
            tmp.append(line[1])
            tmp.append(line[2])
            v_lst.append(tmp)
    elif LATLON == False and SUB_VIDEO == True:
        for line in f:
            line = line[0:-1].split('\t')
            tmp = []
            tmp.append(line[0])
            for index in range(3, len(line)):
                tmp.append(line[index])
            v_lst.append(tmp)
    else:
        for line in f:
            line = line[0:-1].split('\t')
            tmp = []
            for index in range(0,len(line)):
                tmp.append(line[index])
            v_lst.append(tmp)
    f.close()
    return v_lst
def GetNegSourcePath(video_name):
    pano_path = VIDEO_PATH + '/NegSource/' + video_name
    pano_uncut_path = pano_path + '/download'
    pano_cut_path = pano_path + '/cut'
    # check process state
    reconstruction = 'no'
    panolist = 'no'
    panodownload = 'no'
    if os.path.isfile(pano_path + '/reconstruction.json'):
        reconstruction = 'done'
    if os.path.isfile(pano_path + '/pano_lst_finish.txt'):    
        panolist = 'yes'
        #panolist = 'no'
    if os.path.isfile(pano_path + '/pano_lst_precise.txt'):
        panodownload = 'yes'
    state = dict({'reconstruction':reconstruction, 'panolist':panolist, 'panodownload':panodownload})
    output = dict({'pano_path':pano_path,
                   'pano_uncut_path':pano_uncut_path,
                   'pano_cut_path':pano_cut_path,
                   'state':state
                   })

    '''
    for index,key in enumerate(output):
        if key != 'state':
            if not(os.path.isdir(output[key])):
                subprocess.call('mkdir -p %s'%output[key], shell=True)
    '''
    return output
