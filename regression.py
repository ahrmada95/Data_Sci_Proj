import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
from mpl_toolkits.mplot3d import Axes3D
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


#load csvs into dataframes
income = pd.read_csv('income_by_zip.csv')
vac_loc = pd.read_csv('vacc_loc_count.csv')
er_visits = pd.read_csv('er_visits_zip.csv')

#scale the counts for vaccination locations
vac_loc['counts'] = vac_loc['counts'] * 10000
er_visits['percentage_pne'] = er_visits['percentage_pne']

#set indexes
income = income.set_index('zipcode')
vac_loc = vac_loc.set_index('zipcode')
er_visits = er_visits.set_index('zipcode')

#merge on zipcodes
df_temp = pd.merge(vac_loc,income, on = 'zipcode')
df = pd.merge(df_temp,er_visits, on = 'zipcode')
X = df[['counts', 'median_income']]
y = df.percentage_pne

#train model 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=70, random_state=30)
#linear regression
mlr_model = LinearRegression()
#fit model
mlr_model.fit(X_train, y_train)

theta0 = mlr_model.intercept_
theta1, theta2, = mlr_model.coef_
print(theta0, theta1, theta2) 

plt.show()
y_pred = mlr_model.predict(X)
print(r2_score(y, y_pred))
