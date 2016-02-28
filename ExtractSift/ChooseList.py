import sys
sys.path.append('/home/Futen/Dash_Cam_2016')
import numpy as np
import SystemParameter as SP

sample = 200

def SamplePositive(num):
    f = open('../DataList/positive_check.txt','r')
    finish_lst = []
    dic = {}
    for line in f:
        line = line[0:-1].split('\t')
        v_name = line[0].split('.')[0]
        source = line[-1]
        info = SP.GetPath(v_name, 'pos')
        if info['state']['panodownload'] == 'yes':
            finish_lst.append(v_name)
            dic[v_name] = source
    f.close()
    print 'len pos %d'%len(finish_lst)
    do_lst = np.random.choice(finish_lst, num, replace = False)
    return (do_lst,dic)
def SampleNegative(num):
    lst = SP.GetNegSourceList(SUB_VIDEO = True)
    dic = {}
    finish_lst = []
    else_lst = []
    for one in lst:
        info = SP.GetPath(one[0], 'NegSource')
        v_name = one[-1].split('.')[0]
        if info['state']['panodownload'] == 'yes':
            finish_lst.append(v_name)
            dic[v_name] = one[0]
            if len(one) > 2:
                name = one[-2].split('.')[0]
                if name in finish_lst:
                    continue
                finish_lst.append(name)
                dic[name] = one[0]
    print 'len neg %d'%len(finish_lst)
    do_lst = np.random.choice(finish_lst, num, replace = False)
    return (do_lst, dic)

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) != 2:
        print 'Argument Error'
        exit()
    f_name = argv[1]
    (pos_lst,dic) = SamplePositive(500)
    pos_lst = sorted(pos_lst)
    f = open(f_name+'_pos.txt','w')
    for one in pos_lst:
        s = '%s\t%s\n'%(one, dic[one])
        f.write(s)
    f.close()
    (neg_lst,dic) = SampleNegative(750)
    neg_lst = sorted(neg_lst)
    f = open(f_name+'_neg.txt','w')
    for one in neg_lst:
        s = '%s\t%s\n'%(one, dic[one])
        f.write(s)
    f.close()
    #print neg_lst
