from math import sqrt
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
from collections import Counter
style.use('fivethirtyeight')
import warnings

dataset = {'k':[[1,2],[2,3],[3,1]],'r':[[6,5],[7,7],[8,6]]}
new_features = [5,7]


def k_nearest_neighbors(data, predict, k =3):
	if len(data) >= k:
		warnings.warn('k is set to value less than total voting groups')
	distances = []
	for group in data:
		for features in data[group]:
    		# euclidian distance using linear algebra norm
			euclidian_distance = np.linalg.norm(np.array(features)-np.array(predict))
			distances.append([euclidian_distance,group])

	votes = [i[1] for i in sorted(distances)[:k]]
	vote_result = Counter(votes).most_common(1)[0][0]
	print Counter(votes).most_common(1)[0][1]
	print vote_result
	return vote_result


result =  k_nearest_neighbors(dataset, new_features)

[[plt.scatter(ii[0],ii[1], s= 100,color=i)   for ii in dataset[i]] for i in dataset]
plt.scatter(new_features[0],new_features[1],color=result)
plt.show()