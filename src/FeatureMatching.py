import cv2
import math
import numpy as np

def Matching(FDList1, FDList2, FDKDTree2, w):
    matches = []
    '''count = 0
    count2 = 0'''
    for i in range(0, len(FDList1)):
        '''count += 1
        count2 += 1
        if(count == 50):
            count = 0
            print(count2)'''
        dd, ii = FDKDTree2.query(FDList1[i][1].reshape(-1), k=[1,2])
        if (dd[0]/dd[1]) < 0.95 and FDList1[i][0][1] > w / 2:
            matches.append([FDList1[i][0], FDList2[ii[0]][0]])
    return matches
