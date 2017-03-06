import numpy as np
from sklearn import preprocessing, cross_validation, neighbors
import pandas as pd

df = pd.read_csv('dataset/breast_cancer.txt')
df.replace('?',-9999,inplace=True)

# remove useless data, we can also do drop na but that might reduce data set
df.drop(['id'],1,inplace=True)  

x = np.array(df.drop(['class'],1))
y = np.array(df['class'])


x_train, x_test, y_train, y_test = cross_validation.train_test_split(x,y,test_size=0.2)


# train classifier
clf = neighbors.KNeighborsClassifier()
clf.fit(x_train,y_train)

accuracy = clf.score(x_test, y_test)

print(accuracy)

# predict something

example_measures = np.array([[4,2,1,1,1,2,3,4,1],[4,2,1,2,2,2,3,4,1]])
example_measures = example_measures.reshape(len(example_measures),-1)
prediction = clf.predict(example_measures)

print(prediction)
