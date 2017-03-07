import sys
import cv2
import numpy as np 
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join

#base_dir = sys.argv[1]
#all_files = [f for f in listdir(base_dir) if isfile(join(base_dir, f))]


#for file in all_files:
#img = cv2.imread(base_dir + file, 0)
img = cv2.imread(sys.argv[1], 0)
sift = cv2.xfeatures2d.SIFT_create()
kp, des = sift.detectAndCompute(img, None)
img2 = cv2.drawKeypoints(img, kp, None, (255,0,0), 4)
plt.imshow(img), plt.show()
plt.imshow(img2), plt.show()
