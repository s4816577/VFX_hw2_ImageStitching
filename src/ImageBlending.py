import numpy as np
import cv2

def blend_img(img_out, img_in, trans):
    h2, w2, c2 = img_in.shape
    for i in range(0, h2):
        for j in range(0, w2):
            for k in range(0, 3):
                if int(img_out[i+trans[1], j+trans[0], k]) + img_in[i, j, k] > 255:
                    img_out[i+trans[1], j+trans[0], k] = 255
                else:
                    img_out[i+trans[1], j+trans[0], k] += img_in[i, j, k]
    return img_out

def make_weight(pre_tarns, trans, merge_w, w1, w2):
    weighting_1 = np.ones(pre_tarns[0]+w1)
    weighting_2 = np.ones(w2)
    for i in range(trans[0]+5, w1+pre_tarns[0]):
        weighting_1[i] = float(w1+pre_tarns[0]-i-1)/(w1+pre_tarns[0]-trans[0]-5)
    for i in range(0, w1+pre_tarns[0]-trans[0]-5):
        weighting_2[i] = 1 - weighting_1[i+trans[0]+5]
    return weighting_1, weighting_2
    
def make_weighted_img(img1, img2, weight_1, weight_2, width_merge):
    h1, w1, c1 = img1.shape
    h2, w2, c2 = img2.shape
    for i in range(0, h1):
        for j in range(0, width_merge):
            for k in range(0, 3):
                img1[i,j,k] = int(round(float(img1[i,j,k]) * weight_1[j]))
    
    for i in range(0, h2):
        for j in range(0, w2):
            for k in range(0, 3):
                img2[i,j,k] = int(round(float(img2[i,j,k]) * weight_2[j]))
    return img1, img2

def make_sum_trans(i, trans):
    sum_trans_x = 0
    sum_trans_y = 0
    for j in range(0, i):
        sum_trans_x += trans[j][0]
        sum_trans_y += trans[j][1]
    return [sum_trans_x, sum_trans_y] 

def blending(images, transforms):
    h1, w1, c1 = images[0].shape
    sum_x = 0
    sum_y = 0
    for transform in transforms:
        sum_x += transform[0]
        sum_y += transform[1]
    image_merge = np.zeros((int(h1*1.5), w1+sum_x, 3), np.uint8)
    
    for i in range(0, h1):
        for j in range(0, w1):
            image_merge[i, j, :] += images[0][i, j, :]
    for i in range(1, len(images)):
        print('dealing images:',i)
        h_1, w_1, c_1 = images[i-1].shape
        h_2, w_2, c_2 = images[i].shape
        trans = make_sum_trans(i, transforms)
        pre_trans = make_sum_trans(i-1, transforms)
        wei1, wei2 = make_weight(pre_trans, trans, w1+sum_x, w_1, w_2)
        img1, img2 = make_weighted_img(image_merge, images[i], wei1, wei2, w1+pre_trans[0])
        image_merge = blend_img(img1, img2, trans)
    return image_merge