import ImageWarping
import FeatureMatching
import RANSAC
import TransForm
import ImageBlending
import matplotlib.pyplot as plt
import harris
import argparse
import cv2
from scipy.spatial import cKDTree
import numpy as np

def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--files', default=None, type=str, nargs='+')
    parser.add_argument('--focallength', default=0.0, type=float, nargs='+')
    parser.add_argument('--threshold', default=10, type=float)
    parser.add_argument('--constant', default=0.04, type=float)
    return parser.parse_args()

def main():
    print('readimage')
    image_count = len(args.files)
    images = []
    for file_path in args.files:
        images.append(cv2.imread(file_path))
    
    print('harris detection')
    FeatureDescriptors = []
    for i in range(0, image_count):
        FeatureDescriptors.append(harris.FeatureDetection(images[i], args.constant))

    FeatureKDTrees = []
    for i in range(image_count):
        descs = np.stack([desc[1].reshape(-1) for desc in FeatureDescriptors[i]])
        FeatureKDTrees.append(cKDTree(descs))
    
    print('matching')
    if image_count < 2:
        print('warning, the Matches cannot implement due to the img_counts < 2')
    Matches = []
    for i in range(0, image_count-1):
        h, w, c = images[i].shape
        Matches.append(FeatureMatching.Matching(FeatureDescriptors[i], FeatureDescriptors[i+1], FeatureKDTrees[i+1], w))
    
    print('warping')
    avg_focallength = sum(args.focallength) / len(args.focallength)
    warp_images = []
    for i in range(0, image_count):
        warp_images.append(ImageWarping.ImageWarping(images[i], avg_focallength))
    warp_matches = []
    for i in range(0, image_count-1):
        warp_matches.append(ImageWarping.FeatureWarping(Matches[i], avg_focallength, avg_focallength, images[i], images[i+1]))
    
    print('RANSAC')
    best_matches = []
    for i in range(0, image_count-1):
        best_matches.append(RANSAC.ransac(warp_matches[i], args.threshold))
    
    print('transform calculate')
    transforms = []
    for i in range(0, image_count-1):
        transforms.append(TransForm.transform_calculate(best_matches[i]))
    
    print('blending')
    image_out = ImageBlending.blending(warp_images, transforms)
    '''
    for matches_between_picture in best_matches:
        for matching_pair in matches_between_picture:
            print(matching_pair[0], matching_pair[1])
            warp_images[0][matching_pair[0][0]-3:matching_pair[0][0]+3, matching_pair[0][1]-3:matching_pair[0][1]+3] = [255,0,0]
            warp_images[1][matching_pair[1][0]-3:matching_pair[1][0]+3, matching_pair[1][1]-3:matching_pair[1][1]+3] = [255,0,0]
    
    plt.subplot(1,2,1)
    plt.imshow(image1)
    plt.title('image1')
    plt.subplot(1,2,2)
    plt.imshow(image2)
    plt.title('image2')'''
    cv2.imwrite('./stitched_image.png', image_out)
    '''
    plt.show()'''
    

if __name__ == '__main__':
    args = get_args()
    main()
