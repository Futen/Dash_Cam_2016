import sys
sys.path.append('/home/Futen/Dash_Cam_2016')
import numpy as np
import SystemParameter as SP

sample = 200

def SamplePositive(num):
    lst = SP.GetVideoList('pos')
    finish_lst = []
    for one in lst:
        info = SP.GetPath(one, 'pos')
        if info['state']['panodownload'] == 'yes':
            finish_lst.append(one)
    do_lst = np.random.choice(finish_lst, num, replace = False)
    return do_lst
def SampleNegative(num):
    lst = SP.GetNegSourceList(SUB_VIDEO = True)
    dic = {}
    finish_lst = []
    for one in lst:
        info = SP.GetPath(one[0], 'NegSource')
        v_name = one[-1]
        if info['state']['panodownload'] == 'yes':
            finish_lst.append(v_name)
            dic[v_name] = one[0]
    do_lst = np.random.choice(finish_lst, num, replace = False)
    return (do_lst, dic)

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) != 2:
        print 'Argument Error'
    pos_lst = sorted(SamplePositive(sample))
    neg_lst,dic = SampleNegative(sample)
    neg_lst = sorted(neg_lst)
    print neg_lst
