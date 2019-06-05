import numpy as np
import cv2
import math

def ImageWarping(image, focallenth):
    WarpedImage = np.zeros(image.shape, np.uint8)
    high, width, channel = image.shape
    y_center = high / 2
    x_center = width / 2
    for y_new in range(0, high):
        for x_new in range(0, width):
            x_origin = focallenth * math.tan((x_new - x_center)/focallenth)
            y_origin = math.sqrt(x_origin * x_origin + focallenth * focallenth) * (y_new - y_center) / focallenth
            x_origin = int(round(x_origin + x_center))
            y_origin = int(round(y_origin + y_center))
            #print x_origin, y_origin
            if x_origin >= 0 and x_origin < width and y_origin >= 0 and y_origin < high:
                WarpedImage[y_new, x_new, :] = image[y_origin, x_origin, :]
            else:
                WarpedImage[y_new, x_new, :] = 0
    return WarpedImage
    
def FeatureWarping(matches, focallenth1, focallenth2, img1, img2):
    h1, w1, c1 = img1.shape
    h2, w2, c2 = img2.shape
    y_center_1 = h1 / 2
    y_center_2 = h2 / 2
    x_center_1 = w1 / 2
    x_center_2 = w2 / 2
    warped_matches = []
    for i in range(len(matches)):
        img1_y = matches[i][0][0]
        img1_x = matches[i][0][1]
        img2_y = matches[i][1][0]
        img2_x = matches[i][1][1]
        warp_img1_x = int(round(focallenth1 * math.atan((img1_x - x_center_1) / focallenth1)))
        warp_img1_y = int(round(focallenth1 * (img1_y - y_center_1) / math.sqrt(warp_img1_x * warp_img1_x + focallenth1 * focallenth1)))
        warp_img2_x = int(round(focallenth2 * math.atan((img2_x - x_center_2) / focallenth2)))
        warp_img2_y = int(round(focallenth2 * (img2_y - y_center_2) / math.sqrt(warp_img2_x * warp_img2_x + focallenth2 * focallenth2)))
        warped_matches.append([ (warp_img1_y + y_center_1, warp_img1_x + x_center_1) , (warp_img2_y + y_center_2, warp_img2_x + x_center_2) ])
    return warped_matches