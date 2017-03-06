
import quandl
# pandas is python data analysis library; optimized data structures
import pandas as pd
import math, datetime, time
import numpy as np
from sklearn import preprocessing, cross_validation, svm # it will suffle your data
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

# styling of graph
style.use('ggplot')

# 21 Feb 2017
# quandl is used to get the dataset
quandl.ApiConfig.api_key = "v7mGUMf4_SfyhSzMXsWM"
df = quandl.get('WIKI/GOOGL')

# metadata : Using df.head()
# print(df.head()) 

# get meaningful features not all the features
df = df[['Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume']]
df['HL_PCT'] = 100 * (df['Adj. High'] - df['Adj. Close'] )/ df['Adj. Close']
df['PCT_CHNG'] = 100 * ( df['Adj. Close'] - df['Adj. Open'])/ df['Adj. Open']

df = df[['Adj. Close','HL_PCT','PCT_CHNG','Adj. Volume']]

# which label we want to predict
forecast_col = 'Adj. Close'

# fill the dataset , it will be treated as out lier and we don't want to mess with data
df.fillna(-99999,inplace=True)

# regression algo, forecast_out - 
# this variable is telling for how many days we are predicting the label
forecast_out = int(math.ceil(0.1*len(df))) # we are trying to predict only 10% of the data means 10 days data


# shift the forecasr_col to 10% rows above
df['label'] = df[forecast_col].shift(-forecast_out)


##############################################################################
# Lets define X and Y

X = np.array(df.drop(['label'],1))
X = preprocessing.scale(X)
# we dnt have y value for X_trai_latly, we will predict it,
X_latly = X[-forecast_out:]
X = X[:-forecast_out]


df.dropna(inplace=True)
y = np.array(df['label'])
# suffles x->y and then 20% will be for testing
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.2)

# clf = LinearRegression()

# # SVM is giving less accuracy
# # clf = svm.SVR()
# # training
# clf.fit(X_train,y_train)
# ###########################################################
# # saving a classifier using pickle
# with open('linearregression.pickle','wb') as f:
# 	pickle.dump(clf,f)
# ###########################################################

pickle_in = open('linearregression.pickle','rb')
clf = pickle.load(pickle_in)
print clf.coef_
# testing
# it is squared error
accuracy = clf.score(X_test,y_test)

forecast_predict  = clf.predict(X_latly)
#print(forecast_predict,accuracy,forecast_out)

df['Forecast'] = np.nan

last_date = df.iloc[-1].name
print last_date
last_unix = time.mktime(datetime.datetime.strptime(str(last_date), "%Y-%m-%d %H:%M:%S").timetuple())
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_predict:
	next_date = datetime.datetime.fromtimestamp(next_unix)
	next_unix += one_day
	df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()












