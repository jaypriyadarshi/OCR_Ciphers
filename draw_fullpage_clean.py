import cv2
import sys
import numpy as np 
import subprocess
import itertools

def calc_black_pix_row(img):
	height, width = img.shape
	black_pixs = []
	for i in range(height):
		total_black_pixels = 0
		for j in range(width):
			if img.item(i,j) == 0:
				total_black_pixels += 1
		black_pixs.append("c"+str(total_black_pixels))
	return black_pixs

def count_black_pix_poly(img, all_functions, sols, upper, lower, difference, i):
	pixel_list = []
	for func in all_functions:
		pix_count = 0
		for xy in sols[func]:
			if xy[1] >= difference:
				x = xy[0] + i
				y = xy[1] + upper - difference

				if y <= lower:
					try:
						if img.item(y,x) == 0:
							pix_count += 1
					except:
						pix_count += 0

		pixel_list.append((pix_count,func))
	return pixel_list

def count_black_pix_st_ln(img, pixel_list, upper, lower, i):
	st_count = 0
	for j in range(upper,lower):
		if img.item(j,i) == 0:
			st_count += 1
	pixel_list.append((st_count,"StLn"))
	return pixel_list

def find_best_polynomials(pixel_list):
	min_pixel = min(pixel_list)
	all_min = []
	for k in pixel_list:
		if k[0] == min_pixel[0]:
			all_min.append(k)
	return all_min[-1], all_min	


def calc_black_pix_col(img, rows, sols, avg_height, idx):
	upper = int(rows[idx])-1
	lower = int(rows[idx + 1])-1
	row_height = lower - upper
	two_difference = avg_height - row_height
	difference = two_difference/2
	print "iteration " + str(idx)
	pix_counts = []
	opt_parameters = []
	minimums = []
	all_functions = sols.keys()

	height, width = img.shape
	#caluclate the black pixels interesected by each polynomial
	for i in range(width):
		pixel_list = count_black_pix_poly(img, all_functions, sols, upper, lower, difference, i)
		
		#calculate for straight line
		pixel_list = count_black_pix_st_ln(img, pixel_list, upper, lower, i)

		#find the curves which interesect minimum number of black pixels 

		best_poly, all_min = find_best_polynomials(pixel_list)	 
		pix_counts.append("c"+str(best_poly[0]))
		opt_parameters.append(best_poly[1])
		minimums.append((best_poly[0],all_min))
	return pix_counts, opt_parameters


def run_carmel_code(filename, mean, std1, std2, p):
	return subprocess.Popen(". align3 " + filename + " " + mean + " " + std1 + " " + std2 + " " + p, shell=True, stdout=subprocess.PIPE).stdout.read()

def gen_all_params():
	a_pos = [0,0.007,0.2,0.07,0.7,7,70]
	b = [0]
	c_pos = [1,1.2,1.4,1.5,1.8,2.0,2.2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,15,20,30,50]
	a_neg = [0,-0.007,-0.2,-0.07,-0.7,-7,-70]
	c_neg = [-1,-1.2,-1.4,-1.5,-1.8,-2.0,-2.2,-2.5,-3,-3.5,-4,-4.5,-5,-5.5,-6,-6.5,-7,-7.5,-8,-8.5,-9,-9.5,-10,-15,-20,-30,-50]

	neg_param_triplet = []
	neg_param_triplet.append(a_neg)
	neg_param_triplet.append(b)
	neg_param_triplet.append(c_neg)
	all_params = list(itertools.product(*neg_param_triplet))

	pos_param_triplet = []
	pos_param_triplet.append(a_pos)
	pos_param_triplet.append(b)
	pos_param_triplet.append(c_pos)
	pos_params = list(itertools.product(*pos_param_triplet))

	all_params += pos_params
	return all_params

def solve_polynomials(all_params, avg_height):
	avg_height = 140 #average row height
	sols = {}

	st_points = [(0,k) for k in range(avg_height)]
	sols["StLn"] = st_points

	for param in all_params:
		try:
			sols[param] = []
			for h in range(avg_height):
				coeff = [float(param[0]), float(param[1]), float(param[2]), -(avg_height - h)]
				xs = np.roots(coeff)
				imaginary_pt = xs.imag
				for l in range(len(imaginary_pt)):
					if imaginary_pt[l] == 0:
						if (int(round(xs[l])),h) not in sols[param]:
							sols[param].append((int(round(xs[l])),h))
		except:
			pass
	return sols

def visualize_polynomials(img, cols, opt_parameters):
	for i in cols:
		x = int(i)
		x = x-1

		curve = opt_parameters[x]
		print x, curve
		points = sols[curve]
		for xy in points:
			try:
				if xy[1] >= difference:
					if xy[1] + upper - difference <= lower:
						img.itemset((xy[1]+upper - difference,xy[0]+x,0),0)
						img.itemset((xy[1]+upper - difference,xy[0]+x,1),0)
						img.itemset((xy[1]+upper - difference,xy[0]+x,2),255)
			except:
						pass


img = cv2.imread(sys.argv[1],0)
#height_org, width_org = img.shape
#ret,img = cv2.threshold(img,140,255,cv2.THRESH_BINARY)
img2 = cv2.imread(sys.argv[1])

height, width = img.shape
avg_height = 140 # avg_height of each row

f = open('data_page','w')
f.write('\n')
black_pixs = calc_black_pix_row(img)
f.write(' '.join(black_pixs))
f.close()

rows = run_carmel_code('data_page', sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
rows = rows.split()

#draw horizontal lines
for i in rows:
	x = int(i)
	cv2.line(img2,(0,x-1),(width-1,x-1),(0,0,255),2)

img3 = cv2.imread(sys.argv[1],0)
rows.insert(0,'0')


#generating all values of <a,b,c>
all_params = gen_all_params()

#solve all polynomials to get (x,y) solutions
sols = solve_polynomials(all_params, avg_height)


for m in range(len(rows)-1):
	pix_counts, opt_parameters =  calc_black_pix_col(img, rows, sols, avg_height, m)

	f = open('data_page_curve','w')
	f.write(' '.join(pix_counts))
	f.close()

	cols = run_carmel_code('data_page_curve', sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
	cols = cols.split()

	visualize_polynomials(img, cols, opt_parameters)

cv2.imwrite(sys.argv[2],img2)