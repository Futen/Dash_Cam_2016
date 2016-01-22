import os
import subprocess
# Global Parameter
ROOT_PATH = '/home/Futen/Dash_Cam_2016' # root directory
VIDEO_PATH = '/home/Futen/Dash_Cam_2016/Videos' # Location of video
VIDEO_INFO_PATH = '/home/Futen/Dash_Cam_2016/video_info'

# parameter for pano
RADIUS = 1 # download pano with RADIUS km in circle
FRAME_PATH = 'images' # Videos/vname/images
PANO_PATH = 'pano' # Videos/'vname'/pano ------> VIDEO_PATH + vname + PANO_PATH
PANO_UNCUT_PATH = '%s/download'%PANO_PATH # Video/'vname'/pano/download
PANO_CUT_PATH = '%s/cut' %PANO_PATH # Video/'vname'/pano/cut


# Do not change the following code 
# The function is to get the related folder of video
def GetPath(video_name): #GetPath('ZCTXXXX')
    video_path = VIDEO_PATH + '/' + video_name
    if not(os.path.isdir(video_path)) or '\n' in video_name:
        print 'error video dir or /n in name'
        exit()
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
    if os.path.isfile(pano_path + '/pano_lst.txt'):
        panolist = 'yes'
        #panolist = 'no'
    state = dict({'reconstruction':reconstruction, 'panolist':panolist, 'panodownload':panodownload})
    
    output = dict({'video_path':video_path,
                   'frame_path':frame_path, 
                   'pano_path':pano_path, 
                   'pano_uncut_path':pano_uncut_path, 
                   'pano_cut_path':pano_cut_path,
                   'state':state
                   })
    for index, key in enumerate(output):
        if key != 'state':
            if not(os.path.isdir(output[key])):
                subprocess.call('mkdir -p %s'%output[key], shell=True)

    return output
