#! /usr/bin/env python3

# wget 'http://overpass-api.de/api/interpreter?data=[out:json];way(22.6116,120.302 ,22.6275,120.3242);out;' -O all.json

import sys
import urllib2
import json
import numpy as np
from geopy.distance import VincentyDistance as VD

def GetUrlContent(url):
    f = urllib2.urlopen(url)
    data = f.read()
    f.close()
    return data
def GetDistance(point1, point2): #(a,b) (c,d)
    #distance = np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    distance = np.sqrt(np.sum((point1-point2)**2))
    return distance
def GetLineDistance(pointA, pointB, ref_point):
    vector_AB = pointB - pointA
    vector_AC = ref_point - pointA
    len_AB = np.dot(vector_AB, vector_AB)
    product = np.dot(vector_AB, vector_AC)
    if product < 0:
        #return GetDistance(pointA, ref_point)
        return VD(pointA, ref_point)
    elif product > len_AB:
        #return GetDistance(pointB, ref_point)
        return VD(pointB, ref_point)
    pointG = pointA + vector_AB*product/len_AB
    #return GetDistance(ref_point, pointG)
    return VD(ref_point, pointG)

def GetJsonOringinData(bbox):
    url = 'http://overpass-api.de/api/interpreter?data=[out:json];way[highway](%s,%s,%s,%s);out;'%(bbox[0],bbox[1],bbox[2],bbox[3])
    data1 = GetUrlContent(url)
    data1 = json.loads(data1)
    url = 'http://overpass-api.de/api/interpreter?data=[out:json];way[highway](%s,%s,%s,%s);>;out;'%(bbox[0],bbox[1],bbox[2],bbox[3])
    data2 = GetUrlContent(url)
    data2 = json.loads(data2)
    '''
    f = open('tmp.json','w')
    s = json.dumps(data2,ensure_ascii=False,indent=4)
    f.write(s.encode('utf-8'))
    f.close()
    '''
    #data = json.decoder(url)
    return (data1,data2)
def CalculateConnect(dataInput):#(dataWay, dataNode)
    all_node = dataInput[1]
    all_way = dataInput[0]
    node_tmp = {}
    for i in all_node["elements"]:
        node_tmp[i["id"]] = {"lat":i["lat"], "lon":i["lon"]}
    #f = open('tmp.json','w')
    #s = json.dumps(node_tmp,ensure_ascii=False,indent=4)
    #f.write(s.encode('utf-8'))
    #f.close()
    all_relation = {}
    traffic_signals_lst = []
    key_check = 0
    for one_node in all_node["elements"]:
        time = 0
        tag = one_node["id"]
        try:
            if one_node['tags']['highway'] == 'traffic_signals':
                traffic_signals_lst.append(tag)
                #print type(tag)
        except:
            pass
        #print(time)
        for one_way in all_way["elements"]:
            lst = one_way["nodes"]
            key_check = 0
            try:
                tag_lst = one_way["tags"]
                for key,value in one_way["tags"].iteritems():
                    if key == "highway":
                        key_check = 1
                        break
            except KeyError:
                #print(one_way["id"])
                pass
            if key_check == 1:
                for i in range(0, len(lst)):
                    if lst[i] == one_node["id"]:
                        if time == 0:
                            all_relation[ tag ] = {"id":one_node["id"], "lat":one_node["lat"], "lon":one_node["lon"], "connect":[]}
                            time = 1
                        if i-1 >= 0:
                            all_relation[tag]["connect"].append({"id": lst[i-1], "lat":node_tmp[lst[i-1]]["lat"],
                                                             "lon": node_tmp[lst[i-1]]["lon"]})
                        if i+1 < len(lst):
                            all_relation[tag]["connect"].append({"id": lst[i+1], "lat":node_tmp[lst[i+1]]["lat"],
                                                             "lon": node_tmp[lst[i+1]]["lon"]})
    return (all_relation,traffic_signals_lst)
def GetTwoConnect(data):
    finish_point = []
    output_tmp = {}
    index = 1
    for i,node_id in enumerate(data):
        for j,point in enumerate(data[node_id]['connect']):
            if node_id < point['id']:
                tmp = (node_id, point['id'])
            else:
                tmp = (point['id'], node_id)
            if tmp in finish_point:
                continue
            finish_point.append(tmp)
            point1_dic = dict({'lat':data[node_id]['lat'], 'lon':data[node_id]['lon'], 'id':data[node_id]['id']})
            point2_dic = dict({'lat':point['lat'], 'lon':point['lon'], 'id':point['id']})
            output_tmp['%d'%index] = dict({'point1':point1_dic, 'point2':point2_dic})
            #print index
            index += 1
    output = dict({'total':index-1, 'data':output_tmp})
    return output
def Recursive(data, last_id, now_id, signal_lst):
    now_len = len(data[now_id]['connect'])
    #print now_id
    if now_id in signal_lst or now_len >= 3 or now_len == 1:
        return now_id
    else:
        for index,point in enumerate(data[now_id]['connect']):
            if point['id'] != last_id:
                next_id = point['id']
        return Recursive(data, now_id, next_id, signal_lst)

def GetIntersectionID(point1_id, point2_id, data, signal_lst):
    output1_id = ''
    output2_id = ''
    if not point1_id in signal_lst and not len(data[point1_id]['connect']) >= 3 and not len(data[point1_id]['connect']) == 1:
        for index,point in enumerate(data[point1_id]['connect']):
            if point['id'] != point2_id:
                next_id = point['id']
                #print next_id
        output1_id = Recursive(data, point1_id, next_id, signal_lst)
    else:
        output1_id = point1_id
    if not point2_id in signal_lst and not len(data[point2_id]['connect']) >= 3 and not len(data[point2_id]['connect']) == 1:
        for index,point in enumerate(data[point2_id]['connect']):
            if point['id'] != point1_id:
                next_id = point['id']
        output2_id = Recursive(data, point2_id, next_id, signal_lst)
    else:
        output2_id = point2_id
    return (output1_id, output2_id)
def FindResult(lat,lon):
    step_latlon = 0.0009
    step = step_latlon # step_latlon/10-->every ten meter
    bbox = (lat-step,lon-step,lat+step,lon+step)
    #print VD((lat-step,lon-step),(lat+step,lon-step)).km
    (wayData, nodeData) = GetJsonOringinData(bbox)
    (connectData, traffic_signal_lst) = CalculateConnect((wayData,nodeData))
    twoData = GetTwoConnect(connectData)
    time = 1
    point = np.array([lat,lon], dtype=np.float)
    Data = twoData['data']
    for index,key in enumerate(Data):
        data = Data[key]
        pointA = np.array([data['point1']['lat'], data['point1']['lon']], dtype = np.float)
        pointB = np.array([data['point2']['lat'], data['point2']['lon']], dtype = np.float) 
        distance = GetLineDistance(pointA, pointB, point)
        if time == 1:
            min_distance = distance
            min_pointA = data['point1']['id']
            min_pointB = data['point2']['id']
        elif distance < min_distance:
            min_distance = distance
            min_pointA = data['point1']['id']
            min_pointB = data['point2']['id']
        time = 2
    #print min_pointA
    #print min_pointB
    (min_pointA, min_pointB) = GetIntersectionID(min_pointA, min_pointB, connectData, traffic_signal_lst)
    min_pointA = (connectData[min_pointA]['lat'], connectData[min_pointA]['lon'])
    min_pointB = (connectData[min_pointB]['lat'], connectData[min_pointB]['lon'])
    return (min_pointA, min_pointB)
    '''
    s = json.dumps(twoData,ensure_ascii=False,indent=4)
    f= open('gg.json','w')
    f.write(s)
    f.close()
    '''
if __name__ == '__main__':
    point = (25.03048,121.51426)
    A,B = FindResult(point[0], point[1])
    lst = []
    lst.append(A)
    lst.append(point)
    lst.append(B)
    f = open('gg.csv','w')
    f.write('gg\n')
    for i in lst:
        s = '%f %f\n'%(i[0],i[1])
        f.write(s)
    f.close()
