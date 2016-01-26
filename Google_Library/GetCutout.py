import math
import cv2
import numpy as np
from scipy.linalg import expm

### read the panoramas =>  pano_XXX.jpg
### output cutouts for each panoramas in differ angle  => pano_XXX_180.jpg

def cut(src,yaw,wfov,name):
    # spherical size
    Iw = 6656
    Ih = 3328

    # pinhole model size
    #Ow = 936    # 100 degree
    #Oh = 537
    Ow = 1295    # odd!
    Oh = 647


    f = Ow / (2*math.tan(wfov/2))

    Ow = float(Ow)
    Oh = float(Oh)
    Iw = float(Iw)
    Ih = float(Ih)

    # I/O image center
    OUcenter = ( Ow +1 ) / 2
    OVcenter = ( Oh +1 ) / 2
    IUcenter = ( Iw +1 ) / 2
    IVcenter = ( Ih +1 ) / 2

    # X,Y,Z
    xn = np.linspace(1,Ow,Ow)
    yn = np.linspace(1,Oh,Oh)
    X,Y = np.meshgrid(xn,yn)

    X = X-OUcenter
    Y = Y-OVcenter
    Z = X*0 + f

    #print X.shape,Y.shape,Z.shape
    # compensate pitch
    pitch = -4
    Mpitch = np.array( [[0,0,0], [0,0,math.radians(pitch)], [0,-math.radians(pitch),0]] )
    T = expm( Mpitch )

    X = X.reshape(1,-1);
    Y = Y.reshape(1,-1);
    Z = Z.reshape(1,-1);

    PTS = np.concatenate([X,Y,Z])


    PTSt = np.dot(T,PTS)

    Xt = PTSt[0]
    Yt = PTSt[1]
    Zt = PTSt[2]


    data_size = Xt.shape
    #print data_size
    theta = np.zeros(data_size,dtype='float32')
    phi = np.zeros(data_size,dtype='float32')

    #theta[502631] = math.atan2( Xt[502631], Zt[502631] )
    #print data_size[0]

    for l in range(0,data_size[0]):
        theta[l] = math.atan2( Xt[l], Zt[l] )
        phi[l] = math.atan( Yt[l] / math.sqrt( Xt[l]*Xt[l] + Zt[l]*Zt[l] ) )

    theta = theta + math.radians(yaw)
    for num in np.where( theta >= math.pi ):
        theta[num] = theta[num] - 2*math.pi

    for num in np.where( theta < -math.pi ):
        theta[num] = theta[num] + 2*math.pi

    theta = theta.reshape(Oh,-1)
    phi = phi.reshape(Oh,-1)

    U = theta / (2*math.pi) *Iw + IUcenter
    V = phi / (math.pi) * Ih + IVcenter

    ### remap
    map_x_32 = U.astype('float32')
    map_y_32 = V.astype('float32')
    warped = cv2.remap(src, map_x_32, map_y_32, cv2.INTER_CUBIC)
    s = '%s.jpg' % name
    cv2.imwrite(s, warped)

