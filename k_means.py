#python k_means.py <path to image dir>
import sys
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2

def load_data(base_dir):
	data = []
	all_files = [f for f in listdir(base_dir) if isfile(join(base_dir, f))]
	height, width = cv2.imread(base_dir + all_files[0], 0).shape
	for file in all_files:
		data.append(cv2.imread(base_dir + file, 0).ravel())
	return np.float32(np.vstack(data)), height, width

def PCA(data, n):
	cov = np.dot(data.T, data) / data.shape[0]
	U, S, V = np.linalg.svd(cov)
	#xrot = np.dot(data,U) #decorrelate the data, project data into the eigenbasis
	return np.dot(data, U[:,:n])


def kmeans(k, max_iter, data):
	# Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iter, 1.0)
	ret,label,center=cv2.kmeans(data,k,None,criteria,max_iter,cv2.KMEANS_RANDOM_CENTERS)
	return label

def visualize(data, labels, height, width):
	for i in range(k):
		cv2.imwrite('results/' + str(i) + '.png' ,np.hstack(map(lambda x: x.reshape(height, width), data[labels.ravel() == i])))

k = 10
max_iter = 1000
req_dim = 100
data, height, width = load_data(sys.argv[1])

#perform PCA
pca_data = PCA(data, req_dim)

labels = kmeans(k, max_iter, pca_data)
visualize(data, labels, height, width)




