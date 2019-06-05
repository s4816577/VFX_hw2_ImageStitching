import numpy as np
import math
import random

def transform(tuple1, tuple2):
    return [tuple1[0] - tuple2[0], tuple1[1] - tuple2[1]]

def ransac(matches, threshold):
    p = 0.5
    n = 2
    P = 0.99
    k = int(round(math.log(1-P)/math.log(1 - math.pow(p, n))))
    if len(matches) <= 2:
        return matches

    bestMatch = []
    for i in range(0, k):
        random_index1 = random.randint(0, len(matches)-1)
        random_index2 = random.randint(0, len(matches)-1)
        picked_map = np.zeros(len(matches), dtype=bool)
        picked_map[random_index1] = 1
        picked_map[random_index2] = 1

        theta = np.array(transform(matches[random_index1][0], matches[random_index1][1]), np.double)
        theta += np.array(transform(matches[random_index2][0], matches[random_index2][1]), np.double)
        theta /= 2
      
        tempMatch = []
        for i in range(0, len(matches)):
            if picked_map[i] is 1:
                continue
            unpicked_theta = np.array(transform(matches[i][0], matches[i][1]), np.double)
            error = math.sqrt(sum(np.power(unpicked_theta - theta, 2)))
            
            if error < threshold:
                tempMatch.append(matches[i])
        if len(tempMatch) > len(bestMatch):
            bestMatch = tempMatch
    return bestMatch