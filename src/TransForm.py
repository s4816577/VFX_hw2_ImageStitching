import cv2
import math
import numpy as np

def transform_calculate(matches):
    matches_count = len(matches)
    
    '''make A'''
    A = np.zeros((matches_count * 2 + 1, 3))
    for i in range(0, matches_count):
        A[i] = np.array([1,0, matches[i][1][1]])
        A[i+matches_count] = np.array([0, 1, matches[i][1][0]])
        A[matches_count*2] = np.array([0, 0, 1])
        
    '''make B'''
    B = np.zeros((matches_count * 2 + 1, 1))
    for i in range(0, matches_count):
        B[i] = np.array([matches[i][0][1]])
        B[i+matches_count] = np.array([matches[i][0][0]])
        B[matches_count*2] = np.array([1])
    
    '''get x'''
    x,resid,rank,s = np.linalg.lstsq(A,B,rcond=-1)
    
    return [int(round(x[0][0])), int(round(x[1][0]))]
