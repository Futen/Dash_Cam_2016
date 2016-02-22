#! /usr/bin/env python
import SystemParameter as SP

def ExportDownloadList(seg_type, save_name):
    if seg_type == 'NegSource':
        lst = SP.GetNegSourceList()
    else:
        lst = SP.GetVideoList(seg_type)
    f = open(save_name, 'w')
    for one in lst:
        info = SP.GetPath(one,seg_type)
        if info['state']['panodownload'] == 'no':
            f.write(one+'\n')
    f.close

if __name__ == '__main__':
    '''
    test_id = '9ylEY2ntZ2w'
    info = SP.GetPath(test_id, 'NegSource')
    print info
    '''
    TYPE = 'pos'
    ExportDownloadList(TYPE, 'list.txt')
