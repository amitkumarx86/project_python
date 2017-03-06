from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import random

style.use('fivethirtyeight')
# xs = np.array([1,2,3,4,5,6], dtype=np.float64)
# ys = np.array([5,4,6,5,6,7], dtype=np.float64)
# ys = np.array([4.4285714285714288, 4.8571428571428577, 5.2857142857142865, 5.7142857142857144, 6.1428571428571432, 6.5714285714285721],dtype=np.float64)


def create_dataset(hm, variance, step=2, correlation=False):
	val = 1
	ys = []
	for i in range(hm):
		y = val + random.randrange(-variance, variance)
		ys.append(y)
		if correlation and correlation == 'pos':
			val += step
		elif correlation and correlation == 'neg':
			val -= step

	xs = [i for i in range(len(ys))]

	return np.array(xs,dtype=np.float64) , np.array(ys,dtype=np.float64)

def best_fit_slope(xs,ys):
	m = (mean(xs)*mean(ys) - mean(xs*ys)) / ((mean(xs)**2) - mean(xs**2))
	b = mean(ys) - m*mean(xs)
	return m,b

def squared_err(ys_orig, ys_line):
	return sum((ys_line-ys_orig)**2)

def coefficient_of_determination(ys_orig,ys_line):
	y_mean_line = [mean(ys_orig) for y in ys_orig]
	squared_err_regr = squared_err(ys_orig, ys_line)
	squared_err_y_mean = squared_err(ys_orig, y_mean_line)
	return 1 - (squared_err_regr/squared_err_y_mean)	 


xs, ys = create_dataset(40, 80, 2, False)

m,b = best_fit_slope(xs,ys)
regression_line = [(m*x)+b for x in xs ]
print regression_line

r_squared = coefficient_of_determination(ys, regression_line)
print r_squared

predict_x = 9
predict_y = m*predict_x + b
plt.scatter(xs,ys)
plt.scatter(predict_x,predict_y,s=100,color='g')
plt.plot(xs,regression_line)
plt.plot(xs,[mean(ys) for y in ys]), plt.show()

# plt.scatter(xs,ys)
# plt.show()

