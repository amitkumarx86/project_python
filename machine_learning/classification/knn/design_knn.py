import numpy as np
import pandas as pd
from math import sqrt
import warnings
from collections import Counter
import random 

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
	confidence = Counter(votes).most_common(1)[0][0] / (k*1.0)
	# print vote_result
	return vote_result, confidence

# accuracy=[]
# for i in range(25):
df = pd.read_csv('dataset/breast_cancer.txt')
df.replace('?', -9999, inplace = True)
df.drop(['id'],1,inplace = True)
full_data = df.astype(float).values.tolist()

# print full_data[:5]
# print 20*'#'
random.shuffle(full_data)
# print full_data[:5]

test_size = 0.2
train_set = {2:[], 4:[]}
test_set  = {2:[], 4:[]}
train_data = full_data[:-int(test_size*len(full_data))]
test_data = full_data[-int(test_size*len(full_data)):]

# populate the dictionaries
for i in train_data:
	train_set[i[-1]].append(i[:-1]) 

for i in test_data:
	test_set[i[-1]].append(i[:-1]) 

total = 0.0
correct = 0.0
for group in test_set:
	for data in test_set[group]:
		vote, confidence = k_nearest_neighbors(train_set, data, k=5)
		if group == vote:
			correct += 1
		# else:
			# print confidence
		total += 1

# print ('Accuracy',correct/total)
# accuracy.append(correct/total)

# print (sum(accuracy)/len(accuracy))