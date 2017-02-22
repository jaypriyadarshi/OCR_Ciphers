import cv2
import sys
import numpy as np 
import subprocess
import itertools

img = cv2.imread(sys.argv[1],0)
#height_org, width_org = img.shape
ret,img = cv2.threshold(img,140,255,cv2.THRESH_BINARY)
img2 = cv2.imread(sys.argv[1])

#img = img[::-1]
#img1 = np.transpose(img)

height, width = img.shape

f = open('data_page','w')

black_pixs = []
for i in range(height):
	total_black_pixels = 0
	for j in range(width):
		if img.item(i,j) == 0:
			total_black_pixels += 1
	black_pixs.append("c"+str(total_black_pixels))

f.write(' '.join(black_pixs))
f.close()
a = subprocess.Popen("./align3 data_page " + sys.argv[3] + " " + sys.argv[4] + " " + sys.argv[5] + " " + sys.argv[6], shell=True, stdout=subprocess.PIPE).stdout.read()

print "########################"
print a
print "########################"
cols = a.split()


for i in cols:
	x = int(i)
	#print x
	img2 = cv2.line(img2,(0,x-1),(width-1,x-1),(0,0,255),2)
	#img1.itemset((height/2,x-1,0),0)
	#img1.itemset((height/2,x-1,1),0)
	#img1.itemset((height/2,x-1,2),255)
#cv2.imwrite(sys.argv[2],img2)

img3 = cv2.imread(sys.argv[1],0)
cols.insert(0,'0')


#f1 = open('FunctionValues_newp.py','w')
#f2 = open('FunctionValues_newp.txt','w')


#generating all values of <a,b,c>
"""
params = []
temp = [0,0.007,0.2,0.07,0.7,7,70]
temp1 = [0]
temp2 = [1,1.2,1.4,1.5,1.8,2.0,2.2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,15,20,30,50]
temp3 = [0,-0.007,-0.2,-0.07,-0.7,-7,-70]
temp4 = [-1,-1.2,-1.4,-1.5,-1.8,-2.0,-2.2,-2.5,-3,-3.5,-4,-4.5,-5,-5.5,-6,-6.5,-7,-7.5,-8,-8.5,-9,-9.5,-10,-15,-20,-30,-50]



params1 = []
params1.append(temp3)
params1.append(temp1)
params1.append(temp4)

all_params = list(itertools.product(*params1))

params.append(temp)
params.append(temp1)
params.append(temp2)

new_params = list(itertools.product(*params))

all_params += new_params

#all_params.insert(0,(0,0,5))



h = 140/2 #average row height

st_points = [(0,k) for k in range(140)]

sols = {}

sols["StLn"] = st_points
for param in all_params:
	try:
		sols[param] = []
		#average height = 140
		for h1 in range(140):
			coeff = [float(param[0]), float(param[1]), float(param[2]), -(h-h1)]
			xs = np.roots(coeff)
			imaginary_pt = xs.imag
			for l in range(len(imaginary_pt)):
				if imaginary_pt[l] == 0:
					if (int(round(xs[l])),h1) not in sols[param]:
						sols[param].append((int(round(xs[l])),h1))
	except:
		pass

"""

#f1.write("sols = " + str(sols))
#f2.write("sols = " + str(sols))
#f1.close()
#f2.close()
#print sols
print "pass 1"
for m in range(len(cols)-1):
	upper = int(cols[m])-1
	lower = int(cols[m+1])-1
	print "iteration " + str(m)
			
	black_pixs = []

	for i in range(width):
		total_black_pixels = 0
		for j in range(upper,lower):
			if img.item(j,i) == 0:
				total_black_pixels += 1
		black_pixs.append("c"+str(total_black_pixels))
		

	print "pass 2"
	f1 = open('data_page_vline','w')
	f1.write(' '.join(black_pixs))
	f1.close()
	a1 = subprocess.Popen("./align3 data_page_vline " + sys.argv[7] + " " + sys.argv[8] + " " + sys.argv[9] + " " + sys.argv[10], shell=True, stdout=subprocess.PIPE).stdout.read()

	cols1 = a1.split()
	#print minimums[int(cols[10])-1]
	#parameters[int(cols[10])-1] = (0,0,1.2)
	#print sols[(0,0,5)]

	ctr = 1
	for i in cols1:
		x = int(i)
		x = x-1
		img2 = cv2.line(img2,(x,upper),(x,lower),(0,0,255),1)
			
cv2.imwrite(sys.argv[2],img2)