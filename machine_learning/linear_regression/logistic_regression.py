from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

iris = load_iris()
# print iris
X, y = iris.data[:-1,:], iris.target[:-1]
# print y
logistic = LogisticRegression()
logistic.fit(X,y)
print iris.data[-1,:],iris.target[-1]
print logistic.predict(iris.data[-1,:])
print logistic.predict_proba(iris.data[-1,:])
# print  logistic.predict(iris.data[-1,:]),iris.target[-1]
# print 'Probabilities for each class from 0 to 2: %s' % logistic.predict_proba(iris.data[-1,:])
