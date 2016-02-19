#! /usr/bin/env python

f = open('negative_check.txt','r')
f_out = open('negative_arrange.txt','w')
v_lst = []
data = {}
for line in f:
    line = line[0:-1].split('\t')
    if not(line[4] in v_lst):
        v_lst.append(line[4])
        data[line[4]] = []
        data[line[4]].append(line[2])
        data[line[4]].append(line[3])
        data[line[4]].append(line[0])
    else:
        data[line[4]].append(line[0])
for one in v_lst:
    s = '%s\t%s\t%s'%(one, data[one][0], data[one][1])
    index = 2
    for i,j in enumerate(data[one]):
        if i >= index:
            s += '\t%s'%j
    f_out.write(s + '\n')
        
f_out.close()
f.close()
