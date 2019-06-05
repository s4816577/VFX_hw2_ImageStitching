import cv2
import numpy as np
from matplotlib import pyplot as plt

def FeatureDetection(img, const):
    high, width, channel = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)

    gray_dx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=-1)
    gray_dy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=-1)

    Ix2 = gray_dx * gray_dx
    Iy2 = gray_dy * gray_dy
    Ixy = gray_dx * gray_dy

    Sx2 = cv2.GaussianBlur(Ix2, (5,5), 0)
    Sy2 = cv2.GaussianBlur(Iy2, (5,5), 0)
    Sxy = cv2.GaussianBlur(Ixy, (5,5), 0)

    R = (Sx2 * Sy2 - Sxy * Sxy) - const * np.power(Sx2 + Sy2, 2)
    #img[R > 0.01*R.max()] = [255, 0, 0]

    valid_map = np.zeros(gray.shape, dtype=bool)

    border_width = 4
    valid_map[border_width:-border_width-1, border_width:-border_width-1] = True

    #R = cv2.dilate(R, None)
    feature_points = np.unravel_index(np.argsort(R.ravel()), R.shape)

    FeatureDescriptor = []
    for idx in reversed(range(len(feature_points[0]))):
        y = feature_points[0][idx]
        x = feature_points[1][idx]
        if valid_map[y, x]:
            valid_map[y-border_width:y+border_width+1, x-border_width:x+border_width+1] = False
            FeatureDescriptor.append([ (y,x) , img[ y-border_width:y+border_width+1, x-border_width:x+border_width+1 ] ])
        if len(FeatureDescriptor) == 1000:
            break

    '''
    img[[fp[0][0] for fp in FeatureDescriptor], [fp[0][1] for fp in FeatureDescriptor]] = [0, 0, 255]
    img = cv2.dilate(img, None)
    '''
    return FeatureDescriptor
