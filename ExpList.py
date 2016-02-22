import os
import SystemParameter as SP

pos_file = SP.VIDEO_INFO_PATH + '/list_pos.txt'
neg_file = SP.VIDEO_INFO_PATH + '/list_neg.txt'

def GetList(TYPE):
    if TYPE == 'pos':
        f_name = pos_file
    elif TYPE == 'neg':
        f_name = neg_file
    f = open(f_name,'r')
    lst = []
    for line in f:
        line = line[0:-1].split('\t')
        lst.append((line[0], line[1]))
    f.close()
    return lst
def GetVideoInfo(v_name, TYPE):
    return SP.GetPath(v_name, TYPE)

if __name__ == '__main__':
    lst = GetList('neg')
    print GetVideoInfo(lst[-1][0], 'neg')
