#https://maps.googleapis.com/maps/api/staticmap?center=40.737102,-73.990318&zoom=13&size=400x300&maptype=roadmap&sensor=false&path=color:0x00000000|weight:5|fillcolor:0xFFFF0033|8th+Avenue+%26+34th+St,New+York,NY|\8th+Avenue+%26+42nd+St,New+York,NY|Park+Ave+%26+42nd+St,New+York,NY,NY|\Park+Ave+%26+34th+St,New+York,NY,NY

import urllib2
import Image
import cv2

BaseUri = 'https://maps.googleapis.com/maps/api/staticmap'

def GetMap(center_lat, center_lng, zoom, l, w):
        url =  '%s?'
        url += 'center=%s,%s'
        url += '&zoom=%s'                       # zoom level of tile
        url += '&size=%sx%s'                          # x position of tile
        url += '&maptype=roadmap'                          # y position of tile
        url = url % (BaseUri, center_lat, center_lng, zoom, l, w)
        print url
        return GetUrlContents(url)

def GetUrlContents(url):
        f = urllib2.urlopen(url)
        data = f.read()
        f.close()
        return data

'''
if True:

    CENTER = '%s,%s' % (22.6229608658,120.284767846)


    img = GetMap(22.6229608658,120.284767846,17,480,640)
    f = open('test.png','wb')
    f.write(img)
    f.close()

    new_im = Image.open('test.png')
    new_im.rotate(90).save('tt.png')
'''

